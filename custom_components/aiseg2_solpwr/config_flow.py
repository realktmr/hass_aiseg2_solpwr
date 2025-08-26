import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class Aiseg2ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AiSEG2 Solar Power."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # 入力を検証する処理をここに入れても良い（簡単のため省略）
            return self.async_create_entry(title="AiSEG2 Solar Power", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host"): str,
            vol.Required("username"): str,
            vol.Required("password"): str,
        })

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @callback
    def async_get_options_flow(config_entry):
        return Aiseg2OptionsFlow(config_entry)

class Aiseg2OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Required("host", default=self.config_entry.data["host"]): str,
            vol.Required("username", default=self.config_entry.data["username"]): str,
            vol.Required("password", default=self.config_entry.data["password"]): str,
        })
        return self.async_show_form(step_id="init", data_schema=data_schema)
