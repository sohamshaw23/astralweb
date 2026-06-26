"""
Project Zenith
Satellite Risk Feature Engineering

Author: Team Zenith
"""

import pandas as pd


FEATURE_COLUMNS = [

    "collision_probability",

    "orbital_altitude",

    "orbital_velocity",

    "orbital_congestion",

    "debris_density",

    "solar_activity",

    "satellite_age",

    "fuel_remaining",

    "communication_health",

    "battery_health"

]


class SatelliteRiskFeatures:

    def __init__(self):
        pass

    # --------------------------------------------------
    # DataFrame -> Feature Matrix
    # --------------------------------------------------

    def transform(self, dataframe):

        dataframe = dataframe.copy()

        dataframe.fillna(0, inplace=True)

        return dataframe[FEATURE_COLUMNS]

    # --------------------------------------------------
    # Single Prediction Sample
    # --------------------------------------------------

    def build(

        self,

        collision_probability,

        orbital_altitude,

        orbital_velocity,

        orbital_congestion,

        debris_density,

        solar_activity,

        satellite_age,

        fuel_remaining,

        communication_health,

        battery_health

    ):

        return pd.DataFrame([{

            "collision_probability":

                collision_probability,

            "orbital_altitude":

                orbital_altitude,

            "orbital_velocity":

                orbital_velocity,

            "orbital_congestion":

                orbital_congestion,

            "debris_density":

                debris_density,

            "solar_activity":

                solar_activity,

            "satellite_age":

                satellite_age,

            "fuel_remaining":

                fuel_remaining,

            "communication_health":

                communication_health,

            "battery_health":

                battery_health

        }])

    # --------------------------------------------------
    # Feature Names
    # --------------------------------------------------

    def feature_names(self):

        return FEATURE_COLUMNS

    # --------------------------------------------------
    # Validate Dataset
    # --------------------------------------------------

    def validate(self, dataframe):

        missing = []

        for column in FEATURE_COLUMNS:

            if column not in dataframe.columns:

                missing.append(column)

        if len(missing) > 0:

            raise ValueError(

                f"Missing Columns: {missing}"

            )

        return True

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self, dataframe):

        self.validate(dataframe)

        return dataframe[FEATURE_COLUMNS].describe()

    # --------------------------------------------------
    # Normalize Features (Optional)
    # --------------------------------------------------

    def normalize(self, dataframe):

        dataframe = dataframe.copy()

        for column in FEATURE_COLUMNS:

            maximum = dataframe[column].max()

            minimum = dataframe[column].min()

            if maximum != minimum:

                dataframe[column] = (

                    dataframe[column] - minimum

                ) / (

                    maximum - minimum

                )

        return dataframe


if __name__ == "__main__":

    feature_engine = SatelliteRiskFeatures()

    print(

        feature_engine.feature_names()

    )