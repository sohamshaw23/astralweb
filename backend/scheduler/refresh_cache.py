"""
scheduler/refresh_cache.py
"""

from services.cache_service import cache
from services.analytics_service import AnalyticsService

analytics = AnalyticsService()


def refresh():

    cache.clear()

    cache.set(

        "dashboard",

        analytics.dashboard(),

        ttl=600

    )

    cache.set(

        "mission",

        analytics.mission_control(),

        ttl=600

    )

    print("Cache refreshed.")


if __name__ == "__main__":

    refresh()
