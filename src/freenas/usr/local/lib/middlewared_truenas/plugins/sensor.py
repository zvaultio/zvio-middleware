# Copyright (c) - zvault.
#
# Licensed under the terms of the repo License

import asyncio
import random
import re

from middlewared.service import Service, filterable
from middlewared.utils import filter_list, run


class SensorService(Service):
    @filterable
    async def query(self, filters, options):
        system_info = await self.middleware.call('system.dmidecode_info')
        board_manufacturer = system_info['baseboard-manufacturer']
        is_supported_hardware = board_manufacturer == "Supermicro"
        if not is_supported_hardware:
            return []
        
        sensor_data = await self._fetchIpmiSensors()
        sensor_data = await self._processSupermicroSensors(sensor_data)
        return filter_list(sensor_data, filters, options)
    
    async def _processSupermicroSensors(self, sensors):
        for sensor in sensors:
            ps_match = re.match(r"(PS[0-9]+) Status", sensor["name"])
            if not ps_match:
                continue
            ps_id = ps_match.group(1)
            if sensor["value"] == 0:
                sensor = await self._rereadPsStatus(sensor, ps_id)
            sensor["notes"] = self._getPsStatusNotes(sensor["value"])
                
        return sensors
    
    async def _rereadPsStatus(self, sensor, ps_id):
        for attempt in range(3):
            self.logger.info("%r Status = 0x0, rereading", ps_id)
            await asyncio.sleep(random.uniform(1, 3))
            new_sensors = await self._fetchIpmiSensors()
            for new_sensor in new_sensors:
                new_ps_match = re.match(r"(PS[0-9]+) Status", new_sensor["name"])
                if new_ps_match and new_ps_match.group(1) == ps_id:
                    if new_sensor["value"] != 0:
                        sensor.update(new_sensor)
                        return sensor
                        
        return sensor
    
    def _getPsStatusNotes(self, status_value):
        notes = []
        
        if not (status_value & 0x1):
            notes.append("No presence detected")
            
        ps_failure_conditions = [
            (0x2, "Failure detected"),
            (0x4, "Predictive failure"),
            (0x8, "Power Supply AC lost"),
            (0x10, "AC lost or out-of-range"),
            (0x20, "AC out-of-range, but present"),
        ]
        
        for bitmask, description in ps_failure_conditions:
            if status_value & bitmask:
                notes.append(description)
                
        return notes

    async def _fetchIpmiSensors(self):
        proc = await run(["/usr/local/bin/ipmitool", "sensor", "list"], check=False)
        output_text = proc.stdout.decode(errors="ignore").strip("\n")
        sensor_lines = output_text.split("\n")
        
        sensors = []
        for line in sensor_lines:
            fields = [field.strip(" ") for field in line.split("|")]
            fields = [None if field == "na" else field for field in fields]
            if len(fields) != 10:
                continue
            sensor = {
                "name": fields[0],
                "value": fields[1],
                "desc": fields[2],
                "locrit": fields[5],
                "lowarn": fields[6],
                "hiwarn": fields[7],
                "hicrit": fields[8],
            }
            self._convertSensorValues(sensor)
            
            sensors.append(sensor)
            
        return sensors
    
    def _convertSensorValues(self, sensor):
        numeric_fields = ["value", "locrit", "lowarn", "hicrit", "hiwarn"]
        for field in numeric_fields:
            if sensor[field] is None:
                continue
            if sensor[field].startswith("0x"):
                try:
                    sensor[field] = int(sensor[field], 16)
                except ValueError:
                    sensor[field] = None
            else:
                try:
                    sensor[field] = float(sensor[field])
                except ValueError:
                    sensor[field] = None
