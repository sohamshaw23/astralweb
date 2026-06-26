"""
Project Zenith
Orbital Congestion Training
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from congestion.features import CongestionFeatures

DATASET = "dataset.csv"

MODEL = "../models/congestion_model.pkl"
SCALER = "../models/congestion_scaler.pkl"


class CongestionTrainer:

    def __init__(self):

        self.features = CongestionFeatures()

    def train(self):

        df = DatasetLoader.load_csv(DATASET)

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        X = self.features.transform(df)

        y = df["congestion"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

        model = GradientBoostingClassifier(

            n_estimators=250,

            learning_rate=0.05,

            max_depth=4,

            random_state=42

        )

        model.fit(

            X_train,

            y_train

        )

        prediction = model.predict(X_test)

        accuracy = accuracy_score(

            y_test,

            prediction

        )

        print()

        print(f"Accuracy : {accuracy}")

        joblib.dump(

            model,

            MODEL

        )

        print("Congestion Model Saved.")


if __name__ == "__main__":

    CongestionTrainer().train()