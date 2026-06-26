"""
Project Zenith
Evaluation Metrics
"""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


class Metrics:

    @staticmethod
    def classification(y_true, y_pred):

        return {

            "accuracy":

                round(

                    accuracy_score(

                        y_true,

                        y_pred

                    ),

                    4

                ),

            "precision":

                round(

                    precision_score(

                        y_true,

                        y_pred,

                        average="weighted",

                        zero_division=0

                    ),

                    4

                ),

            "recall":

                round(

                    recall_score(

                        y_true,

                        y_pred,

                        average="weighted",

                        zero_division=0

                    ),

                    4

                ),

            "f1_score":

                round(

                    f1_score(

                        y_true,

                        y_pred,

                        average="weighted"

                    ),

                    4

                )

        }

    @staticmethod
    def auc(y_true, probabilities):

        return round(

            roc_auc_score(

                y_true,

                probabilities

            ),

            4

        )
