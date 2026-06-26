"""
app.py

Project Zenith
Space Situational Awareness &
Disaster Intelligence Platform
"""

import logging
import os
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# -------------------------------
# Route Imports
# -------------------------------

from routes.health_routes import health_routes
from routes.celestial_routes import celestial_routes
from routes.satellite_routes import satellite_routes
from routes.disaster_routes import disaster_routes
from routes.proprietary_routes import proprietary_routes
from routes.ai_routes import ai_routes
from api.iss import iss_bp
from api.isro import isro_bp


# -------------------------------
# Create App
# -------------------------------

def create_app():

    # ---------------------------------------------------------------
    # Logging
    # ---------------------------------------------------------------
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    # -------------------------------
    # Database Initialization (Defensive)
    # -------------------------------
    try:
        from database.postgres import init_database
        init_database()
    except Exception as exc:
        app.logger.warning(f"Database initialization skipped/failed: {exc}")

    # ---------------------------------------------------------------
    # Background Scheduler
    # Guarded against Flask debug-mode double-start (Werkzeug reloader
    # spawns a child process that also calls create_app; we only want
    # the scheduler in the actual worker, not the stat-monitoring parent).
    # ---------------------------------------------------------------
    _in_reloader_parent = (
        os.environ.get("WERKZEUG_RUN_MAIN") != "true"
        and app.debug
    )
    if not _in_reloader_parent:
        try:
            from scheduler.main import start_scheduler, stop_scheduler
            start_scheduler()

            import atexit
            atexit.register(stop_scheduler)

        except Exception as exc:
            app.logger.warning(
                f"Background scheduler could not start: {exc}"
            )

    # -------------------------------
    # Register Blueprints
    # -------------------------------

    app.register_blueprint(
        health_routes,
        url_prefix="/api/health"
    )

    app.register_blueprint(
        celestial_routes,
        url_prefix="/api/celestial"
    )

    app.register_blueprint(
        satellite_routes,
        url_prefix="/api/satellites"
    )

    app.register_blueprint(
        disaster_routes,
        url_prefix="/api/disasters"
    )

    app.register_blueprint(
        proprietary_routes,
        url_prefix="/api/analytics"
    )

    app.register_blueprint(
        ai_routes,
        url_prefix="/api/ai"
    )

    app.register_blueprint(
        iss_bp,
        url_prefix="/api/iss"
    )

    app.register_blueprint(
        isro_bp,
        url_prefix="/api/isro"
    )

    # -------------------------------
    # Home
    # -------------------------------

    @app.route("/")
    def home():

        return jsonify({

            "project": "Project Zenith",

            "description":
            "Space Situational Awareness & Disaster Intelligence Platform",

            "version": "1.0.0",

            "status": "Running",

            "organization": "Team Zenith"

        })

    # -------------------------------
    # API Version
    # -------------------------------

    @app.route("/api")
    def api():

        return jsonify({

            "version": "v1",

            "documentation": "/docs",

            "status": "Available"

        })

    # -------------------------------
    # 404 Handler
    # -------------------------------

    @app.errorhandler(404)
    def not_found(error):

        return jsonify({

            "error": "Endpoint not found"

        }), 404

    # -------------------------------
    # 500 Handler
    # -------------------------------

    @app.errorhandler(500)
    def internal(error):

        return jsonify({

            "error": "Internal Server Error"

        }), 500

    return app


# -------------------------------
# Main
# -------------------------------

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )