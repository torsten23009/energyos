"""Deterministic real-time surplus advisor; never controls devices."""
from datetime import datetime, timedelta, timezone

def optimize(snapshot, *, reserve_w=250, charger_min_w=1400, charger_max_w=3600, now=None):
    now = now or datetime.now(timezone.utc)
    result = {"mode": "observe_only", "advice": "insufficient_data", "recommended_ev_w": None,
              "valid_until": now + timedelta(minutes=2), "estimated_surplus_w": None, "explanation": ""}
    values = snapshot.get("values", {})
    if not snapshot.get("safe_to_optimize"):
        result["explanation"] = "Unhealthy input; no charging recommendation."
        return result
    pv, grid, ev = values.get("pv"), values.get("grid"), values.get("ev")
    if pv is None or grid is None:
        result["explanation"] = "PV or grid measurement missing."
        return result
    headroom = max(0, -grid - reserve_w)
    result["estimated_surplus_w"] = round(headroom)
    if ev is None:
        result.update(advice="monitor_only", explanation="Missing EV power sensor; recommendation withheld.")
        return result
    target = min(charger_max_w, max(0, ev + headroom))
    if target < charger_min_w:
        result.update(advice="insufficient_surplus", recommended_ev_w=0,
                      explanation="Below nominal minimum; informational, never stops charger.")
    else:
        result.update(advice="increase_or_hold", recommended_ev_w=int(target),
                      explanation="Single snapshot; EVSE phases and battery boundary not verified.")
    return result

def diagnose_mapping(mapping, snapshot, candidates=None):
    advice = []
    if not (mapping.get("pv") or mapping.get("pv_roof") or mapping.get("pv_carport")):
        advice.append("Assign a valid PV power sensor")
    if not (mapping.get("grid") or (mapping.get("grid_import") and mapping.get("grid_export"))):
        advice.append("Assign signed grid power or both import/export power sensors")
    for reason in snapshot.get("reasons", ()):
        if reason.endswith(":stale"):
            advice.append(f"Investigate source freshness: {reason}")
        elif reason == "balance:deviation":
            advice.append("Verify sign conventions, AC/DC boundaries, timestamps and meter topology")
        elif reason.endswith(":invalid"):
            advice.append(f"Verify units and sensor class: {reason}")
    if candidates:
        for role, items in candidates.items():
            if not mapping.get(role) and items:
                advice.append(f"Review candidate for {role}: {items[0].entity_id}; confirmation required")
    return advice
