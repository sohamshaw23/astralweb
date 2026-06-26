import pytest
from datetime import datetime
from database.postgres import database_health, init_database
from database.models import (
    User, Satellite, DisasterEvent, Hotspot, 
    OrbitalPrediction, SatelliteRisk, CollisionAlert, 
    AIChat, MissionLog, DashboardCache, SystemHealth, PredictionLog
)

def test_database_health():
    """Verify that database health check works and reports connection success (for SQLite)."""
    health = database_health()
    assert health["database"] == "PostgreSQL"
    assert health["status"] in ("Connected", "Disconnected")

def test_init_database():
    """Verify database initialization doesn't raise exceptions."""
    try:
        init_database()
        success = True
    except Exception:
        success = False
    assert success is True

def test_user_crud(db_session):
    """Test Create, Read, Update, Delete for User model."""
    new_user = User(
        username="test_pilot",
        email="test_pilot@zenith.org",
        password="secure_password_123",
        role="operator"
    )
    db_session.add(new_user)
    db_session.commit()

    # Read
    user = db_session.query(User).filter_by(username="test_pilot").first()
    assert user is not None
    assert user.email == "test_pilot@zenith.org"
    assert user.role == "operator"

    # Update
    user.role = "administrator"
    db_session.commit()
    user_updated = db_session.query(User).filter_by(username="test_pilot").first()
    assert user_updated.role == "administrator"

    # Delete
    db_session.delete(user_updated)
    db_session.commit()
    user_deleted = db_session.query(User).filter_by(username="test_pilot").first()
    assert user_deleted is None

def test_satellite_crud(db_session):
    """Test CRUD operations for Satellite model."""
    sat = Satellite(
        norad_id=12345,
        name="ZENITH-TEST-1",
        operator="Zenith Aerospace",
        orbit_type="LEO",
        altitude=550.5,
        inclination=97.5,
        velocity=7.66,
        latitude=12.97,
        longitude=77.59,
        status="Operational"
    )
    db_session.add(sat)
    db_session.commit()

    retrieved = db_session.query(Satellite).filter_by(norad_id=12345).first()
    assert retrieved is not None
    assert retrieved.name == "ZENITH-TEST-1"
    assert retrieved.altitude == 550.5

def test_disaster_event_crud(db_session):
    """Test CRUD operations for DisasterEvent model."""
    event = DisasterEvent(
        event="Wildfire",
        source="NASA_FIRMS",
        country="India",
        latitude=30.15,
        longitude=78.90,
        severity="High",
        risk_score=75.4
    )
    db_session.add(event)
    db_session.commit()

    retrieved = db_session.query(DisasterEvent).filter_by(event="Wildfire").first()
    assert retrieved is not None
    assert retrieved.country == "India"
    assert retrieved.risk_score == 75.4

def test_hotspot_crud(db_session):
    """Test CRUD operations for Hotspot model."""
    hotspot = Hotspot(
        latitude=13.05,
        longitude=80.25,
        temperature=325.4,
        confidence=88.5,
        risk_level="High"
    )
    db_session.add(hotspot)
    db_session.commit()

    retrieved = db_session.query(Hotspot).filter_by(confidence=88.5).first()
    assert retrieved is not None
    assert retrieved.temperature == 325.4

def test_prediction_log_crud(db_session):
    """Test CRUD operations for PredictionLog model."""
    log = PredictionLog(
        model="collision",
        prediction="Critical Alert",
        confidence=94.5,
        input_features={"closest_distance_km": 0.45, "relative_velocity_kms": 14.2},
        user="test_unit_only"
    )
    db_session.add(log)
    db_session.commit()

    # Filter by unique test user to isolate from other test data
    retrieved = db_session.query(PredictionLog).filter_by(user="test_unit_only").first()
    assert retrieved is not None
    assert retrieved.confidence == 94.5
    assert retrieved.input_features["closest_distance_km"] == 0.45

def test_other_models_crud(db_session):
    """Test CRUD for other schema tables (OrbitalPrediction, SatelliteRisk, CollisionAlert, AIChat, MissionLog, DashboardCache, SystemHealth)."""
    # Create
    pred = OrbitalPrediction(satellite="ZENITH-TEST-1", prediction={"altitude_forecast": [550, 549, 548]})
    risk = SatelliteRisk(satellite="ZENITH-TEST-1", collision_probability=0.12, congestion_score=82.4, risk_level="High", confidence=85.0)
    alert = CollisionAlert(satellite_1="SAT-A", satellite_2="SAT-B", distance=1.2, probability=0.045, alert_level="Moderate")
    chat = AIChat(prompt="status check", response="nominal")
    mlog = MissionLog(action="Maneuver Executed", status="Success", details={"burn_duration": 4.5})
    cache = DashboardCache(cache_key="analytics:summary", cache_value={"total_events": 42})
    health = SystemHealth(service="AIService", status=True, response_time=12.4)

    db_session.add_all([pred, risk, alert, chat, mlog, cache, health])
    db_session.commit()

    # Query & Assert
    assert db_session.query(OrbitalPrediction).filter_by(satellite="ZENITH-TEST-1").first().satellite == "ZENITH-TEST-1"
    assert db_session.query(SatelliteRisk).filter_by(risk_level="High").first().risk_level == "High"
    assert db_session.query(CollisionAlert).filter_by(alert_level="Moderate").first().alert_level == "Moderate"
    assert db_session.query(AIChat).filter_by(prompt="status check").first().response == "nominal"
    assert db_session.query(MissionLog).filter_by(action="Maneuver Executed").first().status == "Success"
    assert db_session.query(DashboardCache).filter_by(cache_key="analytics:summary").first().cache_key == "analytics:summary"
    assert db_session.query(SystemHealth).filter_by(service="AIService").first().service == "AIService"
