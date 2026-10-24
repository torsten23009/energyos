"""Native config flow with conservative auto-suggestions and manual confirmation."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from .const import DOMAIN
from .ha_discovery import discover

ENTITY = selector.EntitySelector(selector.EntitySelectorConfig(domain="sensor"))

def mapping_schema(defaults=None):
    defaults = defaults or {}
    fields = {}
    for role in ("pv", "grid", "battery", "soc", "load", "ev"):
        marker = vol.Required(role, default=defaults[role]) if role in defaults else (
            vol.Required(role) if role in ("pv", "grid") else vol.Optional(role))
        fields[marker] = ENTITY
    fields[vol.Optional("invert_grid", default=defaults.get("invert_grid", False))] = bool
    fields[vol.Optional("invert_battery", default=defaults.get("invert_battery", False))] = bool
    return vol.Schema(fields)

class EnergyOSConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id("home")
            self._abort_if_unique_id_configured()
            mapped = [v for k, v in user_input.items() if k in ("pv", "grid", "battery", "soc", "load", "ev")]
            if len(mapped) != len(set(mapped)):
                return self.async_show_form(step_id="user", data_schema=mapping_schema(user_input),
                                            errors={"base": "same_source"})
            return self.async_create_entry(title="EnergyOS Home", data=user_input)
        proposed, _ = discover(self.hass)
        return self.async_show_form(step_id="user", data_schema=mapping_schema(proposed),
                                    description_placeholders={"autodetected": ", ".join(sorted(proposed)) or "none"})

    @staticmethod
    def async_get_options_flow(config_entry):
        return EnergyOSOptionsFlow()

class EnergyOSOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        proposed, _ = discover(self.hass)
        defaults = {**proposed, **self.config_entry.data, **self.config_entry.options}
        return self.async_show_form(step_id="init", data_schema=mapping_schema(defaults))
