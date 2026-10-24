from datetime import datetime, timezone
from energyos.engine import Reading, evaluate
from energyos.topology import compose

NOW = datetime.now(timezone.utc)

def source(value):
    return Reading(value, NOW)

def test_both_pv_and_import_export():
    readings = {"pv_roof":source(2200), "pv_carport":source(900),
                "grid_import":source(0), "grid_export":source(1400), "battery":source(0)}
    result = compose(readings, {"pv_roof":"a","pv_carport":"b","grid_import":"c","grid_export":"d"})
    assert result["pv"].watts == 3100
    assert result["grid"].watts == -1400
    assert evaluate(result, now=NOW)["values"]["pv"] == 3100

def test_import_only():
    readings = {"pv_roof":source(1000), "grid_import":source(400),
                "grid_export":source(0)}
    result = compose(readings, {"pv_roof":"a","grid_import":"c","grid_export":"d"})
    assert result["grid"].watts == 400

def test_missing_second_pv_no_partial_total():
    readings = {"pv_roof":source(1000),"pv_carport":Reading(None,None)}
    assert compose(readings, {"pv_roof":"a","pv_carport":"b"})["pv"].watts is None

def test_missing_grid_channel_no_false_zero():
    readings = {"grid_import":source(200), "grid_export":Reading(None,None)}
    assert compose(readings, {"grid_import":"a","grid_export":"b"})["grid"].watts is None

def test_refuse_negative_split_import():
    readings = {"grid_import":source(-50), "grid_export":source(50)}
    assert compose(readings, {"grid_import":"a","grid_export":"b"})["grid"].watts is None
