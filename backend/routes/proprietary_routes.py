"""
routes/proprietary_routes.py

Project Zenith
Proprietary Analytics Routes
"""

from flask import Blueprint

# Import Proprietary APIs
from proprietary_apis.visibility_api import visibility_bp
from proprietary_apis.hotspot_api import hotspot_bp
from proprietary_apis.collision_api import collision_bp
from proprietary_apis.congestion_api import congestion_bp
from proprietary_apis.orbital_prediction_api import orbital_prediction_bp
from proprietary_apis.satellite_risk_api import satellite_risk_bp
from proprietary_apis.disaster_score_api import disaster_score_bp
from proprietary_apis.coverage_api import coverage_bp
from proprietary_apis.anomaly_api import anomaly_bp


proprietary_routes = Blueprint(
    "proprietary_routes",
    __name__
)

from services.analytics_service import analytics_service
from flask import jsonify

@proprietary_routes.route("/dashboard", methods=["GET"])
def get_main_dashboard():
    return jsonify(analytics_service.dashboard())


# ---------------------------------------------------
# Register Proprietary Blueprints
# ---------------------------------------------------

proprietary_routes.register_blueprint(
    visibility_bp,
    url_prefix="/visibility"
)

proprietary_routes.register_blueprint(
    hotspot_bp,
    url_prefix="/hotspots"
)

proprietary_routes.register_blueprint(
    collision_bp,
    url_prefix="/collision"
)

proprietary_routes.register_blueprint(
    congestion_bp,
    url_prefix="/congestion"
)

proprietary_routes.register_blueprint(
    orbital_prediction_bp,
    url_prefix="/orbital"
)

proprietary_routes.register_blueprint(
    satellite_risk_bp,
    url_prefix="/risk"
)

proprietary_routes.register_blueprint(
    disaster_score_bp,
    url_prefix="/disaster-score"
)

proprietary_routes.register_blueprint(
    coverage_bp,
    url_prefix="/coverage"
)

proprietary_routes.register_blueprint(
    anomaly_bp,
    url_prefix="/anomaly"
)
