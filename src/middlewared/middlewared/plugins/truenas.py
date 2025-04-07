from middlewared.service import Service, private


class TrueNASService(Service):
    """
    This is a stub implementation of the TrueNAS service.
    All methods return default values that should not break the rest of the code.
    """

    @private
    def get_chassis_hardware(self):
        """
        Returns the chassis hardware.
        This is a stub implementation that returns a value that doesn't start with "TRUENAS-M".
        """
        return "ZVIO"
