"""Constants for the Cleddau Bridge Status integration."""

DOMAIN = "cleddau_bridge"
DEFAULT_NAME = "Cleddau Bridge Status"

DEFAULT_SCAN_INTERVAL = 10  # minutes
DEFAULT_ICON = "mdi:bridge"

API_URL = "https://api.pembrokeshire.gov.uk/myaccount/api/widget"
API_PAYLOAD = {"widgetID": 26}
