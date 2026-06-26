"""
Project Zenith
Dataset Loader
"""

import pandas as pd


class DatasetLoader:

    @staticmethod
    def load_csv(path):

        return pd.read_csv(path)

    @staticmethod
    def save_csv(dataframe, path):

        dataframe.to_csv(

            path,

            index=False

        )

    @staticmethod
    def info(dataframe):

        return {

            "rows": dataframe.shape[0],

            "columns": dataframe.shape[1],

            "features": dataframe.columns.tolist()

        }