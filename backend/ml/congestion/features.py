"""
Project Zenith
Orbital Congestion Feature Engineering
"""

import pandas as pd

FEATURE_COLUMNS = [

    "active_satellites",

    "inactive_satellites",

    "debris_objects",

    "average_altitude",

    "orbital_velocity",

    "launch_frequency",

    "collision_alerts",

    "solar_activity",

    "orbital_region",

    "traffic_density"

]


class CongestionFeatures:

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna(0, inplace=True)

        return dataframe[FEATURE_COLUMNS]

    def build(

        self,

        active_satellites,

        inactive_satellites,

        debris_objects,

        average_altitude,

        orbital_velocity,

        launch_frequency,

        collision_alerts,

        solar_activity,

        orbital_region,

        traffic_density

    ):

        return pd.DataFrame([{

            "active_satellites": active_satellites,

            "inactive_satellites": inactive_satellites,

            "debris_objects": debris_objects,

            "average_altitude": average_altitude,

            "orbital_velocity": orbital_velocity,

            "launch_frequency": launch_frequency,

            "collision_alerts": collision_alerts,

            "solar_activity": solar_activity,

            "orbital_region": orbital_region,

            "traffic_density": traffic_density

        }])
