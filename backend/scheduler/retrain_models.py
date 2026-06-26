"""
scheduler/retrain_models.py

Retrains ML Models
"""

import subprocess
import sys

import os

def train_collision_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/collision", env=env, check=True)

def train_anomaly_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/anomaly", env=env, check=True)

def train_hotspot_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/hotspot", env=env, check=True)

def train_disaster_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/disaster", env=env, check=True)

def train_congestion_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/congestion", env=env, check=True)

def train_satellite_risk_model():
    env = os.environ.copy()
    env["PYTHONPATH"] = ".."
    subprocess.run([sys.executable, "train.py"], cwd="ml/satellite_risk", env=env, check=True)




def retrain():

    print("Retraining Collision Model (XGBoost)...")
    train_collision_model()

    print("Retraining Anomaly Detection Model (Isolation Forest)...")
    train_anomaly_model()

    print("Retraining Hotspot Detection Model (XGBoost)...")
    train_hotspot_model()

    print("Retraining Disaster Classification Model (Random Forest)...")
    train_disaster_model()

    print("Retraining Congestion Model (Gradient Boosting)...")
    train_congestion_model()

    print("Retraining Satellite Risk Model (XGBoost)...")
    train_satellite_risk_model()

    print("All Models Updated Successfully.")


if __name__ == "__main__":

    retrain()