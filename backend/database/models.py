"""
Project Zenith
Database Models
"""

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    Text,
    JSON
)

from database.postgres import Base


# =====================================================
# Users
# =====================================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(100), unique=True)

    email = Column(String(150), unique=True)

    password = Column(String(255))

    role = Column(String(50), default="user")

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Satellites
# =====================================================

class Satellite(Base):

    __tablename__ = "satellites"

    id = Column(Integer, primary_key=True)

    norad_id = Column(Integer)

    name = Column(String(200))

    operator = Column(String(100))

    orbit_type = Column(String(50))

    altitude = Column(Float)

    inclination = Column(Float)

    velocity = Column(Float)

    latitude = Column(Float)

    longitude = Column(Float)

    status = Column(String(50))

    updated_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Disaster Events
# =====================================================

class DisasterEvent(Base):

    __tablename__ = "disaster_events"

    id = Column(Integer, primary_key=True)

    event = Column(String(100))

    source = Column(String(100))

    country = Column(String(100))

    latitude = Column(Float)

    longitude = Column(Float)

    severity = Column(String(50))

    risk_score = Column(Float)

    detected_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Hotspots
# =====================================================

class Hotspot(Base):

    __tablename__ = "hotspots"

    id = Column(Integer, primary_key=True)

    latitude = Column(Float)

    longitude = Column(Float)

    temperature = Column(Float)

    confidence = Column(Float)

    risk_level = Column(String(50))

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Orbital Prediction
# =====================================================

class OrbitalPrediction(Base):

    __tablename__ = "orbital_predictions"

    id = Column(Integer, primary_key=True)

    satellite = Column(String(150))

    prediction = Column(JSON)

    generated_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Satellite Risk
# =====================================================

class SatelliteRisk(Base):

    __tablename__ = "satellite_risk"

    id = Column(Integer, primary_key=True)

    satellite = Column(String(150))

    collision_probability = Column(Float)

    congestion_score = Column(Float)

    risk_level = Column(String(50))

    confidence = Column(Float)

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Collision Alerts
# =====================================================

class CollisionAlert(Base):

    __tablename__ = "collision_alerts"

    id = Column(Integer, primary_key=True)

    satellite_1 = Column(String(150))

    satellite_2 = Column(String(150))

    distance = Column(Float)

    probability = Column(Float)

    alert_level = Column(String(50))

    timestamp = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# AI Chat History
# =====================================================

class AIChat(Base):

    __tablename__ = "ai_chat"

    id = Column(Integer, primary_key=True)

    prompt = Column(Text)

    response = Column(Text)

    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Mission Logs
# =====================================================

class MissionLog(Base):

    __tablename__ = "mission_logs"

    id = Column(Integer, primary_key=True)

    action = Column(String(200))

    status = Column(String(50))

    details = Column(JSON)

    timestamp = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Dashboard Cache
# =====================================================

class DashboardCache(Base):

    __tablename__ = "dashboard_cache"

    id = Column(Integer, primary_key=True)

    cache_key = Column(String(100), unique=True)

    cache_value = Column(JSON)

    updated_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# System Health
# =====================================================

class SystemHealth(Base):

    __tablename__ = "system_health"

    id = Column(Integer, primary_key=True)

    service = Column(String(100))

    status = Column(Boolean)

    response_time = Column(Float)

    checked_at = Column(

        DateTime,

        default=datetime.utcnow

    )


# =====================================================
# Prediction Log  (unified ML audit table)
# =====================================================

class PredictionLog(Base):
    """
    Stores every ML prediction across all six models.

    Columns
    -------
    model            : which model produced this result
                       (collision / hotspot / disaster / satellite_risk /
                        congestion / anomaly)
    prediction       : primary prediction label returned to the client
    confidence       : model confidence / probability (0-100)
    timestamp        : UTC time of the prediction
    input_features   : full JSON snapshot of the raw input parameters
    user             : username or IP of the requesting user (nullable)
    mission_log_id   : optional FK to mission_logs.id for cross-reference
    """

    __tablename__ = "prediction_logs"

    id             = Column(Integer,  primary_key=True)
    model          = Column(String(50),  nullable=False, index=True)
    prediction     = Column(String(200), nullable=False)
    confidence     = Column(Float,       nullable=True)
    timestamp      = Column(DateTime,    default=datetime.utcnow, index=True)
    input_features = Column(JSON,        nullable=True)
    user           = Column(String(200), nullable=True)
    mission_log_id = Column(Integer,     nullable=True)   # soft ref to mission_logs.id
