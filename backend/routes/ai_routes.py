"""
routes/ai_routes.py

Project Zenith
AI Mission Assistant Routes
"""

from flask import Blueprint, request, jsonify
from services.ai_service import AIService

ai_routes = Blueprint(
    "ai_routes",
    __name__
)

ai = AIService()


# ---------------------------------------------------
# Chat with AI
# ---------------------------------------------------

@ai_routes.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    prompt = data.get("prompt")

    response = ai.chat(prompt)

    return jsonify(response)


# ---------------------------------------------------
# Mission Insights
# ---------------------------------------------------

@ai_routes.route("/insights", methods=["GET"])
def insights():

    response = ai.generate_insights()

    return jsonify(response)


# ---------------------------------------------------
# Space Weather Analysis
# ---------------------------------------------------

@ai_routes.route("/space-weather", methods=["GET"])
def space_weather():

    response = ai.space_weather()

    return jsonify(response)


# ---------------------------------------------------
# Disaster Analysis
# ---------------------------------------------------

@ai_routes.route("/disaster-analysis", methods=["GET"])
def disaster_analysis():

    latitude = request.args.get("lat")

    longitude = request.args.get("lon")

    response = ai.disaster_analysis(

        latitude,

        longitude

    )

    return jsonify(response)


# ---------------------------------------------------
# Satellite Recommendation
# ---------------------------------------------------

@ai_routes.route("/recommendation", methods=["GET"])
def recommendation():

    latitude = request.args.get("lat")

    longitude = request.args.get("lon")

    response = ai.recommend_satellite(

        latitude,

        longitude

    )

    return jsonify(response)


# ---------------------------------------------------
# Visibility Explanation
# ---------------------------------------------------

@ai_routes.route("/visibility", methods=["GET"])
def visibility():

    latitude = request.args.get("lat")

    longitude = request.args.get("lon")

    response = ai.visibility_report(

        latitude,

        longitude

    )

    return jsonify(response)


# ---------------------------------------------------
# Mission Summary
# ---------------------------------------------------

@ai_routes.route("/summary", methods=["GET"])
def summary():

    response = ai.mission_summary()

    return jsonify(response)


# ---------------------------------------------------
# Health Check
# ---------------------------------------------------

@ai_routes.route("/health", methods=["GET"])
def health():

    return jsonify({

        "service": "AI Mission Assistant",

        "status": "Running"

    })
