"""
services/disaster_service.py

Project Zenith
Disaster Intelligence Service

Request → _parse_params → _run_inference (ModelManager + PreprocessingPipeline)
→ enriched JSON with predicted_disaster, confidence, severity, recommended_response.
Routes contain zero ML logic.
"""

import json
import os
import requests
import random
from flask import request, jsonify
from datetime import datetime
from ml.model_manager import model_manager
from ml.disaster.features import DisasterFeatures
from ml.preprocessing.pipeline import PreprocessingPipeline
from database.prediction_logger import log_prediction
from database.redis_cache import cache_manager

NASA_EONET = "https://eonet.gsfc.nasa.gov/api/v3/events"

DATA_PATH = "data/processed"


# ---------------------------------------------------------------------------
# Disaster classification tables
# ---------------------------------------------------------------------------

# Raw model labels (matches training dataset encoding)
_DISASTER_LABELS = {0: "Flood", 1: "Wildfire", 2: "Cyclone", 3: "Landslide"}

# Severity bands keyed on model confidence (0–1)
_SEVERITY_BANDS = [
    (0.85, "Extreme"),
    (0.70, "High"),
    (0.50, "Moderate"),
    (0.00, "Low"),
]

# Per-disaster recommended response playbooks
_RECOMMENDED_RESPONSES = {
    "Flood": (
        "Activate flood barriers and drainage pumps. "
        "Issue evacuation orders for low-lying areas. "
        "Pre-position rescue boats and emergency shelters."
    ),
    "Wildfire": (
        "Deploy aerial firefighting assets immediately. "
        "Establish firebreaks and evacuate at-risk communities. "
        "Issue air-quality advisories and activate relief camps."
    ),
    "Cyclone": (
        "Issue cyclone warning to coastal regions. "
        "Evacuate vulnerable populations to designated shelters. "
        "Secure critical infrastructure and pre-position disaster response teams."
    ),
    "Landslide": (
        "Close at-risk roads and hillside zones immediately. "
        "Deploy geotechnical teams to assess slope stability. "
        "Evacuate settlements in the landslide corridor."
    ),
}


def _classify_severity(confidence: float) -> str:
    for threshold, label in _SEVERITY_BANDS:
        if confidence >= threshold:
            return label
    return "Low"


