from datetime import datetime, timezone
from energyos.advisor import optimize

def test_headroom():
    now = datetime.now(timezone.utc)
    result = optimize({"safe_to_optimize": True, "values": {"pv": 2000, "grid": -2000, "ev": 0}}, now=now)
    assert result["estimated_surplus_w"] == 1750
    assert result["recommended_ev_w"] == 1750
    assert result["mode"] == "observe_only"

def test_unhealthy_blocks():
    result = optimize({"safe_to_optimize": False, "values": {"pv": 5000, "grid": -4000, "ev": 0}})
    assert result["recommended_ev_w"] is None
