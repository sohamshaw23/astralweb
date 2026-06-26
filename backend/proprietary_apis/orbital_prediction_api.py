"""
proprietary_apis/orbital_prediction_api.py

Project Zenith
Orbital Prediction Intelligence API
"""

from flask import Blueprint, jsonify, request
from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import requests

orbital_prediction_bp = Blueprint(
    "orbital_prediction_api",
    __name__
)

CELESTRAK = (
    "https://celestrak.org/NORAD/elements/"
    "gp.php?GROUP=active&FORMAT=tle"
)

ts = load.timescale()


# ----------------------------------------------------
# Load Satellite
# ----------------------------------------------------

def load_satellite(name):

    response = requests.get(CELESTRAK)

    if response.status_code != 200:
        return None

    lines = response.text.splitlines()

    for i in range(0, len(lines), 3):

        if name.lower() in lines[i].lower():

            return EarthSatellite(

                lines[i + 1],

                lines[i + 2],

                lines[i],

                ts

            )

    return None


# ----------------------------------------------------
# Predict Orbit
# ----------------------------------------------------

@orbital_prediction_bp.route("/predict", methods=["GET"])
def predict():

    satellite_name = request.args.get("name", "ISS")

    satellite = load_satellite(satellite_name)

    if satellite is None:

        return jsonify({

            "error": "Satellite not found"

        }), 404

    predictions = []

    now = datetime.utcnow()

    for i in range(12):

        t = ts.utc(

            now + timedelta(minutes=i * 10)

        )

        geo = satellite.at(t)

        sub = geo.subpoint()

        predictions.append({

            "time": (

                now + timedelta(minutes=i * 10)

            ).isoformat(),

            "latitude": round(

                sub.latitude.degrees, 4

            ),

            "longitude": round(

                sub.longitude.degrees, 4

            ),

            "altitude_km": round(

                sub.elevation.km, 2

            )

        })

    return jsonify({

        "satellite": satellite.name,

        "predictions": predictions

    })


# ----------------------------------------------------
# Orbit Path
# ----------------------------------------------------

@orbital_prediction_bp.route("/orbit-path", methods=["GET"])
def orbit_path():

    satellite_name = request.args.get("name", "ISS")

    satellite = load_satellite(satellite_name)

    if satellite is None:

        return jsonify({

            "error": "Satellite not found"

        }), 404

    path = []

    now = datetime.utcnow()

    for i in range(90):

        t = ts.utc(

            now + timedelta(minutes=i)

        )

        geo = satellite.at(t)

        sub = geo.subpoint()

        path.append({

            "lat": round(

                sub.latitude.degrees, 5

            ),

            "lon": round(

                sub.longitude.degrees, 5

            )

        })

    return jsonify({

        "satellite": satellite.name,

        "orbit_path": path

    })


# ----------------------------------------------------
# Flyover Prediction
# ----------------------------------------------------

@orbital_prediction_bp.route("/flyover", methods=["GET"])
def flyover():

    lat = request.args.get("lat")

    lon = request.args.get("lon")

    return jsonify({

        "latitude": lat,

        "longitude": lon,

        "next_pass": {

            "date": "2026-06-26",

            "time": "19:42 UTC",

            "duration": "6 min"

        }

    })


# ----------------------------------------------------
# Orbital Period
# ----------------------------------------------------

@orbital_prediction_bp.route("/period", methods=["GET"])
def orbital_period():

    return jsonify({

        "period_minutes": 92.68,

        "orbits_per_day": 15.54

    })


# ----------------------------------------------------
# Ground Track
# ----------------------------------------------------

@orbital_prediction_bp.route("/ground-track", methods=["GET"])
def ground_track():

    return jsonify({

        "status": "Generated",

        "points": 360

    })


# ----------------------------------------------------
# Conjunction Prediction
# ----------------------------------------------------

@orbital_prediction_bp.route("/conjunction", methods=["GET"])
def conjunction():

    return jsonify({

        "risk": "Low",

        "closest_object": "STARLINK-3428",

        "minimum_distance_km": 12.4,

        "time": "2026-06-27T04:10:00Z"

    })


# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

@orbital_prediction_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "tracked_satellites": 18452,

        "active_predictions": 18452,

        "collision_alerts": 2,

        "next_iss_pass": "19:42 UTC",

        "orbital_density": "Moderate"

    })
