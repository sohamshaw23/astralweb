"""
proprietary_apis/anomaly_api.py

Project Zenith
Orbital Anomaly Detection API
"""

from flask import Blueprint
from services.orbit_service import orbit_service

anomaly_bp = Blueprint(
    "anomaly_api",
    __name__
)


# -------------------------------------------------------
# Satellite Anomaly
# -------------------------------------------------------

@anomaly_bp.route("/", methods=["GET"])
def anomaly():
    return orbit_service.predict_anomaly()


# -------------------------------------------------------
# Detailed Analysis
# -------------------------------------------------------

@anomaly_bp.route("/analysis", methods=["GET"])
def analysis():
    return orbit_service.predict_anomaly_analysis()


# -------------------------------------------------------
# Active Anomalies
# -------------------------------------------------------

@anomaly_bp.route("/active", methods=["GET"])
def active():
    return orbit_service.get_anomaly_active()


# -------------------------------------------------------
# Trajectory Deviations
# -------------------------------------------------------

@anomaly_bp.route("/trajectory", methods=["GET"])
def trajectory():
    return orbit_service.get_anomaly_trajectory()


# -------------------------------------------------------
# High Risk Objects
# -------------------------------------------------------

@anomaly_bp.route("/high-risk", methods=["GET"])
def high_risk():
    return orbit_service.get_anomaly_high_risk()


# -------------------------------------------------------
# Statistics
# -------------------------------------------------------

@anomaly_bp.route("/statistics", methods=["GET"])
def statistics():
    return orbit_service.get_anomaly_statistics()


# -------------------------------------------------------
# Historical Trend
# -------------------------------------------------------

@anomaly_bp.route("/history", methods=["GET"])
def history():
    return orbit_service.get_anomaly_history()


# -------------------------------------------------------
# Dashboard
# -------------------------------------------------------

@anomaly_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return orbit_service.get_anomaly_dashboard()