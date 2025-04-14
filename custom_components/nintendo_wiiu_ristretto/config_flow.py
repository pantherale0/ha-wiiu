"""Config flow handling."""

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    CONF_IP_ADDRESS,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TIMEOUT,
)

from .const import DEFAULT_TIMEOUT, DEFAULT_UPDATE_INTERVAL, DOMAIN

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_IP_ADDRESS): str,
        vol.Required(CONF_PORT, default=8572): int,
        vol.Optional(CONF_NAME, default="Wii U"): str,
        vol.Optional(CONF_SCAN_INTERVAL, default=10): int,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle flow."""

    VERSION = 1
    _dhcp_discovery_info = None

    async def async_step_dhcp(self, discovery_info) -> ConfigFlowResult:
        """Process initial DHCP discovery step."""
        self._dhcp_discovery_info = discovery_info
        return await self.async_step_dhcp_confirm()

    async def async_step_dhcp_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """DHCP Discovery configuration."""
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        configuration = {
            CONF_IP_ADDRESS: self._dhcp_discovery_info.ip,
            CONF_PORT: 8572,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_SCAN_INTERVAL: DEFAULT_UPDATE_INTERVAL
        }
        return self.async_show_form(
            step_id="dhcp_confirm",
            data_schema=self.add_suggested_values_to_schema(
                data_schema=SCHEMA,
                suggested_values=configuration
            ),
            description_placeholders={
                CONF_IP_ADDRESS: self._dhcp_discovery_info.ip
            }
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """User setup step."""
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors=errors,
        )
