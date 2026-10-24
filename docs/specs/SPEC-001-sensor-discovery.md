# SPEC-001 · Sensor discovery and verified mapping
**Status:** Partially implemented.

Goal: detect plausible HA sensor entities for PV, grid, battery, SOC, house load, EV charge power without invasive changes.

Algorithm: query registry/state, reject unavailable entries or incompatible units/device classes, rank using role-specific naming and integration metadata, propose mapping only when sufficiently confident and unambiguous. Always require user review.

AC-SPEC001-01: No arbitrary sensor from unsupported class/unit is suggested.
AC-SPEC001-02: Ambiguous top-two candidates are withheld.
AC-SPEC001-03: EnergyOS's own sensors are never chosen as sources.
AC-SPEC001-04: Sign and electrical measuring boundary require explicit confirmation.
AC-SPEC001-05 (future): Confidence calibrated using time-series independent verification and user-confirmed source metadata; never auto-remap production mappings without approval.

Data quality is not the same as sensor correctness: plausible metadata can still identify a wrong meter.
