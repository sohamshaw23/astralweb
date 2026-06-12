"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, useMotionValue, useTransform, useSpring } from "framer-motion";
import { SatelliteInfo, DisasterAlert } from "@/hooks/useMissionData";

interface EarthGlobeProps {
  satellites: SatelliteInfo[];
  disasters: DisasterAlert[];
  selectedSatellite: SatelliteInfo | null;
  onSelectSatellite: (sat: SatelliteInfo) => void;
  layers: {
    satellites: boolean;
    debris: boolean;
    orbits: boolean;
    disasters: boolean;
    assets: boolean;
  };
  onToggleLayer: (layer: "satellites" | "debris" | "orbits" | "disasters" | "assets") => void;
}

export function EarthGlobe({
  satellites,
  disasters,
  selectedSatellite,
  onSelectSatellite,
  layers,
  onToggleLayer,
}: EarthGlobeProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springConfig = { stiffness: 80, damping: 18 };
  const rotateX = useSpring(useTransform(mouseY, [-300, 300], [20, -20]), springConfig);
  const rotateY = useSpring(useTransform(mouseX, [-300, 300], [-20, 20]), springConfig);

  const [hoveredOrbit, setHoveredOrbit] = useState<string | null>(null);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      mouseX.set(x);
      mouseY.set(y);
    };
    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, [mouseX, mouseY]);

  // Orbit info lookup
  const orbitData: Record<string, { count: number; congestion: string }> = {
    LEO: { count: 18400, congestion: "HIGH (87%)" },
    MEO: { count: 4200, congestion: "MODERATE (42%)" },
    GEO: { count: 1247, congestion: "LOW (14%)" },
  };

  return (
    <div className="flex flex-col items-center justify-center space-y-8 flex-grow w-full relative z-10 py-6">
      {/* Globe Wrap */}
      <div
        ref={containerRef}
        className="relative w-80 h-80 sm:w-96 sm:h-96 md:w-[480px] md:h-[480px] flex items-center justify-center select-none"
      >
        {/* Ambient atmospheric halo */}
        <div className="absolute inset-0 rounded-full bg-radial from-status-accent/20 via-primary/5 to-transparent blur-3xl scale-120 pointer-events-none" />

        {/* Orbit Rings (Thin svg pathways) */}
        {layers.orbits && (
          <svg className="absolute inset-[-60px] w-[calc(100%+120px)] h-[calc(100%+120px)] pointer-events-none" viewBox="0 0 100 100">
            {/* LEO Ring */}
            <ellipse
              cx="50"
              cy="50"
              rx="46"
              ry="18"
              fill="none"
              stroke={hoveredOrbit === "LEO" ? "var(--status-accent)" : "rgba(0, 229, 255, 0.25)"}
              strokeWidth={hoveredOrbit === "LEO" ? "0.6" : "0.35"}
              className="origin-center animate-orbit-rotate pointer-events-auto cursor-pointer"
              onMouseEnter={() => setHoveredOrbit("LEO")}
              onMouseLeave={() => setHoveredOrbit(null)}
              style={{ pointerEvents: "auto" }}
            />
            {/* MEO Ring */}
            <ellipse
              cx="50"
              cy="50"
              rx="54"
              ry="30"
              fill="none"
              stroke={hoveredOrbit === "MEO" ? "var(--primary-vivid)" : "rgba(139, 92, 246, 0.2)"}
              strokeWidth={hoveredOrbit === "MEO" ? "0.6" : "0.3"}
              className="origin-center animate-orbit-rotate-reverse pointer-events-auto cursor-pointer"
              onMouseEnter={() => setHoveredOrbit("MEO")}
              onMouseLeave={() => setHoveredOrbit(null)}
              style={{ pointerEvents: "auto" }}
            />
            {/* GEO Ring */}
            <ellipse
              cx="50"
              cy="50"
              rx="62"
              ry="42"
              fill="none"
              stroke={hoveredOrbit === "GEO" ? "var(--status-safe)" : "rgba(0, 255, 200, 0.15)"}
              strokeWidth={hoveredOrbit === "GEO" ? "0.6" : "0.25"}
              className="origin-center animate-orbit-rotate pointer-events-auto cursor-pointer"
              onMouseEnter={() => setHoveredOrbit("GEO")}
              onMouseLeave={() => setHoveredOrbit(null)}
              style={{ pointerEvents: "auto" }}
            />
          </svg>
        )}

        {/* Orbit Hover Tooltip */}
        {hoveredOrbit && (
          <div className="absolute top-0 bg-bg-surface/90 border border-status-accent/30 rounded-lg p-3 font-mono text-[10px] space-y-1 shadow-[0_0_20px_rgba(0,229,255,0.15)] z-30">
            <div className="font-bold text-white uppercase">{hoveredOrbit} ORBIT SECTOR</div>
            <div>OBJECT COUNT: {orbitData[hoveredOrbit].count.toLocaleString()}</div>
            <div>CONGESTION: <span className="text-status-accent">{orbitData[hoveredOrbit].congestion}</span></div>
          </div>
        )}

        {/* Rotating 3D Earth Globe Sphere */}
        <motion.div
          style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
          className="w-full h-full rounded-full relative overflow-hidden bg-gradient-to-br from-[#0a122e] via-[#040713] to-[#000104] shadow-[inset_-30px_-30px_90px_rgba(0,0,0,0.95),inset_20px_20px_60px_rgba(255,255,255,0.05),0_0_40px_rgba(0,229,255,0.08)] border border-white/10"
        >
          {/* Graticule Grid lines */}
          <div className="absolute inset-0 opacity-35 bg-[linear-gradient(to_right,rgba(255,255,255,0.035)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.035)_1px,transparent_1px)] bg-[size:18px_18px]" />

          {/* Continents translation mapping */}
          <motion.div
            animate={{ x: [0, -1000] }}
            transition={{ repeat: Infinity, duration: 90, ease: "linear" }}
            className="absolute inset-0 flex w-[2000px] h-full pointer-events-none"
          >
            <div className="w-[1000px] h-full relative opacity-50">
              <svg viewBox="0 0 1000 400" className="w-full h-full fill-primary/30">
                <rect x="80" y="60" width="140" height="90" rx="20" />
                <rect x="300" y="120" width="180" height="150" rx="30" />
                <rect x="580" y="50" width="220" height="160" rx="40" />
                <rect x="850" y="180" width="100" height="90" rx="20" />
                <circle cx="200" cy="220" r="50" />
                <circle cx="500" cy="80" r="40" />
                <circle cx="750" cy="240" r="55" />
              </svg>
            </div>
            <div className="w-[1000px] h-full relative opacity-50">
              <svg viewBox="0 0 1000 400" className="w-full h-full fill-primary/30">
                <rect x="80" y="60" width="140" height="90" rx="20" />
                <rect x="300" y="120" width="180" height="150" rx="30" />
                <rect x="580" y="50" width="220" height="160" rx="40" />
                <rect x="850" y="180" width="100" height="90" rx="20" />
                <circle cx="200" cy="220" r="50" />
                <circle cx="500" cy="80" r="40" />
                <circle cx="750" cy="240" r="55" />
              </svg>
            </div>
          </motion.div>

          {/* Debris field overlay dots */}
          {layers.debris && (
            <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(rgba(255,255,255,0.06)_1px,transparent_1.5px)] bg-[size:10px_10px] mix-blend-screen opacity-70" />
          )}

          {/* Disaster Overlays (Red-orange localized hazard heat indicators) */}
          {layers.disasters &&
            disasters.map((dist, idx) => {
              // Approximate mapping coordinate ratios
              const top = 40 + dist.coordinates[0] * 1.5;
              const left = 50 + dist.coordinates[1] * 0.4;
              return (
                <div
                  key={idx}
                  style={{ top: `${top}%`, left: `${left}%` }}
                  className="absolute -translate-x-1/2 -translate-y-1/2 flex items-center justify-center"
                >
                  <div className="w-8 h-8 rounded-full bg-status-critical/15 border border-status-critical/45 animate-ping" />
                  <div className="absolute w-3.5 h-3.5 rounded-full bg-status-critical/40 border border-status-critical" />
                </div>
              );
            })}

          {/* Interactive Satellites layer overlay */}
          {layers.satellites &&
            satellites.map((sat) => {
              // Convert coordinate latitude/longitudes roughly inside our bounded earth circle
              const top = 50 - sat.latitude * 1.1;
              const left = 50 + sat.longitude * 0.45;

              // Color styles
              const colorMap = {
                nominal: "bg-status-safe border-status-safe",
                warning: "bg-status-warning border-status-warning",
                critical: "bg-status-critical border-status-critical",
              };

              const isSelected = selectedSatellite?.id === sat.id;

              return (
                <button
                  key={sat.id}
                  onClick={() => onSelectSatellite(sat)}
                  style={{ top: `${top}%`, left: `${left}%` }}
                  className={`absolute -translate-x-1/2 -translate-y-1/2 w-4 h-4 flex items-center justify-center rounded-full group focus:outline-none transition-all duration-300 ${
                    isSelected ? "scale-140 z-20" : "scale-100 hover:scale-120 z-10"
                  }`}
                >
                  {/* Pulse Ring */}
                  <span
                    className={`absolute inset-0 rounded-full animate-ping opacity-35 ${
                      sat.status === "nominal"
                        ? "bg-status-safe"
                        : sat.status === "warning"
                        ? "bg-status-warning"
                        : "bg-status-critical"
                    }`}
                  />
                  {/* Solid Point */}
                  <span
                    className={`w-2 h-2 rounded-full border shadow-md transition-colors duration-300 ${
                      colorMap[sat.status]
                    } ${isSelected ? "shadow-[0_0_10px_rgba(255,255,255,0.8)] scale-110" : ""}`}
                  />

                  {/* Satellite mini-tooltip */}
                  <span className="absolute left-6 top-1/2 -translate-y-1/2 font-mono text-[8px] bg-bg-surface/90 border border-white/10 px-1.5 py-0.5 rounded text-white hidden group-hover:block pointer-events-none whitespace-nowrap">
                    {sat.name} // ALT: {sat.altitude}km
                  </span>
                </button>
              );
            })}

          {/* Day/Night terminator shade overlay */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-black/30 to-black/85 pointer-events-none" />

          {/* Atmosphere rim overlay */}
          <div className="absolute inset-0 shadow-[inset_15px_15px_30px_rgba(0,229,255,0.2),inset_-15px_-15px_30px_rgba(0,0,0,0.9)] rounded-full pointer-events-none" />
        </motion.div>
      </div>

      {/* Layer Toggles Control Strip */}
      <div className="flex flex-wrap items-center justify-center gap-3 bg-bg-surface/70 border border-white/8 px-4 py-2.5 rounded-xl backdrop-blur-md max-w-lg w-full">
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
    </div>
  );
}
export default EarthGlobe;
