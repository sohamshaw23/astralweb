import pandas as pd

class HotspotGenerator:

    @staticmethod
    def generate(events):

        df = pd.DataFrame(events)

        hotspots = (
            df.groupby(["latitude","longitude"])
              .size()
              .reset_index(name="intensity")
        )

        return hotspots.to_dict(orient="records")

