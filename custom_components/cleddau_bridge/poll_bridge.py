"""Fetch Cleddau Bridge status from Pembrokeshire Council API."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp

from .const import API_URL, API_PAYLOAD

_LOGGER = logging.getLogger(__name__)


class CleddauBridgeApiError(Exception):
    """Raised when the Pembrokeshire Council API request fails."""


async def async_get_bridge_status(
    session: aiohttp.ClientSession,
) -> dict[str, Any]:
    """Fetch bridge status from the Pembrokeshire Council API.

    Returns a dict with keys: status_id, status_message, status_date.
    Raises CleddauBridgeApiError on any failure.
    """
    try:
        async with session.post(API_URL, json=API_PAYLOAD) as response:
            response.raise_for_status()
            data = await response.json()
            widget_data = data["data"]["widgetData"]["data"]
            return {
                "status_id": widget_data["status_id"],
                "status_message": widget_data["status_message"],
                "status_date": widget_data["status_date"],
            }
    except (aiohttp.ClientError, KeyError, ValueError) as err:
        raise CleddauBridgeApiError(
            f"Error fetching bridge status: {err}"
        ) from err
