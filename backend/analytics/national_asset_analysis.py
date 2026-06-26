
class NationalAssetAnalysis:

    @staticmethod
    def analyse(satellites):

        assets = []

        for sat in satellites:

            if sat["country"] == "India":

                assets.append({
                    "name": sat["name"],
                    "purpose": sat["purpose"],
                    "status": "Operational"
                })

        return assets

