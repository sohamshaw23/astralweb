from flask import Blueprint, jsonify, request
import requests
from skyfield.api import EarthSatellite, load

satellite_bp = Blueprint("satellites", __name__)

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

ts = load.timescale()


def load_tle():
    """
    Fetch Active Satellite TLEs from CelesTrak
    """

    response = requests.get(CELESTRAK_URL)

    if response.status_code != 200:
        return []

    lines = response.text.splitlines()

    satellites = []

    for i in range(0, len(lines), 3):

        if i + 2 >= len(lines):
            break

        try:

            satellite = EarthSatellite(
                lines[i + 1],
                lines[i + 2],
                lines[i],
                ts
            )

            satellites.append(satellite)

        except Exception:
            continue

    return satellites


@satellite_bp.route("/live", methods=["GET"])
def live_satellites():

    satellites = load_tle()

    t = ts.now()

    results = []

    for sat in satellites[:100]:

        geo = sat.at(t)

        subpoint = geo.subpoint()

        results.append({

            "name": sat.name,

            "latitude": round(subpoint.latitude.degrees, 5),

            "longitude": round(subpoint.longitude.degrees, 5),

            "altitude_km": round(subpoint.elevation.km, 2)

        })

    return jsonify(results)


@satellite_bp.route("/count", methods=["GET"])
def satellite_count():

    satellites = load_tle()

    return jsonify({

        "active_satellites": len(satellites)

    })


@satellite_bp.route("/search", methods=["GET"])
def search_satellite():

    name = request.args.get("name", "").lower()

    satellites = load_tle()

    t = ts.now()

    for sat in satellites:

        if name in sat.name.lower():

            geo = sat.at(t)

            sub = geo.subpoint()

            return jsonify({

                "name": sat.name,

                "latitude": sub.latitude.degrees,

                "longitude": sub.longitude.degrees,

                "altitude": sub.elevation.km

            })

    return jsonify({

        "error": "Satellite not found"

    }), 404


@satellite_bp.route("/nearby", methods=["GET"])
def nearby_satellites():

    lat = float(request.args.get("lat"))

    lon = float(request.args.get("lon"))

    satellites = load_tle()

    t = ts.now()

    nearby = []

    for sat in satellites:

        geo = sat.at(t)

        sub = geo.subpoint()

        if abs(sub.latitude.degrees - lat) < 10 and abs(sub.longitude.degrees - lon) < 10:

            nearby.append({

                "name": sat.name,

                "latitude": sub.latitude.degrees,

                "longitude": sub.longitude.degrees,

                "altitude": sub.elevation.km

            })

    return jsonify(nearby)
