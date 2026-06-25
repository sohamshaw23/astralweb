"use client";

import React, { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic";
import * as THREE from "three";
import { motion } from "framer-motion";
import { Globe as GlobeIcon, Radio } from "lucide-react";

// Dynamic load react-globe.gl to avoid SSR errors
const Globe = dynamic(() => import("react-globe.gl"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-full flex items-center justify-center font-mono text-xs text-status-accent">
      <div className="flex flex-col items-center gap-3">
        <span className="w-8 h-8 rounded-full border-2 border-status-accent border-t-transparent animate-spin" />
        INITIALIZING ORBITAL HYPERPLANE ENGINE...
      </div>
    </div>
  ),
});

interface SSASatellite {
  id: string;
  name: string;
  country: string;
  orbitType: "LEO" | "MEO" | "GEO" | "Debris";
  status: "Active" | "Inactive" | "Debris";
  altitude: number;
  velocity: number;
  inclination: number;
  apogee: number;
  perigee: number;
  operator: string;
  launchDate: string;
  missionType: string;
  lastUpdated: string;
  color: string;
  size: number;
  
  // Mathematical Orbit configurations
  alt: number; // Normalized altitude projection scale
  inclinationRad: number;
  rightAscension: number;
  orbitSpeed: number;
  initialPhase: number;
  activationTime: number;
}

interface SSAGlobeProps {
  globeRef: React.RefObject<any>;
  ssaMode: boolean;
  isTransitioning: boolean;
  transitionProgress: number;
  transitionText: string;
  ssaStartTime: number;
  satellites: SSASatellite[];
  selectedSatellite: SSASatellite | null;
  orbitFilter: "ALL" | "LEO" | "MEO" | "GEO" | "Debris";
  onSelectSatellite: (sat: SSASatellite) => void;
  onActivateSSA: () => void;
}

// Compute Orbit Coordinate Points for Trajectory Lines
const computeOrbitPath = (sat: SSASatellite) => {
  const coords = [];
  const numPoints = 64;
  for (let i = 0; i <= numPoints; i++) {
    const theta = (i / numPoints) * Math.PI * 2;
    const cosTheta = Math.cos(theta);
    const sinTheta = Math.sin(theta);
    const cosI = Math.cos(sat.inclinationRad);
    const sinI = Math.sin(sat.inclinationRad);
    const cosOmega = Math.cos(sat.rightAscension);
    const sinOmega = Math.sin(sat.rightAscension);

    const x = cosTheta * cosOmega - sinTheta * cosI * sinOmega;
    const y = cosTheta * sinOmega + sinTheta * cosI * cosOmega;
    const z = sinTheta * sinI;

    // Convert to lat/lng
    const lat = Math.asin(z) * (180 / Math.PI);
    const lng = Math.atan2(y, x) * (180 / Math.PI);
    coords.push([lat, lng, sat.alt]);
  }
  return {
    coords,
    color: `${sat.color}25`, // Low opacity trajectory line
    stroke: 0.25,
    id: sat.id
  };
};

