"use client";

import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  Satellite,
  Compass,
  Radio,
  Activity,
  Shield,
  Trash2,
  ShieldAlert,
  Globe as GlobeIcon,
  RefreshCw,
  Play,
  X,
  ChevronRight,
  Search,
  SlidersHorizontal,
  Clock,
  Database
} from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { GlassCard } from "@/components/ui/glass-card";
import { SSAGlobe } from "@/components/globe/ssa-globe";

// Satellite Interface
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

// Generate Satellites Data
const generateSSASatellites = (activationTime: number): SSASatellite[] => {
  const satellites: SSASatellite[] = [];
  const countries = ["USA", "ESA", "Japan", "India", "China", "UK", "Germany", "Canada"];
  const operators = ["NASA", "SpaceX", "ESA", "ISRO", "JAXA", "US Space Force", "Eutelsat", "Inmarsat"];

  // 1. Generate LEO (80 satellites)
  for (let i = 1; i <= 80; i++) {
    const isISS = i === 1;
    const name = isISS ? "ISS (ZARYA)" : `STARLINK-${1000 + i}`;
    const alt = 350 + Math.random() * 450;
    const inc = isISS ? 51.64 : 53.0 + Math.random() * 45;
    const launchDate = `202${Math.floor(Math.random() * 4)}-0${Math.floor(Math.random() * 9) + 1}-${Math.floor(Math.random() * 20) + 10}`;

    satellites.push({
      id: `leo-${i}`,
      name,
      country: isISS ? "USA" : "USA",
      orbitType: "LEO",
      status: "Active",
      altitude: Math.round(alt),
      velocity: Number((7.8 - (alt / 1000) * 0.4).toFixed(2)),
      inclination: Number(inc.toFixed(2)),
      apogee: Math.round(alt + Math.random() * 10),
      perigee: Math.round(alt - Math.random() * 10),
      operator: isISS ? "NASA / Multilateral" : "SpaceX",
      launchDate,
      missionType: isISS ? "Scientific / Habitation" : "Broadband Comms",
      lastUpdated: new Date().toLocaleTimeString(),
      color: "#00ffc8", // Teal
      size: isISS ? 2.0 : 1.1,
      alt: alt / 6378,
      inclinationRad: inc * (Math.PI / 180),
      rightAscension: Math.random() * Math.PI * 2,
      orbitSpeed: 0.15 + Math.random() * 0.15,
      initialPhase: Math.random() * Math.PI * 2,
      activationTime,
    });
  }

  // 2. Generate MEO (30 satellites)
  for (let i = 1; i <= 30; i++) {
    const name = `GPS-III-SV${i < 10 ? '0' + i : i}`;
    const alt = 20180 + Math.random() * 800;
    const inc = 55.0 + Math.random() * 10;
    const launchDate = `201${Math.floor(Math.random() * 8) + 2}-0${Math.floor(Math.random() * 9) + 1}-${Math.floor(Math.random() * 20) + 10}`;

    satellites.push({
      id: `meo-${i}`,
      name,
      country: "USA",
      orbitType: "MEO",
      status: "Active",
      altitude: Math.round(alt),
      velocity: Number((3.9 - ((alt - 20000) / 10000) * 0.2).toFixed(2)),
      inclination: Number(inc.toFixed(2)),
      apogee: Math.round(alt + Math.random() * 50),
      perigee: Math.round(alt - Math.random() * 50),
      operator: "US Space Force",
      launchDate,
      missionType: "Navigation / GPS",
      lastUpdated: new Date().toLocaleTimeString(),
      color: "#ffc857", // Gold
      size: 1.4,
      alt: alt / 20000 + 0.15,
      inclinationRad: inc * (Math.PI / 180),
      rightAscension: Math.random() * Math.PI * 2,
      orbitSpeed: 0.05 + Math.random() * 0.05,
      initialPhase: Math.random() * Math.PI * 2,
      activationTime,
    });
  }

  // 3. Generate GEO (30 satellites)
  for (let i = 1; i <= 30; i++) {
    const name = `INMARSAT-5-F${i}`;
    const alt = 35786;
    const inc = Math.random() * 1.5;
    const launchDate = `201${Math.floor(Math.random() * 6) + 3}-0${Math.floor(Math.random() * 9) + 1}-${Math.floor(Math.random() * 20) + 10}`;

    satellites.push({
      id: `geo-${i}`,
      name,
      country: "UK",
      orbitType: "GEO",
      status: "Active",
      altitude: alt,
      velocity: 3.07,
      inclination: Number(inc.toFixed(2)),
      apogee: 35790,
      perigee: 35782,
      operator: "Inmarsat",
      launchDate,
      missionType: "Global Telecom",
      lastUpdated: new Date().toLocaleTimeString(),
      color: "#ff4d4d", // Red
      size: 1.6,
      alt: 0.52,
      inclinationRad: inc * (Math.PI / 180),
      rightAscension: Math.random() * Math.PI * 2,
      orbitSpeed: 0.02 + Math.random() * 0.02,
      initialPhase: Math.random() * Math.PI * 2,
      activationTime,
    });
  }

  // 4. Generate Debris (40 satellites)
  const debrisNames = ["FENGYUN 1C DEBRIS", "IRIDIUM 33 DEBRIS", "COSMOS 2251 DEBRIS", "DELTA 2 R/B", "SL-16 R/B", "TITAN 3C DEBRIS"];
  for (let i = 1; i <= 40; i++) {
    const name = `${debrisNames[Math.floor(Math.random() * debrisNames.length)]} [#${Math.floor(Math.random() * 90000) + 10000}]`;
    const alt = 300 + Math.random() * 2200;
    const inc = Math.random() * 120;
    const launchDate = `19${Math.floor(Math.random() * 40) + 60}-0${Math.floor(Math.random() * 9) + 1}-${Math.floor(Math.random() * 20) + 10}`;

    satellites.push({
      id: `debris-${i}`,
      name,
      country: countries[Math.floor(Math.random() * countries.length)],
      orbitType: "Debris",
      status: "Debris",
      altitude: Math.round(alt),
      velocity: Number((7.9 - (alt / 1000) * 0.5).toFixed(2)),
      inclination: Number(inc.toFixed(2)),
      apogee: Math.round(alt + Math.random() * 120),
      perigee: Math.round(alt - Math.random() * 120),
      operator: "Unknown / Inactive",
      launchDate,
      missionType: "Space Debris",
      lastUpdated: new Date().toLocaleTimeString(),
      color: "#888888", // Gray
      size: 0.8,
      alt: alt / 6378,
      inclinationRad: inc * (Math.PI / 180),
      rightAscension: Math.random() * Math.PI * 2,
      orbitSpeed: 0.08 + Math.random() * 0.12,
      initialPhase: Math.random() * Math.PI * 2,
      activationTime,
    });
  }

  return satellites;
};

