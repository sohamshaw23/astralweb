"""
services/orbit_service.py

Project Zenith
Orbital Intelligence Service

Congestion endpoints: _parse_congestion_params → _run_congestion_inference
(ModelManager + PreprocessingPipeline) → enriched JSON with
orbital_congestion, traffic_density, future_congestion, confidence.
Routes contain zero ML logic.
"""

import os
import math
import random
from datetime import datetime, timedelta
from flask import request, jsonify
from skyfield.api import load, EarthSatellite
from ml.model_manager import model_manager
from ml.anomaly.features import AnomalyFeatures
from ml.congestion.features import CongestionFeatures
from ml.preprocessing.pipeline import PreprocessingPipeline
from database.prediction_logger import log_prediction
from database.redis_cache import cache_manager

ts = load.timescale()


# ---------------------------------------------------------------------------
# Congestion classification tables
# ---------------------------------------------------------------------------

_CONGESTION_LABELS = {0: "Low", 1: "Moderate", 2: "High", 3: "Critical"}

# Traffic density description keyed on congestion label
_TRAFFIC_DENSITY = {
    "Low":      "Sparse — fewer than 5,000 active objects in this orbital band.",
    "Moderate": "Elevated — 5,000–10,000 objects; manoeuvre windows still available.",
    "High":     "Dense — 10,000–18,000 objects; close-approach alerts increasing.",
    "Critical": "Saturated — 18,000+ objects; collision risk significantly elevated.",
}

# Future congestion projection keyed on current label and launch frequency
def _project_future_congestion(current_label: str, launch_frequency: float) -> str:
    """
    Simple heuristic: if launch frequency > 20/month the next band up is
    expected within 12 months; > 40 within 6 months.
    """
    _order = ["Low", "Moderate", "High", "Critical"]
    idx = _order.index(current_label)
    if launch_frequency > 40 and idx < 3:
        next_label = _order[min(idx + 1, 3)]
        return f"{next_label} expected within 6 months at current launch rate."
    elif launch_frequency > 20 and idx < 3:
        next_label = _order[min(idx + 1, 3)]
        return f"{next_label} expected within 12 months at current launch rate."
    elif idx == 3:
        return "Orbital band already at Critical saturation. Regulatory intervention required."
    else:
        return "Congestion level projected to remain stable over the next 12 months."


# ---------------------------------------------------------------------------
# Anomaly classification tables  (Isolation Forest)
# ---------------------------------------------------------------------------

# Isolation Forest predict() returns +1 (normal) or -1 (anomaly)
_ANOMALY_STATUS = {1: "Normal", -1: "Anomaly"}

# Severity bands keyed on anomaly_score (0–100, higher = more anomalous)
_ANOMALY_SEVERITY_BANDS = [
    (85, "Critical"),
    (65, "High"),
    (40, "Moderate"),
    (0,  "Low"),
]


def _classify_anomaly_severity(anomaly_score: float) -> str:
    for threshold, label in _ANOMALY_SEVERITY_BANDS:
        if anomaly_score > threshold:
            return label
    return "Low"


def _anomaly_confidence(decision_score: float) -> float:
    """
    Convert Isolation Forest decision_function score to a 0–100 confidence
    value.  Negative decision scores signal anomalies; the further below
    zero, the more confident the model is.  We clamp and invert so that:
      - deep anomaly  (score << 0)  → confidence near 100
      - clean normal  (score >> 0)  → confidence near 100 (opposite end)
    The confidence reflects how decisive the model is, regardless of class.
    """
    # decision_function typically ranges roughly [-0.5, 0.5]
    # Map to [0, 1] then to percentage
    clamped = max(-0.5, min(0.5, decision_score))
    # For anomaly: score is negative; flip sign so anomalous → high conf
    # For normal:  score is positive; keep as is
    if decision_score < 0:
        return round((0.5 + abs(clamped)) * 100, 2)   # anomaly confidence
    else:
        return round((0.5 + clamped) * 100, 2)         # normal confidence


