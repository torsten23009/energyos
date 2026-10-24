# ADR-001: Home Assistant OS native deployment
**Status: Accepted** — 2026-10-24

Decision: Package as Home Assistant custom integration, installable through HACS or directly under /config/custom_components. Use built-in config flow, HA entities and Recorder. No host apt/pip, host-level Docker Compose or unmanaged OS modifications.

Rationale: managed HAOS on Pi 4, maintenance and predictable upgrades. Heavy solvers are optional and must have independently verified HAOS-compatible packaging.

Consequence: core must remain lightweight and deterministic.
