# Cleddau Bridge Status

A custom [Home Assistant](https://www.home-assistant.io/) integration that provides a sensor showing the current open/closed status of the Cleddau Bridge in Pembrokeshire, Wales.

The status is fetched from the [Pembrokeshire County Council](https://www.pembrokeshire.gov.uk/) API.

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click the three dots in the top right corner and select **Custom repositories**
3. Add `https://github.com/Pricey1600/cleddau_bridge_HA` as a custom repository with category **Integration**
4. Click **Install**
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/cleddau_bridge` directory to your Home Assistant `custom_components` folder
2. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **Add Integration**
3. Search for **Cleddau Bridge Status**
4. Click **Submit** to complete setup

## Sensor

The integration creates a single sensor:

| Entity | Description |
|--------|-------------|
| `sensor.cleddau_bridge_status` | Current status of the Cleddau Bridge |

### Attributes

| Attribute | Description |
|-----------|-------------|
| `status_id` | Numeric status identifier from the API |
| `status_date` | Date/time the status was last updated by the council |

The sensor polls the Pembrokeshire Council API every 10 minutes.
