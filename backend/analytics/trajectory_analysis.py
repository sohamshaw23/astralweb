import numpy as np

class TrajectoryAnalysis:

    @staticmethod
    def predict_path(position, velocity):

        future_position = position + velocity * 60

        return {
            "current": position.tolist(),
            "predicted": future_position.tolist()
        }

