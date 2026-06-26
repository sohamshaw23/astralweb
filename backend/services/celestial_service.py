"""
services/celestial_service.py

Project Zenith
Celestial Intelligence Service
"""

from skyfield.api import load, Topos
from datetime import datetime

ts = load.timescale()
eph = load("de421.bsp")

earth = eph["earth"]

PLANETS = {

    "Sun": eph["sun"],
    "Moon": eph["moon"],
    "Mercury": eph["mercury"],
    "Venus": eph["venus"],
    "Mars": eph["mars"],
    "Jupiter": eph["jupiter barycenter"],
    "Saturn": eph["saturn barycenter"]

}


class CelestialService:

    def __init__(self):

        self.ts = ts

        self.eph = eph

    # -------------------------------------
    # Observer
    # -------------------------------------

    def observer(self, latitude, longitude):

        return earth + Topos(

            latitude_degrees=latitude,

            longitude_degrees=longitude

        )

    # -------------------------------------
    # Planet Positions
    # -------------------------------------

    def planets(self, latitude, longitude):

        observer = self.observer(

            latitude,

            longitude

        )

        t = self.ts.now()

        data = []

        for name, body in PLANETS.items():

            alt, az, distance = (

                observer.at(t)

                .observe(body)

                .apparent()

                .altaz()

            )

            data.append({

                "name": name,

                "altitude":

                    round(

                        alt.degrees,

                        2

                    ),

                "azimuth":

                    round(

                        az.degrees,

                        2

                    ),

                "distance_km":

                    round(

                        distance.km

                    )

            })

        return data

    # -------------------------------------
    # Visible Objects
    # -------------------------------------

    def visible(self, latitude, longitude):

        planets = self.planets(

            latitude,

            longitude

        )

        return [

            p

            for p in planets

            if p["altitude"] > 0

        ]

    # -------------------------------------
    # Moon Phase
    # -------------------------------------

    def moon_phase(self):

        return {

            "phase":"Waxing Gibbous",

            "illumination":"72%"

        }

    # -------------------------------------
    # Sunrise / Sunset
    # -------------------------------------

    def daylight(self,

                 latitude,

                 longitude):

        return {

            "sunrise":"05:34",

            "sunset":"18:28",

            "civil_twilight":"05:10"

        }

    # -------------------------------------
    # Constellations
    # -------------------------------------

    def constellations(self):

        return [

            "Orion",

            "Cassiopeia",

            "Ursa Major",

            "Scorpius",

            "Leo",

            "Cygnus",

            "Taurus",

            "Pegasus"

        ]

    # -------------------------------------
    # Bright Stars
    # -------------------------------------

    def stars(self):

        return [

            "Sirius",

            "Betelgeuse",

            "Rigel",

            "Polaris",

            "Vega",

            "Altair",

            "Deneb"

        ]

    # -------------------------------------
    # Zenith Object
    # -------------------------------------

    def zenith(self,

               latitude,

               longitude):

        return {

            "planet":"Venus",

            "constellation":"Orion",

            "visibility":"Excellent"

        }

    # -------------------------------------
    # Sky Quality
    # -------------------------------------

    def sky_quality(self):

        return {

            "cloud_cover":12,

            "light_pollution":"Low",

            "visibility":"Excellent"

        }

    # -------------------------------------
    # Dashboard
    # -------------------------------------

    def dashboard(self):

        return {

            "visible_planets":5,

            "visible_constellations":8,

            "moon_phase":"Waxing Gibbous",

            "sky_quality":"Excellent",

            "generated":

                datetime.utcnow().isoformat()

        }

    # -------------------------------------
    # Astronomy Events
    # -------------------------------------

    def upcoming_events(self):

        return [

            {

                "event":"ISS Flyover",

                "date":"2026-06-27"

            },

            {

                "event":"Meteor Shower",

                "date":"2026-07-14"

            },

            {

                "event":"Full Moon",

                "date":"2026-07-10"

            }

        ]

    # -------------------------------------
    # Celestial Summary
    # -------------------------------------

    def summary(self,

                latitude,

                longitude):

        return {

            "visible":

                len(

                    self.visible(

                        latitude,

                        longitude

                    )

                ),

            "moon":

                self.moon_phase(),

            "quality":

                self.sky_quality(),

            "events":

                self.upcoming_events()

        }
