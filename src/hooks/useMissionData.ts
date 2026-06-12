"use client";

import { useState, useEffect } from "react";

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
  ]);

  const [logs, setLogs] = useState<string[]>([
    "Initial telemetry lock acquired on ZENITH constellations.",
    "Orbit collision matrix updated for LEO band.",
    "Scanning Southeast Asia coordinate array for thermal hazard indexes.",
  ]);

  useEffect(() => {
    const updateInterval = setInterval(() => {
      // Trigger shimmer animation
      setShimmer(true);
      setTimeout(() => setShimmer(false), 800);

      // Fluctuate counts
      setSatelliteCount((prev) => ({
        active: prev.active + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 5),
        warning: prev.warning + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 2),
        critical: Math.max(40, prev.critical + (Math.random() > 0.5 ? 1 : -1) * Math.floor(Math.random() * 2)),
      }));

      // Update Satellites position and details
      setSatellites((prev) =>
        prev.map((sat) => ({
          ...sat,
          latitude: Number((sat.latitude + (Math.random() - 0.5) * 4).toFixed(4)),
          longitude: Number((sat.longitude + (Math.random() - 0.5) * 4).toFixed(4)),
          signalStrength: Math.max(10, Math.min(100, sat.signalStrength + Math.floor((Math.random() - 0.5) * 6))),
        }))
      );

      // Mutate Anomaly Scores
      setAnomalies((prev) =>
        prev.map((anom) => ({
          ...anom,
          score: Math.max(10, Math.min(99, anom.score + Math.floor((Math.random() - 0.5) * 8))),
          trend: Math.random() > 0.6 ? (Math.random() > 0.5 ? "up" : "down") : anom.trend,
        }))
      );

      // Add a fresh log line randomly
      if (Math.random() > 0.4) {
        const events = [
          "Warning: Spatial congestion detected in GEO slot 12B.",
          "Atmospheric telemetry calibrating sensor sweeps.",
          "Payload download verified for GUARDIAN-EYE-1.",
          "Anomaly alert: Orbital drift registered on target segment s2.",
          "Geospatial fire footprint expansion scanned on sector 44-D.",
        ];
        const randomEvent = events[Math.floor(Math.random() * events.length)];
        setLogs((prev) => [`[${new Date().toLocaleTimeString()}] ${randomEvent}`, ...prev.slice(0, 7)]);
      }
    }, 4500);

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
