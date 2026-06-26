"""
Project Zenith
Orbital Congestion Prediction Inference Engine

Uses Gradient Boosting Classifier to predict
orbital congestion level.
"""

import os
import sys
import joblib

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from congestion.features import CongestionFeatures


MODEL_PATH = "../models/congestion_model.pkl"
SCALER_PATH = "../models/congestion_scaler.pkl"


class CongestionPredictor:

    def __init__(self):

        self.features = CongestionFeatures()

        self.model = self.load_model()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scaler_path = os.path.join(base_dir, "ml", "models", "congestion_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

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

        active_satellites,

        inactive_satellites,

        debris_objects,

        average_altitude,

        orbital_velocity,

        launch_frequency,

        collision_alerts,

        solar_activity,

        orbital_region,

        traffic_density

    ):

        sample = self.features.build(

            active_satellites,

            inactive_satellites,

            debris_objects,

            average_altitude,

            orbital_velocity,

            launch_frequency,

            collision_alerts,

            solar_activity,

            orbital_region,

            traffic_density

        )

        sample = self.pipeline.preprocess_sample(sample)
        sample = self.features.transform(sample)

        prediction = self.model.predict(sample)[0]

        probability = self.model.predict_proba(sample).max()

        levels = {

            0: "Low",

            1: "Moderate",

            2: "High",

            3: "Critical"

        }

        return {

            "congestion_level":

                levels.get(prediction, str(prediction)),

            "confidence":

                round(

                    float(probability * 100),

                    2

                )

        }

    # --------------------------------------------------
    # Batch Prediction
    # --------------------------------------------------

    def batch_predict(self, dataframe):

        dataframe = self.pipeline.preprocess_df(dataframe, training=False)

        X = self.features.transform(dataframe)

        predictions = self.model.predict(X)

        probabilities = self.model.predict_proba(X)

        levels = {0: "Low", 1: "Moderate", 2: "High", 3: "Critical"}

        results = []

        for i in range(len(predictions)):

            results.append({

                "congestion_level":

                    levels.get(predictions[i], str(predictions[i])),

                "confidence":

                    round(

                        float(probabilities[i].max() * 100),

                        2

                    )

            })

        return results


if __name__ == "__main__":

    predictor = CongestionPredictor()

    print(

        predictor.predict(

            9200,

            1800,

            31000,

            550,

            7.65,

            28,

            6,

            3,

            1,

            88

        )

    )