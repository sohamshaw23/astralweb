"""
proprietary_apis/congestion_api.py

Project Zenith
Orbital Congestion Intelligence API
"""

from flask import Blueprint
from services.orbit_service import orbit_service

congestion_bp = Blueprint(
    "congestion_api",
    __name__
)


# ---------------------------------------------------------
# Overall Congestion
# ---------------------------------------------------------

@congestion_bp.route("/", methods=["GET"])
def congestion():
    return orbit_service.predict_congestion()


# ---------------------------------------------------------
# Detailed Analysis
# ---------------------------------------------------------

@congestion_bp.route("/analysis", methods=["GET"])
def analysis():
    return orbit_service.predict_congestion_analysis()


# ---------------------------------------------------------
# LEO
# ---------------------------------------------------------

@congestion_bp.route("/leo", methods=["GET"])
def leo():
    return orbit_service.get_congestion_leo()


# ---------------------------------------------------------
# MEO
# ---------------------------------------------------------

@congestion_bp.route("/meo", methods=["GET"])
def meo():
    return orbit_service.get_congestion_meo()


# ---------------------------------------------------------
# GEO
# ---------------------------------------------------------

@congestion_bp.route("/geo", methods=["GET"])
def geo():
    return orbit_service.get_congestion_geo()


# ---------------------------------------------------------
# HEO
# ---------------------------------------------------------

@congestion_bp.route("/heo", methods=["GET"])
def heo():
    return orbit_service.get_congestion_heo()


# ---------------------------------------------------------
# Heatmap
# ---------------------------------------------------------

@congestion_bp.route("/heatmap", methods=["GET"])
def heatmap():
    return orbit_service.get_congestion_heatmap()


# ---------------------------------------------------------
# High Density Regions
# ---------------------------------------------------------

@congestion_bp.route("/critical", methods=["GET"])
def critical():
    return orbit_service.get_congestion_critical()


# ---------------------------------------------------------
# Debris Density
# ---------------------------------------------------------

@congestion_bp.route("/debris", methods=["GET"])
def debris():
    return orbit_service.get_congestion_debris()


# ---------------------------------------------------------
# Statistics
# ---------------------------------------------------------

@congestion_bp.route("/statistics", methods=["GET"])
def statistics():
    return orbit_service.get_congestion_statistics()


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@congestion_bp.route("/dashboard", methods=["GET"])
def dashboard():
    return orbit_service.get_congestion_dashboard()