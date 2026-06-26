"""
Project Zenith
Hotspot Prediction Engine
"""

import os
import sys
import joblib

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from hotspot.features import HotspotFeatures

MODEL_PATH = "../models/hotspot_model.pkl"
SCALER = "../models/hotspot_scaler.pkl"


class HotspotPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL_PATH)

        self.features = HotspotFeatures()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scaler_path = os.path.join(base_dir, "ml", "models", "hotspot_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    def predict(

        self,

        temperature,

        humidity,

        wind_speed,

        rainfall,

        vegetation_index,

        thermal_anomaly,

        population_density,

        elevation,

        soil_moisture,

        historical_frequency

    ):

        sample = self.features.build(

            temperature,

            humidity,

            wind_speed,

            rainfall,

            vegetation_index,

            thermal_anomaly,

            population_density,

            elevation,

            soil_moisture,

            historical_frequency

        )

        sample = self.pipeline.preprocess_sample(sample)
        sample = self.features.transform(sample)

        probability = self.model.predict_proba(sample)[0][1]

        prediction = self.model.predict(sample)[0]

        return {

            "hotspot_probability":

                round(

                    probability*100,

                    2

                ),

            "prediction":

                int(prediction),

            "risk_level":

                "High"

                if probability > 0.8

                else

                "Moderate"

                if probability > 0.5

                else

                "Low"

        }


if __name__ == "__main__":

    predictor = HotspotPredictor()

    result = predictor.predict(

        temperature=41,

        humidity=28,

        wind_speed=13,

        rainfall=2,

        vegetation_index=0.31,

        thermal_anomaly=89,

        population_density=740,

        elevation=82,

        soil_moisture=11,

        historical_frequency=7

    )

    print(result)
