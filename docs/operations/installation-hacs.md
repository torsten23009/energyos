# HAOS HACS installation and verification
1. Take a full HAOS backup.
2. Open HACS → Custom repositories; paste https://github.com/torsten23009/energyos and select **Integration**.
3. Download EnergyOS; restart HA Core.
4. Settings → Devices & services → Add integration → EnergyOS.
5. Review discovered PV, grid, battery, SOC, house load and EV sensors. Verify units and signs.
6. Check Quality Score and Data Healthy. Compare measured power against physical smart meter and evcc.
7. Check HA Logs for custom component exceptions. If HACS listing or release is unavailable, copy only custom_components/energyos into /config/custom_components/energyos using Studio Code Server, then restart HA Core.
8. Import dashboard YAML carefully and verify resulting entity IDs: entity names may differ after setup.

No OS-level package installation. Do not enable device automation; alpha is read-only.
