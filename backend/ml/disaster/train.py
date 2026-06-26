"""
Project Zenith
Disaster Classification Training
"""

import os
import sys
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from disaster.features import DisasterFeatures

DATASET = "dataset.csv"

MODEL = "../models/disaster_model.pkl"
SCALER = "../models/disaster_scaler.pkl"


class DisasterTrainer:

    def __init__(self):

        self.features = DisasterFeatures()

    def train(self):

        df = DatasetLoader.load_csv(DATASET)

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        X = self.features.transform(df)

        y = df["disaster"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

        model = RandomForestClassifier(

            n_estimators=250,

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

        print("Accuracy :", accuracy)

        joblib.dump(

            model,

            MODEL

        )

        print("Model Saved.")


if __name__ == "__main__":

    DisasterTrainer().train()