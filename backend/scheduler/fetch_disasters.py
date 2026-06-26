"""
scheduler/fetch_disasters.py

Downloads latest disaster events.
"""

import requests
import json
from datetime import datetime

NASA_EONET = "https://eonet.gsfc.nasa.gov/api/v3/events"

OUTPUT = "data/raw/eonet_events.json"


def fetch():

    response = requests.get(
        NASA_EONET,
        timeout=30
    )

    response.raise_for_status()

    with open(OUTPUT, "w") as file:

        json.dump(

            response.json(),

            file,

            indent=4

        )

    print(

        f"[{datetime.utcnow()}] Disaster data updated."

    )


if __name__ == "__main__":

    fetch()
