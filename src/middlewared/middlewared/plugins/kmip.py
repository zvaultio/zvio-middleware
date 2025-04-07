from middlewared.service import Service, periodic


class KMIPService(Service):
    """
    Stub service for KMIP functionality which has been removed.
    This service exists only to handle periodic task registration.
    """

    @periodic(86400)
    async def sync_keys(self):
        """
        This is a stub implementation for the removed KMIP sync_keys functionality.
        The periodic task is kept to avoid errors during system startup.
        """
        self.logger.debug('KMIP functionality has been removed, sync_keys is a no-op')

    async def retrieve_zfs_keys(self):
        """
        Stub implementation for retrieve_zfs_keys.
        """
        return {}

    async def reset_zfs_key(self, dataset_name, kmip_uid):
        """
        Stub implementation for reset_zfs_key.
        """
        pass
