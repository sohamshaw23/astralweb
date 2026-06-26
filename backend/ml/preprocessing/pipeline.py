"""
ml/preprocessing/pipeline.py

Project Zenith
Unified Preprocessing Pipeline
"""

import os
import sys
import pandas as pd

# Add base directory to path to ensure absolute import compatibility
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from ml.preprocessing.dataset_loader import DatasetLoader
from ml.preprocessing.cleaning import DataCleaner
from ml.preprocessing.encoder import Encoder
from ml.preprocessing.feature_engineering import FeatureEngineering
from ml.preprocessing.scaler import FeatureScaler


class PreprocessingPipeline:

    def __init__(self, scaler_path=None, encoder_path=None):
        self.cleaner = DataCleaner()
        self.encoder = Encoder()
        self.scaler = FeatureScaler()
        self.scaler_path = scaler_path
        self.encoder_path = encoder_path

        # Lazy load encoder/scaler if they exist on disk
        if encoder_path and os.path.exists(encoder_path):
            self.encoder.load(encoder_path)
        if scaler_path and os.path.exists(scaler_path):
            self.scaler.load(scaler_path)

    def preprocess_df(self, df, training=False):
        """
        Cleans, engineers features, and scales/encodes a DataFrame.
        """
        df = df.copy()

        # 1. Data Cleaning
        df = self.cleaner.clean(df)

        # 2. Feature Engineering
        # Altitude bands
        if "orbital_altitude" in df.columns:
            df = FeatureEngineering.altitude_band(df, "orbital_altitude")
        elif "altitude" in df.columns:
            df = FeatureEngineering.altitude_band(df, "altitude")
        elif "average_altitude" in df.columns:
            df = FeatureEngineering.altitude_band(df, "average_altitude")

        # Congestion index
        if "debris_density" in df.columns and "orbital_congestion" in df.columns:
            df = FeatureEngineering.congestion_index(df)

        # Velocity normalization
        if "velocity" in df.columns:
            df = FeatureEngineering.normalize_velocity(df, "velocity")
        elif "relative_velocity" in df.columns:
            df = FeatureEngineering.normalize_velocity(df, "relative_velocity")
        elif "orbital_velocity" in df.columns:
            df = FeatureEngineering.normalize_velocity(df, "orbital_velocity")

        # 3. Scaling Numeric Columns
        target_cols = {"collision", "anomaly", "hotspot", "disaster", "risk_level", "congestion_level", "risk", "status", "congestion"}
        # Select numeric columns that are not class targets
        numeric_cols = [c for c in df.columns if df[c].dtype in ["float64", "int64", "float32", "int32"] and c not in target_cols]

        if len(numeric_cols) > 0:
            if training:
                # Fit and transform, then save scaler
                scaled_values = self.scaler.fit_transform(df[numeric_cols])
                if self.scaler_path:
                    os.makedirs(os.path.dirname(os.path.abspath(self.scaler_path)), exist_ok=True)
                    self.scaler.save(self.scaler_path)
            else:
                # Transform using loaded scaler
                if self.scaler_path and os.path.exists(self.scaler_path):
                    scaled_values = self.scaler.transform(df[numeric_cols])
                else:
                    # Fallback if scaler pkl doesn't exist
                    scaled_values = df[numeric_cols].values
            
            df[numeric_cols] = scaled_values

        return df

    def preprocess_sample(self, sample_df):
        """
        Preprocesses a single sample DataFrame during inference.
        """
        return self.preprocess_df(sample_df, training=False)
