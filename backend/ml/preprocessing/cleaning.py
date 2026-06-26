"""
Project Zenith
Data Cleaning
"""

import pandas as pd


class DataCleaner:

    @staticmethod
    def remove_duplicates(dataframe):

        return dataframe.drop_duplicates()

    @staticmethod
    def remove_nulls(dataframe):

        return dataframe.dropna()

    @staticmethod
    def fill_missing(dataframe):

        return dataframe.fillna(

            dataframe.median(

                numeric_only=True

            )

        )

    @staticmethod
    def clean(dataframe):

        dataframe = DataCleaner.remove_duplicates(

            dataframe

        )

        dataframe = DataCleaner.fill_missing(

            dataframe

        )

        return dataframe