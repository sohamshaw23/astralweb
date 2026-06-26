"""
services/cache_service.py

Project Zenith
Caching Service
"""

from datetime import datetime, timedelta


class CacheService:

    def __init__(self):

        self.cache = {}

        self.expiry = {}

    # -----------------------------------------
    # Store
    # -----------------------------------------

    def set(

        self,

        key,

        value,

        ttl=300

    ):

        self.cache[key] = value

        self.expiry[key] = (

            datetime.utcnow()

            +

            timedelta(seconds=ttl)

        )

    # -----------------------------------------
    # Retrieve
    # -----------------------------------------

    def get(

        self,

        key

    ):

        if key not in self.cache:

            return None

        if datetime.utcnow() > self.expiry[key]:

            self.delete(key)

            return None

        return self.cache[key]

    # -----------------------------------------
    # Exists
    # -----------------------------------------

    def exists(

        self,

        key

    ):

        return self.get(key) is not None

    # -----------------------------------------
    # Delete
    # -----------------------------------------

    def delete(

        self,

        key

    ):

        self.cache.pop(key, None)

        self.expiry.pop(key, None)

    # -----------------------------------------
    # Clear
    # -----------------------------------------

    def clear(self):

        self.cache.clear()

        self.expiry.clear()

    # -----------------------------------------
    # Cache Size
    # -----------------------------------------

    def size(self):

        return len(self.cache)

    # -----------------------------------------
    # Statistics
    # -----------------------------------------

    def statistics(self):

        return {

            "cached_items":

                len(self.cache),

            "service":

                "In-Memory Cache",

            "status":

                "Running"

        }

    # -----------------------------------------
    # Dashboard
    # -----------------------------------------

    def dashboard(self):

        return {

            "cache_size":

                self.size(),

            "status":

                "Healthy",

            "generated":

                datetime.utcnow().isoformat()

        }


# Singleton Instance
cache = CacheService()