class DisasterService:

    def __init__(self):

        self.events = []

        self.hotspots = []

        self.last_updated = None

        self.features = DisasterFeatures()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scaler_path = os.path.join(base_dir, "ml", "models", "disaster_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

        self.load_processed_data()


    # --------------------------------------------------
    # Load Local Datasets
    # --------------------------------------------------

    def load_processed_data(self):

        files = [

            "hotspot_data.json",

            "wildfires.json",

            "floods.json",

            "cyclones.json",

            "volcanoes.json"

        ]

        self.hotspots = []

        for file in files:

            path = os.path.join(

                DATA_PATH,

                file

            )

            if os.path.exists(path):

                with open(path) as f:

                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = [data]
                        for item in data:
                            if not isinstance(item, dict):
                                continue
                            if "risk_score" not in item:
                                # Map alertlevel or severity to a numeric risk_score
                                alert = str(item.get("alertlevel", item.get("severity", ""))).lower()
                                sev = item.get("severity", 0.0)
                                if isinstance(sev, str):
                                    sev = 50.0 # Default if severity is a string
                                
                                # Default mapping of alertlevels
                                if any(x in alert for x in ("red", "extreme", "critical", "high")):
                                    base = 80.0
                                elif any(x in alert for x in ("orange", "moderate", "medium")):
                                    base = 50.0
                                elif any(x in alert for x in ("yellow", "low")):
                                    base = 30.0
                                else:
                                    base = 20.0
                                
                                item["risk_score"] = float(min(100.0, max(0.0, base + (float(sev) % 20.0) if isinstance(sev, (int, float)) else base)))
                        self.hotspots.extend(data)
                    except Exception as e:
                        print(f"Warning: Failed to load {file} in disaster_service: {e}")

        self.last_updated = datetime.utcnow()

    # --------------------------------------------------
    # NASA EONET
    # --------------------------------------------------

    def live_events(self):

        try:

            response = requests.get(

                NASA_EONET,

                timeout=20

            )

            data = response.json()

            self.events = data["events"]

            return self.events

        except:

            return []

    # --------------------------------------------------
    # Total Events
    # --------------------------------------------------

    def count(self):

        return len(self.hotspots)

    # --------------------------------------------------
    # Get All
    # --------------------------------------------------

    def all(self):

        return self.hotspots

    # --------------------------------------------------
    # Wildfires
    # --------------------------------------------------

    def wildfires(self):

        return [

            x

            for x in self.hotspots

            if x["event"].lower()

            == "wildfire"

        ]

    # --------------------------------------------------
    # Floods
    # --------------------------------------------------

    def floods(self):

        return [

            x

            for x in self.hotspots

            if x["event"].lower()

            == "flood"

        ]

    # --------------------------------------------------
    # Cyclones
    # --------------------------------------------------

    def cyclones(self):

        return [

            x

            for x in self.hotspots

            if x["event"].lower()

            == "cyclone"

        ]

    # --------------------------------------------------
    # Volcanoes
    # --------------------------------------------------

    def volcanoes(self):

        return [

            x

            for x in self.hotspots

            if x["event"].lower()

            == "volcano"

        ]

    # --------------------------------------------------
    # Highest Risk
    # --------------------------------------------------

    def highest_risk(self):

        if len(self.hotspots) == 0:

            return None

        return max(

            self.hotspots,

            key=lambda x:

            x["risk_score"]

        )

    # --------------------------------------------------
    # Average Risk
    # --------------------------------------------------

    def average_risk(self):

        if len(self.hotspots) == 0:

            return 0

        return round(

            sum(

                x["risk_score"]

                for x in self.hotspots

            )

            /

            len(self.hotspots),

            2

        )

    # --------------------------------------------------
    # Country Filter
    # --------------------------------------------------

    def by_country(

        self,

        country

    ):

        return [

            x

            for x in self.hotspots

            if x["country"].lower()

            == country.lower()

        ]

    # --------------------------------------------------
    # Event Filter
    # --------------------------------------------------

    def by_event(

        self,

        event

    ):

        return [

            x

            for x in self.hotspots

            if x["event"].lower()

            == event.lower()

        ]

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self):

        return {

            "total_events":

                self.count(),

            "wildfires":

                len(

                    self.wildfires()

                ),

            "floods":

                len(

                    self.floods()

                ),

            "cyclones":

                len(

                    self.cyclones()

                ),

            "volcanoes":

                len(

                    self.volcanoes()

                ),

            "average_risk":

                self.average_risk()

        }

    # --------------------------------------------------
    # Dashboard
    # --------------------------------------------------

    def dashboard(self):

        return {

            "active_events":

                self.count(),

            "highest_risk":

                self.highest_risk(),

            "average_risk":

                self.average_risk(),

            "updated":

                self.last_updated.isoformat()

                if self.last_updated

                else None

        }

    # --------------------------------------------------
    # Disaster Summary
    # --------------------------------------------------

    def summary(self):

        return {

            "events":

                self.statistics(),

            "live_events":

                len(

                    self.live_events()

                ),

            "status":

                "Monitoring"

        }

    # --------------------------------------------------
    # Private: parse & validate request parameters
    # --------------------------------------------------

    def _parse_params(self):
        """
        Parses and validates the numeric query parameters shared by
        all disaster prediction endpoints.
        Returns (params_dict, error_response). One of them is None.
        """
        try:
            params = {
                "temperature":        float(request.args.get("temperature",        40.0)),
                "humidity":           float(request.args.get("humidity",           24.0)),
                "wind_speed":         float(request.args.get("wind_speed",         13.0)),
                "rainfall":           float(request.args.get("rainfall",           1.0)),
                "pressure":           float(request.args.get("pressure",           1005.0)),
                "soil_moisture":      float(request.args.get("soil_moisture",      9.0)),
                "vegetation_index":   float(request.args.get("vegetation_index",   0.31)),
                "thermal_anomaly":    float(request.args.get("thermal_anomaly",    91.0)),
                "population_density": float(request.args.get("population_density", 680.0)),
                "elevation":          float(request.args.get("elevation",          82.0)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        return params, None

    # --------------------------------------------------
    # Private: build sample, preprocess, run model
    # --------------------------------------------------

    def _run_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the preprocessing pipeline,
        and runs the disaster classification model from ModelManager.
        Returns (predicted_disaster, confidence_pct, error_response).
        """
        # 1. Build raw feature DataFrame
        sample = self.features.build(**params)

        # 2. Preprocess via shared pipeline (clean → engineer → scale)
        sample = self.pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model       = model_manager.get_disaster_model()
            prediction  = model.predict(sample)[0]
            confidence  = float(model.predict_proba(sample).max())
        except Exception as exc:
            return None, None, (jsonify({"error": f"Model inference failed: {exc}"}), 500)

        predicted_disaster = _DISASTER_LABELS.get(prediction, "Flood")
        confidence_pct     = round(confidence * 100, 2)

        return predicted_disaster, confidence_pct, None

    # --------------------------------------------------
    # ML Disaster Prediction  (GET /)
    # --------------------------------------------------

    def predict_disaster(self):
        """
        Primary disaster classification endpoint.

        Returns:
            predicted_disaster   – Flood / Wildfire / Cyclone / Landslide
            confidence           – model's class-probability % (0–100)
            severity             – Low / Moderate / High / Extreme
            recommended_response – disaster-specific operational response string
        """
        params, err = self._parse_params()
        if err:
            return err

        cache_params = {**params, "endpoint": "predict"}
        cached_result = cache_manager.get_cached("disaster", cache_params)
        if cached_result:
            return jsonify(cached_result)

        predicted_disaster, confidence, err = self._run_inference(params)
        if err:
            return err

        severity             = _classify_severity(confidence / 100)
        recommended_response = _RECOMMENDED_RESPONSES[predicted_disaster]

        log_prediction(
            model="disaster",
            prediction=predicted_disaster,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            "location":            request.args.get("location", "India"),
            "predicted_disaster":  predicted_disaster,
            "confidence":          confidence,
            "severity":            severity,
            "recommended_response": recommended_response,
        }
        cache_manager.set_cached("disaster", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # --------------------------------------------------
    # ML Disaster Analysis  (GET /analysis)
    # --------------------------------------------------

    def predict_disaster_analysis(self):
        """
        Extended disaster analysis with full input echo.

        Returns all fields from predict_disaster plus the raw input
        parameters so clients can audit what was fed to the model.
        """
        params, err = self._parse_params()
        if err:
            return err

        cache_params = {**params, "endpoint": "analysis"}
        cached_result = cache_manager.get_cached("disaster", cache_params)
        if cached_result:
            return jsonify(cached_result)

        predicted_disaster, confidence, err = self._run_inference(params)
        if err:
            return err

        severity             = _classify_severity(confidence / 100)
        recommended_response = _RECOMMENDED_RESPONSES[predicted_disaster]

        log_prediction(
            model="disaster",
            prediction=predicted_disaster,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            # Core prediction fields
            "location":             request.args.get("location", "India"),
            "predicted_disaster":   predicted_disaster,
            "confidence":           confidence,
            "severity":             severity,
            "recommended_response": recommended_response,

            # Input echo for audit / debugging
            "inputs": {
                "temperature_c":       params["temperature"],
                "humidity_pct":        params["humidity"],
                "wind_speed_kmh":      params["wind_speed"],
                "rainfall_mm":         params["rainfall"],
                "pressure_hpa":        params["pressure"],
                "soil_moisture_pct":   params["soil_moisture"],
                "vegetation_index":    params["vegetation_index"],
                "thermal_anomaly":     params["thermal_anomaly"],
                "population_density":  params["population_density"],
                "elevation_m":         params["elevation"],
            },
        }
        cache_manager.set_cached("disaster", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    def get_top_risk_json(self):
        locations = ["Odisha", "West Bengal", "Assam", "Kerala", "Tamil Nadu", "Andhra Pradesh", "Gujarat"]
        data = []
        for place in locations:
            data.append({
                "location": place,
                "risk_score": random.randint(50, 100)
            })
        data.sort(key=lambda x: x["risk_score"], reverse=True)
        return jsonify({
            "high_risk_locations": data
        })

    def get_heatmap_json(self):
        heatmap = []
        for _ in range(30):
            heatmap.append({
                "latitude": round(random.uniform(-90, 90), 4),
                "longitude": round(random.uniform(-180, 180), 4),
                "weight": random.randint(10, 100)
            })
        return jsonify({
            "heatmap": heatmap
        })

    def get_statistics_json(self):
        return jsonify({
            "active_events": 124,
            "critical_events": 18,
            "average_risk": 67,
            "high_risk_regions": 23,
            "safe_regions": 81
        })

    def get_trend_json(self):
        history = []
        for i in range(7):
            history.append({
                "day": f"Day {i+1}",
                "risk_score": random.randint(30, 95)
            })
        return jsonify({
            "trend": history
        })

    def get_alerts_json(self):
        return jsonify({
            "alerts": [
                {
                    "location": "Odisha",
                    "event": "Cyclone",
                    "risk": "Extreme"
                },
                {
                    "location": "California",
                    "event": "Wildfire",
                    "risk": "High"
                }
            ]
        })

    def get_dashboard_json(self):
        return jsonify({
            "active_disasters": 124,
            "high_risk_regions": 23,
            "average_risk": 67,
            "critical_alerts": 5,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        })


# Export default instance
disaster_service = DisasterService()