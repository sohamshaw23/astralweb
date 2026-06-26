import pandas as pd

class DisasterAnalysis:

    @staticmethod
    def severity_score(events):

        df = pd.DataFrame(events)

        score = len(df) * 10

        return {
            "events": len(df),
            "severity_score": score
        }

