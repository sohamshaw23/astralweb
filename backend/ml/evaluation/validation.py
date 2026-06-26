"""
Project Zenith
Model Validation
"""

from sklearn.model_selection import cross_val_score


class ModelValidator:

    @staticmethod
    def validate(

        model,

        X,

        y,

        folds=5

    ):

        scores = cross_val_score(

            model,

            X,

            y,

            cv=folds,

            scoring="accuracy"

        )

        return {

            "scores":

                scores.tolist(),

            "mean":

                scores.mean(),

            "std":

                scores.std()

        }