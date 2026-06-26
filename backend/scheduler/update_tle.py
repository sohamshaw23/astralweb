"""
scheduler/update_tle.py

Downloads the latest TLE dataset.
"""

import requests
from datetime import datetime

CELESTRAK = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

OUTPUT = "data/raw/active_satellites.tle"


def update():

    response = requests.get(CELESTRAK, timeout=30)

    response.raise_for_status()

    with open(OUTPUT, "w") as file:
        file.write(response.text)

    print(
        f"[{datetime.utcnow()}] TLE Updated Successfully"
    )


if __name__ == "__main__":
    update()
