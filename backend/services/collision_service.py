"""
services/collision_service.py

Project Zenith
Collision Prediction Service

Collects request data → validates → preprocesses via PreprocessingPipeline
→ runs model from ModelManager → returns enriched JSON.
Routes contain zero ML logic.
"""

import os
import random
from datetime import datetime

from flask import request, jsonify

from ml.model_manager import model_manager
from ml.collision.features import CollisionFeatures
from ml.preprocessing.pipeline import PreprocessingPipeline
from database.prediction_logger import log_prediction
from database.redis_cache import cache_manager


# ---------------------------------------------------------------------------
# Risk thresholds
# ---------------------------------------------------------------------------

_RISK_THRESHOLDS = [
    (0.85, "Critical"),
    (0.65, "High"),
    (0.35, "Moderate"),
    (0.00, "Low"),
]

_RECOMMENDATIONS = {
    "Critical": "Immediate evasive manoeuvre required. Alert ground control now.",
    "High":     "Schedule avoidance burn within the next 6 hours.",
    "Moderate": "Monitor closely. Prepare contingency manoeuvre plan.",
    "Low":      "No immediate action required. Continue routine monitoring.",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _classify_risk(probability: float) -> str:
    for threshold, label in _RISK_THRESHOLDS:
        if probability >= threshold:
            return label
    return "Low"


class CollisionService:

    def __init__(self):
        self.features = CollisionFeatures()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scaler_path = os.path.join(base_dir, "ml", "collision", "scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    # ------------------------------------------------------------------
    # Private: parse & validate request parameters
    # ------------------------------------------------------------------

    def _parse_params(self):
        """
        Parses and validates numeric query parameters shared across
        all collision prediction endpoints.
        Returns (params_dict, error_response).  One of them is None.
        """
        try:
            params = {
                "relative_velocity":  float(request.args.get("relative_velocity",  7.4)),
                "closest_distance":   float(request.args.get("closest_distance",   3.1)),
                "orbital_altitude":   float(request.args.get("orbital_altitude",   550.0)),
                "inclination":        float(request.args.get("inclination",         98.2)),
                "eccentricity":       float(request.args.get("eccentricity",        0.001)),
                "orbital_congestion": float(request.args.get("orbital_congestion",  82.0)),
                "debris_density":     float(request.args.get("debris_density",      65.0)),
                "solar_kp_index":     float(request.args.get("solar_kp_index",      4.0)),
                "satellite_age":      float(request.args.get("satellite_age",       5.0)),
                "cross_section":      float(request.args.get("cross_section",       6.2)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        return params, None

    # ------------------------------------------------------------------
    # Private: build sample, preprocess, run model
    # ------------------------------------------------------------------

    def _run_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the preprocessing pipeline,
        and runs the collision model from ModelManager.
        Returns (probability, prediction, error_response).
        """
        # 1. Build raw feature DataFrame
        sample = self.features.build(**params)

        # 2. Preprocess via shared pipeline (cleaning → engineering → scaling)
        sample = self.pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model = model_manager.get_collision_model()
            probability = float(model.predict_proba(sample)[0][1])
            prediction  = int(model.predict(sample)[0])
        except Exception as exc:
            return None, None, (jsonify({"error": f"Model inference failed: {exc}"}), 500)

        return probability, prediction, None

    # ------------------------------------------------------------------
    # Public: predict_collision  (GET /)
    # ------------------------------------------------------------------

    def predict_collision(self):
        """
        Primary collision risk endpoint.

        Returns:
            satellite            – name from query string (default ISS)
            collision_probability – percentage (0 – 100)
            risk_level           – Low / Moderate / High / Critical
            confidence           – same as collision_probability (model's p-max %)
            recommendation       – human-readable action string
            prediction           – raw binary label (0 / 1)
        """
        params, err = self._parse_params()
        if err:
            return err

        satellite_name = request.args.get("name", "ISS")
        cache_params = {**params, "satellite": satellite_name}
        cached_result = cache_manager.get_cached("collision", cache_params)
        if cached_result:
            return jsonify(cached_result)

        probability, prediction, err = self._run_inference(params)
        if err:
            return err

        risk         = _classify_risk(probability)
        confidence   = round(probability * 100, 2)
        recommendation = _RECOMMENDATIONS[risk]

        log_prediction(
            model="collision",
            prediction=risk,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            "satellite":             satellite_name,
            "collision_probability": confidence,
            "risk_level":            risk,
            "confidence":            confidence,
            "recommendation":        recommendation,
            "prediction":            prediction,
        }
        cache_manager.set_cached("collision", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # ------------------------------------------------------------------
    # Public: predict_collision_analysis  (GET /analysis)
    # ------------------------------------------------------------------

    def predict_collision_analysis(self):
        """
        Extended collision analysis with full input echo.

        Returns all fields from predict_collision plus the raw input parameters
        so clients can audit exactly what was fed to the model.
        """
        params, err = self._parse_params()
        if err:
            return err

        satellite_name = request.args.get("name", "ISS")
        cache_params = {**params, "satellite": satellite_name, "analysis": True}
        cached_result = cache_manager.get_cached("collision", cache_params)
        if cached_result:
            return jsonify(cached_result)

        probability, prediction, err = self._run_inference(params)
        if err:
            return err

        risk           = _classify_risk(probability)
        confidence     = round(probability * 100, 2)
        recommendation = _RECOMMENDATIONS[risk]

        log_prediction(
            model="collision",
            prediction=risk,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            # Core prediction fields
            "satellite":             satellite_name,
            "collision_probability": confidence,
            "risk_level":            risk,
            "confidence":            confidence,
            "recommendation":        recommendation,
            "prediction":            prediction,

            # Input echo for audit / debugging
            "inputs": {
                "relative_velocity_km_s": params["relative_velocity"],
                "closest_distance_km":    params["closest_distance"],
                "orbital_altitude_km":    params["orbital_altitude"],
                "inclination_deg":        params["inclination"],
                "eccentricity":           params["eccentricity"],
                "orbital_congestion":     params["orbital_congestion"],
                "debris_density":         params["debris_density"],
                "solar_kp_index":         params["solar_kp_index"],
                "satellite_age_yrs":      params["satellite_age"],
                "cross_section_m2":       params["cross_section"],
            },
        }
        cache_manager.set_cached("collision", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # ------------------------------------------------------------------
    # Public: close_approaches  (GET /close-approaches)
    # ------------------------------------------------------------------

    def close_approaches(self):
        approaches = [
            {
                "satellite":          f"SAT-{100 + i}",
                "closest_distance_km": round(random.uniform(1, 20), 2),
                "time":               datetime.utcnow().isoformat() + "Z",
            }
            for i in range(5)
        ]
        return jsonify({"count": len(approaches), "approaches": approaches})

    # ------------------------------------------------------------------
    # Public: alerts  (GET /alerts)
    # ------------------------------------------------------------------

    def alerts(self):
        alerts = [
            {"satellite": "STARLINK-4021", "risk": "High",     "distance_km": 3.8},
            {"satellite": "ONEWEB-198",    "risk": "Moderate",  "distance_km": 8.6},
        ]
        return jsonify({"alerts": alerts})

    # ------------------------------------------------------------------
    # Public: high_risk  (GET /high-risk)
    # ------------------------------------------------------------------

    def high_risk(self):
        objects = sorted(
            [
                {"satellite": f"SAT-{1000 + i}", "probability": round(random.uniform(0.5, 4.0), 2)}
                for i in range(10)
            ],
            key=lambda x: x["probability"],
            reverse=True,
        )
        return jsonify({"high_risk_satellites": objects})

    # ------------------------------------------------------------------
    # Public: statistics  (GET /statistics)
    # ------------------------------------------------------------------

    def statistics(self):
        return jsonify({
            "tracked_satellites":  18452,
            "predicted_collisions": 3,
            "high_risk_objects":   17,
            "safe_objects":        18435,
        })

    # ------------------------------------------------------------------
    # Public: prediction  (GET /prediction)
    # ------------------------------------------------------------------

    def prediction(self):
        return jsonify({
            "prediction_window":  "Next 24 Hours",
            "highest_risk":       "STARLINK-4021",
            "probability":        2.83,
            "recommended_action": "Monitor",
        })

    # ------------------------------------------------------------------
    # Public: dashboard  (GET /dashboard)
    # ------------------------------------------------------------------

    def dashboard(self):
        return jsonify({
            "collision_alerts": 3,
            "critical":         1,
            "high":             5,
            "moderate":         12,
            "low":              18434,
            "updated":          datetime.utcnow().isoformat() + "Z",
        })


# Export a default instance for easy access
collision_service = CollisionService()
