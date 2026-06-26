"""
services/satellite_service.py

Project Zenith
Satellite Intelligence Service

Request → _parse_params → _run_inference (ModelManager + PreprocessingPipeline)
→ enriched JSON with risk_level, confidence, criticality, recommended_action.
Routes contain zero ML logic.
"""

import os
import requests
import random
from flask import request, jsonify
from skyfield.api import load, EarthSatellite, Topos
from datetime import datetime
from ml.model_manager import model_manager
from ml.satellite_risk.features import SatelliteRiskFeatures
from ml.preprocessing.pipeline import PreprocessingPipeline
from database.prediction_logger import log_prediction
from database.redis_cache import cache_manager


# ---------------------------------------------------------------------------
# Risk classification tables
# ---------------------------------------------------------------------------

_RISK_LABELS = {0: "Low", 1: "Moderate", 2: "High", 3: "Critical"}

_CRITICALITY = {
    "Low":      "Nominal — satellite operating within expected parameters.",
    "Moderate": "Elevated — one or more subsystems approaching degraded state.",
    "High":     "Serious — multiple threat factors converging; intervention likely needed.",
    "Critical": "Severe — immediate operational risk detected across key systems.",
}

_RECOMMENDED_ACTIONS = {
    "Low":      "Continue routine monitoring. No immediate action required.",
    "Moderate": "Increase telemetry polling frequency. Review fuel and battery margins.",
    "High":     "Schedule preventive manoeuvre. Alert ground operations team.",
    "Critical": "Initiate emergency protocol. Execute avoidance burn and notify mission control immediately.",
}

ts = load.timescale()

CELESTRAK_URL = (
    "https://celestrak.org/NORAD/elements/"
    "gp.php?GROUP=active&FORMAT=tle"
)


