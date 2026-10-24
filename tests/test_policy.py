from datetime import datetime, timedelta, timezone
from energyos.policy import assess_plan

def test_observe_only():
    plan = {"valid_until": datetime.now(timezone.utc) + timedelta(minutes=2)}
    assert assess_plan(plan, healthy=True) == (False, "observe_only")

def test_fail_closed_even_enabled():
    plan = {"valid_until": datetime.now(timezone.utc) + timedelta(minutes=2)}
    assert assess_plan(plan, healthy=True, enabled=True) == (False, "no_actuator_gateway")
