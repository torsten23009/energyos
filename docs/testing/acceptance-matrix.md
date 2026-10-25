# Acceptance matrix

| Requirement | Evidence | Status |
|---|---|---|
| AC-DATA-001 normalization | Pure Python tests | Partially covered |
| AC-DATA-002 freshness | Pure Python tests | Partially covered |
| AC-DISC-001 metadata ranking | Pure Python tests | Partially covered |
| AC-OPT-001 surplus advice | Pure Python tests | Partially covered |
| AC-SAFE-001 policy closed | Pure Python tests | Covered |
| HA Core lifecycle, migration, options, recovery | 14 real-HA tests on Core 2026.2.3 and 2026.10.4 | Passed locally; CI matrix added |
| AC-HOME-001 real HAOS installation | Actual HAOS acceptance checklist | Not done |
| Pi 4 long running stability | 48-hour soak test | Not done |
| Device-specific topology correctness | Measured comparison | Not done |
| HACS install/update | HAOS install test | Not done |
| Phase 2 24h scheduler | Forecast backtest | Not implemented |
| Phase 4 automation | Security/guardrail hardware test | Not implemented |

See [HA integration verification](ha-integration.md) for environments, scope and the actual HAOS acceptance checklist.
