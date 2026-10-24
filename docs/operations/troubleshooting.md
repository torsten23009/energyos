# Troubleshooting
- Integration unavailable: verify file path, HA Core restart and logs.
- Duplicate mappings: pick physically independent source sensors.
- Quality 0/low: inspect unavailable data, timestamps and units; source devices may stop updating.
- Energy-balance residual: compare topology, AC/DC conversions, sign polarity and timestamps; avoid arbitrary corrections.
- EV recommendation absent: EV meter may be unmapped or data are quality-gated.
- Sensor names differ from dashboard YAML: inspect HA Entity Registry and update dashboard YAML.
- HACS installation fails: check release metadata, default branch and integration repository format; manual integration install is a fallback.
- Pi performance degrades: disable EnergyOS first; profile update frequency and source integration availability before enabling it again.
