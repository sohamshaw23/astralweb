"""
proprietary_apis/collision_api.py

Project Zenith
Satellite Collision Intelligence API
"""

from flask import Blueprint
from services.collision_service import collision_service

collision_bp = Blueprint(
    "collision_api",
    __name__
)


# ----------------------------------------------------
# Collision Risk
# ----------------------------------------------------

@collision_bp.route("/", methods=["GET"])
def collision():
    return collision_service.predict_collision()


# ----------------------------------------------------
# Detailed Analysis
# ----------------------------------------------------

@collision_bp.route("/analysis", methods=["GET"])
def analysis():
    return collision_service.predict_collision_analysis()


# ----------------------------------------------------
# Close Approaches
# ----------------------------------------------------

@collision_bp.route("/close-approaches", methods=["GET"])
def close_approaches():
    return collision_service.close_approaches()


# ----------------------------------------------------
# Collision Alerts
# ----------------------------------------------------

@collision_bp.route("/alerts", methods=["GET"])
def alerts():
    return collision_service.alerts()


# ----------------------------------------------------
# Top High-Risk Objects
# ----------------------------------------------------

@collision_bp.route("/high-risk", methods=["GET"])
def high_risk():
    return collision_service.high_risk()


# ----------------------------------------------------
# Collision Statistics
# ----------------------------------------------------

@collision_bp.route("/statistics", methods=["GET"])
def statistics():
    return collision_service.statistics()


# ----------------------------------------------------
# Future Prediction
# ----------------------------------------------------

@collision_bp.route("/prediction", methods=["GET"])
def prediction():
    return collision_service.prediction()


# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

@collision_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return collision_service.dashboard()

