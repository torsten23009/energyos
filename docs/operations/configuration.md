# Configuration
Role mapping uses Home Assistant entity IDs, selected manually or from discovery suggestions. Grid positive means importing from public grid; battery positive means discharging into house. `invert_grid` and `invert_battery` invert incorrect upstream sign directions without changing the original sensor.

Cross-check power unit W/kW, SOC %, timestamps, sampling frequency and AC/DC measurement boundary. Never map EnergyOS derived sensors back into its own source role. The numeric advisor reserve and EV target limits are currently constants, not user-configurable controls; change only with code review.


## Dual-PV + split smart-meter configuration (v0.3.1)
- `pv_roof`: KOSTAL PIKO MP Plus roof PV **instantaneous power** (W/kW).
- `pv_carport`: Anker Solarbank 2 Pro carport PV **instantaneous PV production** (W/kW).
- Keep legacy `pv` blank when mapping roof + carport separately.
- `grid_import` / `grid_export`: smart-meter instantaneous nonnegative **power** channels (W/kW), not lifetime energy totals (Wh/kWh).
- Keep `grid` blank in split-meter mode. Alternatively use `grid` alone with positive import / negative export.
- `battery`: optional signed battery charging/discharging power (positive discharge, negative charge) at a consistent electrical boundary; do not substitute inverter AC output or PV generation.
- `soc`: Anker battery state of charge (%).
- `load`: OPTIONAL independent house power reading. Do **not** use Home Power Estimated to validate EnergyOS's calculated house power: an estimated input can be circular.
- `ev`: optional evcc measured charging power (W/kW); evcc continues to control the EVSE.
**Caveat:** Anker PV power and AC battery output can cause double counting if the selected telemetry spans mismatched AC/DC boundaries. Compare with smart meter and battery flow before trusting house-load balance.
If an existing EnergyOS entry exists, edit via integration configuration/options; if the old fields are locked, delete only the EnergyOS entry and add it again.
