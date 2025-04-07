import pytest

# Skip all tests since failover.py has been removed
pytestmark = pytest.mark.skip("Failover functionality has been removed")
