"""DataUpdateCoordinator for Cleddau Bridge."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .poll_bridge import (
    async_get_bridge_status,
    async_get_bridge_weather,
    CleddauBridgeApiError,
)

_LOGGER = logging.getLogger(__name__)


class CleddauBridgeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the Pembrokeshire Council API for bridge status."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=DEFAULT_SCAN_INTERVAL),
        )
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch the latest bridge status and weather from the APIs."""
        try:
            data = await async_get_bridge_status(self._session)
        except CleddauBridgeApiError as err:
            raise UpdateFailed(str(err)) from err

        weather = await async_get_bridge_weather(self._session)
        if weather:
            data.update(weather)

        return data
