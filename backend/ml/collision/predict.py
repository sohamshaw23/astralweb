"""
Project Zenith
Collision Prediction Inference Engine

Uses the trained XGBoost model to predict
satellite collision probability.
"""

import os
import joblib
import numpy as np

from features import CollisionFeatures


MODEL_PATH = "model.pkl"


class CollisionPredictor:

    def __init__(self):

        self.feature_builder = CollisionFeatures()

        self.model = self.load_model()

    # --------------------------------------------------
    # Load Model
    # --------------------------------------------------

    def load_model(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(

                f"Model not found: {MODEL_PATH}"

            )

        return joblib.load(MODEL_PATH)

    # --------------------------------------------------
    # Predict
    # --------------------------------------------------

    def predict(

        self,

        relative_velocity,

        closest_distance,

        orbital_altitude,

        inclination,

        eccentricity,

        orbital_congestion,

        debris_density,

        solar_kp_index,

        satellite_age,

        cross_section

    ):

        sample = self.feature_builder.build(

            relative_velocity,

            closest_distance,

            orbital_altitude,

            inclination,

            eccentricity,

            orbital_congestion,

            debris_density,

            solar_kp_index,

            satellite_age,

            cross_section

        )

        probability = self.model.predict_proba(sample)[0][1]

        prediction = self.model.predict(sample)[0]

        if probability >= 0.85:

            risk = "Critical"

        elif probability >= 0.65:

            risk = "High"

        elif probability >= 0.35:

            risk = "Moderate"

        else:

            risk = "Low"

        return {

            "collision_probability":

                round(

                    float(probability * 100),

                    2

                ),

            "prediction":

                int(prediction),

            "risk_level":

                risk

        }

    # --------------------------------------------------
    # Batch Prediction
    # --------------------------------------------------

    def batch_predict(self, dataframe):

        X = self.feature_builder.transform(

            dataframe

        )

        probabilities = self.model.predict_proba(X)

        predictions = self.model.predict(X)

        results = []

        for i in range(len(predictions)):

            results.append({

                "collision_probability":

                    round(

                        float(

                            probabilities[i][1] * 100

                        ),

                        2

                    ),

                "prediction":

                    int(predictions[i])

            })

        return results


if __name__ == "__main__":

    predictor = CollisionPredictor()

    result = predictor.predict(

        relative_velocity=7.4,

        closest_distance=3.1,

        orbital_altitude=550,

        inclination=98.2,

        eccentricity=0.001,

        orbital_congestion=82,

        debris_density=65,

        solar_kp_index=4,

        satellite_age=5,

        cross_section=6.2

    )

    print(result)