"""
api/isro.py
ISRO Bhuvan & MOSDAC Routes
Project Zenith
"""

from flask import Blueprint, jsonify, request
import json
import os

isro_bp = Blueprint("isro", __name__)

DATA_PATH = "data/processed"


def load_json(filename):
    filepath = os.path.join(DATA_PATH, filename)

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r") as f:
        return json.load(f)


# ----------------------------
# ISRO Satellites
# ----------------------------

@isro_bp.route("/satellites", methods=["GET"])
def indian_satellites():

    satellites = load_json("indian_satellites.json")

    return jsonify({
        "count": len(satellites),
        "satellites": satellites
    })


# ----------------------------
# Weather
# ----------------------------

@isro_bp.route("/weather", methods=["GET"])
def weather():

    weather_data = load_json("weather.json")

    return jsonify(weather_data)


# ----------------------------
# Cyclones
# ----------------------------

@isro_bp.route("/cyclones", methods=["GET"])
def cyclones():

    cyclones = load_json("cyclones.json")

    return jsonify({
        "active_cyclones": cyclones
    })


# ----------------------------
# Floods
# ----------------------------

@isro_bp.route("/floods", methods=["GET"])
def floods():

    floods = load_json("floods.json")

    return jsonify({
        "flood_regions": floods
    })


# ----------------------------
# Wildfires
# ----------------------------

@isro_bp.route("/wildfires", methods=["GET"])
def wildfires():

    fires = load_json("wildfires.json")

    return jsonify({
        "wildfires": fires
    })


# ----------------------------
# Disaster Hotspots
# ----------------------------

@isro_bp.route("/hotspots", methods=["GET"])
def hotspots():

    hotspots = load_json("hotspot_data.json")

    return jsonify({
        "hotspots": hotspots
    })


# ----------------------------
# Coverage
# ----------------------------

@isro_bp.route("/coverage", methods=["GET"])
def coverage():

    latitude = request.args.get("lat")
    longitude = request.args.get("lon")

    return jsonify({

        "latitude": latitude,

        "longitude": longitude,

        "covered_by": [

            "INSAT-3D",

            "EOS-06",

            "Resourcesat-2A"

        ]

    })


# ----------------------------
# National Assets
# ----------------------------

@isro_bp.route("/assets", methods=["GET"])
def assets():

    assets = load_json("national_assets.json")

    return jsonify({

        "count": len(assets),

        "assets": assets

    })


# ----------------------------
# Space Situational Awareness
# ----------------------------

@isro_bp.route("/ssa", methods=["GET"])
def ssa():

    return jsonify({

        "orbital_risk": "Low",

        "traffic_density": "Moderate",

        "protected_assets": 53,

        "active_missions": 21,

        "debris_alert": False

    })


# ----------------------------
# Mission Dashboard Summary
# ----------------------------

@isro_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "weather_alerts": 3,

        "active_cyclones": 1,

        "flood_regions": 7,

        "wildfires": 12,

        "hotspots": 24,

        "indian_satellites": 53,

        "protected_assets": 53

    })
