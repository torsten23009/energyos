"""Pure Python calculations; no external runtime dependencies."""
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite

@dataclass(frozen=True)
class Reading:
    watts: float | None
    observed_at: datetime | None
    problem: str | None = None

def normalized(value, unit, kind="power", invert=False):
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if not isfinite(val):
        return None
    multiplier = {"power": {"W": 1, "kW": 1000}, "soc": {"%": 1}}.get(kind, {}).get(unit)
    if multiplier is None:
        return None
    val *= multiplier
    return -val if invert else val

def evaluate(values, now=None, limits=None):
    """Grid positive = import; battery positive = discharge; data timestamps must be valid."""
    now = now or datetime.now(timezone.utc)
    limits = limits or {}
    max_age = {"pv": 90, "grid": 60, "battery": 90, "soc": 1200, "load": 90, "ev": 120}
    reasons = []
    valid = {}
    for key in max_age:
        reading = values.get(key, Reading(None, None))
        if reading.watts is None:
            valid[key] = None
            if key in ("pv", "grid"):
                reasons.append(f"{key}:missing")
            continue
        if reading.observed_at is None:
            valid[key] = None
            reasons.append(f"{key}:timestamp_missing")
            continue
        age = (now - reading.observed_at).total_seconds()
        if age < -5 or age > max_age[key]:
            valid[key] = None
            reasons.append(f"{key}:stale")
            continue
        val = reading.watts
        if not isfinite(val) or (key == "soc" and not 0 <= val <= 100) or (key in ("pv", "ev", "load") and val < -1):
            valid[key] = None
            reasons.append(f"{key}:invalid")
            continue
        if key in limits and abs(val) > limits[key] * 1.1:
            valid[key] = None
            reasons.append(f"{key}:out_of_range")
            continue
        valid[key] = val
    pv, grid, battery, load = (valid[k] for k in ("pv", "grid", "battery", "load"))
    metrics = {}
    if grid is not None:
        metrics.update(import_power=max(grid, 0), export_power=max(-grid, 0))
    if battery is not None:
        metrics.update(battery_discharge=max(battery, 0), battery_charge=max(-battery, 0))
    if pv is not None and grid is not None and battery is not None:
        derived = pv + grid + battery
        metrics["derived_load"] = derived if derived >= -100 else None
        if load is not None:
            metrics["balance_residual"] = derived - load
            tolerance = max(150, .05 * max(1, abs(pv), abs(grid), abs(battery), abs(load)))
            if abs(derived - load) > tolerance:
                reasons.append("balance:deviation")
    quality = max(0, 100 - len(reasons) * 20)
    safe = pv is not None and grid is not None and not reasons and quality == 100
    return {"values": valid, "metrics": metrics, "reasons": tuple(reasons), "quality": quality, "safe_to_optimize": safe}
