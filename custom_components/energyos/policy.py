"""Safety policy: no actuator gateway; cannot authorize hardware commands."""
from datetime import datetime, timezone

def assess_plan(plan, *, healthy, enabled=False, now=None):
    now = now or datetime.now(timezone.utc)
    if not healthy:
        return False, "inputs_unhealthy"
    if not isinstance(plan, dict):
        return False, "invalid_plan"
    valid_until = plan.get("valid_until")
    if not isinstance(valid_until, datetime) or valid_until.tzinfo is None or valid_until <= now:
        return False, "expired_plan"
    if not enabled:
        return False, "observe_only"
    return False, "no_actuator_gateway"
