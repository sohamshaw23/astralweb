"""
Project Zenith
Anomaly Feature Engineering
"""

import pandas as pd

FEATURE_COLUMNS = [

    "velocity",

    "altitude",

    "inclination",

    "eccentricity",

    "orbital_period",

    "mean_motion",

    "trajectory_deviation",

    "debris_density",

    "solar_activity",

    "orbital_congestion"

]


class AnomalyFeatures:

    def __init__(self):
        pass

    # ---------------------------------
    # Transform DataFrame
    # ---------------------------------

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna(0, inplace=True)

        return dataframe[FEATURE_COLUMNS]

    # ---------------------------------
    # Build Single Sample
    # ---------------------------------

    def build(

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

        return pd.DataFrame([{

            "velocity": velocity,

            "altitude": altitude,

            "inclination": inclination,

            "eccentricity": eccentricity,

            "orbital_period": orbital_period,

            "mean_motion": mean_motion,

            "trajectory_deviation": trajectory_deviation,

            "debris_density": debris_density,

            "solar_activity": solar_activity,

            "orbital_congestion": orbital_congestion

        }])
