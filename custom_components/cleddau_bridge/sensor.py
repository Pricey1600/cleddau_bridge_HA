"""Sensor platform for Cleddau Bridge Status."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_ICON, DEFAULT_NAME, DOMAIN
from .coordinator import CleddauBridgeCoordinator

# Weather sensors from api.pembrokeshire.gov.uk/bridge/latest
WEATHER_SENSORS: list[dict[str, Any]] = [
    {
        "key": "current_wind_speed",
        "name": "Wind Speed",
        "icon": "mdi:weather-windy",
        "unit": "mph",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "current_wind_direction",
        "name": "Wind Direction",
        "icon": "mdi:compass-outline",
        "unit": "°",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "current_wind_compass_cardinal_direction",
        "name": "Wind Compass Direction",
        "icon": "mdi:compass-rose",
        "unit": None,
        "state_class": None,
    },
    {
        "key": "current_max_3s_gust",
        "name": "Max 3s Gust",
        "icon": "mdi:weather-tornado",
        "unit": "mph",
        "state_class": SensorStateClass.MEASUREMENT,
    },
    {
        "key": "air_temperature",
        "name": "Air Temperature",
        "icon": "mdi:thermometer",
        "unit": "°C",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Cleddau Bridge sensors from a config entry."""
    coordinator: CleddauBridgeCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[SensorEntity] = [
        CleddauBridgeStatusSensor(coordinator, entry),
    ]
    for cfg in WEATHER_SENSORS:
        entities.append(CleddauBridgeWeatherSensor(coordinator, entry, cfg))
    async_add_entities(entities)


class CleddauBridgeStatusSensor(
    CoordinatorEntity[CleddauBridgeCoordinator], SensorEntity
):
    """Sensor showing the current status of the Cleddau Bridge."""

    _attr_icon = DEFAULT_ICON
    _attr_name = DEFAULT_NAME

    def __init__(
        self,
        coordinator: CleddauBridgeCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def native_value(self) -> str | None:
        """Return the bridge status title (headline from strong tag)."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("status_title") or self.coordinator.data.get("status_message")

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return None
        return {
            "status_id": self.coordinator.data.get("status_id"),
            "status_message": self.coordinator.data.get("status_message"),
            "status_date": self.coordinator.data.get("status_date"),
        }


class CleddauBridgeWeatherSensor(
    CoordinatorEntity[CleddauBridgeCoordinator], SensorEntity
):
    """Sensor for bridge weather/wind data from the API."""

    def __init__(
        self,
        coordinator: CleddauBridgeCoordinator,
        entry: ConfigEntry,
        config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._key = config["key"]
        self._attr_unique_id = f"{entry.entry_id}_{self._key}"
        self._attr_name = f"{DEFAULT_NAME} {config['name']}"
        self._attr_icon = config.get("icon", "mdi:weather-partly-cloudy")
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_device_class = config.get("device_class")
        self._attr_state_class = config.get("state_class")

    @property
    def native_value(self) -> str | int | float | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self._key)
