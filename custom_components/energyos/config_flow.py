"""HAOS-native setup: separate roof/carport PV and import/export smart-meter channels."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN
from .ha_discovery import discover

ENTITY = selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor"))
ROLES = ("pv_roof", "pv_carport", "pv", "grid", "grid_import", "grid_export", "battery", "soc", "load", "ev")

def mapping_schema(defaults=None):
    defaults = defaults or {}
    fields = {}
    for role in ROLES:
        marker = vol.Optional(role, default=defaults[role]) if defaults.get(role) else vol.Optional(role)
        fields[marker] = ENTITY
    fields[vol.Optional("invert_grid", default=defaults.get("invert_grid", False))] = bool
    fields[vol.Optional("invert_battery", default=defaults.get("invert_battery", False))] = bool
    return vol.Schema(fields)

def validate_mapping(values):
    if not (values.get("pv") or values.get("pv_roof") or values.get("pv_carport")):
        return "pv_required"
    if values.get("pv") and (values.get("pv_roof") or values.get("pv_carport")):
        return "pv_conflict"
    if not (values.get("grid") or (values.get("grid_import") and values.get("grid_export"))):
        return "grid_required"
    if values.get("grid") and (values.get("grid_import") or values.get("grid_export")):
        return "grid_conflict"
    picked = [values[k] for k in ROLES if values.get(k)]
    if len(picked) != len(set(picked)):
        return "same_source"
    return None

def discovered_suggestions(hass):
    proposed, _ = discover(hass)
    # Do not auto-fill ambiguous dual PV topology: user must assign physical systems.
    return {key: value for key, value in proposed.items() if key not in ("pv", "grid")}

class EnergyOSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            error = validate_mapping(user_input)
            if error:
                return self.async_show_form(step_id="user", data_schema=mapping_schema(user_input),
                                            errors={"base": error})
            await self.async_set_unique_id("home")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="EnergyOS Home", data=user_input)
        return self.async_show_form(step_id="user", data_schema=mapping_schema(discovered_suggestions(self.hass)))

    @staticmethod
    def async_get_options_flow(config_entry):
        return EnergyOSOptionsFlow()

class EnergyOSOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            error = validate_mapping(user_input)
            if error:
                return self.async_show_form(step_id="init", data_schema=mapping_schema(user_input),
                                            errors={"base": error})
            return self.async_create_entry(title="", data=user_input)
        defaults = {**discovered_suggestions(self.hass), **self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=mapping_schema(defaults))
