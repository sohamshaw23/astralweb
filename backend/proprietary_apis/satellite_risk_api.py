"""
proprietary_apis/satellite_risk_api.py

Project Zenith
Satellite Risk Intelligence API
"""

from flask import Blueprint
from services.satellite_service import satellite_service

satellite_risk_bp = Blueprint(
    "satellite_risk_api",
    __name__
)


# ------------------------------------------------------
# Satellite Risk
# ------------------------------------------------------

@satellite_risk_bp.route("/", methods=["GET"])
def satellite_risk():
    return satellite_service.predict_risk()


# ------------------------------------------------------
# Detailed Analysis
# ------------------------------------------------------

@satellite_risk_bp.route("/analysis", methods=["GET"])
def analysis():
    return satellite_service.predict_risk_analysis()


# ------------------------------------------------------
# Top High-Risk Satellites
# ------------------------------------------------------

@satellite_risk_bp.route("/top-risk", methods=["GET"])
def top_risk():
    return satellite_service.get_top_risk_json()


# ------------------------------------------------------
# Debris Risk
# ------------------------------------------------------

@satellite_risk_bp.route("/debris", methods=["GET"])
def debris():
    return satellite_service.get_debris_json()


# ------------------------------------------------------
# Collision Probability
# ------------------------------------------------------

@satellite_risk_bp.route("/collision", methods=["GET"])
def collision():
    return satellite_service.get_collision_json()


# ------------------------------------------------------
# Solar Weather Risk
# ------------------------------------------------------

@satellite_risk_bp.route("/solar", methods=["GET"])
def solar():
    return satellite_service.get_solar_json()


# ------------------------------------------------------
# Risk History
# ------------------------------------------------------

@satellite_risk_bp.route("/history", methods=["GET"])
def history():
    return satellite_service.get_history_json()


# ------------------------------------------------------
# Dashboard
# ------------------------------------------------------

@satellite_risk_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return satellite_service.get_dashboard_json()