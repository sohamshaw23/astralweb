"""
api/iss.py
Project Zenith

International Space Station APIs
"""

from flask import Blueprint, jsonify, request
import requests
from datetime import datetime

iss_bp = Blueprint("iss", __name__)

ISS_NOW_URL = "http://api.open-notify.org/iss-now.json"
ISS_PEOPLE_URL = "http://api.open-notify.org/astros.json"


# -----------------------------------
# Current ISS Position
# -----------------------------------

@iss_bp.route("/location", methods=["GET"])
def current_location():

    try:

        response = requests.get(ISS_NOW_URL, timeout=10)
        data = response.json()

        return jsonify({

            "timestamp": data["timestamp"],

            "latitude": float(
                data["iss_position"]["latitude"]
            ),

            "longitude": float(
                data["iss_position"]["longitude"]
            ),

            "status": data["message"]

        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# -----------------------------------
# Crew Members
# -----------------------------------

@iss_bp.route("/crew", methods=["GET"])
def crew():

    try:

        response = requests.get(ISS_PEOPLE_URL, timeout=10)

        astronauts = response.json()

        crew = []

        for person in astronauts["people"]:

            if person["craft"] == "ISS":

                crew.append(person["name"])

        return jsonify({

            "count": len(crew),

            "crew": crew

        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# -----------------------------------
# ISS Speed
# -----------------------------------

@iss_bp.route("/speed", methods=["GET"])
def speed():

    return jsonify({

        "speed_kmh": 27600,

        "speed_mph": 17150

    })


# -----------------------------------
# ISS Altitude
# -----------------------------------

@iss_bp.route("/altitude", methods=["GET"])
def altitude():

    return jsonify({

        "altitude_km": 420,

        "status": "Operational"

    })


# -----------------------------------
# Visibility
# -----------------------------------

@iss_bp.route("/visibility", methods=["GET"])
def visibility():

    latitude = request.args.get("lat")
    longitude = request.args.get("lon")

    return jsonify({

        "latitude": latitude,

        "longitude": longitude,

        "visible": True,

        "elevation": 67.2,

        "azimuth": 214.8,

        "duration_seconds": 380

    })


# -----------------------------------
# Next Flyover (Placeholder)
# -----------------------------------

@iss_bp.route("/flyover", methods=["GET"])
def flyover():

    latitude = request.args.get("lat")
    longitude = request.args.get("lon")

    return jsonify({

        "latitude": latitude,

        "longitude": longitude,

        "next_pass":

        {

            "date": "2026-06-26",

            "time": "19:42 UTC",

            "duration": "6 minutes"

        }

    })


# -----------------------------------
# Telemetry
# -----------------------------------

@iss_bp.route("/telemetry", methods=["GET"])
def telemetry():

    return jsonify({

        "velocity_kmh": 27600,

        "altitude_km": 420,

        "orbital_period_minutes": 92,

        "orbits_per_day": 15.5

    })


# -----------------------------------
# Orbit Summary
# -----------------------------------

@iss_bp.route("/orbit", methods=["GET"])
def orbit():

    return jsonify({

        "orbit_type": "Low Earth Orbit",

        "inclination": 51.64,

        "eccentricity": 0.0004,

        "average_altitude": 420

    })


# -----------------------------------
# Dashboard
# -----------------------------------

@iss_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "crew": 7,

        "speed": "27,600 km/h",

        "altitude": "420 km",

        "orbit": "LEO",

        "status": "Operational",

        "next_event": "Flyover"

    })


# -----------------------------------
# Health
# -----------------------------------

@iss_bp.route("/health", methods=["GET"])
def health():

    return jsonify({

        "service": "ISS API",

        "status": "Running",

        "timestamp": datetime.utcnow().isoformat() + "Z"

    })
