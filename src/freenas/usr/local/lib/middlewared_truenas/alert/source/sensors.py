# Copyright (c) - zvault.
#
# Licensed under the terms of the repo License

import logging
import re

from middlewared.alert.base import AlertClass, AlertCategory, AlertLevel, AlertSource, Alert

logger = logging.getLogger(__name__)

RE_CPUTEMP = re.compile(r'^cpu.*temp$', re.I)
RE_SYSFAN = re.compile(r'^sys_fan\d+$', re.I)

PS_FAILURES = [
    (0x2, "Failure detected"),
    (0x4, "Predictive failure"),
    (0x8, "Power Supply AC lost"),
    (0x10, "AC lost or out-of-range"),
    (0x20, "AC out-of-range, but present"),
]

class SensorAlertClass(AlertClass):
    category = AlertCategory.HARDWARE
    level = AlertLevel.CRITICAL
    title = "Sensor Value Is Outside of Proper Range"
    text = "%(name)s sensor has a value of %(relative)s %(level)s: %(value)d %(description)s"

class PowerSupplyAlertClass(AlertClass):
    category = AlertCategory.HARDWARE
    level = AlertLevel.CRITICAL
    title = "Power Supply Fas Failed"
    text = "The %(number)s Power supply has failed: %(errors)s."

class SensorsAlertSource(AlertSource):
    
    async def check(self):
        sensors = await self.middleware.call("sensor.query")
        sensor_alerts = self.checkSensorThresholdsAlerts(sensors)
        power_supply_alerts = self.checkPowerSupplyAlerts(sensors)
        return sensor_alerts + power_supply_alerts
    
    def checkSensorThresholdsAlerts(self, sensors):
        alerts = []
        
        for sensor in sensors:
            if sensor["value"] is None:
                continue
            if not (RE_CPUTEMP.match(sensor["name"]) or RE_SYSFAN.match(sensor["name"])):
                continue
            alert_data = self.checkSensorThresholds(sensor)
            if alert_data:
                alerts.append(Alert(
                    SensorAlertClass,
                    alert_data,
                    key=[sensor["name"], alert_data["relative"], alert_data["level"]],
                ))
                
        return alerts
    
    def checkSensorThresholds(self, sensor):
        if sensor["lowarn"] and sensor["value"] < sensor["lowarn"]:
            relative = "below"
            if sensor["value"] < sensor["locrit"]:
                level = "critical"
            else:
                level = "recommended"
            return self.createSensorAlertData(sensor, relative, level)
        elif sensor["hiwarn"] and sensor["value"] > sensor["hiwarn"]:
            relative = "above"
            if sensor["value"] > sensor["hicrit"]:
                level = "critical"
            else:
                level = "recommended"
            return self.createSensorAlertData(sensor, relative, level)
        
        return None
    
    def createSensorAlertData(self, sensor, relative, level):
        return {
            "name": sensor["name"],
            "relative": relative,
            "level": level,
            "value": sensor["value"],
            "desc": sensor["desc"],
        }
    
    def checkPowerSupplyAlerts(self, sensors):
        alerts = []
        
        for sensor in sensors:
            # Check for power supply sensors
            ps_match = re.match("(PS[0-9]+) Status", sensor["name"])
            if ps_match and sensor["notes"]:
                ps = ps_match.group(1)
                alerts.append(Alert(
                    PowerSupplyAlertClass,
                    {
                        "number": ps,
                        "errors": ", ".join(sensor["notes"]),
                    }
                ))
                
        return alerts
