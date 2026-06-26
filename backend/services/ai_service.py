"""
services/ai_service.py

Project Zenith
AI Mission Assistant Service - v2.0
Connected to MissionAssistant reasoning engine.
"""

from datetime import datetime
from services.analytics_service import AnalyticsService
from services.satellite_service import SatelliteService
from services.hotspot_service import HotspotService
from ml.transformer.mission_assistant import MissionAssistant


class AIService:

    def __init__(self):
        self.analytics = AnalyticsService()
        self.satellites = SatelliteService()
        self.hotspots = HotspotService()
        self.assistant = MissionAssistant()

    # ---------------------------------------------------
    # AI Chat
    # ---------------------------------------------------

    def chat(self, prompt):
        response_text = self.assistant.chat(prompt)
        return {
            "response": response_text
        }

    # ---------------------------------------------------
    # AI Insights
    # ---------------------------------------------------

    def generate_insights(self):
        dashboard = self.analytics.dashboard()
        summary_text = self.assistant.mission_summary(dashboard)

        return {
            "summary": summary_text,
            "tracked_satellites": dashboard.get("total_satellites", 0),
            "hotspots": dashboard.get("active_hotspots", {}).get("total", 0),
            "generated": datetime.utcnow().isoformat()
        }

    # ---------------------------------------------------
    # Space Weather
    # ---------------------------------------------------

    def space_weather(self):
        dashboard = self.analytics.dashboard()
        sw = dashboard.get("space_weather", {})

        return {
            "solar_activity": "High" if sw.get("kp_index", 2.0) >= 5.0 else "Quiet",
            "kp_index": sw.get("kp_index", 2.0),
            "geomagnetic_storm": sw.get("geomagnetic_storm", "Quiet"),
            "recommendation": (
                "Nominal operations."
                if sw.get("kp_index", 2.0) < 5.0
                else "Prepare safe-hold payload protocols."
            )
        }

    # ---------------------------------------------------
    # Disaster Analysis
    # ---------------------------------------------------

    def disaster_analysis(self, latitude, longitude):
        nearby = self.hotspots.nearby(
            float(latitude),
            float(longitude),
            200
        )

        severity = "High" if len(nearby) > 2 else "Moderate" if len(nearby) > 0 else "Low"
        ai_recommendation = self.assistant.disaster_analysis(
            disaster="Thermal Hotspot",
            country="Coastal Region",
            severity=severity
        )

        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "nearby_hotspots": len(nearby),
            "recommendation": ai_recommendation
        }

    # ---------------------------------------------------
    # Satellite Recommendation
    # ---------------------------------------------------

    def recommend_satellite(self, latitude, longitude):
        visible = self.satellites.nearby(
            float(latitude),
            float(longitude)
        )

        best = "EOS-06"
        purpose = "Earth Observation"
        reason = "Provides high-resolution imagery over the selected location."

        if visible:
            best = visible[0].name
            if "INSAT" in best:
                purpose = "Meteorological / Communication"
                reason = f"Active meteorological payload {best} is in line-of-sight for atmospheric sounding."
            elif "EOS" in best:
                purpose = "Earth Observation"
                reason = f"High-resolution optical/radar satellite {best} is available for surface imagery."
            elif "Cartosat" in best:
                purpose = "High-Resolution Mapping"
                reason = f"Cartosat series asset {best} is in pass window for sub-meter mapping."

        return {
            "best_satellite": best,
            "purpose": purpose,
            "reason": reason
        }

    # ---------------------------------------------------
    # Visibility Report
    # ---------------------------------------------------

    def visibility_report(self, latitude, longitude):
        visible = self.satellites.nearby(
            float(latitude),
            float(longitude)
        )

        return {
            "visible_satellites": len(visible),
            "visibility": (
                "Excellent" if len(visible) >= 3
                else "Moderate" if len(visible) > 0
                else "Poor"
            )
        }

    # ---------------------------------------------------
    # Defence Strategy
    # ---------------------------------------------------

    def defence_strategy(self):
        strategy_text = self.assistant.defence_strategy(country="India")
        lines = [
            line.strip().lstrip("- ").lstrip("123. ")
            for line in strategy_text.splitlines()
            if line.strip() and (line.strip().startswith("-") or line.strip()[0].isdigit())
        ]

        return {
            "strategy": lines if lines else [
                "Monitor hostile orbital activity",
                "Protect communication satellites",
                "Track debris and conjunctions",
                "Maintain SSA alerts",
                "Enable rapid disaster response"
            ],
            "full_briefing": strategy_text
        }

    # ---------------------------------------------------
    # Orbital Intelligence
    # ---------------------------------------------------

    def orbital_summary(self):
        dashboard = self.analytics.dashboard()

        return {
            "tracked_objects": self.satellites.count(),
            "orbital_status": "Stable" if dashboard.get("collision_alerts", 0) == 0 else "Congested",
            "collision_alerts": dashboard.get("collision_alerts", 0)
        }

    # ---------------------------------------------------
    # Mission Summary
    # ---------------------------------------------------

    def mission_summary(self):
        dashboard = self.analytics.dashboard()
        summary_text = self.assistant.mission_summary(dashboard)

        return {
            "mission": "Project Zenith",
            "status": "Operational",
            "dashboard": dashboard,
            "summary": summary_text,
            "generated": datetime.utcnow().isoformat()
        }

    # ---------------------------------------------------
    # AI Explainability
    # ---------------------------------------------------

    def explain(self, topic):
        explanations = {
            "collision": "Collision probability is estimated using orbital distance, velocity and congestion.",
            "risk": "Risk combines congestion, debris density and orbital prediction.",
            "hotspot": "Hotspots are generated using satellite imagery and disaster intelligence.",
            "coverage": "Coverage is determined using active Earth observation and communication satellites."
        }

        return {
            "topic": topic,
            "explanation": explanations.get(
                topic.lower(),
                "No explanation available."
            )
        }
