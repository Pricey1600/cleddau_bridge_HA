"""Checks status of bridge."""

import requests


class api_polling:
    """Checks status of bridge using API."""

    global API_URL
    API_URL = "https://api.pembrokeshire.gov.uk/myaccount/api/widget"
    global PAYLOAD
    PAYLOAD = {"widgetID": 26}

    def check_status():
        """Check status of bridge."""
        session = requests.Session()

        form_data = PAYLOAD

        response = session.post(API_URL, json=form_data)

        status_id = response.json()["data"]["widgetData"]["data"]["status_id"]
        status_message = response.json()["data"]["widgetData"]["data"]["status_message"]
        status_date = response.json()["data"]["widgetData"]["data"]["status_date"]

        return [status_id, status_message, status_date]
