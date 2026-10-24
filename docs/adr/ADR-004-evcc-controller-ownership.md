# ADR-004: Single EVSE authority
**Status: Accepted** — 2026-10-24

Decision: evcc is sole EVSE controller. EnergyOS reads measurements and supplies recommendations; no direct OCPP, duplicate load-control loops, or wallbox state modifications. Any future automation must be explicitly approved via a separate capability-aware gateway.
