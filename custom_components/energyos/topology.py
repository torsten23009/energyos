"""Compose multi-source instantaneous W readings into virtual signed PV/grid sources.

Split grid values must be instantaneous non-negative import/export power, never kWh totals.
No silent partial sums. Oldest source timestamp is retained.
"""
from .engine import Reading

def combine(readings, keys):
    if not keys:
        return Reading(None, None)
    values = [readings.get(key, Reading(None, None)) for key in keys]
    if any(value.watts is None or value.observed_at is None for value in values):
        return Reading(None, None)
    return Reading(sum(value.watts for value in values),
                   min(value.observed_at for value in values))

def compose(readings, config):
    combined = dict(readings)
    pv_roles = ["pv"] if config.get("pv") else [
        key for key in ("pv_roof", "pv_carport") if config.get(key)]
    combined["pv"] = combine(readings, pv_roles)
    if config.get("grid"):
        combined["grid"] = readings.get("grid", Reading(None, None))
    else:
        power_in = readings.get("grid_import", Reading(None, None))
        power_out = readings.get("grid_export", Reading(None, None))
        if (power_in.watts is None or power_out.watts is None
            or power_in.observed_at is None or power_out.observed_at is None
            or power_in.watts < 0 or power_out.watts < 0):
            combined["grid"] = Reading(None, None)
        else:
            combined["grid"] = Reading(power_in.watts-power_out.watts,
                                       min(power_in.observed_at,power_out.observed_at))
    return combined
