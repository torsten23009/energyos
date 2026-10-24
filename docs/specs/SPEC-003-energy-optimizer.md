# SPEC-003 · Deterministic optimizer
**Status:** Snapshot advisory implemented; predictive scheduling missing.

Inputs: quality-gated PV/grid/EV measured power, reserve (default 250W), minimum/maximum advisory EV charge power (1400W/3600W). Output: short-lived, explainable advisory snapshot. Export headroom = max(0, -grid - reserve); target = min(maxEV, EV power + headroom). Does not issue commands.

AC-SPEC003-01: Missing mandatory telemetry blocks recommendation.
AC-SPEC003-02: Charging advice never bypasses quality gate.
AC-SPEC003-03: Export sign convention respected.
AC-SPEC003-04: Every recommendation includes explanation and expiry.
AC-SPEC003-05 (future): Forecast adapters and optimization objective (cost, self-consumption, battery reserve, comfort) implemented with reproducible scenario tests.
AC-SPEC003-06 (future): Feasibility constraints account for EVSE active phases, charger min current, Anker wallbox behavior and evcc authority.

Do not claim this is HAEO, EMHASS or EOS. It is a lightweight local heuristic advisory.
