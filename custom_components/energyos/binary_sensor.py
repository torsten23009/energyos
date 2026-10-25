from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([EnergyOSHealth(entry.runtime_data, entry.entry_id)])

class EnergyOSHealth(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = False
    _attr_name = "EnergyOS Data Healthy"

    def __init__(self, coordinator, entry_id):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_data_healthy"

    @property
    def is_on(self):
        return bool((self.coordinator.data or {}).get("safe_to_optimize", False))
