import os


def render(service, middleware):
    """
    Render failover configuration files.
    
    Since failover is never licensed on this system, this function
    simply creates an empty pf.conf.block file and removes any
    existing failover.json file.
    
    Args:
        service: The service object
        middleware: The middleware client
    """
    # Define file paths
    failover_json = '/tmp/failover.json'
    pf_block = '/etc/pf.conf.block'
    
    # Clean up existing failover.json if it exists
    try:
        os.unlink(failover_json)
    except OSError:
        pass

    # Create an empty pf.conf.block file
    open(pf_block, 'w+').close()
