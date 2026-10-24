# SPEC-005 · Safe automation
**Status:** Write control intentionally not implemented.

evcc remains sole owner of wallbox control. EnergyOS SHALL NEVER directly send EVSE OCPP commands. Actuation requires approved explicit HA/evcc gateway, independent safeguards, device-specific integration verification, §14a priority, minimum-current validation, manual opt-in, audit trail, idempotency, watchdog and rollback.

AC-SPEC005-01: Current policy always denies any command request.
AC-SPEC005-02: Unhealthy or expired plan denies any action.
AC-SPEC005-03 (future): Commissioned gateway requires human approval and verified rollback.
AC-SPEC005-04 (future): EnergyOS coexists with evcc without competing controller loops.
