from middlewared.service import Service, private


class EnclosureService(Service):
    """
    Stub service for enclosure functionality which has been removed.
    This service exists only to handle calls that are still being made to it.
    """

    @private
    async def sync_disk(self, disk_identifier):
        """
        Stub implementation for sync_disk.
        This method was called from disk_.sync.py to update enclosure slot information for a disk.
        """
        self.logger.debug('Enclosure functionality has been removed, sync_disk is a no-op')

    @private
    def sync_disks(self, enclosure_id, disks, ha_sync=False):
        """
        Stub implementation for sync_disks.
        This method was called from disk_.sync.py to update enclosure slot information for all disks.
        """
        self.logger.debug('Enclosure functionality has been removed, sync_disks is a no-op')
