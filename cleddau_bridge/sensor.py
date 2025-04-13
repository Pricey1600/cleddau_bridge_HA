"""Platform for sensor integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DEFAULT_SCAN_INTERVAL
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

    _attr_name = "Bridge Status"
    # _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    # _attr_device_class = SensorDeviceClass.TEMPERATURE
    # _attr_state_class = SensorStateClass.MEASUREMENT
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


# print(poll_bridge.check_status()[1])
