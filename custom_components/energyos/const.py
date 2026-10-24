DOMAIN = "energyos"
DEFAULT_SCAN_INTERVAL = 30
SOURCE_KEYS = ("pv", "grid", "battery", "soc", "load", "ev")
DEFAULT_STALE = {"pv": 90, "grid": 60, "battery": 90, "soc": 1200, "load": 90, "ev": 120}
