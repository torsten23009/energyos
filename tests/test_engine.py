from datetime import datetime, timedelta, timezone
from energyos.engine import Reading, normalized, evaluate

NOW = datetime.now(timezone.utc)

def test_normalize_power():
    assert normalized("1.2", "kW") == 1200

def test_normalize_unknown_unit():
    assert normalized("2", "kWh") is None

def test_nonfinite_rejected():
    assert normalized("nan", "W") is None

def test_sign_flip():
    assert normalized("200", "W", invert=True) == -200

def test_snapshot_and_balance():
    values = {"pv": Reading(2000, NOW), "grid": Reading(-500, NOW),
              "battery": Reading(0, NOW), "load": Reading(1500, NOW)}
    data = evaluate(values, now=NOW)
    assert data["safe_to_optimize"]
    assert data["metrics"]["balance_residual"] == 0

def test_stale_grid():
    values = {"pv": Reading(2000, NOW), "grid": Reading(-500, NOW - timedelta(minutes=2))}
    assert not evaluate(values, now=NOW)["safe_to_optimize"]
