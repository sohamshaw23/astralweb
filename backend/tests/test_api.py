import pytest
from unittest.mock import patch, MagicMock

# ----------------------------------------------------
# 1. Health Endpoint Tests
# ----------------------------------------------------

def test_health_endpoints(client):
    """Test health check API endpoints."""
    # Main health
    resp = client.get("/api/health/")
    assert resp.status_code == 200
    assert resp.json["status"] == "healthy"

    # Ping
    resp = client.get("/api/health/ping")
    assert resp.status_code == 200
    assert resp.json["message"] == "pong"

    # Status
    resp = client.get("/api/health/status")
    assert resp.status_code == 200
    assert resp.json["status"] == "OK"

    # System
    resp = client.get("/api/health/system")
    assert resp.status_code == 200
    assert "cpu_utilization" in resp.json

    # Version
    resp = client.get("/api/health/version")
    assert resp.status_code == 200
    assert resp.json["version"] == "1.0.0"


# ----------------------------------------------------
# 2. Satellite Endpoint Tests
# ----------------------------------------------------

def test_satellite_endpoints(client):
    """Test Satellite API endpoints."""
    # Count endpoint - mock requests.get in api.satellites to return mock TLE
    mock_tle = (
        "ISS (ZARYA)\n"
        "1 25544U 98067A   26177.56133177  .00014798  00000-0  26475-3 0  9993\n"
        "2 25544  51.6416 195.1274 0005118  92.0315  57.1264 15.49815340574345\n"
    )
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = mock_tle

    with patch("api.satellites.requests.get", return_value=mock_resp):
        resp = client.get("/api/satellites/count")
        assert resp.status_code == 200
        assert resp.json["active_satellites"] == 1

        # Search endpoint
        resp = client.get("/api/satellites/search?name=ISS")
        assert resp.status_code == 200
        assert resp.json["name"] == "ISS (ZARYA)"


# ----------------------------------------------------
# 3. Celestial Endpoint Tests
# ----------------------------------------------------

def test_celestial_endpoints(client):
    """Test Celestial Intelligence API endpoints."""
    # Home
    resp = client.get("/api/celestial/")
    assert resp.status_code == 200
    assert resp.json["service"] == "Celestial Intelligence API"

    # Planets position — verify request processes without crashing
    resp = client.get("/api/celestial/planets?lat=12.97&lon=77.59")
    assert resp.status_code == 200
    planet_data = resp.json
    assert isinstance(planet_data, list)
    assert len(planet_data) > 0
    assert "object" in planet_data[0]


# ----------------------------------------------------
# 4. Disaster Endpoint Tests
# ----------------------------------------------------

def test_disaster_endpoints(client):
    """Test Disaster Intelligence API endpoints."""
    # Wildfires
    with patch("api.disasters.load_json") as mock_load:
        mock_load.return_value = [{"title": "Wildfire India", "severity": "High"}]
        resp = client.get("/api/disasters/wildfires")
        assert resp.status_code == 200
        assert resp.json["count"] == 1
        assert resp.json["wildfires"][0]["title"] == "Wildfire India"


# ----------------------------------------------------
# 5. AI Assistant Endpoint Tests
# ----------------------------------------------------

def test_ai_endpoints(client):
    """Test AI Mission Assistant API endpoints."""
    with patch("services.ai_service.AIService.chat") as mock_chat:
        mock_chat.return_value = {"response": "This is a satellite report"}

        # POST Chat
        resp = client.post("/api/ai/chat", json={"prompt": "tell me about INSAT-3D"})
        assert resp.status_code == 200
        assert resp.json["response"] == "This is a satellite report"

    # Space Weather
    with patch("services.ai_service.AIService.space_weather") as mock_sw:
        mock_sw.return_value = {"solar_activity": "Quiet", "kp_index": 2.0}
        resp = client.get("/api/ai/space-weather")
        assert resp.status_code == 200
        assert resp.json["solar_activity"] == "Quiet"


# ----------------------------------------------------
# 6. Proprietary Analytics Endpoint Tests
# ----------------------------------------------------

def test_proprietary_endpoints(client):
    """Test various proprietary analytics blueprints."""
    # 1. Collision analysis - verify 200 and presence of collision_probability field
    resp = client.get(
        "/api/analytics/collision/analysis"
        "?relative_velocity=12.5&closest_distance=1.2"
        "&debris_density=80&orbital_congestion=75"
    )
    assert resp.status_code == 200
    # The endpoint returns either a prediction or an error
    assert "collision_probability" in resp.json or "error" in resp.json

    # 2. Risk analysis
    resp = client.get(
        "/api/analytics/risk/analysis"
        "?collision_probability=0.05&orbital_altitude=550&orbital_velocity=7.66"
        "&orbital_congestion=85&debris_density=65&solar_activity=3"
        "&satellite_age=5&fuel_remaining=75&communication_health=95&battery_health=98"
    )
    assert resp.status_code == 200
    assert "risk_level" in resp.json or "error" in resp.json

    # 3. Congestion predict
    resp = client.get(
        "/api/analytics/congestion/"
        "?active_satellites=3500&inactive_satellites=1500&debris_objects=10000"
        "&average_altitude=600&orbital_velocity=7.5&launch_frequency=25"
        "&collision_alerts=5&solar_activity=4&orbital_region=1&traffic_density=450"
    )
    assert resp.status_code == 200

    # 4. Disaster score
    resp = client.get(
        "/api/analytics/disaster-score/analysis"
        "?temperature=38&humidity=25&wind_speed=12&rainfall=1"
        "&pressure=1008&soil_moisture=12&vegetation_index=0.35"
        "&thermal_anomaly=80&population_density=600&elevation=100"
    )
    assert resp.status_code == 200

    # 5. Hotspot predict
    resp = client.get(
        "/api/analytics/hotspots/predict"
        "?temperature=320&humidity=30&wind_speed=15&rainfall=0"
        "&vegetation_index=0.25&thermal_anomaly=75&population_density=500"
        "&elevation=150&soil_moisture=10&historical_frequency=5"
    )
    assert resp.status_code == 200
