"""
Project Zenith
Disaster Feature Engineering
"""

import pandas as pd

FEATURE_COLUMNS = [

    "temperature",

    "humidity",

    "wind_speed",

    "rainfall",

    "pressure",

    "soil_moisture",

    "vegetation_index",

    "thermal_anomaly",

    "population_density",

    "elevation"

]


class DisasterFeatures:

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna(0, inplace=True)

        return dataframe[FEATURE_COLUMNS]

    def build(

        self,

        temperature,

        humidity,

        wind_speed,

        rainfall,

        pressure,

        soil_moisture,

        vegetation_index,

        thermal_anomaly,

        population_density,

        elevation

    ):

        return pd.DataFrame([{

            "temperature": temperature,

            "humidity": humidity,

            "wind_speed": wind_speed,

            "rainfall": rainfall,

            "pressure": pressure,

            "soil_moisture": soil_moisture,

            "vegetation_index": vegetation_index,

            "thermal_anomaly": thermal_anomaly,

            "population_density": population_density,

            "elevation": elevation

        }])
