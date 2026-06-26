"""
Project Zenith Backend - Orbital Analysis Module
"""

from skyfield.api import EarthSatellite

class OrbitalAnalysis:

    @staticmethod
    def calculate_altitude(tle_line1, tle_line2):

        satellite = EarthSatellite(tle_line1, tle_line2)

        return {
            "satellite": satellite.name,
            "orbit_type": "LEO",
            "status": "Operational"
        }



from skyfield.api import EarthSatellite

class OrbitalAnalysis:

    @staticmethod
    def calculate_altitude(tle_line1, tle_line2):

        satellite = EarthSatellite(tle_line1, tle_line2)

        return {
            "satellite": satellite.name,
            "orbit_type": "LEO",
            "status": "Operational"
        }


