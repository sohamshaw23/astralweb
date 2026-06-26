"""
Project Zenith
Satellite Risk Model Training

Algorithm:
XGBoost Multi-Class Classification
"""

import os
import sys
import joblib
import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Ensure absolute import path resolves for pipeline
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from satellite_risk.features import SatelliteRiskFeatures


DATASET = "dataset.csv"

MODEL = "../models/satellite_risk_model.pkl"
SCALER = "../models/satellite_risk_scaler.pkl"


class SatelliteRiskTrainer:

    def __init__(self):

        self.features = SatelliteRiskFeatures()

    # ---------------------------------------
    # Load Dataset
    # ---------------------------------------

    def load_dataset(self):

        return DatasetLoader.load_csv(DATASET)

    # ---------------------------------------
    # Train
    # ---------------------------------------

    def train(self):

        print("=" * 60)
        print("Project Zenith - Satellite Risk Model")
        print("=" * 60)

        df = self.load_dataset()

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        self.features.validate(df)

        X = self.features.transform(df)

        y = df["risk"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.20,

            random_state=42,

            stratify=y

        )

        model = xgb.XGBClassifier(

            objective="multi:softprob",

            num_class=4,

            n_estimators=300,

            learning_rate=0.05,

            max_depth=6,

            subsample=0.9,

            colsample_bytree=0.9,

            eval_metric="mlogloss",

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
        print(f"Accuracy : {accuracy:.4f}")
        print()

        print("Classification Report")
        print()

        print(

            classification_report(

                y_test,

                prediction,

                digits=4

            )

        )

        print("Confusion Matrix")
        print()

        print(

            confusion_matrix(

                y_test,

                prediction

            )

        )

        joblib.dump(

            model,

            MODEL

        )

        print()
        print("Model Saved Successfully")
        print(f"Location : {MODEL}")

        return model

    # ---------------------------------------
    # Feature Importance
    # ---------------------------------------

    def feature_importance(self, model):

        importance = model.feature_importances_

        names = self.features.feature_names()

        print()

        print("Feature Importance")

        print("-" * 40)

        for name, score in zip(

            names,

            importance

        ):

            print(

                f"{name:30} {score:.4f}"

            )


if __name__ == "__main__":

    trainer = SatelliteRiskTrainer()

    model = trainer.train()

    trainer.feature_importance(model)