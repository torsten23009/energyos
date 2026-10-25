# Home Assistant integration verification

The unit suite in `tests/` deliberately bypasses the HA package initializer.
The separate `tests_ha/` suite imports `custom_components.energyos` through the
real Home Assistant loader. No HA lifecycle methods or entity platforms are mocked.
Only the temporary update-failure test injects an exception.

## Reproducible environments

| Python | HA Core | pytest-homeassistant-custom-component |
|---|---|---|
| 3.13 | 2026.2.3 | 0.13.316 |
| 3.14 | 2026.10.4 | 0.13.375 |

In a development virtual environment, install `requirements-ha.txt`, then run:

```sh
python -m pytest tests_ha -q -o asyncio_mode=auto
```

Local result on 2026-10-25: 14 integration tests passed in each environment.

Both environments are separate CI jobs. The lightweight Python 3.12 unit job
continues to install only `requirements-dev.txt`.

Coverage: actual config flow and duplicate prevention; invalid topology forms;
v1-to-v2 entry migration preserving mappings; creation of 20 entities; reload
without duplicate entity IDs; unload; complete options replacement and optional
sensor removal; missing/stale inputs; recovery; initial update failure and HA's
automatic retry; diagnostics using the active mapping.

## HAOS acceptance on the actual installation (still required)

1. Back up HA, install the reviewed integration update using HACS or copy only
   `custom_components/energyos` into `/config/custom_components/energyos`.
   Restart **Home Assistant Core**. Do not install Python packages on the HAOS host.
2. Open Settings → Devices & services → EnergyOS. Existing v1 entries must load
   and retain their source IDs. `already_configured` means an entry exists;
   inspect its state rather than adding or deleting it again.
3. Configure roof and carport PV, plus instantaneous grid import/export in W/kW.
   Leave the alternative total PV and signed-grid fields empty. Never map kWh
   cumulative counters as power. Save; verify the integration reloads.
4. Under Settings → Devices & services → Entities, filter by EnergyOS.
   There should be 19 sensors and one binary sensor for the entry, including
   PV Total Power and Data Healthy. This integration does not create a device
   or a dashboard automatically. A missing device card is not a failed setup.
5. Compare PV total to roof + carport, and signed grid to import minus export.
   Check actual physical meter readings, timestamps and AC/DC boundaries.
   Unknown optional sensors are expected when those roles are not mapped.
6. Reload, then restart Core; confirm entity IDs remain stable and there are no
   EnergyOS setup/migration errors. Confirm diagnostic download works.
7. Observe for 48 hours on the Pi 4. Check memory, recorder volume and stale
   source handling. This is not covered by simulated HA Core tests.

The integration remains read-only. No wallbox, inverter or battery commands are
introduced. Real hardware accuracy, HACS delivery and HAOS stability are not
proven by a green Core test suite.

Rollback: restore the previous integration files and restart Core. Version 0.3.1
understands v2 mappings; restoring 0.3.0 (v1) also requires the pre-update HA backup.

## Design references

- https://developers.home-assistant.io/docs/config_entries_index/
- https://developers.home-assistant.io/docs/integration_fetching_data/
- https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
- https://developers.home-assistant.io/docs/core/integration-quality-scale/rules/runtime-data/
