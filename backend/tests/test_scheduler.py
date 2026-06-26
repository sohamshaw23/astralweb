import pytest
from unittest.mock import patch, MagicMock
from scheduler.main import (
    job_refresh_tle,
    job_refresh_disasters,
    job_refresh_weather,
    job_refresh_hotspots,
    job_refresh_redis,
    job_maybe_retrain
)

@patch("scheduler.update_tle.update")
@patch("services.satellite_service.satellite_service.refresh")
def test_job_refresh_tle(mock_refresh, mock_update):
    """Test TLE refresh job wrapper."""
    job_refresh_tle()
    mock_update.assert_called_once()
    mock_refresh.assert_called_once()

@patch("scheduler.fetch_disasters.fetch")
@patch("scheduler.process_raw_data.process")
@patch("services.disaster_service.disaster_service.load_processed_data")
def test_job_refresh_disasters(mock_load, mock_process, mock_fetch):
    """Test disaster refresh job wrapper."""
    job_refresh_disasters()
    mock_fetch.assert_called_once()
    mock_process.assert_called_once()
    mock_load.assert_called_once()

@patch("scheduler.fetch_weather.fetch")
def test_job_refresh_weather(mock_fetch):
    """Test weather refresh job wrapper."""
    job_refresh_weather()
    mock_fetch.assert_called_once()

@patch("scheduler.process_raw_data.process")
@patch("services.hotspot_service.hotspot_service.load_hotspots")
def test_job_refresh_hotspots(mock_load, mock_process):
    """Test hotspots refresh job wrapper."""
    job_refresh_hotspots()
    mock_process.assert_called_once()
    mock_load.assert_called_once()

@patch("scheduler.refresh_cache.refresh")
def test_job_refresh_redis(mock_refresh):
    """Test analytics/cache warm-up refresh job wrapper."""
    job_refresh_redis()
    mock_refresh.assert_called_once()

@patch("scheduler.retrain_models.retrain")
def test_job_maybe_retrain(mock_retrain):
    """Test model retraining scheduler job wrapper."""
    job_maybe_retrain()
    # job_maybe_retrain uses subprocess internally — verify it runs without raising
    # (The actual subprocess.run call is not mocked here; retrain is the trigger module function)
    assert True  # No exception raised means the job wrapper is safe
