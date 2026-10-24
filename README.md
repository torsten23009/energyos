# EnergyOS · HAOS-native energy intelligence

**Status: v0.3.0 development alpha — read-only, NOT validated on production hardware.**

EnergyOS is a Home Assistant OS compatible, low-overhead custom integration for unified PV/grid/battery/EV energy telemetry, conservative sensor autodiscovery, data-health diagnostics, and deterministic *advisory-only* charging recommendations.

## Features
- Native Home Assistant config/options flows; six sensor roles: PV, grid, battery, SOC, load, EV.
- Metadata-based suggestions. Mapping must be reviewed before applying.
- Unit conversion W/kW/%; optional signed grid/battery inversion.
- Data freshness, sanity and optional power-balance checks.
- Virtual EnergyOS sensors, health state and diagnostics.
- Live surplus advisor with fixed reserve and charger recommendation (not a 24-hour forecast).
- **No devices controlled. evcc remains the sole EVSE controller.**

## HAOS / HACS install
1. Back up Home Assistant.
2. HACS → menu → Custom repositories → `https://github.com/torsten23009/energyos`, category **Integration**.
3. Select EnergyOS, download; restart Home Assistant.
4. Settings → Devices & services → Add integration → EnergyOS.
5. Review manually PV, grid, battery, EV and load mapping, including sign conventions.
6. Validate derived metrics against HA Energy Dashboard before trusting any recommendation.
7. The example dashboard is in `dashboards/energyos-overview.yaml`, with entity IDs to review.

HACS may require a repository release and compatibility review; if unavailable, manually copy `custom_components/energyos` into HAOS `/config/custom_components/energyos` via Studio Code Server or File Editor and restart HA Core.

**HAOS constraint:** No host apt/pip, Docker Compose or privileged host access. `requirements-dev.txt` is for local CI/dev machines, not the HAOS host.

## Source semantics
- Grid: **positive = import**, negative = export.
- Battery: **positive = discharge**, negative = charging.
- Power values in watts; state of charge as percentage.
- Freshness uses HA state timestamps; an unchanged HA state may hide a stale physical device value. Follow up with vendor-specific telemetry freshness.

## Documentation
- [System architecture](docs/architecture.md)
- [Implementation status](docs/implementation-status.md)
- [Acceptance criteria](docs/acceptance.md)
- [Specs](docs/specs/SPEC-001-sensor-discovery.md)
- [ADRs](docs/adr/ADR-001-haos-native.md)
- [HACS guide](docs/operations/installation-hacs.md)
- [Rollback](docs/operations/rollback.md)
- [Test matrix](docs/testing/acceptance-matrix.md)

## Known limitations
- No optimized 24-hour schedule, HAEO/EMHASS/EOS adapter or predictive forecasting yet.
- No storage or EVSE write integration; policy always denies actuator requests.
- No real PIKO MP Plus/Anker/Tesla/evcc or Raspberry Pi 4 runtime validation.
- Metrics can be inaccurate when PV/grid/battery sensors have differing electrical boundaries or sampling times.
- Example dashboard is not a custom frontend panel. Device and sensor identities must be confirmed.
