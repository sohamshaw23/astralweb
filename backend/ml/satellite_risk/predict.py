"""
Project Zenith
Satellite Risk Prediction Engine

Uses a trained XGBoost model to predict
satellite operational risk.
"""

import os
import sys
import joblib

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from satellite_risk.features import SatelliteRiskFeatures


MODEL_PATH = "../models/satellite_risk_model.pkl"


class SatelliteRiskPredictor:

    def __init__(self):

        self.feature_builder = SatelliteRiskFeatures()

        self.model = self.load_model()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scaler_path = os.path.join(base_dir, "ml", "models", "satellite_risk_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    # ---------------------------------------
    # Load Model
    # ---------------------------------------

    def load_model(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(

                f"Model not found: {MODEL_PATH}"

            )

        return joblib.load(MODEL_PATH)

    # ---------------------------------------
    # Predict Risk
    # ---------------------------------------

    def predict(

        self,

        collision_probability,

        orbital_altitude,

        orbital_velocity,

        orbital_congestion,

        debris_density,

        solar_activity,

        satellite_age,

        fuel_remaining,

        communication_health,

        battery_health

    ):

        sample = self.feature_builder.build(

            collision_probability,

            orbital_altitude,

            orbital_velocity,

            orbital_congestion,

            debris_density,

            solar_activity,

            satellite_age,

            fuel_remaining,

            communication_health,

            battery_health

        )
        sample = self.pipeline.preprocess_sample(sample)
        sample = self.feature_builder.transform(sample)

        prediction = self.model.predict(sample)[0]

        probabilities = self.model.predict_proba(sample)[0]

        confidence = float(max(probabilities))

        labels = {

            0: "Low",

            1: "Moderate",

            2: "High",

            3: "Critical"

        }

        recommendations = {

            "Low":
                "Routine monitoring.",

            "Moderate":
                "Increase observation frequency.",

            "High":
                "Monitor continuously and prepare mitigation.",

            "Critical":
                "Immediate assessment and collision avoidance recommended."

        }

        level = labels[prediction]

        return {

            "risk_level": level,

            "confidence":

                round(

                    confidence * 100,

                    2

                ),

            "recommended_action":

                recommendations[level]

        }

    # ---------------------------------------
    # Batch Prediction
    # ---------------------------------------

    def batch_predict(self, dataframe):

        dataframe = self.pipeline.preprocess_df(dataframe, training=False)

        X = self.feature_builder.transform(

            dataframe

        )

        predictions = self.model.predict(X)

        probabilities = self.model.predict_proba(X)

        labels = {

            0: "Low",

            1: "Moderate",

            2: "High",

            3: "Critical"

        }

        results = []

        for i in range(len(predictions)):

            results.append({

                "risk_level":

                    labels[predictions[i]],

                "confidence":

                    round(

                        float(

                            max(

                                probabilities[i]

                            )

                        ) * 100,

                        2

                    )

            })

        return results


if __name__ == "__main__":

    predictor = SatelliteRiskPredictor()

    result = predictor.predict(

        collision_probability=0.81,

        orbital_altitude=550,

        orbital_velocity=7.66,

        orbital_congestion=88,

        debris_density=73,

        solar_activity=4,

        satellite_age=6,

        fuel_remaining=58,

        communication_health=91,

        battery_health=93

    )

    print(result)