export function SSAGlobe({
  globeRef,
  ssaMode,
  isTransitioning,
  transitionProgress,
  transitionText,
  ssaStartTime,
  satellites,
  selectedSatellite,
  orbitFilter,
  onSelectSatellite,
  onActivateSSA,
}: SSAGlobeProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = useState(false);
  const [dimensions, setDimensions] = useState({ width: 400, height: 400 });

  useEffect(() => {
    setMounted(true);
  }, []);

  // Handle Dimension Responsiveness
  useEffect(() => {
    if (!mounted) return;

    const updateDimensions = () => {
      if (containerRef.current) {
        const rect = containerRef.current.getBoundingClientRect();
        const padding = 32;
        const size = Math.max(280, Math.min(rect.width - padding, 430));
        setDimensions({
          width: size,
          height: size,
        });
      }
    };

    updateDimensions();
    window.addEventListener("resize", updateDimensions);
    return () => window.removeEventListener("resize", updateDimensions);
  }, [mounted]);

  // Orbit rotation and Camera Limits Configuration
  useEffect(() => {
    if (mounted && globeRef.current) {
      const controls = globeRef.current.controls();
      if (controls) {
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.5;
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        controls.minDistance = 270;
        controls.maxDistance = 330;
        controls.update();
      }

      const camera = globeRef.current.camera();
      if (camera) {
        camera.fov = 45;
        camera.updateProjectionMatrix();
      }
      globeRef.current.pointOfView({ altitude: 2.0 }, 0);
    }
  }, [mounted, globeRef.current]);

  if (!mounted) return null;

  // Generate path data for orbits
  const orbitPathsData = ssaMode
    ? satellites
        .filter((s) => orbitFilter === "ALL" || s.orbitType === orbitFilter)
        .map((s) => computeOrbitPath(s))
    : [];

  // Inject Custom Layer Data (Satellites + Rotating Radar Sweep)
  const customLayerData = ssaMode
    ? [
        ...satellites.map((s) => ({
          ...s,
          isSelected: selectedSatellite?.id === s.id,
          type: "satellite"
        })),
        { type: "radar", activationTime: ssaStartTime }
      ]
    : [];

  return (
    <div
      ref={containerRef}
      className="w-full flex items-center justify-center relative aspect-square max-w-[450px] p-4"
    >
      {/* Ambient Circular Glow Background behind globe */}
      <div className="absolute inset-0 rounded-full bg-[radial-gradient(circle_at_center,rgba(0,229,255,0.06)_0%,transparent_65%)] animate-pulse pointer-events-none" />

      {/* Earth WebGL View */}
      <Globe
        ref={globeRef}
        width={dimensions.width}
        height={dimensions.height}
        backgroundColor="rgba(0, 0, 0, 0)"
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
        showAtmosphere={true}
        atmosphereColor="rgba(0, 229, 255, 0.3)"
        atmosphereAltitude={0.13}

        // Path Trajectory Lines (Dynamic coordinates)
        pathsData={orbitPathsData as any}
        pathColor={(p: any) => p.color}
        pathStroke={(p: any) => p.stroke}

        // Instanced Custom Layer (Satellites & Sweep)
        customLayerData={customLayerData}
        customThreeObject={(d: any) => {
          if (d.type === "radar") {
            const group = new THREE.Group();
            const geom = new THREE.RingGeometry(100.2, 132, 64, 1, 0, Math.PI / 12);
            const mat = new THREE.MeshBasicMaterial({
              color: "rgba(0, 229, 255, 0.12)",
              side: THREE.DoubleSide,
              transparent: true,
              depthWrite: false
            });
            const mesh = new THREE.Mesh(geom, mat);
            mesh.rotation.x = Math.PI / 2;
            group.add(mesh);

            const edgeGeom = new THREE.BufferGeometry().setFromPoints([
              new THREE.Vector3(100.2, 0, 0),
              new THREE.Vector3(132, 0, 0)
            ]);
            const edgeMat = new THREE.LineBasicMaterial({ color: "rgba(0, 229, 255, 0.75)" });
            const edgeLine = new THREE.Line(edgeGeom, edgeMat);
            group.add(edgeLine);

            return group;
          } else {
            const geom = new THREE.SphereGeometry(d.size || 1.1, 6, 6);
            const mat = new THREE.MeshBasicMaterial({ color: d.color || "#00ffc8" });
            return new THREE.Mesh(geom, mat);
          }
        }}
        customThreeObjectUpdate={(obj, d: any) => {
          if (d.type === "radar") {
            const time = (Date.now() - d.activationTime) / 1000;
            obj.rotation.y = time * 0.4;
          } else {
            const time = (Date.now() - d.activationTime) / 1000;
            const theta = d.initialPhase + time * d.orbitSpeed;
            
            const cosTheta = Math.cos(theta);
            const sinTheta = Math.sin(theta);
            const cosI = Math.cos(d.inclinationRad);
            const sinI = Math.sin(d.inclinationRad);
            const cosOmega = Math.cos(d.rightAscension);
            const sinOmega = Math.sin(d.rightAscension);

            const x = cosTheta * cosOmega - sinTheta * cosI * sinOmega;
            const y = cosTheta * sinOmega + sinTheta * cosI * cosOmega;
            const z = sinTheta * sinI;

            const r = 100 * (1 + d.alt);
            obj.position.set(x * r, y * r, z * r);

            const animDuration = 1.8;
            const progress = Math.min(time / animDuration, 1.0);
            const eased = progress * progress * (3 - 2 * progress);
            
            let scale = eased;
            let opacity = eased * 0.95;

            if (d.isSelected) {
              const pulse = 1.0 + Math.sin(Date.now() / 150) * 0.3;
              scale = scale * pulse;
              opacity = 1.0;
            }

            obj.scale.set(scale, scale, scale);
            const mesh = obj as THREE.Mesh;
            if (mesh.material) {
              const mats = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
              mats.forEach((mat) => {
                mat.transparent = true;
                mat.opacity = opacity;
              });
            }
          }
        }}
        customLayerLabel={(d: any) => {
          if (d.type === "radar") return "";
          return `
            <div style="background: rgba(7, 11, 34, 0.95); border: 1px solid ${d.color}; padding: 10px; border-radius: 8px; font-family: monospace; font-size: 10px; color: #fff; box-shadow: 0 0 12px ${d.color}35; min-width: 140px;">
              <div style="font-weight: bold; color: ${d.color}; font-size: 11px; margin-bottom: 5px;">${d.name}</div>
              <div style="margin-bottom: 3px;"><span style="color: #666;">COUNTRY:</span> ${d.country}</div>
              <div style="margin-bottom: 3px;"><span style="color: #666;">ALTITUDE:</span> ${d.altitude} km</div>
              <div style="margin-bottom: 3px;"><span style="color: #666;">VELOCITY:</span> ${d.velocity} km/s</div>
              <div style="margin-bottom: 3px;"><span style="color: #666;">ORBIT:</span> ${d.orbitType}</div>
              <div><span style="color: #666;">STATUS:</span> <span style="color: ${d.status === 'Active' ? '#00ffc8' : '#ff4d4d'}; font-weight: bold;">${d.status.toUpperCase()}</span></div>
            </div>
          `;
        }}
        onCustomLayerClick={(d: any) => {
          if (d && d.type !== "radar") {
            onSelectSatellite(d);
          }
        }}
        onGlobeClick={() => {
          if (!ssaMode && !isTransitioning) {
            onActivateSSA();
          }
        }}
      />

      {/* INITIAL OVERLAY: Deploy Prompt */}
      {!ssaMode && !isTransitioning && (
        <div
          onClick={onActivateSSA}
          className="absolute inset-0 bg-black/30 backdrop-blur-[1px] hover:bg-black/15 transition-all duration-300 rounded-full flex flex-col justify-center items-center z-20 cursor-pointer border border-white/5 shadow-inner"
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0.8 }}
            animate={{ scale: [0.9, 1.05, 0.9], opacity: [0.8, 1, 0.8] }}
            transition={{ repeat: Infinity, duration: 2.2 }}
            className="flex flex-col items-center justify-center text-center space-y-4 px-6"
          >
            <GlobeIcon className="w-12 h-12 text-status-accent" />
            <h3 className="font-display font-bold text-xs uppercase tracking-[0.25em] text-white">
              SSA TELEMETRY DETACHED
            </h3>
            <div className="font-mono text-[9px] text-status-accent px-4 py-2 border border-status-accent/40 bg-status-accent/5 rounded uppercase tracking-wider">
              CLICK GLOBE TO INITIATE SWEEP
            </div>
          </motion.div>
        </div>
      )}

      {/* CINEMATIC TRANSITION OVERLAY: Scanning Matrix */}
      {isTransitioning && (
        <div className="absolute inset-0 bg-[#050816]/80 rounded-full backdrop-blur-sm flex flex-col justify-center items-center z-20 border border-status-accent/20">
          <div className="flex flex-col items-center justify-center text-center space-y-4 max-w-[280px]">
            <Radio className="w-12 h-12 text-status-accent animate-pulse" />
            <div className="w-full bg-white/5 border border-white/10 rounded-full h-1.5 overflow-hidden">
              <motion.div
                className="bg-status-accent h-full"
                initial={{ width: 0 }}
                animate={{ width: `${transitionProgress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <h4 className="font-mono font-bold text-[10px] text-status-accent uppercase tracking-widest leading-relaxed">
              {transitionText || "DEPLOYING TELEMETRY..."}
            </h4>
            <p className="font-mono text-[8px] text-text-secondary uppercase">
              SYS PROGRESS: {transitionProgress}%
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
export default SSAGlobe;
