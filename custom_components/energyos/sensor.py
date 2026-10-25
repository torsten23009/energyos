"""Read-only diagnostic and energy sensors."""
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

SENSORS = {
    "pv_power": ("PV Total Power", "pv", "W", SensorDeviceClass.POWER),
    "roof_power": ("Roof PV Power", "pv_roof", "W", SensorDeviceClass.POWER),
    "carport_power": ("Carport PV Power", "pv_carport", "W", SensorDeviceClass.POWER),
    "grid_signed": ("Grid Signed", "grid", "W", SensorDeviceClass.POWER),
    "battery_signed": ("Battery Signed", "battery", "W", SensorDeviceClass.POWER),
    "house_load": ("Measured House Load", "load", "W", SensorDeviceClass.POWER),
    "derived_load": ("Calculated House Load", "derived_load", "W", SensorDeviceClass.POWER),
    "grid_import": ("Grid Import Power", "import_power", "W", SensorDeviceClass.POWER),
    "grid_export": ("Grid Export Power", "export_power", "W", SensorDeviceClass.POWER),
    "battery_charge": ("Battery Charge Power", "battery_charge", "W", SensorDeviceClass.POWER),
    "battery_discharge": ("Battery Discharge Power", "battery_discharge", "W", SensorDeviceClass.POWER),
    "ev_power": ("EV Charge Power", "ev", "W", SensorDeviceClass.POWER),
    "soc": ("Battery SOC", "soc", "%", SensorDeviceClass.BATTERY),
    "balance": ("Energy Balance Residual", "balance_residual", "W", SensorDeviceClass.POWER),
    "quality": ("Data Quality Score", "quality", "%", None),
    "surplus": ("Surplus Reserve Adjusted", "estimated_surplus_w", "W", SensorDeviceClass.POWER),
    "ev_recommendation": ("EV Suggested Charge Power", "recommended_ev_w", "W", SensorDeviceClass.POWER),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data
    async_add_entities(
        [EnergyOSMetric(coordinator, entry, key, *spec) for key, spec in SENSORS.items()]
        + [EnergyOSTextMetric(coordinator, entry, "optimizer_advice"), EnergyOSTextMetric(coordinator, entry, "data_advice")]
    )

class EnergyOSMetric(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = False

    def __init__(self, coordinator, entry, key, label, source, unit, device_class):
        super().__init__(coordinator)
        self._key = key
        self._source = source
        self._attr_name = f"EnergyOS {label}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if self._source == "quality":
            return data.get("quality")
        if self._source in ("estimated_surplus_w", "recommended_ev_w"):
            return data.get("optimizer", {}).get(self._source)
        if self._source in data.get("values", {}):
            return data["values"].get(self._source)
        return data.get("metrics", {}).get(self._source)

    @property
    def extra_state_attributes(self):
        if self._key == "quality":
            return {"issues": list((self.coordinator.data or {}).get("reasons", ()))}
        return None

class EnergyOSTextMetric(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = False

    def __init__(self, coordinator, entry, key):
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_name = "EnergyOS " + ("Optimizer Advice" if key == "optimizer_advice" else "Data Advice")

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if self._key == "optimizer_advice":
            return data.get("optimizer", {}).get("advice", "unknown")
        return "review" if data.get("advice") else "healthy"

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data or {}
        if self._key == "data_advice":
            return {"recommendations": data.get("advice", [])[:20]}
        return {"explanation": data.get("optimizer", {}).get("explanation", ""), "mode": "observe_only"}
