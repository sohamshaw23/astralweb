"""
Project Zenith
Anomaly Detection Model Training

Algorithm:
Isolation Forest
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.ensemble import IsolationForest

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from anomaly.features import AnomalyFeatures


DATASET = "dataset.csv"
MODEL = "../models/anomaly_model.pkl"
SCALER = "../models/anomaly_scaler.pkl"


class AnomalyTrainer:

    def __init__(self):

        self.features = AnomalyFeatures()

    # ------------------------------------------
    # Load Dataset
    # ------------------------------------------

    def load_dataset(self):

        return DatasetLoader.load_csv(DATASET)

    # ------------------------------------------
    # Train Model
    # ------------------------------------------

    def train(self):

        print("=" * 60)
        print("Project Zenith - Anomaly Detection")
        print("=" * 60)

        df = self.load_dataset()

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        X = self.features.transform(df)

        model = IsolationForest(

            n_estimators=200,

            contamination=0.02,

            random_state=42

        )

        model.fit(X)

        prediction = model.predict(X)

        anomaly_count = (prediction == -1).sum()

        print()
        print(f"Dataset Size     : {len(df)}")
        print(f"Normal Samples   : {(prediction == 1).sum()}")
        print(f"Anomalies Found  : {anomaly_count}")
        print()

        joblib.dump(

            model,

            MODEL

        )

        print("Model Saved Successfully.")
        print(f"Location : {MODEL}")

        return model


if __name__ == "__main__":

    trainer = AnomalyTrainer()

    trainer.train()