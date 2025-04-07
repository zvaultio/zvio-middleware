from middlewared.service import Service, private, CallError, job
from middlewared.schema import accepts, Bool, Dict, Int, List, Str
import errno
import logging

logger = logging.getLogger('failover')


class FailoverService(Service):
    """
    This is a stub implementation of the failover service to replace the removed failover.py.
    All methods return default values that should not break the rest of the code.
    """

    @accepts(Dict(
        'failover_update',
        Bool('disabled'),
        Bool('master'),
    ))
    @job(lock='failover_update')
    async def update(self, job, data):
        """
        Update failover state.
        Since failover has been removed, this is a no-op.
        """
        return data

    @private
    def licensed(self):
        """
        Returns whether failover is licensed.
        Since failover has been removed, this always returns False.
        """
        return False

    @private
    def status(self):
        """
        Returns the failover status.
        Since failover has been removed, this always returns 'SINGLE'.
        """
        return 'SINGLE'

    @private
    def node(self):
        """
        Returns the node.
        Since failover has been removed, this always returns 'A'.
        """
        return 'A'

    @private
    def call_remote(self, method, args=None, kwargs=None):
        """
        Calls a method on the remote node.
        Since failover has been removed, this raises a CallError.
        """
        raise CallError('Failover has been removed', errno.ENOTSUP)

    @private
    def config(self):
        """
        Returns the failover configuration.
        Since failover has been removed, this returns a default configuration.
        """
        return {
            'disabled': True,
            'master': False,
            'timeout': 0,
        }

    @private
    def hardware(self):
        """
        Returns the hardware type.
        Since failover has been removed, this returns 'MANUAL'.
        """
        return 'MANUAL'

    @private
    def internal_interfaces(self):
        """
        Returns the internal interfaces.
        Since failover has been removed, this returns an empty list.
        """
        return []

    @private
    def send_database(self):
        """
        Sends the database to the remote node.
        Since failover has been removed, this does nothing.
        """
        pass

    @private
    def send_small_file(self, path):
        """
        Sends a small file to the remote node.
        Since failover has been removed, this does nothing.
        """
        pass

    @private
    def remote_ip(self):
        """
        Returns the remote IP.
        Since failover has been removed, this returns None.
        """
        return None

    @private
    def disabled_reasons(self):
        """
        Returns the reasons why failover is disabled.
        Since failover has been removed, this returns ['NO_FAILOVER'].
        """
        return ['NO_FAILOVER']

    @private
    def upgrade_version(self):
        """
        Upgrades the version.
        Since failover has been removed, this does nothing.
        """
        pass

    @private
    def is_single_master_node(self):
        """
        Returns whether this is a single master node.
        Since failover has been removed, this always returns True.
        """
        return True

    @private
    class VipService:
        def __init__(self, middleware):
            self.middleware = middleware

        def get_states(self):
            """
            Returns the VIP states.
            Since failover has been removed, this returns [False].
            """
            return [False]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vip = self.VipService(self.middleware)
