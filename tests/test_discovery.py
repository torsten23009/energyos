from energyos.discovery import propose_mapping, score_sensor

def test_reject_nonpower():
    assert score_sensor("pv", entity_id="sensor.pv_power", unit="kWh") == 0

def test_discovery():
    rows = [{"entity_id": "sensor.pv_power", "name": "Solar Power", "unit": "W", "device_class": "power", "state_class": "measurement", "available": True}]
    proposed, _ = propose_mapping(rows)
    assert proposed.get("pv") == "sensor.pv_power"

def test_ambiguous_candidates():
    rows = [{"entity_id": f"sensor.pv_power_{i}", "name": "Solar Power", "unit": "W", "device_class": "power", "available": True} for i in range(2)]
    proposed, _ = propose_mapping(rows)
    assert "pv" not in proposed
