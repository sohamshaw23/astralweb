"""
ml/model_manager.py

Project Zenith
Model Manager (Singleton Pattern)

Provides thread-safe-like caching of serialized model weights.
Loads each model only once upon demand (lazy loading).
"""

import os
import joblib


class ModelManager:
    """
    Singleton class to manage and cache trained machine learning models.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModelManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # Define paths relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self._paths = {
            "collision": os.path.join(base_dir, "collision", "model.pkl"),
            "anomaly": os.path.join(base_dir, "models", "anomaly_model.pkl"),
            "hotspot": os.path.join(base_dir, "models", "hotspot_model.pkl"),
            "disaster": os.path.join(base_dir, "models", "disaster_model.pkl"),
            "satellite_risk": os.path.join(base_dir, "models", "satellite_risk_model.pkl"),
            "congestion": os.path.join(base_dir, "models", "congestion_model.pkl")
        }
        self._models = {}
        self._initialized = True

    def _load_model(self, key):
        """
        Loads the model from disk if it hasn't been loaded already.
        """
        if key not in self._models:
            path = self._paths.get(key)
            if not path or not os.path.exists(path):
                raise FileNotFoundError(
                    f"Trained model '{key}' not found at expected path: {path}"
                )
            
            # Load model
            self._models[key] = joblib.load(path)
            
        return self._models[key]

    def get_collision_model(self):
        """
        Retrieves the cached collision classification model.
        """
        return self._load_model("collision")

    def get_anomaly_model(self):
        """
        Retrieves the cached anomaly detection (Isolation Forest) model.
        """
        return self._load_model("anomaly")

    def get_hotspot_model(self):
        """
        Retrieves the cached hotspot classification model.
        """
        return self._load_model("hotspot")

    def get_disaster_model(self):
        """
        Retrieves the cached disaster classification model.
        """
        return self._load_model("disaster")

    def get_satellite_risk_model(self):
        """
        Retrieves the cached satellite operational risk classification model.
        """
        return self._load_model("satellite_risk")

    def get_congestion_model(self):
        """
        Retrieves the cached orbital congestion classification model.
        """
        return self._load_model("congestion")


# Export a default instance for easy access
model_manager = ModelManager()
