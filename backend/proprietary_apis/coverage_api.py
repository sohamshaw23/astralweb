"""
proprietary_apis/coverage_api.py

Project Zenith
Satellite Coverage Intelligence API
"""

from flask import Blueprint
from services.analytics_service import analytics_service

coverage_bp = Blueprint(
    "coverage_api",
    __name__
)


# ---------------------------------------------------------
# Overall Coverage
# ---------------------------------------------------------

@coverage_bp.route("/", methods=["GET"])
def coverage():
    return analytics_service.predict_coverage()


# ---------------------------------------------------------
# Detailed Analysis
# ---------------------------------------------------------

@coverage_bp.route("/analysis", methods=["GET"])
def analysis():
    return analytics_service.predict_coverage_analysis()


# ---------------------------------------------------------
# Communication Coverage
# ---------------------------------------------------------

@coverage_bp.route("/communication", methods=["GET"])
def communication():
    return analytics_service.get_communication()


# ---------------------------------------------------------
# Navigation Coverage
# ---------------------------------------------------------

@coverage_bp.route("/navigation", methods=["GET"])
def navigation():
    return analytics_service.get_navigation()


# ---------------------------------------------------------
# Weather Coverage
# ---------------------------------------------------------

@coverage_bp.route("/weather", methods=["GET"])
def weather():
    return analytics_service.get_weather()


# ---------------------------------------------------------
# Earth Observation
# ---------------------------------------------------------

@coverage_bp.route("/earth-observation", methods=["GET"])
def earth_observation():
    return analytics_service.get_earth_observation()


# ---------------------------------------------------------
# Defence Assets
# ---------------------------------------------------------

@coverage_bp.route("/defence", methods=["GET"])
def defence():
    return analytics_service.get_defence()


# ---------------------------------------------------------
# Best Satellite
# ---------------------------------------------------------

@coverage_bp.route("/best", methods=["GET"])
def best():
    return analytics_service.get_best()


# ---------------------------------------------------------
# Coverage Heatmap
# ---------------------------------------------------------

@coverage_bp.route("/heatmap", methods=["GET"])
def heatmap():
    return analytics_service.get_heatmap()


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@coverage_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return analytics_service.get_coverage_dashboard_json()
