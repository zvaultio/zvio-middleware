import os

# Path to the packet filter block configuration file
PF_BLOCK_FILE = '/etc/pf.conf.block'


def render(service, middleware):
    """
    Render the packet filter configuration file.
    
    Since failover is never licensed on this system, this function
    simply removes any existing block file.
    
    Args:
        service: The service object
        middleware: The middleware client
    """
    # Remove the block file if it exists
    if os.path.exists(PF_BLOCK_FILE):
        try:
            os.unlink(PF_BLOCK_FILE)
        except Exception as e:
            middleware.logger.warning(f'Failed to remove {PF_BLOCK_FILE}: {e}')
