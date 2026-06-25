"use client";

import React, { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import * as THREE from "three";
import { SatelliteInfo, DisasterAlert } from "@/hooks/useMissionData";

// Load react-globe.gl dynamically to bypass SSR compilation errors in Next.js
const Globe = dynamic(() => import("react-globe.gl"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center font-mono text-xs text-status-accent">
      <div className="flex flex-col items-center gap-3">
        <span className="w-8 h-8 rounded-full border-2 border-status-accent border-t-transparent animate-spin" />
        INITIALIZING ORBITAL ENGINE...
      </div>
    </div>
  ),
});

interface EarthGlobeProps {
  satellites?: SatelliteInfo[];
  disasters?: DisasterAlert[];
  selectedSatellite?: SatelliteInfo | null;
  onSelectSatellite?: (sat: SatelliteInfo) => void;
  layers?: {
    satellites: boolean;
    debris: boolean;
    orbits: boolean;
    disasters: boolean;
    assets: boolean;
  };
  onToggleLayer?: (layer: "satellites" | "debris" | "orbits" | "disasters" | "assets") => void;
  showControls?: boolean;
  autoRotate?: boolean;
}

export function EarthGlobe({
  satellites = [],
  disasters = [],
  selectedSatellite = null,
  onSelectSatellite = () => {},
  layers = { satellites: true, debris: true, orbits: true, disasters: true, assets: true },
  onToggleLayer = () => {},
  showControls = true,
  autoRotate = true,
}: EarthGlobeProps) {
  const globeRef = useRef<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = useState(false);
  const [dimensions, setDimensions] = useState({ width: 450, height: 450 });

  useEffect(() => {
    setMounted(true);
  }, []);

  // Make globe responsive to container size
  useEffect(() => {
    if (!mounted) return;

    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const padding = 32; // 16px padding on left/right for p-4
        const size = Math.max(0, Math.min(rect.width - padding, 400));
        if (size > 0) {
          setDimensions({
            width: size,
            height: size,
          });
        }
      }
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);
    return () => window.removeEventListener("resize", updateDimensions);
  }, [mounted]);

  // Configure automatic rotation & zoom controls on mount
  useEffect(() => {
    if (mounted && globeRef.current) {
      const controls = globeRef.current.controls();
      if (controls) {
        controls.autoRotate = autoRotate;
        controls.autoRotateSpeed = 0.55; // Smooth rotation
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 150; // Allow user to zoom in more
        controls.maxDistance = 330; // Prevent minimizing
        controls.update();
      }

      // Explicitly configure camera settings
      const camera = globeRef.current.camera();
      if (camera) {
        camera.fov = 45; // Fixed field of view for consistent perspective
        camera.updateProjectionMatrix();
      }

      // Position the camera to 2.0 altitude (distance 300) to keep 10% padding
      globeRef.current.pointOfView({ altitude: 2.0 }, 0);
    }
  }, [mounted, globeRef.current, autoRotate]);

  if (!mounted) return null;

  // 1. Generate 30+ Satellites Data mapping coordinates
  const satellitesData = layers.satellites
    ? satellites.map((sat) => ({
        lat: sat.latitude,
        lng: sat.longitude,
        alt: (sat.altitude / 3000) + 0.05, // Normalized altitude projection scale
        radius: 1.5,
        color:
          sat.status === "nominal"
            ? "rgba(0, 255, 200, 0.95)"
            : sat.status === "warning"
            ? "rgba(255, 200, 87, 0.95)"
            : "rgba(255, 77, 77, 0.95)",
        name: sat.name,
        velocity: sat.velocity,
        altitude: sat.altitude,
        status: sat.status,
        originalSat: sat,
      }))
    : [];

  // 2. Generate Debris Cloud Data (thousands of small LEO particles)
  const debrisData = layers.debris
    ? Array.from({ length: 450 }).map(() => {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(Math.random() * 2 - 1);
        const radiusMultiplier = 1.05 + Math.random() * 0.07; // LEO Band
        return {
          lat: (phi * 180) / Math.PI - 90,
          lng: (theta * 180) / Math.PI,
          size: Math.random() * 0.5 + 0.15,
          color: Math.random() > 0.85 ? "rgba(255, 200, 87, 0.35)" : "rgba(180, 180, 180, 0.25)",
        };
      })
    : [];

  // 3. Generate Orbit Paths (Circular orbit ring coordinates)
  const pathsData = layers.orbits
    ? satellites.map((sat) => {
        // Construct coordinates around a circle representing the orbit
        const numPoints = 64;
        const coords = [];
        for (let i = 0; i <= numPoints; i++) {
          const ratio = i / numPoints;
          const angle = ratio * Math.PI * 2;
          // Project points around the satellite's polar or inclined angles
          const lat = sat.latitude + Math.sin(angle) * 14;
          const lng = sat.longitude + Math.cos(angle) * 360 * ratio;
          coords.push([lat, lng, (sat.altitude / 3000) + 0.05]);
        }
        return {
          coords,
          color:
            sat.status === "critical"
              ? "rgba(255, 77, 77, 0.35)"
              : sat.status === "warning"
              ? "rgba(255, 200, 87, 0.25)"
              : "rgba(0, 229, 255, 0.15)",
        };
      })
    : [];

  // 4. Generate Disaster Alert Rings
  const disasterRings = layers.disasters
    ? disasters.map((dist) => ({
        lat: dist.coordinates[0],
        lng: dist.coordinates[1],
        maxR: dist.severity === "critical" ? 8 : 4,
        propagationSpeed: 2.5,
        repeatPeriod: 1500,
        color:
          dist.severity === "critical"
            ? "rgba(255, 77, 77, 0.85)"
            : dist.severity === "warning"
            ? "rgba(255, 200, 87, 0.75)"
            : "rgba(0, 229, 255, 0.75)",
      }))
    : [];

  // 5. Strategic National Assets (Guardian Layer) Shield animations
  const assetShields = layers.assets
    ? satellites
        .filter((s) => s.name.includes("ZENITH") || s.status === "nominal")
        .map((sat) => ({
          lat: sat.latitude,
          lng: sat.longitude,
          maxR: 3.5,
          propagationSpeed: 1.2,
          repeatPeriod: 2200,
          color: "rgba(0, 255, 200, 0.45)", // Security shield nominal glow color
        }))
    : [];

  return (
    <div className="flex flex-col items-center justify-center space-y-6 flex-grow w-full relative z-10 py-4">
      {/* 3D WebGL Globe View */}
      <div ref={containerRef} className="relative w-full max-w-[450px] aspect-square flex items-center justify-center p-4">
        <Globe
          ref={globeRef}
          width={dimensions.width}
          height={dimensions.height}
          backgroundColor="rgba(0, 0, 0, 0)"
          globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
          bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
          showAtmosphere={true}
          atmosphereColor="rgba(0, 229, 255, 0.35)"
          atmosphereAltitude={0.14}
          
          // Satellites markers (points layer)
          pointsData={satellitesData}
          pointLat="lat"
          pointLng="lng"
          pointColor="color"
          pointRadius="radius"
          pointAltitude="alt"
          pointLabel={(d: any) => `
            <div style="background: rgba(7, 11, 34, 0.9); border: 1px solid rgba(255,255,255,0.15); padding: 8px; border-radius: 6px; font-family: monospace; font-size: 10px; color: #fff; box-shadow: 0 0 10px rgba(0,229,255,0.2)">
              <div style="font-weight: bold; color: var(--status-accent); margin-bottom: 2px;">${d.name}</div>
              <div>ALTITUDE: ${d.altitude} KM</div>
              <div>VELOCITY: ${d.velocity} KM/S</div>
              <div>STATUS: <span style="color: ${d.status === 'nominal' ? '#00FFC8' : d.status === 'warning' ? '#FFC857' : '#FF4D4D'}">${d.status.toUpperCase()}</span></div>
            </div>
          `}
          onPointClick={(d: any) => {
            if (globeRef.current) {
              globeRef.current.pointOfView({ lat: d.lat, lng: d.lng, altitude: 1.7 }, 1000);
            }
            onSelectSatellite(d.originalSat);
          }}

          // Debris Cloud markers (custom overlay as dots with small altitude)
          customLayerData={[...debrisData]}
          customThreeObject={(d: any) => {
            const geom = new THREE.SphereGeometry(d.size || 0.3, 4, 4);
            const mat = new THREE.MeshBasicMaterial({ color: d.color || "#ccc" });
            return new THREE.Mesh(geom, mat);
          }}
          customThreeObjectUpdate={(obj, d: any) => {
            const coords = globeRef.current?.getCoords(d.lat, d.lng, 0.06);
            if (coords) {
              Object.assign(obj.position, coords);
            }
          }}

          // Orbit paths (paths layer)
          pathsData={pathsData.map(p => p.coords)}
          pathColor={() => "rgba(0, 229, 255, 0.14)"}
          pathStroke={0.4}

          // Disasters and Asset shields (rings layer)
          ringsData={[...disasterRings, ...assetShields]}
          ringLat="lat"
          ringLng="lng"
          ringColor="color"
          ringMaxRadius="maxR"
          ringPropagationSpeed="propagationSpeed"
          ringRepeatPeriod="repeatPeriod"
        />
      </div>

      {/* Layer Toggles Control Strip */}
      {showControls && (
        <div className="flex flex-wrap items-center justify-center gap-3 bg-bg-surface/75 border border-white/8 px-4 py-2.5 rounded-xl backdrop-blur-md max-w-lg w-full">
          {(Object.keys(layers) as Array<keyof typeof layers>).map((layer) => {
            const isActive = layers[layer];

            // Indicator color mapping
            const colors = {
              satellites: "bg-status-safe border-status-safe",
              debris: "bg-text-secondary border-text-secondary",
              orbits: "bg-status-accent border-status-accent",
              disasters: "bg-status-critical border-status-critical",
              assets: "bg-primary-vivid border-primary-vivid",
            };

            return (
              <button
                key={layer}
                onClick={() => onToggleLayer(layer)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-[10px] font-mono uppercase tracking-wider transition-all duration-200 cursor-pointer ${
                  isActive
                    ? "bg-white/5 border-white/15 text-white"
                    : "bg-transparent border-transparent text-text-muted hover:text-text-secondary"
                }`}
              >
                <span className={`w-1.5 h-1.5 rounded-full border ${colors[layer]} ${isActive ? "scale-100" : "scale-75 opacity-40"}`} />
                {layer}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
export default EarthGlobe;
