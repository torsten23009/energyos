"""Conservative metadata-based entity discovery; does not reconfigure HA."""
from dataclasses import dataclass

ROLES = ("pv", "grid", "battery", "soc", "load", "ev")
HINTS = {
    "pv": ("pv power", "solar power", "photovoltaic", "pv leistung", "solarleistung"),
    "grid": ("grid power", "grid active power", "netzleistung", "netzbezug", "smart meter", "meter power"),
    "battery": ("battery power", "batterie leistung", "akku leistung", "storage power", "solarbank power"),
    "soc": ("state of charge", "battery soc", "solarbank soc", "battery level", "ladezustand"),
    "load": ("home consumption", "house load", "house power", "verbrauch haus", "home power"),
    "ev": ("charging power", "charge power", "evcc charge", "wallbox power", "ladeleistung"),
}
NEGATIVE = ("forecast", "tomorrow", "daily", "total energy", "yield", "prognose")

@dataclass(frozen=True)
class Candidate:
    entity_id: str
    score: int
    reason: str

def score_sensor(role, *, entity_id, name="", unit="", device_class="", state_class="", integration="", available=True):
    if role not in ROLES or not entity_id.startswith("sensor.") or not available:
        return 0
    if unit not in ({"%"} if role == "soc" else {"W", "kW"}):
        return 0
    if device_class and device_class != ("battery" if role == "soc" else "power"):
        return 0
    if state_class in ("total", "total_increasing"):
        return 0
    label = f"{entity_id.replace('_', ' ')} {name} {integration}".lower()
    if any(term in label for term in NEGATIVE) or "energyos" in label:
        return 0
    matches = [term for term in HINTS[role] if term in label]
    if not matches:
        return 0
    return min(95, 45 + (20 if device_class else 0) + (10 if state_class == "measurement" else 0) + min(20, len(matches) * 10))

def rank_candidates(role, entities):
    results = []
    for entry in entities:
        score = score_sensor(role, **entry)
        if score:
            results.append(Candidate(entry["entity_id"], score, "metadata/name match; sign and boundary unverified"))
    return sorted(results, key=lambda item: (-item.score, item.entity_id))

def propose_mapping(entities, min_score=65, margin=15):
    rankings = {role: rank_candidates(role, entities) for role in ROLES}
    proposed = {}
    for role, items in rankings.items():
        if items and items[0].score >= min_score and (len(items) == 1 or items[0].score - items[1].score >= margin):
            proposed[role] = items[0].entity_id
    assigned = list(proposed.values())
    repeated = {value for value in assigned if assigned.count(value) > 1}
    return {key: value for key, value in proposed.items() if value not in repeated}, rankings
