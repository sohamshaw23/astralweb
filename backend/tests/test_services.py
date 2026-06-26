import pytest
from unittest.mock import MagicMock, patch

from services.satellite_service import SatelliteService
from services.celestial_service import CelestialService
from services.orbit_service import OrbitService
from services.disaster_service import DisasterService
from services.cache_service import CacheService
from services.hotspot_service import HotspotService
from services.collision_service import CollisionService
from services.analytics_service import AnalyticsService
from services.ai_service import AIService

@pytest.fixture
def mock_tle_response():
    """Mock TLE response from Celestrak."""
    return (
        "ISS (ZARYA)\n"
        "1 25544U 98067A   26177.56133177  .00014798  00000-0  26475-3 0  9993\n"
        "2 25544  51.6416 195.1274 0005118  92.0315  57.1264 15.49815340574345\n"
    )

@patch("requests.get")
def test_satellite_service(mock_get, mock_tle_response):
    """Test SatelliteService methods with mocked HTTP response."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = mock_tle_response
    mock_get.return_value = mock_resp

    service = SatelliteService()
    service.refresh()

    # Verify count
    assert service.count() > 0

    # Use search() which does partial-name matching ("ISS" matches "ISS (ZARYA)")
    results = service.search("ISS")
    assert len(results) > 0
    assert "ISS" in results[0]["name"]

    # Test position using the full TLE name
    pos = service.position("ISS (ZARYA)")
    assert pos is not None
    assert "latitude" in pos
    assert "longitude" in pos
    assert "altitude_km" in pos

    # Test nearby returns a list
    nearby = service.nearby(0.0, 0.0)
    assert isinstance(nearby, list)

def test_celestial_service():
    """Test CelestialService positioning of solar system bodies."""
    service = CelestialService()
    planets = service.planets(latitude=12.97, longitude=77.59)
    assert len(planets) > 0
    assert any(p["name"] == "Sun" for p in planets)

def test_orbit_service():
    """Test OrbitService computations initialization."""
    service = OrbitService()
    assert service.anomaly_features is not None

def test_disaster_service():
    """Test DisasterService loading data and risk score lookups."""
    service = DisasterService()
    service.load_processed_data()
    
    assert service.count() >= 0
    assert isinstance(service.average_risk(), float)
    assert isinstance(service.highest_risk(), dict)

def test_hotspot_service():
    """Test HotspotService loader and risk assessments."""
    service = HotspotService()
    service.load_hotspots()
    
    assert service.count() >= 0
    assert isinstance(service.average_risk(), float)
    assert isinstance(service.highest_risk(), dict)

def test_collision_service(app):
    """Test CollisionService conjunction alerts under app context."""
    with app.test_request_context("/"):
        service = CollisionService()
        resp = service.alerts()
        assert resp.status_code == 200
        assert b"STARLINK-4021" in resp.data

def test_analytics_service():
    """Test AnalyticsService dashboard compilation."""
    service = AnalyticsService()
    dash = service.dashboard()
    assert isinstance(dash, dict)
    assert "total_satellites" in dash

def test_ai_service():
    """Test AIService integrations."""
    with patch("ml.transformer.mission_assistant.MissionAssistant.chat") as mock_chat:
        mock_chat.return_value = "Mocked AI Response"
        service = AIService()
        
        r = service.chat("hello satellite status")
        assert r["response"] == "Mocked AI Response"
        
        sw = service.space_weather()
        assert "solar_activity" in sw
        
        dis = service.disaster_analysis(12.97, 77.59)
        assert "location" in dis
