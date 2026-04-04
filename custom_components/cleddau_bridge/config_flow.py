"""Config flow for the Cleddau Bridge Status integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .const import (
    AIOHTTP_MAX_FIELD_SIZE,
    AIOHTTP_MAX_LINE_SIZE,
    DOMAIN,
)
from .poll_bridge import async_get_bridge_status, CleddauBridgeApiError

_LOGGER = logging.getLogger(__name__)


class CleddauBridgeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cleddau Bridge Status."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}

        if user_input is not None:
            session = async_create_clientsession(
                self.hass,
                auto_cleanup=False,
                max_line_size=AIOHTTP_MAX_LINE_SIZE,
                max_field_size=AIOHTTP_MAX_FIELD_SIZE,
            )
            try:
                await async_get_bridge_status(session)
            except CleddauBridgeApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title="Cleddau Bridge",
                    data={},
                )
            finally:
                session.detach()

        return self.async_show_form(step_id="user", errors=errors)
