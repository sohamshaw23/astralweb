"""
api/celestial.py
Project Zenith

Celestial Intelligence APIs
"""

from flask import Blueprint, jsonify, request
from skyfield.api import load, Topos
from datetime import datetime

celestial_bp = Blueprint("celestial", __name__)

# Load ephemeris
ts = load.timescale()
eph = load('de421.bsp')

earth = eph["earth"]
sun = eph["sun"]
moon = eph["moon"]
mercury = eph["mercury"]
venus = eph["venus"]
mars = eph["mars"]
jupiter = eph["jupiter barycenter"]
saturn = eph["saturn barycenter"]


# ----------------------------
# Home
# ----------------------------

@celestial_bp.route("/", methods=["GET"])
def home():

    return jsonify({
        "service": "Celestial Intelligence API",
        "status": "Running"
    })


# ----------------------------
# Planets
# ----------------------------

@celestial_bp.route("/planets", methods=["GET"])
def planets():

    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))

    observer = earth + Topos(latitude_degrees=latitude,
                             longitude_degrees=longitude)

    t = ts.now()

    objects = [
        ("Sun", sun),
        ("Moon", moon),
        ("Mercury", mercury),
        ("Venus", venus),
        ("Mars", mars),
        ("Jupiter", jupiter),
        ("Saturn", saturn)
    ]

    results = []

    for name, body in objects:

        astrometric = observer.at(t).observe(body)

        apparent = astrometric.apparent()

        alt, az, distance = apparent.altaz()

        results.append({

            "object": name,

            "altitude": round(alt.degrees, 2),

            "azimuth": round(az.degrees, 2),

            "distance_km": round(distance.km)

        })

    return jsonify(results)


# ----------------------------
# Visible Objects
# ----------------------------

@celestial_bp.route("/visible", methods=["GET"])
def visible():

    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))

    observer = earth + Topos(latitude_degrees=latitude,
                             longitude_degrees=longitude)

    t = ts.now()

    bodies = [

        ("Sun", sun),

        ("Moon", moon),

        ("Mercury", mercury),

        ("Venus", venus),

        ("Mars", mars),

        ("Jupiter", jupiter),

        ("Saturn", saturn)

    ]

    visible_objects = []

    for name, body in bodies:

        alt, az, distance = (

            observer.at(t)

            .observe(body)

            .apparent()

            .altaz()

        )

        if alt.degrees > 0:

            visible_objects.append({

                "name": name,

                "altitude": round(alt.degrees, 2),

                "azimuth": round(az.degrees, 2)

            })

    return jsonify({

        "count": len(visible_objects),

        "visible_objects": visible_objects

    })


# ----------------------------
# Moon Phase
# ----------------------------

@celestial_bp.route("/moon", methods=["GET"])
def moon_phase():

    t = ts.now()

    phase = eph["earth"].at(t).observe(moon)

    return jsonify({

        "phase": "Waxing",

        "timestamp": datetime.utcnow().isoformat()

    })


# ----------------------------
# Sunrise / Sunset
# ----------------------------

@celestial_bp.route("/daylight", methods=["GET"])
def daylight():

    latitude = request.args.get("lat")

    longitude = request.args.get("lon")

    return jsonify({

        "latitude": latitude,

        "longitude": longitude,

        "sunrise": "05:32",

        "sunset": "18:21"

    })


# ----------------------------
# Star Catalogue
# ----------------------------

@celestial_bp.route("/stars", methods=["GET"])
def stars():

    stars = [

        "Sirius",

        "Betelgeuse",

        "Rigel",

        "Polaris",

        "Vega",

        "Altair",

        "Deneb"

    ]

    return jsonify({

        "count": len(stars),

        "stars": stars

    })


# ----------------------------
# Constellations
# ----------------------------

@celestial_bp.route("/constellations", methods=["GET"])
def constellations():

    constellations = [

        "Orion",

        "Ursa Major",

        "Cassiopeia",

        "Scorpius",

        "Cygnus",

        "Leo",

        "Taurus"

    ]

    return jsonify({

        "count": len(constellations),

        "constellations": constellations

    })


# ----------------------------
# Zenith Object
# ----------------------------

@celestial_bp.route("/zenith", methods=["GET"])
def zenith():

    latitude = request.args.get("lat")

    longitude = request.args.get("lon")

    return jsonify({

        "latitude": latitude,

        "longitude": longitude,

        "current_zenith":

        {

            "planet": "Venus",

            "constellation": "Orion",

            "visibility": "Excellent"

        }

    })


# ----------------------------
# Summary Dashboard
# ----------------------------

@celestial_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "visible_planets": 5,

        "visible_constellations": 8,

        "moon_phase": "Waxing",

        "next_event": "ISS Flyover",

        "visibility_index": 92

    })
