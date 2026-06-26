"""
api/disasters.py
Project Zenith

Disaster Intelligence APIs
"""

from flask import Blueprint, jsonify, request
import requests
import json
import os

disaster_bp = Blueprint("disasters", __name__)

NASA_EONET = "https://eonet.gsfc.nasa.gov/api/v3/events"

DATA_PATH = "data/processed"


# ----------------------------------
# Utility
# ----------------------------------

def load_json(filename):

    filepath = os.path.join(DATA_PATH, filename)

    if not os.path.exists(filepath):
        return []

    with open(filepath, "r") as f:
        return json.load(f)


# ----------------------------------
# Live NASA EONET Events
# ----------------------------------

@disaster_bp.route("/live", methods=["GET"])
def live_events():

    try:

        response = requests.get(NASA_EONET)

        if response.status_code != 200:
            return jsonify({"error": "Unable to fetch data"}), 500

        data = response.json()

        events = []

        for event in data["events"]:

            events.append({

                "id": event["id"],

                "title": event["title"],

                "category": event["categories"][0]["title"],

                "status": event["closed"],

                "geometry": event["geometry"][-1]

            })

        return jsonify({

            "count": len(events),

            "events": events

        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# ----------------------------------
# Wildfires
# ----------------------------------

@disaster_bp.route("/wildfires", methods=["GET"])
def wildfires():

    fires = load_json("wildfires.json")

    return jsonify({

        "count": len(fires),

        "wildfires": fires

    })


# ----------------------------------
# Floods
# ----------------------------------

@disaster_bp.route("/floods", methods=["GET"])
def floods():

    floods = load_json("floods.json")

    return jsonify({

        "count": len(floods),

        "floods": floods

    })


# ----------------------------------
# Cyclones
# ----------------------------------

@disaster_bp.route("/cyclones", methods=["GET"])
def cyclones():

    cyclones = load_json("cyclones.json")

    return jsonify({

        "count": len(cyclones),

        "cyclones": cyclones

    })


# ----------------------------------
# Volcanoes
# ----------------------------------

@disaster_bp.route("/volcanoes", methods=["GET"])
def volcanoes():

    volcanoes = load_json("volcanoes.json")

    return jsonify({

        "count": len(volcanoes),

        "volcanoes": volcanoes

    })


# ----------------------------------
# Disaster Hotspots
# ----------------------------------

@disaster_bp.route("/hotspots", methods=["GET"])
def hotspots():

    hotspots = load_json("hotspot_data.json")

    return jsonify({

        "count": len(hotspots),

        "hotspots": hotspots

    })


# ----------------------------------
# Risk Scores
# ----------------------------------

@disaster_bp.route("/risk", methods=["GET"])
def risk_scores():

    scores = load_json("disaster_scores.json")

    return jsonify({

        "count": len(scores),

        "risk_scores": scores

    })


# ----------------------------------
# Nearby Disaster Search
# ----------------------------------

@disaster_bp.route("/nearby", methods=["GET"])
def nearby():

    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))

    hotspots = load_json("hotspot_data.json")

    nearby_events = []

    for event in hotspots:

        if (

            abs(event["latitude"] - latitude) < 2

            and

            abs(event["longitude"] - longitude) < 2

        ):

            nearby_events.append(event)

    return jsonify({

        "count": len(nearby_events),

        "events": nearby_events

    })


# ----------------------------------
# Dashboard Summary
# ----------------------------------

@disaster_bp.route("/dashboard", methods=["GET"])
def dashboard():

    return jsonify({

        "wildfires": len(load_json("wildfires.json")),

        "floods": len(load_json("floods.json")),

        "cyclones": len(load_json("cyclones.json")),

        "volcanoes": len(load_json("volcanoes.json")),

        "hotspots": len(load_json("hotspot_data.json"))

    })


# ----------------------------------
# Statistics
# ----------------------------------

@disaster_bp.route("/statistics", methods=["GET"])
def statistics():

    return jsonify({

        "active_events": 128,

        "critical_events": 17,

        "average_risk_score": 74,

        "countries_affected": 39

    })
