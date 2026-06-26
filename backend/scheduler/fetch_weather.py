"""
scheduler/fetch_weather.py

Downloads/updates local weather datasets for Project Zenith.
Utilizes Open-Meteo public API (no key required) with a robust mock fallback.
"""

import os
import json
import requests
from datetime import datetime, timezone

OUTPUT = "data/processed/weather.json"

# Key coordinates to track
LOCATIONS = {
    "bengaluru": {"lat": 12.9716, "lon": 77.5946, "name": "Bengaluru (ISRO HQ)"},
    "chennai": {"lat": 13.0827, "lon": 80.2707, "name": "Chennai (SDSC Shar Nearby)"},
    "new_delhi": {"lat": 28.6139, "lon": 77.2090, "name": "New Delhi (Northern Regional Centre)"}
}

def fetch():
    weather_data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "locations": {}
    }
    
    success = False
    for key, loc in LOCATIONS.items():
        try:
            # Fetch from Open-Meteo (free API)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current_weather=true"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                current = response.json().get("current_weather", {})
                weather_data["locations"][key] = {
                    "name": loc["name"],
                    "latitude": loc["lat"],
                    "longitude": loc["lon"],
                    "temperature_c": current.get("temperature"),
                    "wind_speed_kmh": current.get("windspeed"),
                    "weather_code": current.get("weathercode"),
                    "time": current.get("time"),
                    "status": "online"
                }
                success = True
        except Exception:
            pass

    # Fallback to realistic mock values if API is down / offline
    if not success or len(weather_data["locations"]) < len(LOCATIONS):
        # Determine base temperature based on time of day
        hour = datetime.utcnow().hour
        temp_delta = 5.0 if (8 <= hour <= 18) else -2.0
        
        fallback_data = {
            "bengaluru": {
                "name": "Bengaluru (ISRO HQ)",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "temperature_c": round(23.5 + temp_delta, 1),
                "wind_speed_kmh": 12.0,
                "weather_code": 3,
                "time": datetime.utcnow().isoformat(),
                "status": "fallback"
            },
            "chennai": {
                "name": "Chennai (SDSC Shar Nearby)",
                "latitude": 13.0827,
                "longitude": 80.2707,
                "temperature_c": round(29.0 + temp_delta, 1),
                "wind_speed_kmh": 16.5,
                "weather_code": 1,
                "time": datetime.utcnow().isoformat(),
                "status": "fallback"
            },
            "new_delhi": {
                "name": "New Delhi (Northern Regional Centre)",
                "latitude": 28.6139,
                "longitude": 77.2090,
                "temperature_c": round(32.0 + temp_delta, 1),
                "wind_speed_kmh": 9.0,
                "weather_code": 0,
                "time": datetime.utcnow().isoformat(),
                "status": "fallback"
            }
        }
        
        # Merge missing keys
        for key, val in fallback_data.items():
            if key not in weather_data["locations"]:
                weather_data["locations"][key] = val

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    
    with open(OUTPUT, "w") as f:
        json.dump(weather_data, f, indent=4)
        
    print(f"[{datetime.utcnow()}] Weather data updated at {OUTPUT}")

if __name__ == "__main__":
    fetch()
