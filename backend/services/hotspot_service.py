"""
services/hotspot_service.py

Project Zenith
Hotspot Intelligence Service

Request → _parse_params → _run_inference (ModelManager + PreprocessingPipeline)
→ enriched JSON with heat_score, probability, severity, coordinates, confidence.
Routes contain zero ML logic.
"""

import json
import os
import math
import random
from datetime import datetime
from flask import request, jsonify
from ml.model_manager import model_manager
from ml.hotspot.features import HotspotFeatures
from ml.preprocessing.pipeline import PreprocessingPipeline
from database.prediction_logger import log_prediction
from database.redis_cache import cache_manager

DATA_PATH = "data/processed"


# ---------------------------------------------------------------------------
# Classification tables
# ---------------------------------------------------------------------------

# Severity bands keyed on hotspot probability (0–1)
_SEVERITY_BANDS = [
    (0.85, "Extreme"),
    (0.65, "High"),
    (0.40, "Moderate"),
    (0.00, "Low"),
]


def _classify_severity(probability: float) -> str:
    for threshold, label in _SEVERITY_BANDS:
        if probability >= threshold:
            return label
    return "Low"


def _heat_score(temperature: float, thermal_anomaly: float,
                vegetation_index: float, soil_moisture: float) -> float:
    """
    Composite heat score (0–100) derived from the four most thermally
    relevant input features.  Higher temperature, higher thermal anomaly,
    lower vegetation index, and lower soil moisture all raise the score.
    """
    # Normalise each driver to [0, 1] against realistic field ranges
    temp_norm    = min(max((temperature - 0)   / 60.0,  0), 1)   # 0–60 °C
    anomaly_norm = min(max(thermal_anomaly      / 100.0, 0), 1)   # 0–100
    veg_inv      = min(max(1.0 - vegetation_index,       0), 1)   # inverted NDVI (0–1)
    moist_inv    = min(max(1.0 - soil_moisture  / 100.0, 0), 1)   # inverted (%)

    # Weighted composite
    raw = (0.35 * temp_norm + 0.35 * anomaly_norm
           + 0.15 * veg_inv + 0.15 * moist_inv)
    return round(raw * 100, 2)


