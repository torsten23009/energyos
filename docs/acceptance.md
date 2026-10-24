# Acceptance baseline
- AC-DATA-001: W/kW correctly normalized; nonfinite inputs rejected.
- AC-DATA-002: unavailable and stale mandatory sensors block advice.
- AC-DATA-003: sign convention documented; device-specific signs manually verified.
- AC-DISC-001: only plausible available power/SOC sensor candidates suggested.
- AC-DISC-002: ambiguous mappings not silently accepted.
- AC-OPT-001: read-only advisor calculates incremental export headroom minus reserve.
- AC-OPT-002: insufficient data yields no actionable recommendation.
- AC-SAFE-001: policy denies actuator invocation even when enabled.
- AC-HOME-001: deployable as HAOS/HACS custom integration without host changes.
- AC-OPS-001: rollback by disabling integration; backups before installation.

Pure Python test coverage does not prove HA Core compatibility; run hardware-specific acceptance tests separately.
