# Architecture
Home Assistant OS → existing integrations (KOSTAL, Anker, Smart Meter, evcc) → EnergyOS Custom Integration → diagnostic sensors and advisory optimizer → HA Recorder/Dashboards.

`ha_discovery.py` reads entity metadata; `discovery.py` ranks candidates; `config_flow.py` makes review mandatory. `coordinator.py` reads mapped HA sensor states every 30 seconds. `engine.py` applies units, sign conventions, freshness and optional residual checks. `advisor.py` computes a deterministic snapshot EV charge recommendation, and `policy.py` **never authorizes writes**. No API calls to device controllers.

HAOS compatible: integration files under `/config/custom_components/energyos`; no external daemon or unmanaged container. Recorder is optional history infrastructure. HACS distributes custom integration.

Architecture limits: battery boundary and grid sign vary by physical installation. Never treat a computed balance from identical source data as independent data-quality proof.
