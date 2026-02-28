"""Fetch Cleddau Bridge status from Pembrokeshire Council website."""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from html import unescape
from typing import Any

import aiohttp

from .const import BRIDGE_API_URL, BRIDGE_PAGE_URL

_LOGGER = logging.getLogger(__name__)

# Keys to extract from the bridge/latest API response (API key -> stored key)
BRIDGE_WEATHER_KEYS = {
    "currentWindSpeed": "current_wind_speed",
    "currentWindDirection": "current_wind_direction",
    "currentWindCompassCardinalDirection": "current_wind_compass_cardinal_direction",
    "currentMax3sGust": "current_max_3s_gust",
    "airTemperature": "air_temperature",
}


class CleddauBridgeApiError(Exception):
    """Raised when the Pembrokeshire Council bridge status request fails."""


async def async_get_bridge_status(
    session: aiohttp.ClientSession,
) -> dict[str, Any]:
    """Fetch bridge status from the Pembrokeshire Council website.

    Parses the bridgeStatus element from the Cleddau Bridge page.
    Returns a dict with keys: status_id, status_title, status_message, status_date.
    Raises CleddauBridgeApiError on any failure.
    """
    try:
        async with session.get(BRIDGE_PAGE_URL) as response:
            response.raise_for_status()
            html = await response.text()

        block_match = re.search(
            r'<div[^>]*id="bridgeStatus"[^>]*>(.*?)</div>',
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not block_match:
            raise ValueError("bridgeStatus element not found")

        block_html = block_match.group(1)

        # Icon class includes "bridge green" or "bridge red"
        color_match = re.search(
            r'bridge\s+(green|red)',
            block_html,
            flags=re.IGNORECASE,
        )
        color = color_match.group(1).lower() if color_match else "unknown"
        status_id = {"green": "open", "red": "restricted"}.get(color, "unknown")

        # Extract title from <strong> tag
        strong_match = re.search(r"<strong[^>]*>(.*?)</strong>", block_html, re.IGNORECASE | re.DOTALL)
        status_title = unescape(strong_match.group(1).strip()) if strong_match else ""

        # Rest of text (excluding strong) as status_message
        block_without_strong = re.sub(r"<strong[^>]*>.*?</strong>", "", block_html, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r"<br\s*/?>", "\n", block_without_strong, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "", text)
        status_message = unescape(" ".join(text.split())).strip()

        return {
            "status_id": status_id,
            "status_title": status_title,
            "status_message": status_message,
            "status_date": datetime.now(timezone.utc).isoformat(),
        }

    except (aiohttp.ClientError, ValueError) as err:
        raise CleddauBridgeApiError(
            f"Error fetching bridge status: {err}"
        ) from err


async def async_get_bridge_weather(
    session: aiohttp.ClientSession,
) -> dict[str, Any] | None:
    """Fetch weather/wind data from the Pembrokeshire Council bridge API.

    GET https://api.pembrokeshire.gov.uk/bridge/latest
    Returns a dict with snake_case keys for the requested weather fields,
    or None if the request fails (non-fatal; status sensor can still work).
    """
    try:
        async with session.get(BRIDGE_API_URL) as response:
            response.raise_for_status()
            data = await response.json()

        result: dict[str, Any] = {}
        for api_key, stored_key in BRIDGE_WEATHER_KEYS.items():
            if api_key in data:
                result[stored_key] = data[api_key]
        return result

    except (aiohttp.ClientError, ValueError, KeyError) as err:
        _LOGGER.warning("Could not fetch bridge weather data: %s", err)
        return None
