"""
Project Zenith
Hotspot Prediction Model Training
"""

import os
import sys
import joblib
import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from hotspot.features import HotspotFeatures

DATASET = "dataset.csv"
MODEL = "../models/hotspot_model.pkl"
SCALER = "../models/hotspot_scaler.pkl"


class HotspotTrainer:

    def __init__(self):

        self.features = HotspotFeatures()

    def train(self):

        df = DatasetLoader.load_csv(DATASET)

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        X = self.features.transform(df)

        y = df["hotspot"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

        model = xgb.XGBClassifier(

            n_estimators=300,

            max_depth=6,

            learning_rate=0.05,

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

        print("Accuracy:", accuracy)

        joblib.dump(

            model,

            MODEL

        )

        print("Model Saved Successfully")


if __name__ == "__main__":

    trainer = HotspotTrainer()

    trainer.train()