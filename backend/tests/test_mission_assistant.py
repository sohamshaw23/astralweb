import pytest
from ml.transformer.mission_assistant import MissionAssistant

def test_mission_assistant_initialization():
    """Verify that MissionAssistant instantiates and handles fallback modes gracefully."""
    assistant = MissionAssistant()
    # It should have a fallback state or loaded pipeline
    assert hasattr(assistant, "use_fallback")

def test_mission_assistant_chat_routing():
    """Verify that MissionAssistant's chat method routes queries based on pattern matching."""
    assistant = MissionAssistant()

    # 1. Satellite constellation query
    sat_resp = assistant.chat("tell me about the satellites")
    assert "Satellite" in sat_resp or "Constellation" in sat_resp

    # 2. Specific satellite query
    specific_sat_resp = assistant.chat("give me a report on INSAT-3D")
    assert "INSAT-3D" in specific_sat_resp
    assert "Satellite Intelligence Report" in specific_sat_resp

    # 3. Disasters query
    disaster_resp = assistant.chat("what active disasters are tracked?")
    assert "Disaster" in disaster_resp or "Hotspot" in disaster_resp

    # 4. Collision query
    collision_resp = assistant.chat("is there a collision threat?")
    assert "Collision" in collision_resp or "conjunction" in collision_resp or "Congestion" in collision_resp

    # 5. Space weather query
    weather_resp = assistant.chat("what is the space weather index today?")
    assert "Space Weather" in weather_resp or "Storm" in weather_resp or "Kp" in weather_resp

    # 6. Fallback/generic query
    generic_resp = assistant.chat("Hello! Who are you?")
    assert len(generic_resp) > 0
