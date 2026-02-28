# Cleddau Bridge Status

A custom [Home Assistant](https://www.home-assistant.io/) integration that provides sensors for the current status and weather conditions at the Cleddau Bridge in Pembrokeshire, Wales.

Data is fetched from the [Pembrokeshire County Council](https://www.pembrokeshire.gov.uk/cleddau-bridge) website and their [bridge API](https://api.pembrokeshire.gov.uk/bridge/latest).

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

## Sensors

The integration creates six sensors, all polled every 10 minutes:

### Bridge Status

| Entity | Description |
|--------|-------------|
| `sensor.cleddau_bridge_status` | Current bridge status (e.g. "Open to all vehicles") |

**Attributes**

| Attribute | Description |
|-----------|-------------|
| `status_id` | Status type: `open` or `restricted` |
| `status_message` | Full status message from the council |
| `status_date` | ISO timestamp of the last update |

### Weather & Wind

| Entity | Description |
|--------|-------------|
| `sensor.cleddau_bridge_status_wind_speed` | Current wind speed (mph) |
| `sensor.cleddau_bridge_status_wind_direction` | Wind direction in degrees (°) |
| `sensor.cleddau_bridge_status_wind_compass_direction` | Cardinal direction (e.g. NNE, NNW) |
| `sensor.cleddau_bridge_status_max_3s_gust` | Maximum 3-second wind gust (mph) |
| `sensor.cleddau_bridge_status_air_temperature` | Air temperature (°C) |

## Data Sources

- **Bridge status**: Parsed from the [Cleddau Bridge page](https://www.pembrokeshire.gov.uk/cleddau-bridge) HTML
- **Weather data**: [Pembrokeshire Council bridge API](https://api.pembrokeshire.gov.uk/bridge/latest)
