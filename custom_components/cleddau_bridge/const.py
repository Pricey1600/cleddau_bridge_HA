"""Constants for the Cleddau Bridge Status integration."""

DOMAIN = "cleddau_bridge"
DEFAULT_NAME = "Cleddau Bridge Status"

DEFAULT_SCAN_INTERVAL = 10  # minutes
DEFAULT_ICON = "mdi:bridge"

BRIDGE_PAGE_URL = "https://www.pembrokeshire.gov.uk/cleddau-bridge"
BRIDGE_API_URL = "https://api.pembrokeshire.gov.uk/bridge/latest"

# Council pages can send header lines (e.g. Set-Cookie) longer than aiohttp's 8190-byte default.
AIOHTTP_MAX_LINE_SIZE = 65536
AIOHTTP_MAX_FIELD_SIZE = 65536

# HTTP timeouts and retries (transient CDN / TLS / network blips).
REQUEST_TIMEOUT_SECONDS = 45
STATUS_FETCH_RETRIES = 3
STATUS_RETRY_BACKOFF_SECONDS = 1.5
