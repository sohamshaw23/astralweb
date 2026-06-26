import pandas as pd

class CongestionAnalysis:

    @staticmethod
    def orbital_density(df):

        density = (
            df.groupby("orbital_plane")
              .size()
              .reset_index(name="satellite_count")
        )

        return density.to_dict(orient="records")

