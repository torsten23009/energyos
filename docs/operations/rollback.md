# Rollback on Home Assistant OS
1. Disable EnergyOS integration in Settings → Devices & services.
2. If necessary remove EnergyOS custom integration via HACS; restart HA Core.
3. Optionally restore your pre-install HAOS backup to reverse all changes.
4. No actual device/evcc write actions are present in v0.3.0; rollback is confined to EnergyOS entities and configuration.
5. Verify evcc, Anker and KOSTAL continue independently.
