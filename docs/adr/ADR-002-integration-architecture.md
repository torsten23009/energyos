# ADR-002: Source existing HA integrations
**Status: Accepted** — 2026-10-24

Decision: Map trusted HA sensors rather than duplicate PV inverter/storage/EVSE drivers. Separate discovery, normalization, advisory logic and safety policy. Unknown device-specific capabilities are not assumed.

Consequences: fast adoption but dependent on upstream integration data quality. Vendor support for KOSTAL PIKO MP Plus and Anker Solarbank 2 Pro must be verified independently.
