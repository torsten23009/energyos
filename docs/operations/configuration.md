# Configuration
Role mapping uses Home Assistant entity IDs, selected manually or from discovery suggestions. Grid positive means importing from public grid; battery positive means discharging into house. `invert_grid` and `invert_battery` invert incorrect upstream sign directions without changing the original sensor.

Cross-check power unit W/kW, SOC %, timestamps, sampling frequency and AC/DC measurement boundary. Never map EnergyOS derived sensors back into its own source role. The numeric advisor reserve and EV target limits are currently constants, not user-configurable controls; change only with code review.
