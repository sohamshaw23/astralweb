"""
Project Zenith
Categorical Encoder
"""

import joblib

from sklearn.preprocessing import LabelEncoder


class Encoder:

    def __init__(self):

        self.encoder = LabelEncoder()

    def fit(self, column):

        return self.encoder.fit(column)

    def transform(self, column):

        return self.encoder.transform(column)

    def fit_transform(

        self,

        column

    ):

        return self.encoder.fit_transform(

            column

        )

    def inverse(

        self,

        values

    ):

        return self.encoder.inverse_transform(

            values

        )

    def save(

        self,

        path

    ):

        joblib.dump(

            self.encoder,

            path

        )

    def load(

        self,

        path

    ):

        self.encoder = joblib.load(path)