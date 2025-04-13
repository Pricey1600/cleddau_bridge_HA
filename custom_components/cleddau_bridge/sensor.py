"""Platform for sensor integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_NAME,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
import voluptuous as vol

from .const import DEFAULT_SCAN_INTERVAL, DEFAULT_ICON, DEFAULT_NAME
from .poll_bridge import api_polling

SCAN_INTERVAL = timedelta(minutes=DEFAULT_SCAN_INTERVAL)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    add_entities([BridgeSensor()])


class BridgeSensor(SensorEntity):
    """Representation of a Sensor."""

    _state = api_polling.check_status()[1]

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        # self._attr_native_value = poll_bridge.check_status()[1]
        self._attr_native_value = self._state

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "cleddauBridgeStatus"

    @property
    def name(self):
        """Return the name of the sensor."""
        return DEFAULT_NAME

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return DEFAULT_ICON

    @property
    def state_class(self):
        """Return the state class."""
        return SensorStateClass.MEASUREMENT

    @property
    def state(self):
        """Return the state of the device."""
        return self._state
