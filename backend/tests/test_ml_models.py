import pytest
import pandas as pd
from ml.model_manager import model_manager

def test_model_manager_initialization():
    """Verify that ModelManager loads paths correctly."""
    assert model_manager._initialized is True
    assert "collision" in model_manager._paths
    assert "anomaly" in model_manager._paths
    assert "hotspot" in model_manager._paths
    assert "disaster" in model_manager._paths
    assert "satellite_risk" in model_manager._paths
    assert "congestion" in model_manager._paths

def test_collision_model_loading_and_prediction():
    """Test loading and making a prediction with the Collision model."""
    model = model_manager.get_collision_model()
    assert model is not None

    # Use the correct 10 feature columns that the collision model was trained on
    features = pd.DataFrame([{
        "relative_velocity": 12.5,
        "closest_distance": 1.2,
        "orbital_altitude": 550.0,
        "inclination": 98.2,
        "eccentricity": 0.001,
        "orbital_congestion": 75.0,
        "debris_density": 80.0,
        "solar_kp_index": 4.0,
        "satellite_age": 5.0,
        "cross_section": 6.2
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (0, 1, 2, 3)  # low, moderate, high, critical

def test_anomaly_model_loading_and_prediction():
    """Test loading and making a prediction with the Anomaly (Isolation Forest) model."""
    model = model_manager.get_anomaly_model()
    assert model is not None
    
    features = pd.DataFrame([{
        "velocity": 7.67,
        "altitude": 550.0,
        "inclination": 97.5,
        "eccentricity": 0.001,
        "orbital_period": 95.0,
        "mean_motion": 15.1,
        "trajectory_deviation": 0.05,
        "debris_density": 50.0,
        "solar_activity": 2.0,
        "orbital_congestion": 45.0
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (1, -1)  # 1 = normal, -1 = anomaly

def test_hotspot_model_loading_and_prediction():
    """Test loading and making a prediction with the Hotspot model."""
    model = model_manager.get_hotspot_model()
    assert model is not None
    
    features = pd.DataFrame([{
        "temperature": 320.0,
        "humidity": 30.0,
        "wind_speed": 15.0,
        "rainfall": 0.0,
        "vegetation_index": 0.25,
        "thermal_anomaly": 75.0,
        "population_density": 500.0,
        "elevation": 150.0,
        "soil_moisture": 10.0,
        "historical_frequency": 5.0
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (0, 1, 2, 3)

def test_disaster_model_loading_and_prediction():
    """Test loading and making a prediction with the Disaster model."""
    model = model_manager.get_disaster_model()
    assert model is not None
    
    features = pd.DataFrame([{
        "temperature": 38.0,
        "humidity": 25.0,
        "wind_speed": 12.0,
        "rainfall": 1.0,
        "pressure": 1008.0,
        "soil_moisture": 12.0,
        "vegetation_index": 0.35,
        "thermal_anomaly": 80.0,
        "population_density": 600.0,
        "elevation": 100.0
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (0, 1, 2, 3)

def test_satellite_risk_model_loading_and_prediction():
    """Test loading and making a prediction with the Satellite Risk model."""
    model = model_manager.get_satellite_risk_model()
    assert model is not None
    
    features = pd.DataFrame([{
        "collision_probability": 0.05,
        "orbital_altitude": 550.0,
        "orbital_velocity": 7.66,
        "orbital_congestion": 85.0,
        "debris_density": 65.0,
        "solar_activity": 3.0,
        "satellite_age": 5.0,
        "fuel_remaining": 75.0,
        "communication_health": 95.0,
        "battery_health": 98.0
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (0, 1, 2, 3)

def test_congestion_model_loading_and_prediction():
    """Test loading and making a prediction with the Congestion model."""
    model = model_manager.get_congestion_model()
    assert model is not None
    
    features = pd.DataFrame([{
        "active_satellites": 3500,
        "inactive_satellites": 1500,
        "debris_objects": 10000,
        "average_altitude": 600.0,
        "orbital_velocity": 7.5,
        "launch_frequency": 25.0,
        "collision_alerts": 5,
        "solar_activity": 4.0,
        "orbital_region": 1,  # LEO
        "traffic_density": 450.0
    }])
    pred = model.predict(features)
    assert len(pred) == 1
    assert pred[0] in (0, 1, 2, 3)