class OrbitService:

    def __init__(self):
        self.anomaly_features = AnomalyFeatures()
        self.congestion_features = CongestionFeatures()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        anomaly_scaler_path = os.path.join(base_dir, "ml", "models", "anomaly_scaler.pkl")
        congestion_scaler_path = os.path.join(base_dir, "ml", "models", "congestion_scaler.pkl")
        self.anomaly_pipeline = PreprocessingPipeline(scaler_path=anomaly_scaler_path)
        self.congestion_pipeline = PreprocessingPipeline(scaler_path=congestion_scaler_path)

    # ---------------------------------
    # Predict Orbit
    # ---------------------------------

    def predict_orbit(self, satellite, minutes=120):

        predictions = []

        now = datetime.utcnow()

        for i in range(minutes):

            t = ts.utc(now + timedelta(minutes=i))

            geo = satellite.at(t)

            sub = geo.subpoint()

            predictions.append({

                "time": (now + timedelta(minutes=i)).isoformat(),

                "latitude": round(
                    sub.latitude.degrees,
                    4
                ),

                "longitude": round(
                    sub.longitude.degrees,
                    4
                ),

                "altitude_km": round(
                    sub.elevation.km,
                    2
                )

            })

        return predictions

    # ---------------------------------
    # Orbital Elements
    # ---------------------------------

    def orbital_elements(self, satellite):

        model = satellite.model

        return {

            "inclination": model.inclo,

            "eccentricity": model.ecco,

            "raan": model.nodeo,

            "argument_of_perigee": model.argpo,

            "mean_motion": model.no_kozai,

            "mean_anomaly": model.mo

        }

    # ---------------------------------
    # Orbital Period
    # ---------------------------------

    def orbital_period(self, satellite):

        motion = satellite.model.no_kozai

        period = (2 * math.pi) / motion

        return round(period, 2)

    # ---------------------------------
    # Orbit Type
    # ---------------------------------

    def orbit_type(self, altitude):

        if altitude < 2000:
            return "LEO"

        elif altitude < 35786:
            return "MEO"

        elif altitude < 36050:
            return "GEO"

        return "HEO"

    # ---------------------------------
    # Orbit Path
    # ---------------------------------

    def orbit_path(self, satellite):

        path = []

        now = datetime.utcnow()

        for i in range(360):

            t = ts.utc(now + timedelta(minutes=i))

            geo = satellite.at(t)

            sub = geo.subpoint()

            path.append({

                "lat": round(
                    sub.latitude.degrees,
                    4
                ),

                "lon": round(
                    sub.longitude.degrees,
                    4
                )

            })

        return path

    # ---------------------------------
    # Relative Distance
    # ---------------------------------

    def distance(self, sat1, sat2):

        t = ts.now()

        p1 = sat1.at(t).position.km

        p2 = sat2.at(t).position.km

        d = math.sqrt(

            (p1[0]-p2[0])**2 +

            (p1[1]-p2[1])**2 +

            (p1[2]-p2[2])**2

        )

        return round(d, 2)

    # ---------------------------------
    # Collision Probability
    # ---------------------------------

    def collision_probability(self, distance):

        if distance > 100:

            return 0.0

        probability = (

            (100-distance)

            /100

        )*100

        return round(probability,2)

    # ---------------------------------
    # Congestion Score
    # ---------------------------------

    def congestion_score(self, satellites):

        total = len(satellites)

        if total > 18000:

            return 95

        elif total > 15000:

            return 80

        elif total > 10000:

            return 65

        elif total > 5000:

            return 45

        return 20

    # ---------------------------------
    # Risk Index
    # ---------------------------------

    def satellite_risk(self,

                       collision,

                       congestion):

        score = (

            collision*0.6 +

            congestion*0.4

        )

        if score > 80:

            level = "Critical"

        elif score > 60:

            level = "High"

        elif score > 40:

            level = "Moderate"

        else:

            level = "Low"

        return {

            "score": round(score,2),

            "level": level

        }

    # ---------------------------------
    # Coverage Radius
    # ---------------------------------

    def coverage_radius(self,

                        altitude):

        earth = 6371

        radius = math.sqrt(

            (earth+altitude)**2

            -

            earth**2

        )

        return round(radius,2)

    # ---------------------------------
    # Visibility Score
    # ---------------------------------

    def visibility(self,

                    elevation):

        if elevation > 70:

            return "Excellent"

        elif elevation > 45:

            return "Good"

        elif elevation > 20:

            return "Moderate"

        return "Poor"

    # ---------------------------------
    # Dashboard
    # ---------------------------------

    def dashboard(self):

        return {

            "status": "Running",

            "prediction_engine": "Skyfield",

            "collision_engine": "Enabled",

            "risk_engine": "Enabled",

            "coverage_engine": "Enabled",

            "updated":

                datetime.utcnow().isoformat()

        }

    # ---------------------------------
    # Private: parse & validate anomaly parameters
    # ---------------------------------

    def _parse_anomaly_params(self):
        """
        Parses and validates numeric query parameters shared by
        all anomaly detection endpoints.
        Returns (params_dict, error_response). One of them is None.
        """
        try:
            params = {
                "velocity":             float(request.args.get("velocity",             7.95)),
                "altitude":             float(request.args.get("altitude",             560.0)),
                "inclination":          float(request.args.get("inclination",          98.3)),
                "eccentricity":         float(request.args.get("eccentricity",         0.001)),
                "orbital_period":       float(request.args.get("orbital_period",       92.3)),
                "mean_motion":          float(request.args.get("mean_motion",          15.1)),
                "trajectory_deviation": float(request.args.get("trajectory_deviation", 8.4)),
                "debris_density":       float(request.args.get("debris_density",       83.0)),
                "solar_activity":       float(request.args.get("solar_activity",       5.0)),
                "orbital_congestion":   float(request.args.get("orbital_congestion",   92.0)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        return params, None

    # ---------------------------------
    # Private: build sample, preprocess, run model
    # ---------------------------------

    def _run_anomaly_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the anomaly preprocessing
        pipeline, and runs the Isolation Forest model from ModelManager.

        Isolation Forest uses decision_function (not predict_proba).
        Returns (status, anomaly_score, severity, confidence, error_response).
        """
        # 1. Build raw feature DataFrame
        sample = self.anomaly_features.build(**params)

        # 2. Preprocess via shared pipeline (clean → engineer → scale)
        sample = self.anomaly_pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.anomaly_features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model       = model_manager.get_anomaly_model()
            prediction  = int(model.predict(sample)[0])          # +1 or -1
            dec_score   = float(model.decision_function(sample)[0])
        except Exception as exc:
            return None, None, None, None, (
                jsonify({"error": f"Model inference failed: {exc}"}), 500
            )

        # Higher (1 - score) → more anomalous
        anomaly_score = round((1.0 - dec_score) * 100, 2)
        status        = _ANOMALY_STATUS.get(prediction, "Normal")
        severity      = _classify_anomaly_severity(anomaly_score)
        confidence    = _anomaly_confidence(dec_score)

        return status, anomaly_score, severity, confidence, None

    # ---------------------------------
    # Anomaly Detection  (GET /)
    # ---------------------------------

    def predict_anomaly(self):
        """
        Primary anomaly detection endpoint.

        Returns:
            status        – Normal / Anomaly  (Isolation Forest label)
            anomaly_score – deviation index 0–100 (higher = more anomalous)
            severity      – Low / Moderate / High / Critical
            confidence    – model decisiveness % (0–100)
        """
        params, err = self._parse_anomaly_params()
        if err:
            return err

        status, anomaly_score, severity, confidence, err = \
            self._run_anomaly_inference(params)
        if err:
            return err

        log_prediction(
            model="anomaly",
            prediction=status,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        return jsonify({
            "satellite":    request.args.get("name", "ISS"),
            "status":       status,
            "anomaly_score": anomaly_score,
            "severity":     severity,
            "confidence":   confidence,
        })

    # ---------------------------------
    # Anomaly Analysis  (GET /analysis)
    # ---------------------------------

    def predict_anomaly_analysis(self):
        """
        Extended anomaly analysis with full input echo.

        Returns all fields from predict_anomaly plus the raw input
        parameters so clients can audit what was fed to the model.
        """
        params, err = self._parse_anomaly_params()
        if err:
            return err

        status, anomaly_score, severity, confidence, err = \
            self._run_anomaly_inference(params)
        if err:
            return err

        log_prediction(
            model="anomaly",
            prediction=status,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        return jsonify({
            # Core prediction fields
            "satellite":     request.args.get("name", "ISS"),
            "status":        status,
            "anomaly_score": anomaly_score,
            "severity":      severity,
            "confidence":    confidence,

            # Input echo for audit / debugging
            "inputs": {
                "velocity_km_s":           params["velocity"],
                "altitude_km":             params["altitude"],
                "inclination_deg":         params["inclination"],
                "eccentricity":            params["eccentricity"],
                "orbital_period_min":      params["orbital_period"],
                "mean_motion":             params["mean_motion"],
                "trajectory_deviation_deg": params["trajectory_deviation"],
                "debris_density":          params["debris_density"],
                "solar_activity":          params["solar_activity"],
                "orbital_congestion":      params["orbital_congestion"],
            },
        })

    def get_anomaly_active(self):
        anomalies = []
        for i in range(8):
            anomalies.append({
                "satellite": f"SAT-{2000+i}",
                "anomaly_score": round(random.uniform(0.45, 0.99), 2),
                "status": random.choice(["Moderate", "High", "Critical"])
            })
        return jsonify({
            "count": len(anomalies),
            "active_anomalies": anomalies
        })

    def get_anomaly_trajectory(self):
        deviations = []
        for i in range(12):
            deviations.append({
                "satellite": f"SAT-{500+i}",
                "deviation_deg": round(random.uniform(0.5, 18), 2)
            })
        return jsonify({
            "trajectory_deviations": deviations
        })

    def get_anomaly_high_risk(self):
        objects = []
        for i in range(5):
            objects.append({
                "satellite": f"SAT-{700+i}",
                "risk": random.choice(["High", "Critical"]),
                "score": round(random.uniform(0.8, 0.99), 2)
            })
        return jsonify({
            "high_risk_objects": objects
        })

    def get_anomaly_statistics(self):
        return jsonify({
            "tracked_satellites": 18452,
            "normal_objects": 18396,
            "moderate_anomalies": 38,
            "high_anomalies": 14,
            "critical_anomalies": 4
        })

    def get_anomaly_history(self):
        history = []
        for i in range(7):
            history.append({
                "day": f"Day {i+1}",
                "anomalies": random.randint(3, 18)
            })
        return jsonify({
            "history": history
        })

    def get_anomaly_dashboard(self):
        return jsonify({
            "active_anomalies": 18,
            "critical": 4,
            "high": 14,
            "normal": 18396,
            "last_scan": datetime.utcnow().isoformat() + "Z",
            "system_status": "Monitoring"
        })

    # ---------------------------------
    # Private: parse & validate congestion parameters
    # ---------------------------------

    def _parse_congestion_params(self):
        """
        Parses and validates the numeric query parameters shared by
        all congestion prediction endpoints.
        Returns (params_dict, error_response). One of them is None.
        """
        try:
            params = {
                "active_satellites":   float(request.args.get("active_satellites",   9200.0)),
                "inactive_satellites": float(request.args.get("inactive_satellites", 1800.0)),
                "debris_objects":      float(request.args.get("debris_objects",      31000.0)),
                "average_altitude":    float(request.args.get("average_altitude",    550.0)),
                "orbital_velocity":    float(request.args.get("orbital_velocity",    7.65)),
                "launch_frequency":    float(request.args.get("launch_frequency",    28.0)),
                "collision_alerts":    float(request.args.get("collision_alerts",    6.0)),
                "solar_activity":      float(request.args.get("solar_activity",      3.0)),
                "orbital_region":      float(request.args.get("orbital_region",      1.0)),
                "traffic_density":     float(request.args.get("traffic_density",     88.0)),
            }
        except (ValueError, TypeError):
            return None, (jsonify({"error": "Invalid numerical parameters provided."}), 400)

        return params, None

    # ---------------------------------
    # Private: build sample, preprocess, run model
    # ---------------------------------

    def _run_congestion_inference(self, params: dict):
        """
        Builds the feature DataFrame, applies the congestion preprocessing
        pipeline, and runs the congestion model from ModelManager.
        Returns (orbital_congestion, confidence_pct, error_response).
        """
        # 1. Build raw feature DataFrame
        sample = self.congestion_features.build(**params)

        # 2. Preprocess via shared pipeline (clean → engineer → scale)
        sample = self.congestion_pipeline.preprocess_sample(sample)

        # 3. Select exactly the columns the model was trained on
        sample = self.congestion_features.transform(sample)

        # 4. Inference via ModelManager (loads model once, caches forever)
        try:
            model       = model_manager.get_congestion_model()
            prediction  = int(model.predict(sample)[0])
            confidence  = float(model.predict_proba(sample).max())
        except Exception as exc:
            return None, None, (jsonify({"error": f"Model inference failed: {exc}"}), 500)

        orbital_congestion = _CONGESTION_LABELS.get(prediction, "Low")
        confidence_pct     = round(confidence * 100, 2)

        return orbital_congestion, confidence_pct, None

    # ---------------------------------
    # Congestion Prediction  (GET /)
    # ---------------------------------

    def predict_congestion(self):
        """
        Primary orbital congestion endpoint.

        Returns:
            orbital_congestion  – Low / Moderate / High / Critical
            traffic_density     – human-readable density description
            future_congestion   – projected trend based on launch frequency
            confidence          – model's class-probability % (0–100)
        """
        params, err = self._parse_congestion_params()
        if err:
            return err

        cache_params = {**params, "endpoint": "predict"}
        cached_result = cache_manager.get_cached("congestion", cache_params)
        if cached_result:
            return jsonify(cached_result)

        orbital_congestion, confidence, err = self._run_congestion_inference(params)
        if err:
            return err

        traffic_density  = _TRAFFIC_DENSITY[orbital_congestion]
        future_congestion = _project_future_congestion(
            orbital_congestion, params["launch_frequency"]
        )

        log_prediction(
            model="congestion",
            prediction=orbital_congestion,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            "orbital_congestion":  orbital_congestion,
            "traffic_density":     traffic_density,
            "future_congestion":   future_congestion,
            "confidence":          confidence,
        }
        cache_manager.set_cached("congestion", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    # ---------------------------------
    # Congestion Analysis  (GET /analysis)
    # ---------------------------------

    def predict_congestion_analysis(self):
        """
        Extended congestion analysis with full input echo.

        Returns all fields from predict_congestion plus the raw input
        parameters so clients can audit what was fed to the model.
        """
        params, err = self._parse_congestion_params()
        if err:
            return err

        cache_params = {**params, "endpoint": "analysis"}
        cached_result = cache_manager.get_cached("congestion", cache_params)
        if cached_result:
            return jsonify(cached_result)

        orbital_congestion, confidence, err = self._run_congestion_inference(params)
        if err:
            return err

        traffic_density   = _TRAFFIC_DENSITY[orbital_congestion]
        future_congestion = _project_future_congestion(
            orbital_congestion, params["launch_frequency"]
        )

        log_prediction(
            model="congestion",
            prediction=orbital_congestion,
            confidence=confidence,
            input_features=params,
            request=request,
        )

        response_data = {
            # Core prediction fields
            "orbital_congestion":  orbital_congestion,
            "traffic_density":     traffic_density,
            "future_congestion":   future_congestion,
            "confidence":          confidence,

            # Input echo for audit / debugging
            "inputs": {
                "active_satellites":   params["active_satellites"],
                "inactive_satellites": params["inactive_satellites"],
                "debris_objects":      params["debris_objects"],
                "average_altitude_km": params["average_altitude"],
                "orbital_velocity_km_s": params["orbital_velocity"],
                "launch_frequency_per_month": params["launch_frequency"],
                "collision_alerts":    params["collision_alerts"],
                "solar_activity":      params["solar_activity"],
                "orbital_region":      params["orbital_region"],
                "traffic_density_raw": params["traffic_density"],
            },
        }
        cache_manager.set_cached("congestion", cache_params, response_data, ttl_seconds=300)
        return jsonify(response_data)

    def get_congestion_leo(self):
        score = random.randint(70, 100)
        return jsonify({
            "orbit": "Low Earth Orbit",
            "altitude": "160 - 2000 km",
            "tracked_objects": 18452,
            "congestion": score
        })

    def get_congestion_meo(self):
        score = random.randint(20, 50)
        return jsonify({
            "orbit": "Medium Earth Orbit",
            "altitude": "2000 - 35786 km",
            "tracked_objects": 325,
            "congestion": score
        })

    def get_congestion_geo(self):
        score = random.randint(30, 70)
        return jsonify({
            "orbit": "Geostationary Orbit",
            "tracked_objects": 625,
            "congestion": score
        })

    def get_congestion_heo(self):
        score = random.randint(5, 20)
        return jsonify({
            "orbit": "High Earth Orbit",
            "tracked_objects": 92,
            "congestion": score
        })

    def get_congestion_heatmap(self):
        data = []
        for _ in range(60):
            data.append({
                "latitude": round(random.uniform(-90, 90), 4),
                "longitude": round(random.uniform(-180, 180), 4),
                "density": random.randint(10, 100)
            })
        return jsonify({
            "heatmap": data
        })

    def get_congestion_critical(self):
        return jsonify({
            "critical_regions": [
                {
                    "orbit": "LEO",
                    "density": 96,
                    "risk": "High"
                },
                {
                    "orbit": "GEO",
                    "density": 74,
                    "risk": "Moderate"
                }
            ]
        })

    def get_congestion_debris(self):
        return jsonify({
            "tracked_debris": 35781,
            "high_risk_objects": 214,
            "debris_density": "Moderate"
        })

    def get_congestion_statistics(self):
        score = random.randint(40, 75)
        return jsonify({
            "active_satellites": 18452,
            "tracked_debris": 35781,
            "overall_score": score,
            "critical_orbits": 2,
            "collision_alerts": 4
        })

    def get_congestion_dashboard(self):
        leo = random.randint(70, 100)
        meo = random.randint(20, 50)
        geo = random.randint(30, 70)
        heo = random.randint(5, 20)
        overall = round((leo + meo + geo + heo) / 4)
        return jsonify({
            "LEO": leo,
            "MEO": meo,
            "GEO": geo,
            "HEO": heo,
            "overall": overall,
            "updated": datetime.utcnow().isoformat() + "Z"
        })


# Export a default instance for easy access
orbit_service = OrbitService()