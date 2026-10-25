"""Regression tests for HA setup, migration and source reconfiguration."""
from unittest.mock import patch
from datetime import timedelta

from homeassistant.helpers.update_coordinator import UpdateFailed
from homeassistant.util import dt as dt_util

import pytest
from homeassistant.config_entries import ConfigEntryState
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_fire_time_changed

DOMAIN = "energyos"
SINGLE = {"pv": "sensor.pv", "grid": "sensor.grid"}
DUAL = {"pv_roof": "sensor.roof", "pv_carport": "sensor.carport",
        "grid_import": "sensor.import", "grid_export": "sensor.export"}
pytestmark = pytest.mark.asyncio

def sources(hass):
    for name, value in {"pv": 1000, "grid": -400, "roof": 1600,
                        "carport": 400, "import": 0, "export": 700}.items():
        hass.states.async_set(f"sensor.{name}", value,
                              {"unit_of_measurement": "W", "device_class": "power"})

async def setup(hass, *, version=2, data=None, options=None):
    sources(hass)
    entry = MockConfigEntry(domain=DOMAIN, title="EnergyOS Home", unique_id="home",
                            version=version, data=data or SINGLE, options=options or {})
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    return entry

def state(hass, entry, key, domain="sensor"):
    entity_id = er.async_get(hass).async_get_entity_id(domain, DOMAIN, f"{entry.entry_id}_{key}")
    assert entity_id is not None
    return hass.states.get(entity_id)

async def test_setup_reload_unload(hass):
    entry = await setup(hass, data=DUAL)
    assert state(hass, entry, "pv_power").state == "2000.0"
    assert state(hass, entry, "grid_signed").state == "-700.0"
    assert state(hass, entry, "data_healthy", "binary_sensor").state == "on"
    ids = {e.entity_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)}
    assert len(ids) == 20
    assert await hass.config_entries.async_reload(entry.entry_id)
    await hass.async_block_till_done()
    assert ids == {e.entity_id for e in er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)}
    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED

async def test_v1_entry_migrates_without_losing_mapping(hass):
    entry = await setup(hass, version=1)
    assert entry.version == 2
    assert dict(entry.data) == SINGLE

async def test_options_replace_old_topology(hass):
    entry = await setup(hass)
    result = await hass.config_entries.options.async_init(entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.options.async_configure(result["flow_id"], user_input=DUAL)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    assert state(hass, entry, "pv_power").state == "2000.0"
    assert state(hass, entry, "grid_signed").state == "-700.0"

async def test_missing_source_is_unhealthy_not_setup_failure(hass):
    entry = await setup(hass, data={"pv": "sensor.missing", "grid": "sensor.grid"})
    assert state(hass, entry, "data_healthy", "binary_sensor").state == "off"
    assert state(hass, entry, "pv_power").state == "unknown"

async def test_user_flow_and_duplicate(hass):
    sources(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    assert result["type"] is FlowResultType.FORM
    result = await hass.config_entries.flow.async_configure(result["flow_id"], user_input=DUAL)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    await hass.async_block_till_done()
    duplicate = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    if duplicate["type"] is FlowResultType.FORM:
        duplicate = await hass.config_entries.flow.async_configure(duplicate["flow_id"], user_input=DUAL)
    assert duplicate["type"] is FlowResultType.ABORT
    assert duplicate["reason"] in {"already_configured", "single_instance_allowed"}


async def test_initial_update_failure_retries(hass, freezer):
    sources(hass)
    entry = MockConfigEntry(domain=DOMAIN, unique_id="home", version=2, data=SINGLE)
    entry.add_to_hass(hass)
    with patch("custom_components.energyos.coordinator.EnergyOSCoordinator._async_update_data",
               side_effect=UpdateFailed("temporary failure")):
        assert not await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY
    assert not er.async_entries_for_config_entry(er.async_get(hass), entry.entry_id)
    freezer.tick(timedelta(seconds=10))
    async_fire_time_changed(hass, dt_util.utcnow())
    await hass.async_block_till_done(wait_background_tasks=True)
    assert entry.state is ConfigEntryState.LOADED


async def test_stale_sources_recover(hass):
    entry = await setup(hass, data=DUAL)
    with patch("custom_components.energyos.coordinator.dt_util.utcnow",
               return_value=dt_util.utcnow() + timedelta(minutes=3)):
        await entry.runtime_data.async_refresh()
        await hass.async_block_till_done()
    assert state(hass, entry, "data_healthy", "binary_sensor").state == "off"
    assert state(hass, entry, "ev_recommendation").state == "unknown"
    sources(hass)
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()
    assert state(hass, entry, "data_healthy", "binary_sensor").state == "on"


async def test_options_can_remove_optional_sensor(hass):
    entry = await setup(hass, data={**SINGLE, "ev": "sensor.carport"})
    result = await hass.config_entries.options.async_init(entry.entry_id)
    await hass.config_entries.options.async_configure(result["flow_id"], user_input=SINGLE)
    await hass.async_block_till_done()
    assert state(hass, entry, "ev_power").state == "unknown"
    result = await hass.config_entries.options.async_init(entry.entry_id)
    fields = {str(key): key for key in result["data_schema"].schema}
    assert not fields["ev"].description


async def test_diagnostics_use_current_dual_mapping(hass):
    from custom_components.energyos.diagnostics import async_get_config_entry_diagnostics
    entry = await setup(hass, options=DUAL)
    result = await async_get_config_entry_diagnostics(hass, entry)
    assert set(result["configured_roles"]) == set(DUAL)
    assert not any(value in str(result) for value in DUAL.values())


@pytest.mark.parametrize(("mapping", "error"), [
    ({"grid": "sensor.grid"}, "pv_required"),
    ({**SINGLE, "pv_roof": "sensor.roof"}, "pv_conflict"),
    ({"pv": "sensor.pv", "grid_import": "sensor.import"}, "grid_required"),
    ({**SINGLE, "grid_export": "sensor.export"}, "grid_conflict"),
    ({"pv": "sensor.pv", "grid": "sensor.pv"}, "same_source"),
])
async def test_invalid_mapping_stays_in_form(hass, mapping, error):
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": "user"})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], user_input=mapping)
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}
