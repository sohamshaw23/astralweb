"""
proprietary_apis/hotspot_api.py

Project Zenith
Disaster Hotspot Intelligence API
"""

from flask import Blueprint
from services.hotspot_service import hotspot_service

hotspot_bp = Blueprint("hotspot_api", __name__)


# -------------------------------------
# All Hotspots
# -------------------------------------

@hotspot_bp.route("/", methods=["GET"])
def hotspots():
    return hotspot_service.get_all_hotspots_json()


# -------------------------------------
# Nearby Hotspots
# -------------------------------------

@hotspot_bp.route("/nearby", methods=["GET"])
def nearby_hotspots():
    return hotspot_service.get_nearby_hotspots_json()


# -------------------------------------
# Severity Filter
# -------------------------------------

@hotspot_bp.route("/severity/<level>", methods=["GET"])
def severity(level):
    return hotspot_service.get_severity_hotspots_json(level)


# -------------------------------------
# Heatmap
# -------------------------------------

@hotspot_bp.route("/heatmap", methods=["GET"])
def heatmap():
    return hotspot_service.get_heatmap_json()


# -------------------------------------
# Statistics
# -------------------------------------

@hotspot_bp.route("/statistics", methods=["GET"])
def statistics():
    return hotspot_service.get_statistics_json()


# -------------------------------------
# Country Filter
# -------------------------------------

@hotspot_bp.route("/country/<country>", methods=["GET"])
def country(country):
    return hotspot_service.get_country_hotspots_json(country)


# -------------------------------------
# Risk Zones
# -------------------------------------

@hotspot_bp.route("/risk-zones", methods=["GET"])
def risk_zones():
    return hotspot_service.get_risk_zones_json()


# -------------------------------------
# Dashboard
# -------------------------------------

@hotspot_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return hotspot_service.get_dashboard_json()


# -------------------------------------
# Hotspot Prediction
# -------------------------------------

@hotspot_bp.route("/predict", methods=["GET"])
def predict():
    return hotspot_service.predict_hotspot()


@hotspot_bp.route("/analysis", methods=["GET"])
def analysis():
    return hotspot_service.predict_hotspot_analysis()