class HotspotService:

    def __init__(self):
        self.hotspots = []
        self.last_updated = None
        self.features = HotspotFeatures()
        self.load_hotspots()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scaler_path = os.path.join(base_dir, "ml", "models", "hotspot_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    # ----------------------------------------------------
    # Load Dataset
    # ----------------------------------------------------

    def load_hotspots(self):
        filepath = os.path.join(
            DATA_PATH,
            "hotspot_data.json"
        )
        if not os.path.exists(filepath):
            self.hotspots = []
            return
        with open(filepath, "r") as file:
            self.hotspots = json.load(file)
            for hs in self.hotspots:
                if "risk_score" not in hs:
                    hs["risk_score"] = _heat_score(
                        hs.get("temperature", 35.0),
                        hs.get("thermal_anomaly", 50.0),
                        hs.get("vegetation_index", 0.5),
                        hs.get("soil_moisture", 25.0)
                    )
        self.last_updated = datetime.utcnow()

    # ----------------------------------------------------
    # Refresh Dataset
    # ----------------------------------------------------

    def refresh(self):
        self.load_hotspots()

    # ----------------------------------------------------
    # Get All Hotspots
    # ----------------------------------------------------

    def get_all(self):
        return self.hotspots

    # ----------------------------------------------------
    # Total Count
    # ----------------------------------------------------

    def count(self):
        return len(self.hotspots)

    # ----------------------------------------------------
    # Haversine Distance
    # ----------------------------------------------------

    def haversine(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):
        R = 6371
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = (
            math.sin(dLat / 2) ** 2
            +
            math.cos(math.radians(lat1))
            *
            math.cos(math.radians(lat2))
            *
            math.sin(dLon / 2) ** 2
        )
        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
        return R * c

    def nearby(self, latitude, longitude, radius=100):
        results = []
        for hotspot in self.hotspots:
            distance = self.haversine(
                latitude,
                longitude,
                hotspot["latitude"],
                hotspot["longitude"]
            )
            if distance <= radius:
                h_copy = dict(hotspot)
                h_copy["distance_km"] = round(distance, 2)
                results.append(h_copy)
        return results

    def heatmap(self):
        heatmap = []
        for hotspot in self.hotspots:
            heatmap.append({
                "latitude": hotspot["latitude"],
                "longitude": hotspot["longitude"],
                "weight": hotspot["risk_score"]
            })
        return heatmap


    # ----------------------------------------------------
    # Private: parse & validate request parameters
    # ----------------------------------------------------

    def _parse_params(self):
        """
        Parses and validates the numeric query parameters shared by
        all hotspot prediction endpoints.
        Also reads optional lat/lon coordinates (default to None).
        Returns (params_dict, error_response). One of them is None.
        """
        try:
            params = {
                "temperature":          float(request.args.get("temperature",          41.0)),
                "humidity":             float(request.args.get("humidity",             28.0)),
                "wind_speed":           float(request.args.get("wind_speed",           13.0)),
                "rainfall":             float(request.args.get("rainfall",             2.0)),
                "vegetation_index":     float(request.args.get("vegetation_index",     0.31)),
                "thermal_anomaly":      float(request.args.get("thermal_anomaly",      89.0)),
                "population_density":   float(request.args.get("population_density",   740.0)),
                "elevation":            float(request.args.get("elevation",            82.0)),
                "soil_moisture":        float(request.args.get("soil_moisture",        11.0)),
                "historical_frequency": float(request.args.get("historical_frequency", 7.0)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        # Optional geographic coordinates
        lat_raw = request.args.get("latitude")
        lon_raw = request.args.get("longitude")
        try:
            params["latitude"]  = float(lat_raw)  if lat_raw  else None
            params["longitude"] = float(lon_raw)  if lon_raw  else None
        except (ValueError, TypeError):
            params["latitude"]  = None
            params["longitude"] = None

        return params, None

    # ----------------------------------------------------
    # Private: build sample, preprocess, run model
    # ----------------------------------------------------

    def _run_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the preprocessing pipeline,
        and runs the hotspot model from ModelManager.
        Returns (probability, prediction, error_response).
        """
        feature_params = {k: v for k, v in params.items()
                          if k not in ("latitude", "longitude")}

        # 1. Build raw feature DataFrame
        sample = self.features.build(**feature_params)

        # 2. Preprocess via shared pipeline (clean → engineer → scale)
        sample = self.pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model       = model_manager.get_hotspot_model()
            probability = float(model.predict_proba(sample)[0][1])
            prediction  = int(model.predict(sample)[0])
        except Exception as exc:
            return None, None, (jsonify({"error": f"Model inference failed: {exc}"}), 500)

        return probability, prediction, None

    # ----------------------------------------------------
    # ML Hotspot Prediction  (GET /predict)
    # ----------------------------------------------------

    def predict_hotspot(self):
        """
        Primary hotspot prediction endpoint.

        Returns:
            heat_score   – composite thermal index (0–100)
            probability  – model hotspot probability % (0–100)
            severity     – Low / Moderate / High / Extreme
            coordinates  – {latitude, longitude} if supplied, else null
            confidence   – same as probability (model's p-class max %)
        """
        params, err = self._parse_params()
        if err:
            return err

        cached_result = cache_manager.get_cached("hotspot", params)
        if cached_result:
            return jsonify(cached_result)

        probability, prediction, err = self._run_inference(params)
        if err:
            return err

        probability_pct = round(probability * 100, 2)
        severity        = _classify_severity(probability)
        heat_score      = _heat_score(
            params["temperature"],
            params["thermal_anomaly"],
            params["vegetation_index"],
            params["soil_moisture"],
        )
        coordinates = (
            {"latitude": params["latitude"], "longitude": params["longitude"]}
            if params["latitude"] is not None and params["longitude"] is not None
            else None
        )

        log_prediction(
            model="hotspot",
            prediction=severity,
            confidence=probability_pct,
            input_features=params,
            request=request,
        )

        response_data = {
            "heat_score":   heat_score,
            "probability":  probability_pct,
            "severity":     severity,
            "coordinates":  coordinates,
            "confidence":   probability_pct,
            # legacy fields kept for backwards compatibility
            "hotspot_probability": probability_pct,
            "prediction":          prediction,
        }
        cache_manager.set_cached("hotspot", params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # ----------------------------------------------------
    # ML Hotspot Analysis  (GET /analysis)
    # ----------------------------------------------------

    def predict_hotspot_analysis(self):
        """
        Extended hotspot analysis with full input echo.

        Returns all fields from predict_hotspot plus the raw input
        parameters so clients can audit what was fed to the model.
        """
        params, err = self._parse_params()
        if err:
            return err

        cache_params = {**params, "analysis": True}
        cached_result = cache_manager.get_cached("hotspot", cache_params)
        if cached_result:
            return jsonify(cached_result)

        probability, prediction, err = self._run_inference(params)
        if err:
            return err

        probability_pct = round(probability * 100, 2)
        severity        = _classify_severity(probability)
        heat_score      = _heat_score(
            params["temperature"],
            params["thermal_anomaly"],
            params["vegetation_index"],
            params["soil_moisture"],
        )
        coordinates = (
            {"latitude": params["latitude"], "longitude": params["longitude"]}
            if params["latitude"] is not None and params["longitude"] is not None
            else None
        )

        log_prediction(
            model="hotspot",
            prediction=severity,
            confidence=probability_pct,
            input_features=params,
            request=request,
        )

        response_data = {
            # Core prediction fields
            "heat_score":   heat_score,
            "probability":  probability_pct,
            "severity":     severity,
            "coordinates":  coordinates,
            "confidence":   probability_pct,

            # Input echo for audit / debugging
            "inputs": {
                "temperature_c":          params["temperature"],
                "humidity_pct":           params["humidity"],
                "wind_speed_kmh":         params["wind_speed"],
                "rainfall_mm":            params["rainfall"],
                "vegetation_index":       params["vegetation_index"],
                "thermal_anomaly":        params["thermal_anomaly"],
                "population_density":     params["population_density"],
                "elevation_m":            params["elevation"],
                "soil_moisture_pct":      params["soil_moisture"],
                "historical_frequency":   params["historical_frequency"],
            },
        }
        cache_manager.set_cached("hotspot", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # ----------------------------------------------------
    # Service Endpoints wrapping Route Logic
    # ----------------------------------------------------

    def get_all_hotspots_json(self):
        return jsonify({
            "count": self.count(),
            "hotspots": self.hotspots
        })

    def get_nearby_hotspots_json(self):
        try:
            latitude = float(request.args.get("lat"))
            longitude = float(request.args.get("lon"))
            radius = float(request.args.get("radius", 100))
        except (ValueError, TypeError):
            return jsonify({"error": "Latitude and longitude are required numerical parameters."}), 400
        
        nearby_list = self.nearby(latitude, longitude, radius)
        return jsonify({
            "count": len(nearby_list),
            "hotspots": nearby_list
        })

    def get_severity_hotspots_json(self, level):
        results = self.severity(level)
        return jsonify({
            "severity": level,
            "count": len(results),
            "hotspots": results
        })

    def get_country_hotspots_json(self, country):
        results = self.country(country)
        return jsonify({
            "country": country,
            "count": len(results),
            "hotspots": results
        })

    def get_heatmap_json(self):
        return jsonify({
            "heatmap": self.heatmap()
        })

    def get_statistics_json(self):
        stats = self.statistics()
        return jsonify({
            "total_hotspots": stats["total"],
            "high": stats["high"],
            "medium": stats["medium"],
            "low": stats["low"]
        })

    def get_risk_zones_json(self):
        zones = []
        for hotspot in self.hotspots:
            zones.append({
                "latitude": hotspot["latitude"],
                "longitude": hotspot["longitude"],
                "risk": hotspot["risk_score"],
                "event": hotspot["event"]
            })
        return jsonify({
            "zones": zones
        })

    def get_dashboard_json(self):
        critical_count = len([h for h in self.hotspots if h["risk_score"] > 85])
        return jsonify({
            "total_hotspots": self.count(),
            "critical": critical_count,
            "average_risk": self.average_risk(),
            "status": "Monitoring"
        })

    def average_risk(self):
        if len(self.hotspots) == 0:
            return 0
        total = sum(hotspot["risk_score"] for hotspot in self.hotspots)
        return round(total / len(self.hotspots), 2)

    def severity(self, level):
        return [
            hotspot
            for hotspot in self.hotspots
            if hotspot["severity"].lower() == level.lower()
        ]

    def country(self, country):
        return [
            hotspot
            for hotspot in self.hotspots
            if hotspot["country"].lower() == country.lower()
        ]

    def statistics(self):
        high = len(self.severity("High"))
        medium = len(self.severity("Medium"))
        low = len(self.severity("Low"))
        return {
            "total": self.count(),
            "high": high,
            "medium": medium,
            "low": low,
            "average_risk": self.average_risk()
        }

    def highest_risk(self):
        if len(self.hotspots) == 0:
            return None
        return max(
            self.hotspots,
            key=lambda x: x["risk_score"]
        )

    def dashboard(self):
        return {
            "total_hotspots": self.count(),
            "average_risk": self.average_risk(),
            "highest_risk": self.highest_risk(),
            "updated": self.last_updated.isoformat() if self.last_updated else None
        }


# Singleton instance
hotspot_service = HotspotService()
