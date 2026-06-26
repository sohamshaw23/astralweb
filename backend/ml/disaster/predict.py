"""
Project Zenith
Disaster Prediction Engine
"""

import os
import sys
import joblib

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from disaster.features import DisasterFeatures

MODEL = "../models/disaster_model.pkl"
SCALER = "../models/disaster_scaler.pkl"


class DisasterPredictor:

    def __init__(self):

        self.model = joblib.load(MODEL)

        self.features = DisasterFeatures()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scaler_path = os.path.join(base_dir, "ml", "models", "disaster_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    def predict(

        self,

        temperature,

        humidity,

        wind_speed,

        rainfall,

        pressure,

        soil_moisture,

        vegetation_index,

        thermal_anomaly,

        population_density,

        elevation

    ):

        sample = self.features.build(

            temperature,

            humidity,

            wind_speed,

            rainfall,

            pressure,

            soil_moisture,

            vegetation_index,

            thermal_anomaly,

            population_density,

            elevation

        )

        sample = self.pipeline.preprocess_sample(sample)
        sample = self.features.transform(sample)

        prediction = self.model.predict(sample)[0]

        probability = self.model.predict_proba(sample).max()

        labels = {

            0: "Flood",

            1: "Wildfire",

            2: "Cyclone",

            3: "Landslide"

        }

        return {

            "prediction": labels.get(prediction),

            "confidence":

                round(

                    probability*100,

                    2

                )

        }


if __name__ == "__main__":

    predictor = DisasterPredictor()

    result = predictor.predict(

        40,

        24,

        13,

        1,

        1005,

        9,

        0.31,

        91,

        680,

        82

    )

    print(result)
