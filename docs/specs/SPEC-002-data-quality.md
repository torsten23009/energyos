# SPEC-002 · Data quality and physics checks
**Status:** Alpha implementation.

Normalize W/kW, signed grid and battery values. SOC in percent. Reject stale, invalid and nonfinite readings. Derive grid import/export and battery charge/discharge from signed telemetry. Compare measured house load with PV + grid + battery ONLY if all readings share the same AC energy boundary and timestamps are reasonably aligned.

AC-SPEC002-01: Normalization and sign inversion covered by unit tests.
AC-SPEC002-02: Stale PV/grid blocks safe_to_optimize.
AC-SPEC002-03: Missing optional battery does not invent a balance.
AC-SPEC002-04 (future): Independent timestamps and reconciliation distinguish telemetry gaps from genuine imbalances.
AC-SPEC002-05 (future): Sensor health based on source telemetry sequence/timestamps rather than HA update notifications alone.

Risk: battery AC/DC flows and hybrid inverter internals differ between vendors; topology must be documented.
