"""Diagnostics omit raw sensor values and identifiers wherever possible."""
from .const import DOMAIN
from .ha_discovery import discover

async def async_get_config_entry_diagnostics(hass, entry):
    data = hass.data[DOMAIN][entry.entry_id].data or {}
    proposed, ranked = discover(hass)
    return {
        "quality": data.get("quality"),
        "reasons": list(data.get("reasons", ())),
        "safe_to_optimize": data.get("safe_to_optimize"),
        "optimizer": {k: v for k, v in data.get("optimizer", {}).items() if k != "valid_until"},
        "advice": data.get("advice", []),
        "suggested_roles": list(proposed),
        "candidate_counts": {k: len(v) for k, v in ranked.items()},
        "configured_roles": sorted(k for k in ("pv", "grid", "battery", "soc", "load", "ev")
                                   if entry.options.get(k) or entry.data.get(k)),
    }