export default function SSAModePage() {
  const globeRef = useRef<any>(null);
  const [mounted, setMounted] = useState(false);

  // SSA Mode State Machine
  const [ssaMode, setSsaMode] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [transitionProgress, setTransitionProgress] = useState(0);
  const [transitionText, setTransitionText] = useState("");
  const [ssaStartTime, setSsaStartTime] = useState(0);

  // Core Data
  const [satellites, setSatellites] = useState<SSASatellite[]>([]);
  const [selectedSatellite, setSelectedSatellite] = useState<SSASatellite | null>(null);

  // Filters & Search
  const [searchQuery, setSearchQuery] = useState("");
  const [orbitFilter, setOrbitFilter] = useState<"ALL" | "LEO" | "MEO" | "GEO" | "Debris">("ALL");

  // UTC Clock
  const [utcTime, setUtcTime] = useState("");
  const [logs, setLogs] = useState<string[]>([
    "INITIALIZING SSA OS TELEMETRY KERNEL...",
    "WAITING FOR USER INITIATION TRANSIT VECTOR..."
  ]);

  useEffect(() => {
    setMounted(true);
    const interval = setInterval(() => {
      setUtcTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Log Telemetry Random Updates
  useEffect(() => {
    if (!ssaMode) return;

    const interval = setInterval(() => {
      const messages = [
        "TELEMETRY PACKET DOWNLINK VERIFIED - SCAN SECTOR NOMINAL",
        "ORBITAL DECAY SWEEP REGISTERED ON DEBRIS ARRAYS",
        "AI ANOMALY RISK MATRIX RESOLVED - CONJUNCTION RATING: 0.02%",
        "GPS TELEMETRY ALIGNMENT CONVERGED WITHIN 3mm EPSILON",
        "WARNING: MINOR SOLAR DRIFT IN LEO PLANE SEGMENT-C4",
        "GUARDIAN-EYE-1 SECURE DOWNLINK TRANSMITTING LINK VECTORS"
      ];
      const randomMsg = messages[Math.floor(Math.random() * messages.length)];
      setLogs((prev) => [`[${new Date().toLocaleTimeString()}] ${randomMsg}`, ...prev.slice(0, 5)]);
    }, 5000);

    return () => clearInterval(interval);
  }, [ssaMode]);

  if (!mounted) return null;

  // Transition to SSA Mode (Cinematic loader)
  const handleActivateSSA = () => {
    if (isTransitioning || ssaMode) return;
    setIsTransitioning(true);
    setLogs((prev) => [`[${new Date().toLocaleTimeString()}] TRIGGERING SSA SYSTEM SCAN VECTOR...`, ...prev]);

    const loadingTexts = [
      "SYNCHRONIZING RADAR ANTENNA ARRAY...",
      "ACQUIRING COPERNICUS ORBITAL EPHEMERIDES...",
      "RESOLVING CONJUNCTION COLLISION POLYNOMIALS...",
      "SSA TELEMETRY LOCK ESTABLISHED!"
    ];

    let progress = 0;
    const interval = setInterval(() => {
      progress += 25;
      setTransitionProgress(progress);
      setTransitionText(loadingTexts[progress / 25 - 1]);

      if (progress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          const now = Date.now();
          setSsaStartTime(now);
          setSatellites(generateSSASatellites(now));
          setSsaMode(true);
          setIsTransitioning(false);
          setLogs((prev) => [
            `[${new Date().toLocaleTimeString()}] SSA MODE ACTIVE. Constellation points deployed.`,
            ...prev
          ]);
        }, 600);
      }
    }, 600);
  };

  // Fly Camera to Selected Satellite
  const handleSelectSatellite = (sat: SSASatellite) => {
    setSelectedSatellite(sat);
    
    // Focus camera on selected satellite coordinates
    if (globeRef.current) {
      globeRef.current.pointOfView(
        {
          lat: 10,
          lng: 0,
          altitude: 1.6
        },
        1200
      );
    }
    setLogs((prev) => [`[${new Date().toLocaleTimeString()}] LOCKED TRANSLATIONAL TELEMETRY: ${sat.name}`, ...prev]);
  };

  // Filters calculation
  const filteredSatellites = satellites.filter((sat) => {
    const matchesQuery =
      sat.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sat.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sat.operator.toLowerCase().includes(searchQuery.toLowerCase());
    
    if (orbitFilter === "ALL") return matchesQuery;
    return sat.orbitType === orbitFilter && matchesQuery;
  });

  return (
    <div className="relative min-h-screen bg-[#050816] text-white overflow-hidden flex flex-col pt-20 select-none crt-scanlines">
      {/* Space Starry Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,229,255,0.03)_0%,transparent_75%)] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none z-0" />

      {/* Top Navbar */}
      <Navbar />

      {/* Sub Header HUD Stats */}
      <div className="border-b border-white/10 bg-[#050816]/90 py-2.5 z-30 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-3">
          <div className="flex items-center gap-3">
            <Radio className="w-4 h-4 text-status-accent animate-pulse" />
            <span className="font-mono text-[10px] tracking-widest text-text-secondary uppercase">
              DEEP-SPACE SATELLITE SITUATIONAL AWARENESS HUB
            </span>
          </div>

          <div className="flex items-center gap-6 font-mono text-[10px]">
            <div className="flex items-center gap-2">
              <Clock className="w-3.5 h-3.5 text-status-accent" />
              <span className="text-text-secondary">UTC TIME:</span>
              <span className="text-white font-bold">{utcTime || "SYNCING..."}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-1.5 h-1.5 rounded-full bg-status-safe animate-ping" />
              <span className="text-text-secondary">OS CAPTURE:</span>
              <span className="text-status-safe font-bold">ONLINE</span>
            </div>
          </div>
        </div>
      </div>

      {/* MAIN CONTAINER LAYOUT */}
      <div className="flex-grow w-full max-w-7xl mx-auto px-6 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10 items-stretch">
        
        {/* LEFT COLUMN: Satellite Info Panel */}
        <div className="lg:col-span-3 flex flex-col justify-start">
          <AnimatePresence mode="wait">
            {selectedSatellite ? (
              <motion.div
                key={selectedSatellite.id}
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -30 }}
                transition={{ duration: 0.3 }}
                className="h-full flex flex-col"
              >
                <GlassCard glowColor="accent" className="flex-grow flex flex-col justify-between p-5 space-y-4">
                  <div className="space-y-4 flex-grow">
                    {/* Header */}
                    <div className="flex items-center justify-between border-b border-white/10 pb-3">
                      <div className="flex items-center gap-2">
                        <Satellite className="w-4 h-4" style={{ color: selectedSatellite.color }} />
                        <h3 className="font-mono font-bold text-xs tracking-wider uppercase text-white">
                          UNIT DATALINK LOCK
                        </h3>
                      </div>
                      <button
                        onClick={() => setSelectedSatellite(null)}
                        className="text-text-secondary hover:text-white transition-colors cursor-pointer"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>

                    {/* Satellite Avatar */}
                    <div className="flex flex-col items-center justify-center p-4 border border-white/5 bg-white/5 rounded-xl relative overflow-hidden">
                      <div className="absolute top-2 left-2 flex items-center gap-1 font-mono text-[7px] text-text-secondary uppercase">
                        <Activity className="w-2.5 h-2.5" style={{ color: selectedSatellite.color }} />
                        Active Sweep
                      </div>
                      <div className="w-16 h-16 rounded-full border border-white/10 flex items-center justify-center bg-black/40 relative">
                        <Satellite className="w-8 h-8 animate-pulse" style={{ color: selectedSatellite.color }} />
                        <div
                          className="absolute inset-0 rounded-full border animate-ping opacity-30"
                          style={{ borderColor: selectedSatellite.color }}
                        />
                      </div>
                      <h4 className="font-display font-bold text-sm text-white mt-3 text-center">{selectedSatellite.name}</h4>
                      <p className="font-mono text-[9px] text-text-secondary mt-1">{selectedSatellite.operator.toUpperCase()}</p>
                    </div>

                    {/* Specs Grid */}
                    <div className="space-y-2.5 font-mono text-[10px] text-text-secondary">
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>ORIGIN COUNTRY:</span>
                        <span className="text-white font-bold">{selectedSatellite.country}</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>ORBIT CLASSIFY:</span>
                        <span className="font-bold uppercase" style={{ color: selectedSatellite.color }}>
                          {selectedSatellite.orbitType}
                        </span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>MISSION FOCUS:</span>
                        <span className="text-white font-bold text-right">{selectedSatellite.missionType}</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>ALTITUDE APEX:</span>
                        <span className="text-white font-bold">{selectedSatellite.altitude} KM</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>APOGEE / PERIGEE:</span>
                        <span className="text-white font-bold">{selectedSatellite.apogee} KM / {selectedSatellite.perigee} KM</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>ORBIT INCLINE:</span>
                        <span className="text-white font-bold">{selectedSatellite.inclination}°</span>
                      </div>
                      <div className="flex justify-between border-b border-white/5 pb-1">
                        <span>VELOCITY SCALAR:</span>
                        <span className="text-white font-bold">{selectedSatellite.velocity} KM/S</span>
                      </div>
                      <div className="flex justify-between">
                        <span>LAST DATALINK:</span>
                        <span className="text-status-accent font-bold">{selectedSatellite.lastUpdated}</span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="space-y-2 pt-4">
                    <button
                      onClick={() => {
                        setLogs((prev) => [`[${new Date().toLocaleTimeString()}] PING SENT TO ${selectedSatellite.name}. Transponder RTT: 2.14ms.`, ...prev]);
                      }}
                      className="w-full py-2.5 rounded-lg font-mono text-[10px] bg-status-accent/10 border border-status-accent hover:bg-status-accent/25 transition-all text-status-accent uppercase tracking-wider flex items-center justify-center gap-2 cursor-pointer font-bold"
                    >
                      <Radio className="w-3.5 h-3.5" />
                      Ping Transponder
                    </button>
                    <button
                      onClick={() => {
                        setLogs((prev) => [`[${new Date().toLocaleTimeString()}] INTERCEPTING TRANSMISSION DECRYPTION KEY...`, ...prev]);
                      }}
                      className="w-full py-2 rounded-lg font-mono text-[9px] bg-white/5 border border-white/10 hover:bg-white/15 transition-all text-white uppercase tracking-wider flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      Intercept Signal
                    </button>
                  </div>
                </GlassCard>
              </motion.div>
            ) : (
              <motion.div
                key="empty-left"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full flex flex-col"
              >
                <GlassCard className="flex-grow flex flex-col justify-between p-5 text-center">
                  <div className="space-y-4 flex-grow flex flex-col justify-center items-center">
                    <Compass className="w-10 h-10 text-text-muted animate-pulse" />
                    <h3 className="font-display font-bold text-xs uppercase tracking-widest text-text-secondary">
                      ORBITAL SWEEP PENDING
                    </h3>
                    <p className="font-mono text-[10px] text-text-muted max-w-[200px] leading-relaxed">
                      {ssaMode
                        ? "Select a satellite glowing marker on the globe or list to synchronize real-time telemetry downlink channels."
                        : "Activate Space Situational Awareness mode by clicking on the Earth to deploy transponder trackers."}
                    </p>
                  </div>

                  {/* Live Feed Terminal Logs */}
                  <div className="border border-white/5 bg-black/40 p-3 rounded-lg text-left font-mono text-[8px] space-y-1.5 text-text-secondary overflow-hidden max-h-[160px]">
                    <div className="flex items-center gap-1 border-b border-white/5 pb-1 mb-1 text-[9px] font-bold text-status-accent">
                      <Database className="w-3 h-3" />
                      TELEMETRY KERNEL LOGS
                    </div>
                    {logs.map((log, index) => (
                      <div key={index} className="truncate select-text">
                        {log}
                      </div>
                    ))}
                  </div>
                </GlassCard>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* CENTER COLUMN: The 3D Globe Visualizer */}
        <div className="lg:col-span-6 flex flex-col justify-center items-center relative min-h-[400px]">
          <SSAGlobe
            globeRef={globeRef}
            ssaMode={ssaMode}
            isTransitioning={isTransitioning}
            transitionProgress={transitionProgress}
            transitionText={transitionText}
            ssaStartTime={ssaStartTime}
            satellites={satellites}
            selectedSatellite={selectedSatellite}
            orbitFilter={orbitFilter}
            onSelectSatellite={handleSelectSatellite}
            onActivateSSA={handleActivateSSA}
          />
        </div>

        {/* RIGHT COLUMN: Satellite List & Filters */}
        <div className="lg:col-span-3 flex flex-col justify-start">
          <GlassCard className="h-full flex flex-col p-5 space-y-4">
            
            {/* Header */}
            <div className="flex items-center gap-2 border-b border-white/10 pb-3">
              <SlidersHorizontal className="w-4 h-4 text-status-accent" />
              <h3 className="font-mono font-bold text-xs tracking-wider uppercase text-white">
                CONSTELLATION INDEX
              </h3>
            </div>

            {/* Search Input */}
            <div className="relative">
              <input
                type="text"
                placeholder="SEARCH DESIGNATOR..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                disabled={!ssaMode}
                className="w-full bg-black/40 border border-white/10 rounded-lg px-3 py-2 text-[10px] font-mono placeholder-text-muted focus:outline-none focus:border-status-accent transition-colors disabled:opacity-50"
              />
              <Search className="w-3.5 h-3.5 absolute right-3 top-2.5 text-text-muted" />
            </div>

            {/* Orbit Category Switcher */}
            <div className="grid grid-cols-5 gap-1 bg-white/5 border border-white/10 p-0.5 rounded-lg">
              {(["ALL", "LEO", "MEO", "GEO", "Debris"] as const).map((filter) => (
                <button
                  key={filter}
                  onClick={() => setOrbitFilter(filter)}
                  disabled={!ssaMode}
                  className={`py-1 text-[8px] font-mono rounded uppercase cursor-pointer transition-colors disabled:opacity-30 ${
                    orbitFilter === filter
                      ? "bg-white/10 text-status-accent font-bold"
                      : "bg-transparent text-text-secondary hover:text-white"
                  }`}
                >
                  {filter}
                </button>
              ))}
            </div>

            {/* Satellites List */}
            <div className="flex-grow overflow-y-auto max-h-[220px] lg:max-h-[300px] pr-1 space-y-1.5 min-h-[160px]">
              {ssaMode ? (
                filteredSatellites.length > 0 ? (
                  filteredSatellites.map((sat) => {
                    const isSelected = selectedSatellite?.id === sat.id;
                    return (
                      <div
                        key={sat.id}
                        onClick={() => handleSelectSatellite(sat)}
                        className={`flex items-center justify-between p-2 rounded-lg border font-mono text-[9px] cursor-pointer transition-all ${
                          isSelected
                            ? "bg-white/5 border-status-accent shadow-[0_0_10px_rgba(0,229,255,0.1)]"
                            : "bg-transparent border-white/5 hover:bg-white/5"
                        }`}
                      >
                        <div className="flex items-center gap-2 truncate">
                          <span
                            className="w-1.5 h-1.5 rounded-full"
                            style={{ backgroundColor: sat.color }}
                          />
                          <span className="font-bold text-white truncate">{sat.name}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-text-secondary text-[8px]">{sat.orbitType}</span>
                          <ChevronRight className="w-3 h-3 text-text-muted" />
                        </div>
                      </div>
                    );
                  })
                ) : (
                  <div className="py-8 text-center font-mono text-[9px] text-text-muted italic">
                    NO RECORD MATCHING SEARCH
                  </div>
                )
              ) : (
                <div className="py-12 text-center font-mono text-[9px] text-text-muted italic leading-relaxed uppercase">
                  WAITING FOR SSA INITIALIZATION DATA STREAM...
                </div>
              )}
            </div>

            {/* Quick Actions Footer */}
            <div className="pt-2 border-t border-white/5 space-y-2">
              <button
                disabled={!ssaMode}
                onClick={() => {
                  setLogs((prev) => [`[${new Date().toLocaleTimeString()}] INITIATING CONJUNCTION WARNING SWEEP...`, ...prev]);
                }}
                className="w-full py-2 rounded-lg font-mono text-[9px] bg-status-critical/10 border border-status-critical/30 hover:bg-status-critical/20 transition-all text-status-critical uppercase tracking-wider flex items-center justify-center gap-1.5 cursor-pointer disabled:opacity-50"
              >
                <ShieldAlert className="w-3.5 h-3.5" />
                Audit Threat Level
              </button>

              <button
                onClick={() => {
                  setSsaMode(false);
                  setSelectedSatellite(null);
                  setSatellites([]);
                  setLogs([
                    "TELEMETRY STREAM RESET. DISCONNECTING SWEPT RECEIVERS.",
                    "WAITING FOR SSA INITIAL VECTOR..."
                  ]);
                }}
                disabled={!ssaMode}
                className="w-full py-1.5 rounded-lg font-mono text-[8px] bg-white/5 border border-white/5 hover:bg-white/10 transition-all text-text-secondary hover:text-white uppercase tracking-wider flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50"
              >
                <RefreshCw className="w-3 h-3" />
                Reset SSA Mode
              </button>
            </div>
          </GlassCard>
        </div>

      </div>
    </div>
  );
}
