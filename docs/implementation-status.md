# Implementation status · v0.3.1 alpha

| Capability | State |
|---|---|
| Core config flow and mapping | Implemented; Home Assistant runtime not validated |
| Metadata-based conservative auto discovery | Implemented; field accuracy not validated |
| Normalization, power balance, timestamp validation | Implemented as limited v1 rules |
| Live snapshot surplus advisory | Implemented; read only |
| HA-native sensor diagnostics | Implemented; integration smoke test pending |
| Dashboard example | Included; UI rendering not validated |
| 24h/48h optimizer, tariffs, weather forecast | NOT implemented |
| HAEO/EMHASS/EOS integration | NOT implemented |
| Self-learning/automatic remapping | NOT implemented |
| Write control / evcc actuator gateway | NOT implemented, intentionally blocked |
| Pi 4 memory/performance/hardware testing | NOT tested |
| HACS release and installation check | NOT tested |

See specs and ADRs for intended future scope. **Do not use advisory numbers for autonomous charging yet.**

## Multi-PV setup update
Dual PV sources and split smart-meter instantaneous import/export W values are supported at the config and sensor composition layers. Unavailable source sensor blocks total rather than silently reporting a partial measurement. Home Assistant runtime integration testing still pending.
