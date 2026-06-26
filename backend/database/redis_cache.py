"""
Project Zenith
Redis Cache Module

Exposes CacheManager with support for Redis connections and an in-memory fallback.
Includes automatic stale cache invalidation using timestamps for in-memory caching.
"""

import os
import json
import time
import hashlib

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)


class CacheManager:
    # Local fallback storage: maps key -> (value, expires_at)
    _in_memory_cache = {}

    def __init__(self):
        self.client = None
        if REDIS_AVAILABLE:
            try:
                self.client = redis.Redis(
                    host=REDIS_HOST,
                    port=REDIS_PORT,
                    password=REDIS_PASSWORD,
                    decode_responses=True,
                    socket_connect_timeout=2
                )
            except Exception as e:
                print(f"[CacheManager] Redis connection failed, using in-memory: {e}")

    def get(self, key):
        """Get value from cache. Invalidates local stale cache automatically."""
        if self.client:
            try:
                val = self.client.get(key)
                if val:
                    return json.loads(val)
            except Exception:
                pass
        
        # Fallback to local in-memory cache
        entry = self._in_memory_cache.get(key)
        if entry:
            val, expires_at = entry
            if expires_at is None or time.time() < expires_at:
                return val
            else:
                # Invalidate stale cache
                del self._in_memory_cache[key]
        return None

    def set(self, key, value, ex=None):
        """Set value in cache with optional TTL in seconds."""
        if self.client:
            try:
                self.client.set(key, json.dumps(value), ex=ex)
                return True
            except Exception:
                pass
        
        # Local cache fallback
        expires_at = time.time() + ex if ex is not None else None
        self._in_memory_cache[key] = (value, expires_at)
        return True

    def get_cached(self, category: str, params: dict):
        """Compute stable parameter-based hash and get matching cached result."""
        # Convert list/dict parameters to sorted JSON string to ensure hash stability
        stable_str = json.dumps(params, sort_keys=True, default=str)
        param_hash = hashlib.md5(stable_str.encode("utf-8")).hexdigest()
        key = f"cache:{category}:{param_hash}"
        return self.get(key)

    def set_cached(self, category: str, params: dict, value, ttl_seconds: int = 300):
        """Compute stable parameter-based hash and cache the result."""
        stable_str = json.dumps(params, sort_keys=True, default=str)
        param_hash = hashlib.md5(stable_str.encode("utf-8")).hexdigest()
        key = f"cache:{category}:{param_hash}"
        return self.set(key, value, ex=ttl_seconds)

    def get_tle(self, satellite_id):
        return self.get(f"tle:{satellite_id}")

    def set_tle(self, satellite_id, tle_data, ex=None):
        return self.set(f"tle:{satellite_id}", tle_data, ex=ex)

    def health(self):
        if self.client:
            try:
                self.client.ping()
                return {
                    "cache": "Redis",
                    "status": "Connected"
                }
            except Exception as e:
                return {
                    "cache": "Redis (In-Memory Fallback)",
                    "status": "Degraded",
                    "error": str(e)
                }
        return {
            "cache": "In-Memory",
            "status": "Connected"
        }


# Singleton instance
cache_manager = CacheManager()