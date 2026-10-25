"""Exercise the real HA loader, not the pure-core package alias."""
import pytest
import custom_components  # Load the repository namespace before HA's test config.

pytest_plugins = ["pytest_homeassistant_custom_component"]

@pytest.fixture(autouse=True)
def custom_integrations(enable_custom_integrations):
    yield
