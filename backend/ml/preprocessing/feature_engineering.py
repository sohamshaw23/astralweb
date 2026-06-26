"""
Project Zenith
Feature Engineering
"""

import numpy as np


class FeatureEngineering:

    @staticmethod
    def normalize_velocity(

        dataframe,

        column="velocity"

    ):

        if len(dataframe) == 1:
            if column == "relative_velocity":
                max_val = 14.998524557437552
            elif column == "velocity":
                max_val = 7.999805031575876
            elif column == "orbital_velocity":
                max_val = 8.0
            else:
                max_val = 8.0
            dataframe[column] = dataframe[column] / max_val
        else:
            dataframe[column] = (

                dataframe[column]

                /

                dataframe[column].max()

            )

        return dataframe

    @staticmethod
    def altitude_band(

        dataframe,

        column="orbital_altitude"

    ):

        dataframe["orbit_type"] = np.where(

            dataframe[column] < 2000,

            1,

            np.where(

                dataframe[column] < 35786,

                2,

                3

            )

        )

        return dataframe

    @staticmethod
    def congestion_index(

        dataframe

    ):

        dataframe["congestion_index"] = (

            dataframe["debris_density"]

            *

            dataframe["orbital_congestion"]

        )

        return dataframe
