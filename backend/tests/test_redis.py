import pytest
import time
from database.redis_cache import CacheManager

@pytest.fixture
def clean_cache():
    """Returns a fresh instance of CacheManager with a cleared in-memory cache."""
    manager = CacheManager()
    manager._in_memory_cache.clear()
    return manager

def test_cache_set_and_get(clean_cache):
    """Test standard setting and getting values."""
    assert clean_cache.get("key1") is None

    clean_cache.set("key1", {"name": "INSAT-3D", "orbit": "GEO"})
    value = clean_cache.get("key1")
    assert value is not None
    assert value["name"] == "INSAT-3D"
    assert value["orbit"] == "GEO"

def test_cache_expiry(clean_cache):
    """Test that keys expire correctly."""
    clean_cache.set("key_short", "temporary_value", ex=1)
    assert clean_cache.get("key_short") == "temporary_value"

    time.sleep(1.1)
    assert clean_cache.get("key_short") is None

def test_param_based_caching(clean_cache):
    """Test caching based on query parameters with hashing."""
    category = "satellite_visibility"
    params = {"lat": 12.97, "lon": 77.59, "altitude": 550}
    data = {"visible": True, "pass_time": "2026-06-26T18:00:00Z"}

    assert clean_cache.get_cached(category, params) is None

    clean_cache.set_cached(category, params, data, ttl_seconds=10)

    cached_data = clean_cache.get_cached(category, params)
    assert cached_data is not None
    assert cached_data["visible"] is True
    assert cached_data["pass_time"] == "2026-06-26T18:00:00Z"

    # Hash is stable across param ordering
    reordered_params = {"lon": 77.59, "altitude": 550, "lat": 12.97}
    assert clean_cache.get_cached(category, reordered_params) == data

def test_tle_caching(clean_cache):
    """Test helper functions for TLE caching."""
    sat_id = 99999
    tle_lines = [
        "ZENITH-TEST",
        "1 99999U 26001A   26177.50000000  .00000000  00000-0  00000-0 0    01",
        "2 99999  97.5000  77.5000 0001000  90.0000 270.0000 15.10000000    05"
    ]

    assert clean_cache.get_tle(sat_id) is None
    clean_cache.set_tle(sat_id, tle_lines)
    assert clean_cache.get_tle(sat_id) == tle_lines

def test_cache_health(clean_cache):
    """Test health report of CacheManager."""
    health = clean_cache.health()
    assert "cache" in health
    assert "status" in health
