"""
services/analytics_service.py

Project Zenith
Analytics Intelligence Service
"""

import random
from datetime import datetime, timezone
from flask import request, jsonify
from services.satellite_service import satellite_service
from services.orbit_service import orbit_service
from services.hotspot_service import hotspot_service
from services.disaster_service import disaster_service
from database.redis_cache import cache_manager


# ---------------------------------------------------------------------------
# Space Weather Kp Index → human-readable condition lookup
# ---------------------------------------------------------------------------

_KP_CONDITIONS = [
    (9,  "Extreme Storm"),
    (7,  "Severe Storm"),
    (5,  "Moderate Storm"),
    (3,  "Minor Storm"),
    (0,  "Quiet"),
]


def _kp_label(kp: float) -> str:
    for threshold, label in _KP_CONDITIONS:
        if kp >= threshold:
            return label
    return "Quiet"


_WEATHER_CONDITIONS = ["Clear", "Partly Cloudy", "Overcast", "Hazy"]
_WEATHER_TRENDS     = ["Improving", "Stable", "Deteriorating"]



class AnalyticsService:

    def __init__(self):
        self.satellite = satellite_service
        self.orbit = orbit_service
        self.hotspot = hotspot_service
        self.disaster = disaster_service

    # ---------------------------------------
    # Mission Dashboard
    # ---------------------------------------

    # -----------------------------------------------------------------------
    # Mission Dashboard  (full, dashboard-ready payload)
    # -----------------------------------------------------------------------

    def dashboard(self):
        """
        Generate a rich, dashboard-ready JSON blob covering all 7 categories:
          1. total_satellites   – live tracked satellite count
          2. average_risk       – mean hotspot risk score (0-100)
          3. collision_alerts   – derived from orbital congestion score
          4. active_hotspots    – hotspot dataset breakdown by severity
          5. disasters          – disaster event counts by type
          6. weather_summary    – Earth-weather snapshot from coverage assets
          7. space_weather      – solar / geomagnetic conditions

        Result is cached for 60 s (invalidated by scheduler on demand).
        """
        cached = cache_manager.get("analytics:dashboard")
        if cached:
            return cached

        # ── 1. Satellites ──────────────────────────────────────────────────
        all_sats       = self.satellite.all()
        total_sats     = len(all_sats)

        # ── 2. Average risk & hotspots ─────────────────────────────────────
        hs_stats        = self.hotspot.statistics()
        average_risk    = hs_stats["average_risk"]
        active_hotspots = {
            "total":   hs_stats["total"],
            "high":    hs_stats["high"],
            "medium":  hs_stats["medium"],
            "low":     hs_stats["low"],
            "extreme": len([h for h in self.hotspot.get_all()
                            if h.get("severity", "").lower() == "extreme"]),
        }

        # ── 3. Collision alerts ────────────────────────────────────────────
        congestion_pct  = self.orbit.congestion_score(all_sats)     # 0-100
        collision_alerts = max(0, int(congestion_pct / 20))         # 0-5 bands
        collision_status = (
            "Critical"  if congestion_pct >= 80 else
            "High"      if congestion_pct >= 60 else
            "Moderate"  if congestion_pct >= 40 else
            "Low"
        )

        # ── 4. Global risk score ───────────────────────────────────────────
        global_score = round(congestion_pct * 0.5 + average_risk * 0.5, 2)
        global_level = (
            "Critical" if global_score > 80 else
            "High"     if global_score > 60 else
            "Moderate" if global_score > 40 else
            "Low"
        )

        # ── 5. Disasters ───────────────────────────────────────────────────
        disaster_hotspots = self.disaster.all()
        wildfires  = len([d for d in disaster_hotspots
                          if d.get("event", "").lower() == "wildfire"])
        floods     = len([d for d in disaster_hotspots
                          if d.get("event", "").lower() == "flood"])
        cyclones   = len([d for d in disaster_hotspots
                          if d.get("event", "").lower() in ("cyclone", "hurricane")])
        landslides = len([d for d in disaster_hotspots
                          if d.get("event", "").lower() == "landslide"])
        volcanoes  = len([d for d in disaster_hotspots
                          if d.get("event", "").lower() == "volcano"])
        disasters = {
            "total":      len(disaster_hotspots),
            "wildfires":  wildfires,
            "floods":     floods,
            "cyclones":   cyclones,
            "landslides": landslides,
            "volcanoes":  volcanoes,
            "status":     "Monitoring",
        }

        # ── 6. Weather summary (Earth coverage assets) ─────────────────────
        # Seeded by UTC hour so it is stable within a refresh window.
        _seed = datetime.now(timezone.utc).hour
        rng   = random.Random(_seed)
        weather_summary = {
            "condition":          rng.choice(_WEATHER_CONDITIONS),
            "visibility_km":      rng.randint(5, 30),
            "cloud_cover_pct":    rng.randint(5, 85),
            "wind_speed_kmh":     rng.randint(10, 80),
            "temperature_c":      rng.randint(18, 42),
            "humidity_pct":       rng.randint(30, 90),
            "trend":              rng.choice(_WEATHER_TRENDS),
            "coverage_assets":    ["INSAT-3D", "INSAT-3DR"],
            "last_pass_utc":      (
                datetime.now(timezone.utc)
                .strftime("%Y-%m-%dT%H:00:00Z")
            ),
        }

        # ── 7. Space weather (solar & geomagnetic) ─────────────────────────
        kp_index      = round(rng.uniform(0.5, 8.5), 1)
        solar_flux    = rng.randint(75, 220)           # F10.7 cm flux
        sunspot_count = rng.randint(0, 180)
        proton_flux   = round(rng.uniform(0.1, 12.0), 2)   # pfu
        space_weather = {
            "kp_index":          kp_index,
            "geomagnetic_storm": _kp_label(kp_index),
            "solar_flux_f107":   solar_flux,
            "sunspot_count":     sunspot_count,
            "proton_flux_pfu":   proton_flux,
            "xray_class":        rng.choice(["A", "B", "C", "M", "X"]),
            "aurora_visible":    kp_index >= 5,
            "satellite_impact":  (
                "High"     if kp_index >= 7 else
                "Moderate" if kp_index >= 5 else
                "Low"
            ),
            "source":            "NOAA SWPC (Simulated)",
        }

        # ── Assemble final payload ─────────────────────────────────────────
        result = {
            "total_satellites": total_sats,
            "average_risk":     average_risk,
            "collision_alerts": collision_alerts,
            "collision_status": collision_status,
            "congestion_score": congestion_pct,
            "global_risk": {
                "score": global_score,
                "level": global_level,
            },
            "active_hotspots": active_hotspots,
            "disasters":       disasters,
            "weather_summary": weather_summary,
            "space_weather":   space_weather,
            "generated":       datetime.now(timezone.utc).isoformat(),
        }
        cache_manager.set("analytics:dashboard", result, ex=60)
        return result


    # ---------------------------------------
    # Mission Summary
    # ---------------------------------------

    def mission_summary(self):
        return {
            "satellites": self.satellite.count(),
            "hotspots": self.hotspot.count(),
            "highest_risk": self.hotspot.highest_risk(),
            "status": "Operational"
        }

    # ---------------------------------------
    # Global Risk Score
    # ---------------------------------------

    def global_risk(self):
        congestion = self.orbit.congestion_score(
            self.satellite.all()
        )
        disaster = self.hotspot.average_risk()
        score = round(
            congestion * 0.5 +
            disaster * 0.5,
            2
        )
        if score > 80:
            level = "Critical"
        elif score > 60:
            level = "High"
        elif score > 40:
            level = "Moderate"
        else:
            level = "Low"
        return {
            "risk_score": score,
            "risk_level": level
        }

    # ---------------------------------------
    # Collision Overview
    # ---------------------------------------

    def collision_overview(self):
        satellites = self.satellite.count()
        congestion = self.orbit.congestion_score(
            self.satellite.all()
        )
        alerts = int(congestion / 20)
        return {
            "tracked_satellites": satellites,
            "collision_alerts": alerts,
            "status": "Monitoring"
        }

    # ---------------------------------------
    # Disaster Overview
    # ---------------------------------------

    def disaster_overview(self):
        stats = self.hotspot.statistics()
        return {
            "active_events": stats["total"],
            "high": stats["high"],
            "medium": stats["medium"],
            "low": stats["low"],
            "average_risk": stats["average_risk"]
        }

    # ---------------------------------------
    # Orbital Intelligence
    # ---------------------------------------

    def orbital_intelligence(self):
        satellites = self.satellite.all()
        congestion = self.orbit.congestion_score(
            satellites
        )
        return {
            "tracked": len(satellites),
            "congestion": congestion,
            "engine": "Skyfield"
        }

    # ---------------------------------------
    # Coverage Intelligence (ML Mock & Stats)
    # ---------------------------------------

    def predict_coverage(self):
        """
        Calculates and returns the overall coverage metric.
        """
        location = request.args.get("location", "India")
        comm = random.randint(70, 100)
        nav = random.randint(80, 100)
        weather = random.randint(60, 100)
        obs = random.randint(65, 100)
        defence = random.randint(70, 100)
        overall = round((comm + nav + weather + obs + defence) / 5)

        if overall >= 85:
            level = "Excellent"
        elif overall >= 70:
            level = "Good"
        elif overall >= 50:
            level = "Moderate"
        else:
            level = "Poor"

        return jsonify({
            "location": location,
            "coverage_score": overall,
            "status": level
        })

    def predict_coverage_analysis(self):
        """
        Detailed coverage metrics.
        """
        location = request.args.get("location", "India")
        comm = random.randint(70, 100)
        nav = random.randint(80, 100)
        weather = random.randint(60, 100)
        obs = random.randint(65, 100)
        defence = random.randint(70, 100)
        overall = round((comm + nav + weather + obs + defence) / 5)

        return jsonify({
            "location": location,
            "communication": comm,
            "navigation": nav,
            "weather": weather,
            "earth_observation": obs,
            "defence": defence,
            "overall_score": overall
        })

    def get_coverage_active(self):
        satellites_db = {
            "communication": ["GSAT-11", "GSAT-17", "INSAT-4A"],
            "navigation": ["NavIC IRNSS-1A", "NavIC IRNSS-1B", "NavIC IRNSS-1C"],
            "earth_observation": ["EOS-06", "Resourcesat-2A", "Cartosat-3"],
            "weather": ["INSAT-3D", "INSAT-3DR"],
            "defence": ["GSAT-7", "GSAT-7A", "EMISAT"]
        }
        return jsonify({
            "active_assets": satellites_db
        })

    def get_coverage_statistics(self):
        return jsonify({
            "communication": "Excellent",
            "navigation": "Excellent",
            "weather": "Good",
            "earth_observation": "Excellent",
            "defence": "Operational"
        })

    def get_coverage_history(self):
        history = []
        for i in range(7):
            history.append({
                "day": f"Day {i+1}",
                "score": random.randint(75, 98)
            })
        return jsonify({
            "history": history
        })

    def get_coverage_dashboard(self):
        return jsonify({
            "overall_coverage": 82.5,
            "status": "Healthy",
            "active_constellations": 5,
            "updated": datetime.utcnow().isoformat() + "Z"
        })

    def coverage(self):
        return {
            "communication": "Excellent",
            "navigation": "Excellent",
            "weather": "Good",
            "earth_observation": "Excellent",
            "defence": "Operational"
        }

    # ---------------------------------------
    # National Asset Status
    # ---------------------------------------

    def national_assets(self):
        return {
            "active_assets": 53,
            "communication": 12,
            "navigation": 7,
            "earth_observation": 15,
            "weather": 6,
            "defence": 13
        }

    # ---------------------------------------
    # Mission Control
    # ---------------------------------------

    def mission_control(self):
        cached = cache_manager.get("analytics:mission_control")
        if cached:
            return cached
        result = {
            "dashboard": self.dashboard(),
            "risk": self.global_risk(),
            "disaster": self.disaster_overview(),
            "collision": self.collision_overview(),
            "coverage": self.coverage(),
            "assets": self.national_assets()
        }
        cache_manager.set("analytics:mission_control", result, ex=60)
        return result

    # ---------------------------------------
    # Coverage API Blueprints Wrappers
    # ---------------------------------------

    def get_communication(self):
        return jsonify({
            "coverage": "Available",
            "satellites": ["GSAT-11", "GSAT-17", "INSAT-4A"],
            "signal_strength": random.randint(80, 100)
        })

    def get_navigation(self):
        return jsonify({
            "provider": "NavIC",
            "satellites": ["NavIC IRNSS-1A", "NavIC IRNSS-1B", "NavIC IRNSS-1C"],
            "accuracy_m": 5
        })

    def get_weather(self):
        return jsonify({
            "satellites": ["INSAT-3D", "INSAT-3DR"],
            "coverage": "Active"
        })

    def get_earth_observation(self):
        return jsonify({
            "satellites": ["EOS-06", "Resourcesat-2A", "Cartosat-3"],
            "coverage": "High Resolution"
        })

    def get_defence(self):
        return jsonify({
            "satellites": ["GSAT-7", "GSAT-7A", "EMISAT"],
            "surveillance": "Active"
        })

    def get_best(self):
        return jsonify({
            "best_satellite": "EOS-06",
            "coverage_percent": 99
        })

    def get_heatmap(self):
        heatmap = []
        for _ in range(40):
            heatmap.append({
                "latitude": round(random.uniform(-90, 90), 4),
                "longitude": round(random.uniform(-180, 180), 4),
                "weight": random.randint(20, 100)
            })
        return jsonify({
            "heatmap": heatmap
        })

    def get_coverage_dashboard_json(self):
        comm = random.randint(70, 100)
        nav = random.randint(80, 100)
        weather = random.randint(60, 100)
        obs = random.randint(65, 100)
        defence = random.randint(70, 100)
        overall = round((comm + nav + weather + obs + defence) / 5)
        return jsonify({
            "communication": comm,
            "navigation": nav,
            "weather": weather,
            "earth_observation": obs,
            "defence": defence,
            "overall": overall,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        })


# Singleton instance
analytics_service = AnalyticsService()

