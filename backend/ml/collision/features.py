"""
Project Zenith
Collision Feature Engineering
"""

import pandas as pd
import numpy as np


FEATURE_COLUMNS = [

    "relative_velocity",

    "closest_distance",

    "orbital_altitude",

    "inclination",

    "eccentricity",

    "orbital_congestion",

    "debris_density",

    "solar_kp_index",

    "satellite_age",

    "cross_section"

]


class CollisionFeatures:

    def __init__(self):

        pass

    # ------------------------------------
    # DataFrame -> Feature Matrix
    # ------------------------------------

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe = dataframe.fillna(0)

        return dataframe[FEATURE_COLUMNS]

    # ------------------------------------
    # Single Sample
    # ------------------------------------

    def build(

        self,

        relative_velocity,

        closest_distance,

        orbital_altitude,

        inclination,

        eccentricity,

        orbital_congestion,

        debris_density,

        solar_kp_index,

        satellite_age,

        cross_section

    ):

        return pd.DataFrame([{

            "relative_velocity":

                relative_velocity,

            "closest_distance":

                closest_distance,

            "orbital_altitude":

                orbital_altitude,

            "inclination":

                inclination,

            "eccentricity":

                eccentricity,

            "orbital_congestion":

                orbital_congestion,

            "debris_density":

                debris_density,

            "solar_kp_index":

                solar_kp_index,

            "satellite_age":

                satellite_age,

            "cross_section":

                cross_section

        }])
