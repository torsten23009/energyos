"""Diagnostics omit raw sensor values and identifiers wherever possible."""
from .ha_discovery import discover
from .configuration import effective_config, ROLES

async def async_get_config_entry_diagnostics(hass, entry):
    data = entry.runtime_data.data or {}
    proposed, ranked = discover(hass)
    conf = effective_config(entry)
    return {
        "quality": data.get("quality"),
        "reasons": list(data.get("reasons", ())),
        "safe_to_optimize": data.get("safe_to_optimize"),
        "optimizer": {k: v for k, v in data.get("optimizer", {}).items() if k != "valid_until"},
        "advice": data.get("advice", []),
        "suggested_roles": list(proposed),
        "candidate_counts": {k: len(v) for k, v in ranked.items()},
        "configured_roles": sorted(k for k in ROLES if conf.get(k)),
    }
