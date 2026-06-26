"""
Project Zenith
Anomaly Detection Inference Engine

Uses Isolation Forest to detect abnormal
satellite behaviour.
"""

import os
import sys
import joblib

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from anomaly.features import AnomalyFeatures


MODEL_PATH = "../models/anomaly_model.pkl"


class AnomalyPredictor:

    def __init__(self):

        self.feature_builder = AnomalyFeatures()

        self.model = self.load_model()

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        scaler_path = os.path.join(base_dir, "ml", "models", "anomaly_scaler.pkl")
        self.pipeline = PreprocessingPipeline(scaler_path=scaler_path)

    # ------------------------------------------
    # Load Model
    # ------------------------------------------

    def load_model(self):

        if not os.path.exists(MODEL_PATH):

            raise FileNotFoundError(

                f"Model not found: {MODEL_PATH}"

            )

        return joblib.load(MODEL_PATH)

    # ------------------------------------------
    # Predict
    # ------------------------------------------

    def predict(

        self,

        velocity,

        altitude,

        inclination,

        eccentricity,

        orbital_period,

        mean_motion,

        trajectory_deviation,

        debris_density,

        solar_activity,

        orbital_congestion

    ):

        sample = self.feature_builder.build(

            velocity,

            altitude,

            inclination,

            eccentricity,

            orbital_period,

            mean_motion,

            trajectory_deviation,

            debris_density,

            solar_activity,

            orbital_congestion

        )
        sample = self.pipeline.preprocess_sample(sample)
        sample = self.feature_builder.transform(sample)

        prediction = self.model.predict(sample)[0]

        score = self.model.decision_function(sample)[0]

        anomaly_score = round((1 - score) * 100, 2)

        if prediction == -1:

            status = "Anomaly"

        else:

            status = "Normal"

        if anomaly_score > 85:

            severity = "Critical"

        elif anomaly_score > 65:

            severity = "High"

        elif anomaly_score > 40:

            severity = "Moderate"

        else:

            severity = "Low"

        return {

            "status": status,

            "severity": severity,

            "anomaly_score": anomaly_score

        }

    # ------------------------------------------
    # Batch Prediction
    # ------------------------------------------

    def batch_predict(self, dataframe):

        dataframe = self.pipeline.preprocess_df(dataframe, training=False)

        X = self.feature_builder.transform(

            dataframe

        )

        predictions = self.model.predict(X)

        scores = self.model.decision_function(X)

        results = []

        for i in range(len(predictions)):

            results.append({

                "status":

                    "Anomaly"

                    if predictions[i] == -1

                    else "Normal",

                "anomaly_score":

                    round(

                        (1 - scores[i]) * 100,

                        2

                    )

            })

        return results


if __name__ == "__main__":

    predictor = AnomalyPredictor()

    result = predictor.predict(

        velocity=7.95,

        altitude=560,

        inclination=98.3,

        eccentricity=0.001,

        orbital_period=92.3,

        mean_motion=15.1,

        trajectory_deviation=8.4,

        debris_density=83,

        solar_activity=5,

        orbital_congestion=92

    )

    print(result)

