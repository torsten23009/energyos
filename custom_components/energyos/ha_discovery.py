"""Discover available native Home Assistant sensor states."""
from homeassistant.helpers import entity_registry as er
from .discovery import propose_mapping

def discover(hass):
    registry = er.async_get(hass)
    entities = []
    for state in hass.states.async_all("sensor"):
        attrs = state.attributes
        registry_entry = registry.async_get(state.entity_id)
        entities.append({
            "entity_id": state.entity_id,
            "name": attrs.get("friendly_name", state.entity_id),
            "unit": attrs.get("unit_of_measurement", ""),
            "device_class": attrs.get("device_class", ""),
            "state_class": attrs.get("state_class", ""),
            "integration": registry_entry.platform if registry_entry else "",
            "available": state.state not in ("unknown", "unavailable", ""),
        })
    return propose_mapping(entities)
