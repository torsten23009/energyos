"""HA DataUpdateCoordinator. Source entities stay read-only."""
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .engine import Reading, normalized, evaluate
from .advisor import optimize, diagnose_mapping

_LOGGER = logging.getLogger(__name__)

class EnergyOSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, logger=_LOGGER, name=DOMAIN,
                         update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL))
        self.entry = entry

    async def _async_update_data(self):
        conf = {**self.entry.data, **self.entry.options}
        values = {}
        for key in ("pv", "grid", "battery", "soc", "load", "ev"):
            entity_id = conf.get(key)
            state = self.hass.states.get(entity_id) if entity_id else None
            reading = Reading(None, None)
            if state and state.state not in ("unknown", "unavailable", "none", ""):
                kind = "soc" if key == "soc" else "power"
                val = normalized(state.state, state.attributes.get("unit_of_measurement"), kind,
                    invert=(key == "grid" and conf.get("invert_grid", False)) or
                           (key == "battery" and conf.get("invert_battery", False)))
                observed = getattr(state, "last_reported", None) or state.last_updated
                if val is not None:
                    reading = Reading(val, observed)
            values[key] = reading
        result = evaluate(values, now=dt_util.utcnow())
        result["optimizer"] = optimize(result, now=dt_util.utcnow())
        result["advice"] = diagnose_mapping(conf, result)
        return result