class SatelliteService:

    def __init__(self):

        self.satellites = []

        self.last_updated = None

        self.features = SatelliteRiskFeatures()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scaler_path = os.path.join(base_dir, "ml", "models", "satellite_risk_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    # ---------------------------------
    # Download TLE
    # ---------------------------------

    def refresh(self):

        text = None
        try:
            response = requests.get(
                CELESTRAK_URL,
                timeout=20
            )
            if response.status_code == 200:
                text = response.text
                try:
                    os.makedirs("data/processed", exist_ok=True)
                    with open("data/processed/active_tle.txt", "w") as f:
                        f.write(text)
                except Exception as e:
                    print(f"Warning: Failed to save TLE cache file: {e}")
            else:
                raise Exception(f"Non-200 status code: {response.status_code}")
        except Exception as e:
            print(f"Warning: Celestrak TLE download failed: {e}. Attempting local fallback.")
            local_cache_path = "data/processed/active_tle.txt"
            local_raw_path = "data/raw/celestrak/active_satellites.tle"
            if os.path.exists(local_cache_path):
                try:
                    with open(local_cache_path, "r") as f:
                        text = f.read()
                except Exception:
                    text = None
            if not text and os.path.exists(local_raw_path):
                try:
                    with open(local_raw_path, "r") as f:
                        text = f.read()
                except Exception:
                    text = None
            if not text:
                raise Exception("Unable to download TLE and no local fallback available.")

        lines = text.splitlines()

        satellites = []

        for i in range(0, len(lines), 3):

            if i + 2 >= len(lines):

                break

            try:

                satellite = EarthSatellite(

                    lines[i + 1],

                    lines[i + 2],

                    lines[i],

                    ts

                )

                satellites.append(satellite)

            except:

                continue

        self.satellites = satellites

        self.last_updated = datetime.utcnow()

    # ---------------------------------
    # All Satellites
    # ---------------------------------

    def all(self):

        if len(self.satellites) == 0:

            self.refresh()

        return self.satellites

    # ---------------------------------
    # Count
    # ---------------------------------

    def count(self):

        return len(self.all())

    # ---------------------------------
    # Search
    # ---------------------------------

    def search(self, keyword):

        keyword = keyword.lower()

        result = []

        for satellite in self.all():

            if keyword in satellite.name.lower():

                result.append({

                    "name": satellite.name

                })

        return result

    # ---------------------------------
    # By Name
    # ---------------------------------

    def get(self, name):

        for satellite in self.all():

            if satellite.name.lower() == name.lower():

                return satellite

        return None

    # ---------------------------------
    # Position
    # ---------------------------------

    def position(self, name):

        satellite = self.get(name)

        if satellite is None:

            return None

        t = ts.now()

        geo = satellite.at(t)

        sub = geo.subpoint()

        return {

            "name": satellite.name,

            "latitude":

                round(

                    sub.latitude.degrees,

                    4

                ),

            "longitude":

                round(

                    sub.longitude.degrees,

                    4

                ),

            "altitude_km":

                round(

                    sub.elevation.km,

                    2

                )

        }

    # ---------------------------------
    # Nearby
    # ---------------------------------

    def nearby(

            self,

            latitude,

            longitude,

            radius=10

    ):

        observer = Topos(

            latitude_degrees=latitude,

            longitude_degrees=longitude

        )

        t = ts.now()

        visible = []

        for satellite in self.all():

            difference = satellite - observer

            topocentric = difference.at(t)

            alt, az, distance = topocentric.altaz()

            if alt.degrees > radius:

                visible.append({

                    "name":

                        satellite.name,

                    "altitude":

                        round(

                            alt.degrees,

                            2

                        ),

                    "azimuth":

                        round(

                            az.degrees,

                            2

                        ),

                    "distance":

                        round(

                            distance.km,

                            2

                        )

                })

        return visible

    # ---------------------------------
    # Orbit
    # ---------------------------------

    def orbit(self, name):

        satellite = self.get(name)

        if satellite is None:

            return None

        model = satellite.model

        return {

            "name": satellite.name,

            "inclination":

                model.inclo,

            "eccentricity":

                model.ecco,

            "mean_motion":

                model.no_kozai,

            "raan":

                model.nodeo,

            "argument_perigee":

                model.argpo

        }

    # ---------------------------------
    # Statistics
    # ---------------------------------

    def statistics(self):

        satellites = self.all()

        return {

            "total":

                len(satellites),

            "updated":

                self.last_updated.isoformat()

                if self.last_updated

                else None

        }

    # ---------------------------------
    # Dashboard
    # ---------------------------------

    def dashboard(self):

        return {

            "tracked_satellites":

                self.count(),

            "database":

                "CelesTrak",

            "updated":

                self.last_updated.isoformat()

                if self.last_updated

                else None

        }

    # -------------------------------------------------------------------
    # Private: parse & validate request parameters
    # -------------------------------------------------------------------

    def _parse_params(self):
        """
        Parses and validates the numeric query parameters shared by
        all satellite risk prediction endpoints.
        Returns (params_dict, error_response). One of them is None.
        """
        try:
            params = {
                "collision_probability": float(request.args.get("collision_probability", 0.81)),
                "orbital_altitude":      float(request.args.get("orbital_altitude",      550.0)),
                "orbital_velocity":      float(request.args.get("orbital_velocity",      7.66)),
                "orbital_congestion":    float(request.args.get("orbital_congestion",    88.0)),
                "debris_density":        float(request.args.get("debris_density",        73.0)),
                "solar_activity":        float(request.args.get("solar_activity",        4.0)),
                "satellite_age":         float(request.args.get("satellite_age",         6.0)),
                "fuel_remaining":        float(request.args.get("fuel_remaining",        58.0)),
                "communication_health":  float(request.args.get("communication_health",  91.0)),
                "battery_health":        float(request.args.get("battery_health",        93.0)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        return params, None

    # -------------------------------------------------------------------
    # Private: build sample, preprocess, run model
    # -------------------------------------------------------------------

    def _run_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the preprocessing pipeline,
        and runs the satellite risk model from ModelManager.
        Returns (risk_level, confidence_pct, error_response).
        """
        # 1. Build raw feature DataFrame
        sample = self.features.build(**params)

        # 2. Preprocess via shared pipeline (clean → engineer → scale)
        sample = self.pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model        = model_manager.get_satellite_risk_model()
            prediction   = int(model.predict(sample)[0])
            probabilities = model.predict_proba(sample)[0]
            confidence   = float(max(probabilities))
        except Exception as exc:
            return None, None, (jsonify({"error": f"Model inference failed: {exc}"}), 500)

        risk_level     = _RISK_LABELS.get(prediction, "Low")
        confidence_pct = round(confidence * 100, 2)

        return risk_level, confidence_pct, None

    # -------------------------------------------------------------------
    # ML Satellite Risk Prediction  (GET /)
    # -------------------------------------------------------------------

    def predict_risk(self):
        """
        Primary satellite risk endpoint.

        Returns:
            satellite          – name from query string (default ISS)
            risk_level         – Low / Moderate / High / Critical
            confidence         – model's class-probability % (0 – 100)
            criticality        – human-readable severity description
            recommended_action – operational action string
        """
        params, err = self._parse_params()
        if err:
            return err

        satellite_name = request.args.get("name", "ISS")
        cache_params = {**params, "satellite": satellite_name}
        cached_result = cache_manager.get_cached("satellite_risk", cache_params)
        if cached_result:
            return jsonify(cached_result)

        risk_level, confidence, err = self._run_inference(params)
        if err:
            return err

        log_prediction(
            model="satellite_risk",
            prediction=risk_level,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            "satellite":          satellite_name,
            "risk_level":         risk_level,
            "confidence":         confidence,
            "criticality":        _CRITICALITY[risk_level],
            "recommended_action": _RECOMMENDED_ACTIONS[risk_level],
        }
        cache_manager.set_cached("satellite_risk", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # -------------------------------------------------------------------
    # ML Satellite Risk Analysis  (GET /analysis)
    # -------------------------------------------------------------------

    def predict_risk_analysis(self):
        """
        Extended satellite risk analysis with full input echo.

        Returns all fields from predict_risk plus the raw input parameters
        so clients can audit exactly what was fed to the model.
        """
        params, err = self._parse_params()
        if err:
            return err

        satellite_name = request.args.get("name", "ISS")
        cache_params = {**params, "satellite": satellite_name, "analysis": True}
        cached_result = cache_manager.get_cached("satellite_risk", cache_params)
        if cached_result:
            return jsonify(cached_result)

        risk_level, confidence, err = self._run_inference(params)
        if err:
            return err

        log_prediction(
            model="satellite_risk",
            prediction=risk_level,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            # Core prediction fields
            "satellite":          satellite_name,
            "risk_level":         risk_level,
            "confidence":         confidence,
            "criticality":        _CRITICALITY[risk_level],
            "recommended_action": _RECOMMENDED_ACTIONS[risk_level],

            # Input echo for audit / debugging
            "inputs": {
                "collision_probability": params["collision_probability"],
                "orbital_altitude_km":   params["orbital_altitude"],
                "orbital_velocity_km_s": params["orbital_velocity"],
                "orbital_congestion":    params["orbital_congestion"],
                "debris_density":        params["debris_density"],
                "solar_activity":        params["solar_activity"],
                "satellite_age_yrs":     params["satellite_age"],
                "fuel_remaining_pct":    params["fuel_remaining"],
                "communication_health":  params["communication_health"],
                "battery_health":        params["battery_health"],
            },
        }
        cache_manager.set_cached("satellite_risk", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    def get_top_risk_json(self):
        satellites = []
        for i in range(10):
            score = random.randint(40, 100)
            satellites.append({
                "satellite": f"SAT-{1000+i}",
                "risk_score": score
            })
        satellites.sort(key=lambda x: x["risk_score"], reverse=True)
        return jsonify({
            "high_risk_satellites": satellites
        })

    def get_debris_json(self):
        return jsonify({
            "debris_density": "Moderate",
            "tracked_objects": 35781,
            "dangerous_objects": 247,
            "risk_level": "Medium"
        })

    def get_collision_json(self):
        return jsonify({
            "collision_probability": round(random.uniform(0.01, 4.5), 3),
            "nearest_object": "STARLINK-3054",
            "distance_km": 7.84
        })

    def get_solar_json(self):
        return jsonify({
            "kp_index": 3,
            "solar_flare": "Minor",
            "geomagnetic_storm": False,
            "risk": "Low"
        })

    def get_history_json(self):
        history = []
        for i in range(7):
            history.append({
                "day": f"Day {i+1}",
                "risk_score": random.randint(20, 90)
            })
        return jsonify({
            "history": history
        })

    def get_dashboard_json(self):
        return jsonify({
            "tracked_satellites": 18452,
            "high_risk": 17,
            "medium_risk": 96,
            "low_risk": 18339,
            "average_risk_score": 42,
            "critical_alerts": 2
        })


# Export a default instance for easy access
satellite_service = SatelliteService()

