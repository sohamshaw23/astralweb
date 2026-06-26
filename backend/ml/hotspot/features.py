"""
Project Zenith
Hotspot Feature Engineering
"""

import pandas as pd

FEATURE_COLUMNS = [

    "temperature",

    "humidity",

    "wind_speed",

    "rainfall",

    "vegetation_index",

    "thermal_anomaly",

    "population_density",

    "elevation",

    "soil_moisture",

    "historical_frequency"

]


class HotspotFeatures:

    def __init__(self):
        pass

    # --------------------------------------
    # Transform Dataset
    # --------------------------------------

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna(0, inplace=True)

        return dataframe[FEATURE_COLUMNS]

    # --------------------------------------
    # Single Sample
    # --------------------------------------

    def build(

        self,

        temperature,

        humidity,

        wind_speed,

        rainfall,

        vegetation_index,

        thermal_anomaly,

        population_density,

        elevation,

        soil_moisture,

        historical_frequency

    ):

        return pd.DataFrame([{

            "temperature": temperature,

            "humidity": humidity,

            "wind_speed": wind_speed,

            "rainfall": rainfall,

            "vegetation_index": vegetation_index,

            "thermal_anomaly": thermal_anomaly,

            "population_density": population_density,

            "elevation": elevation,

            "soil_moisture": soil_moisture,

            "historical_frequency": historical_frequency

        }])
