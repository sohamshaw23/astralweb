import { useState, useEffect } from "react";
import { getAnalytics, getSatellites } from "@/lib/api";

export interface SatelliteInfo {
  id: string;
  name: string;
  status: "nominal" | "warning" | "critical";
  altitude: number; // in km
  velocity: number; // in km/s
  inclination: number; // degrees
  latitude: number;
  longitude: number;
  signalStrength: number; // %
}

export interface DisasterAlert {
  id: string;
  type: string;
  severity: "critical" | "warning" | "info";
  location: string;
  coordinates: [number, number];
}

export interface AnomalyInfo {
  id: string;
  source: string;
  score: number; // 0-100
  trend: "up" | "down" | "stable";
  timestamp: string;
}

export function useMissionData() {
  const [shimmer, setShimmer] = useState(false);
  const [satelliteCount, setSatelliteCount] = useState({
    active: 23847,
    warning: 312,
    critical: 47,
  });

  const [disasters, setDisasters] = useState<DisasterAlert[]>([
    { id: "d1", type: "Cyclone", severity: "critical", location: "Bay of Bengal", coordinates: [15, 88] },
    { id: "d2", type: "Wildfire", severity: "warning", location: "New South Wales", coordinates: [-33, 150] },
    { id: "d3", type: "Flood Warning", severity: "info", location: "Southeast Asia", coordinates: [10, 105] },
  ]);

  const [anomalies, setAnomalies] = useState<AnomalyInfo[]>([
    { id: "a1", source: "SAT-ZENITH-A1", score: 87, trend: "up", timestamp: "12:04:12" },
    { id: "a2", source: "DEBRIS-GRID-90", score: 64, trend: "stable", timestamp: "12:02:44" },
    { id: "a3", source: "COSMOS-2499", score: 41, trend: "down", timestamp: "11:58:19" },
  ]);

  const [riskMatrix, setRiskMatrix] = useState([
    { name: "Orbital Collision", prob: 0.75, imp: 0.85, quad: 1 },
    { name: "Solar Flare Impact", prob: 0.35, imp: 0.9, quad: 2 },
    { name: "Debris Swarm LEO", prob: 0.85, imp: 0.45, quad: 3 },
    { name: "Ground Link Loss", prob: 0.2, imp: 0.6, quad: 4 },
  ]);

  const [satellites, setSatellites] = useState<SatelliteInfo[]>([
    { id: "s1", name: "ZENITH-01", status: "nominal", altitude: 418, velocity: 7.66, inclination: 51.6, latitude: 12.5, longitude: 77.5, signalStrength: 98 },
    { id: "s2", name: "ZENITH-02", status: "warning", altitude: 620, velocity: 7.55, inclination: 98.2, latitude: 35.6, longitude: 139.6, signalStrength: 72 },
    { id: "s3", name: "ZENITH-ALERT", status: "critical", altitude: 358, velocity: 7.72, inclination: 28.5, latitude: -25.3, longitude: 130.8, signalStrength: 14 },
    { id: "s4", name: "COSMIC-SCAN-A", status: "nominal", altitude: 830, velocity: 7.43, inclination: 98.8, latitude: 48.85, longitude: 2.35, signalStrength: 91 },
    { id: "s5", name: "GUARDIAN-EYE-1", status: "nominal", altitude: 540, velocity: 7.59, inclination: 45.2, latitude: 38.9, longitude: -77.0, signalStrength: 89 },
    { id: "s6", name: "ZENITH-03", status: "nominal", altitude: 480, velocity: 7.62, inclination: 51.6, latitude: 45.1, longitude: -12.3, signalStrength: 95 },
    { id: "s7", name: "ZENITH-04", status: "nominal", altitude: 510, velocity: 7.60, inclination: 51.6, latitude: -15.4, longitude: 40.2, signalStrength: 93 },
    { id: "s8", name: "COSMIC-SCAN-B", status: "nominal", altitude: 840, velocity: 7.42, inclination: 98.8, latitude: 20.5, longitude: 110.1, signalStrength: 88 },
    { id: "s9", name: "GUARDIAN-EYE-2", status: "warning", altitude: 550, velocity: 7.58, inclination: 45.2, latitude: -30.2, longitude: -50.8, signalStrength: 68 },
    { id: "s10", name: "METEO-SAT-9", status: "nominal", altitude: 720, velocity: 7.50, inclination: 82.4, latitude: 60.1, longitude: 90.3, signalStrength: 92 },
    { id: "s11", name: "STAR-LINK-X", status: "critical", altitude: 340, velocity: 7.74, inclination: 53.0, latitude: 5.6, longitude: -80.2, signalStrength: 8 },
    { id: "s12", name: "METEO-SAT-10", status: "nominal", altitude: 710, velocity: 7.52, inclination: 82.4, latitude: -40.1, longitude: 120.3, signalStrength: 96 }
  ]);

  const [logs, setLogs] = useState<string[]>([
    "Initial telemetry lock acquired on ZENITH constellations.",
    "Orbit collision matrix updated for LEO band.",
    "Scanning Southeast Asia coordinate array for thermal hazard indexes.",
  ]);

  // Backend Integration Effect
  useEffect(() => {
    const fetchData = async () => {
      try {
        const analytics = await getAnalytics();
        if (analytics) {
          setSatelliteCount({
            active: analytics.total_satellites || 23847,
            warning: analytics.active_hotspots?.medium || 312,
            critical: analytics.active_hotspots?.high || 47,
          });
        }
      } catch (err) {
        console.warn("Could not fetch analytics from backend, keeping mock data.", err);
      }

      try {
        const liveSats = await getSatellites();
        if (liveSats && liveSats.length > 0) {
          const mapped = liveSats.slice(0, 12).map((sat, index) => {
            const status: "nominal" | "warning" | "critical" =
              index % 11 === 0 ? "critical" : index % 7 === 0 ? "warning" : "nominal";
            return {
              id: `s-${index + 1}`,
              name: sat.name,
              status,
              altitude: sat.altitude_km,
              velocity: Number((7.8 - (sat.altitude_km / 1000) * 0.4).toFixed(2)),
              inclination: 51.6 + (index % 10),
              latitude: sat.latitude,
              longitude: sat.longitude,
              signalStrength: status === "nominal" ? 90 + (index % 11) : status === "warning" ? 60 + (index % 13) : 10 + (index % 5),
            };
          });
          setSatellites(mapped);
        }
      } catch (err) {
        console.warn("Could not fetch live satellites from backend, keeping mock data.", err);
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";
        const res = await fetch(`${apiUrl}/api/analytics/anomaly/active`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data)) {
            const mapped = data.slice(0, 3).map((an: any, idx: number) => ({
              id: an.id || `a-${idx}`,
              source: an.satellite || `SAT-ZENITH-A${idx + 1}`,
              score: Math.round(an.score || (70 - idx * 10)),
              trend: (an.trend || (idx % 2 === 0 ? "up" : "stable")) as "up" | "down" | "stable",
              timestamp: an.time || new Date().toLocaleTimeString(),
            }));
            setAnomalies(mapped);
          }
        }
      } catch (err) {
        console.warn("Could not fetch anomalies from backend, keeping mock data.", err);
      }

      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";
        const res = await fetch(`${apiUrl}/api/disasters/live`);
        if (res.ok) {
          const data = await res.json();
          if (data && Array.isArray(data.events)) {
            const mapped = data.events.slice(0, 3).map((ev: any, idx: number) => ({
              id: ev.id || `d-${idx}`,
              type: ev.category || "Incident",
              severity: (ev.status === "closed" ? "info" : "critical") as "critical" | "warning" | "info",
              location: ev.title || "Global Vector",
              coordinates: ev.geometry ? [ev.geometry.coordinates[1], ev.geometry.coordinates[0]] as [number, number] : [0, 0] as [number, number],
            }));
            if (mapped.length > 0) {
              setDisasters(mapped);
            }
          }
        }
      } catch (err) {
        console.warn("Could not fetch disasters from backend, keeping mock data.", err);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 15000);
    return () => clearInterval(intervalId);
  }, []);

  // Ambient Simulation Updates (Maintains 60 FPS Three.js rendering responsiveness)
  useEffect(() => {
    const updateInterval = setInterval(() => {
      // Trigger shimmer animation
      setShimmer(true);
      setTimeout(() => setShimmer(false), 800);

      // Fluctuate counts gently
      setSatelliteCount((prev) => ({
        active: prev.active + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 3),
        warning: prev.warning + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 2),
        critical: Math.max(40, prev.critical + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 2)),
      }));

      // Update Satellites position and details
      setSatellites((prev) =>
        prev.map((sat) => ({
          ...sat,
          latitude: Number((sat.latitude + (Math.random() - 0.5) * 1.5).toFixed(4)),
          longitude: Number((sat.longitude + (Math.random() - 0.5) * 1.5).toFixed(4)),
          signalStrength: Math.max(10, Math.min(100, sat.signalStrength + Math.floor((Math.random() - 0.5) * 4))),
        }))
      );

      // Mutate Anomaly Scores
      setAnomalies((prev) =>
        prev.map((anom) => ({
          ...anom,
          score: Math.max(10, Math.min(99, anom.score + Math.floor((Math.random() - 0.5) * 6))),
          trend: Math.random() > 0.6 ? (Math.random() > 0.5 ? "up" : "down") : anom.trend,
        }))
      );

      // Add a fresh log line randomly
      if (Math.random() > 0.4) {
        const events = [
          "Warning: Spatial congestion detected in GEO slot 12B.",
          "Atmospheric telemetry calibrating sensor sweeps.",
          "Payload download verified for GUARDIAN-EYE-1.",
          "Anomaly alert: Orbital drift registered on target segment.",
          "Geospatial fire footprint expansion scanned.",
        ];
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        setLogs((prev) => [`[${new Date().toLocaleTimeString()}] ${randomEvent}`, ...prev.slice(0, 7)]);
      }
    }, 5000);

    return () => clearInterval(updateInterval);
  }, []);

  return {
    shimmer,
    satelliteCount,
    disasters,
    anomalies,
    riskMatrix,
    satellites,
    logs,
  };
}
