"""
Project Zenith
Collision Model Training
"""

import os
import joblib
import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from ml.preprocessing.pipeline import PreprocessingPipeline
from ml.preprocessing.dataset_loader import DatasetLoader
from features import CollisionFeatures


DATASET = "dataset.csv"

MODEL = "model.pkl"
SCALER = "scaler.pkl"


class CollisionTrainer:

    def __init__(self):

        self.features = CollisionFeatures()

    # ---------------------------------------
    # Load Dataset
    # ---------------------------------------

    def load_dataset(self):

        return DatasetLoader.load_csv(DATASET)

    # ---------------------------------------
    # Train Model
    # ---------------------------------------

    def train(self):

        df = self.load_dataset()

        # Instantiate pipeline and fit scaler
        pipeline = PreprocessingPipeline(scaler_path=SCALER)
        df = pipeline.preprocess_df(df, training=True)

        X = self.features.transform(df)

        y = df["collision"]

        X_train, X_test, y_train, y_test = train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42

        )

        model = xgb.XGBClassifier(

            n_estimators=200,

            learning_rate=0.05,

            max_depth=6,

            objective="binary:logistic",

            eval_metric="logloss",

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

        print("="*60)

        print("Collision Prediction Model")

        print("="*60)

        print()

        print(

            f"Accuracy : {accuracy:.4f}"

        )

        print()

        print(

            classification_report(

                y_test,

                prediction

            )

        )

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

        print("Model Saved Successfully.")

        return model


if __name__ == "__main__":

    trainer = CollisionTrainer()

    trainer.train()