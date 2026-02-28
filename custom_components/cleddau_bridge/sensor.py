"""Sensor platform for Cleddau Bridge Status."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_ICON, DEFAULT_NAME, DOMAIN
from .coordinator import CleddauBridgeCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Cleddau Bridge sensor from a config entry."""
    coordinator: CleddauBridgeCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([CleddauBridgeSensor(coordinator, entry)])


class CleddauBridgeSensor(CoordinatorEntity[CleddauBridgeCoordinator], SensorEntity):
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
        """Return the bridge status message."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("status_message")

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        """Return additional state attributes."""
        if self.coordinator.data is None:
            return None
        return {
            "status_id": self.coordinator.data.get("status_id"),
            "status_date": self.coordinator.data.get("status_date"),
        }
