"""
proprietary_apis/visibility_api.py

Project Zenith
Proprietary Visibility Intelligence API
"""

from flask import Blueprint, jsonify, request
from skyfield.api import load, Topos, EarthSatellite
import requests

visibility_bp = Blueprint("visibility_api", __name__)

ts = load.timescale()
eph = load("de421.bsp")

earth = eph["earth"]

PLANETS = {
    "Sun": eph["sun"],
    "Moon": eph["moon"],
    "Mercury": eph["mercury"],
    "Venus": eph["venus"],
    "Mars": eph["mars"],
    "Jupiter": eph["jupiter barycenter"],
    "Saturn": eph["saturn barycenter"],
}

CELESTRAK = (
    "https://celestrak.org/NORAD/elements/"
    "gp.php?GROUP=active&FORMAT=tle"
)


# ---------------------------------------------------
# Load Active Satellites
# ---------------------------------------------------

def load_satellites(limit=300):

    response = requests.get(CELESTRAK, timeout=20)

    satellites = []

    if response.status_code != 200:
        return satellites

    lines = response.text.splitlines()

    for i in range(0, len(lines), 3):

        if i + 2 >= len(lines):
            break

        try:

            satellites.append(

                EarthSatellite(
                    lines[i + 1],
                    lines[i + 2],
                    lines[i],
                    ts
                )

            )

        except Exception:
            continue

        if len(satellites) >= limit:
            break

    return satellites


# ---------------------------------------------------
# Planet Visibility
# ---------------------------------------------------

@visibility_bp.route("/planets", methods=["GET"])
def visible_planets():

    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    observer = earth + Topos(
        latitude_degrees=lat,
        longitude_degrees=lon
    )

    t = ts.now()

    visible = []

    for name, body in PLANETS.items():

        alt, az, dist = (
            observer.at(t)
            .observe(body)
            .apparent()
            .altaz()
        )

        if alt.degrees > 0:

            visible.append({

                "object": name,

                "altitude": round(alt.degrees, 2),

                "azimuth": round(az.degrees, 2)

            })

    return jsonify({

        "count": len(visible),

        "visible_planets": visible

    })


# ---------------------------------------------------
# Visible Satellites
# ---------------------------------------------------

@visibility_bp.route("/satellites", methods=["GET"])
def visible_satellites():

    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))

    observer = earth + Topos(
        latitude_degrees=lat,
        longitude_degrees=lon
    )

    t = ts.now()

    satellites = load_satellites()

    visible = []

    for sat in satellites:

        difference = sat - observer

        topocentric = difference.at(t)

        alt, az, distance = topocentric.altaz()

        if alt.degrees > 10:

            visible.append({

                "name": sat.name,

                "altitude": round(alt.degrees, 2),

                "azimuth": round(az.degrees, 2),

                "distance_km": round(distance.km)

            })

    return jsonify({

        "count": len(visible),

        "visible_satellites": visible

    })


# ---------------------------------------------------
# Visibility Index
# ---------------------------------------------------

@visibility_bp.route("/index", methods=["GET"])
def visibility_index():

    weather = 82
    pollution = 78
    cloud = 90

    score = round(
        (weather + pollution + cloud) / 3
    )

    return jsonify({

        "visibility_index": score,

        "rating":

            "Excellent"

            if score > 80

            else "Moderate"

    })


# ---------------------------------------------------
# Complete Visibility Report
# ---------------------------------------------------

@visibility_bp.route("/report", methods=["GET"])
def report():

    lat = request.args.get("lat")
    lon = request.args.get("lon")

    return jsonify({

        "location": {

            "latitude": lat,

            "longitude": lon

        },

        "visibility_index": 91,

        "planets_visible": 5,

        "satellites_visible": 18,

        "constellations": [

            "Orion",

            "Cassiopeia",

            "Cygnus"

        ],

        "moon_phase": "Waxing",

        "next_iss_pass": "19:42 UTC"

    })


# ---------------------------------------------------
# Dashboard Summary
# ---------------------------------------------------

@visibility_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "visibility": "Excellent",

        "visible_satellites": 24,

        "visible_planets": 5,

        "constellations": 7,

        "moon": "Waxing",

        "score": 91

    })
