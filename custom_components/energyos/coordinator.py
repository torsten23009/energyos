"""Read HAOS telemetry, compose multi-PV and split meter sources; no device writes."""
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .configuration import effective_config, ROLES
from .engine import Reading, normalized, evaluate
from .topology import compose
from .advisor import optimize, diagnose_mapping

_LOGGER = logging.getLogger(__name__)

class EnergyOSCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(hass, logger=_LOGGER, name=DOMAIN, config_entry=entry,
                         update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL))
        self.entry = entry

    async def _async_update_data(self):
        conf = effective_config(self.entry)
        readings = {}
        for role in ROLES:
            state = self.hass.states.get(conf[role]) if conf.get(role) else None
            val, timestamp = None, None
            if state and state.state not in ("unknown", "unavailable", "none", ""):
                val = normalized(
                    state.state, state.attributes.get("unit_of_measurement"),
                    "soc" if role == "soc" else "power",
                    invert=(role == "grid" and conf.get("invert_grid", False)) or
                           (role == "battery" and conf.get("invert_battery", False)))
                timestamp = getattr(state, "last_reported", None) or state.last_updated
            readings[role] = Reading(val, timestamp if val is not None else None)
        now = dt_util.utcnow()
        composed = compose(readings, conf)
        result = evaluate(composed, now=now)
        extra = []
        for role in ("pv_roof", "pv_carport", "grid_import", "grid_export"):
            if not conf.get(role):
                continue
            v = readings[role]
            if v.watts is None or v.observed_at is None:
                extra.append(role + ":missing")
            elif (now-v.observed_at).total_seconds() > 90:
                extra.append(role + ":stale")
        if extra:
            result["reasons"] = tuple(result["reasons"]) + tuple(extra)
            result["quality"] = max(0, result["quality"] - 20*len(extra))
            result["safe_to_optimize"] = False
        for role in ("pv_roof", "pv_carport"):
            result["metrics"][role] = readings[role].watts
        result["optimizer"] = optimize(result, now=now)
        result["advice"] = diagnose_mapping(conf, result)
        return result
