"""
routes/disaster_routes.py

Project Zenith
Disaster Intelligence Routes
"""

from flask import Blueprint

# Import Disaster Blueprint
from api.disasters import disaster_bp

disaster_routes = Blueprint(
    "disaster_routes",
    __name__
)


# -------------------------------------------------------
# Register Disaster Blueprint
# -------------------------------------------------------

disaster_routes.register_blueprint(
    disaster_bp,
    url_prefix="/"
)
