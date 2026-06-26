"""
proprietary_apis/disaster_score_api.py

Project Zenith
Disaster Risk Intelligence API
"""

from flask import Blueprint
from services.disaster_service import disaster_service

disaster_score_bp = Blueprint(
    "disaster_score_api",
    __name__
)


# ----------------------------------------------------
# Risk Score
# ----------------------------------------------------

@disaster_score_bp.route("/", methods=["GET"])
def disaster_score():
    return disaster_service.predict_disaster()


# ----------------------------------------------------
# Detailed Analysis
# ----------------------------------------------------

@disaster_score_bp.route("/analysis", methods=["GET"])
def analysis():
    return disaster_service.predict_disaster_analysis()


# ----------------------------------------------------
# Top High Risk Areas
# ----------------------------------------------------

@disaster_score_bp.route("/top-risk", methods=["GET"])
def top_risk():
    return disaster_service.get_top_risk_json()


# ----------------------------------------------------
# Heatmap Data
# ----------------------------------------------------

@disaster_score_bp.route("/heatmap", methods=["GET"])
def heatmap():
    return disaster_service.get_heatmap_json()


# ----------------------------------------------------
# Statistics
# ----------------------------------------------------

@disaster_score_bp.route("/statistics", methods=["GET"])
def statistics():
    return disaster_service.get_statistics_json()


# ----------------------------------------------------
# Trend
# ----------------------------------------------------

@disaster_score_bp.route("/trend", methods=["GET"])
def trend():
    return disaster_service.get_trend_json()


# ----------------------------------------------------
# Alerts
# ----------------------------------------------------

@disaster_score_bp.route("/alerts", methods=["GET"])
def alerts():
    return disaster_service.get_alerts_json()


# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

@disaster_score_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return disaster_service.get_dashboard_json()
