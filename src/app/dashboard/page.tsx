"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useMissionData, SatelliteInfo } from "@/hooks/useMissionData";
import { RiskPanel } from "@/components/mission/risk-panel";
import { AnomalyPanel } from "@/components/mission/anomaly-panel";
import { EarthGlobe } from "@/components/globe/earth-globe";
import { Terminal, ShieldAlert, Cpu } from "lucide-react";

export default function DashboardPage() {
  const {
    shimmer,
    satelliteCount,
    disasters,
    anomalies,
    riskMatrix,
    satellites,
    logs,
  } = useMissionData();

  const [utcTime, setUtcTime] = useState("");
  const [selectedSatellite, setSelectedSatellite] = useState<SatelliteInfo | null>(null);
  const [astronautMode, setAstronautMode] = useState(false);

  // Layers Toggles
  const [layers, setLayers] = useState({
    satellites: true,
    debris: true,
    orbits: true,
    disasters: true,
    assets: true,
  });

  useEffect(() => {
    const clock = setInterval(() => {
      setUtcTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(clock);
  }, []);

  const handleSelectSatellite = (sat: SatelliteInfo) => {
    setSelectedSatellite(sat);
  };

  const handleToggleLayer = (layer: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  return (
    <div
      className={`relative min-h-screen overflow-hidden flex flex-col pt-20 px-6 pb-6 select-none transition-colors duration-500 ${
        astronautMode
          ? "bg-[#020d05] text-[#00ff66] [text-shadow:0_0_5px_#00ff66]"
          : "bg-bg-void text-text-primary"
      }`}
    >
      {/* Dynamic Star Ambient Background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.012)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.012)_1px,transparent_1px)] bg-[size:5rem_5rem] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(79,70,229,0.03)_0%,transparent_75%)] pointer-events-none z-0" />

      {/* TOP COMMAND BAR */}
      <div
        className={`border-b py-3 mb-4 flex justify-between items-center transition-colors duration-500 ${
          astronautMode
            ? "border-[#00ff66]/30 bg-[#020d05]/80"
            : "border-white/10 bg-bg-void/80"
        }`}
      >
        <div className="w-full flex flex-col sm:flex-row justify-between items-center gap-4">
          {/* Left: Sub-system Branding */}
          <div className="flex items-center gap-3">
            <span className={`font-mono text-xs font-bold uppercase tracking-widest ${
              astronautMode ? "text-[#00ff66]" : "text-white"
            }`}>
              SYSTEM OVERWATCH MODULE
            </span>
          </div>

          {/* Center: System health indicator */}
          <div className="flex items-center gap-2">
            <span className="flex gap-1">
              {[1, 2, 3, 4, 5].map((dot) => (
                <span
                  key={dot}
                  className={`w-1.5 h-1.5 rounded-full ${
                    astronautMode ? "bg-[#00ff66]" : "bg-status-safe"
                  } animate-pulse`}
                />
              ))}
            </span>
            <span className={`font-mono text-[10px] font-bold ${
              astronautMode ? "text-[#00ff66]" : "text-status-safe"
            }`}>
              LEO CONST SYSTEM NOMINAL
            </span>
          </div>

          {/* Right: Mode Selector pills */}
          <div className="flex items-center gap-1.5 bg-white/5 border border-white/10 p-0.5 rounded-lg">
            <button
              onClick={() => setAstronautMode(false)}
              className={`px-3 py-1 text-[10px] font-mono rounded cursor-pointer transition-colors ${
                !astronautMode
                  ? "bg-primary text-white shadow-md"
                  : "bg-transparent text-text-secondary hover:text-white"
              }`}
            >
              STANDARD
            </button>
            <button
              onClick={() => setAstronautMode(true)}
              className={`px-3 py-1 text-[10px] font-mono rounded cursor-pointer transition-colors ${
                astronautMode
                  ? "bg-[#00ff66]/20 border border-[#00ff66] text-[#00ff66]"
                  : "bg-transparent text-text-secondary hover:text-white"
              }`}
            >
              ASTRONAUT HUD
            </button>
          </div>
        </div>
      </div>

      {/* ASTRONAUT HUD FIRST-PERSON VISOR EFFECTS */}
      {astronautMode && (
        <div className="absolute inset-0 pointer-events-none z-30 border-[16px] border-[#00ff66]/10 flex flex-col justify-between p-4">
          {/* Corner brackets overlay */}
          <div className="flex justify-between">
            <div className="w-8 h-8 border-t-2 border-l-2 border-[#00ff66]" />
            <div className="w-8 h-8 border-t-2 border-r-2 border-[#00ff66]" />
          </div>
          {/* Crosshair indicator */}
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 border border-[#00ff66]/30 rounded-full flex items-center justify-center">
            <div className="w-1.5 h-1.5 bg-[#00ff66]/60 rounded-full" />
          </div>
          <div className="flex justify-between items-end">
            <div className="w-8 h-8 border-b-2 border-l-2 border-[#00ff66]" />
            <div className="w-8 h-8 border-b-2 border-r-2 border-[#00ff66]" />
          </div>
        </div>
      )}

      {/* MAIN MISSION INTERFACES CONTROL */}
      <main className="max-w-7xl mx-auto w-full flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch relative z-10 pt-4">
        {/* Left Intelligence Panel (20%) */}
        <section className="lg:col-span-3 flex flex-col justify-start">
          <RiskPanel
            satelliteCount={satelliteCount}
            disasters={disasters}
            logs={logs}
            shimmer={shimmer}
          />
        </section>

        {/* Center Interactive Globe (60%) */}
        <section className="lg:col-span-6 flex flex-col items-center justify-center min-h-[400px]">
          <EarthGlobe
            satellites={satellites}
            disasters={disasters}
            selectedSatellite={selectedSatellite}
            onSelectSatellite={handleSelectSatellite}
            layers={layers}
            onToggleLayer={handleToggleLayer}
            autoRotate={false}
          />
        </section>

        {/* Right Intelligence Panel (20%) */}
        <section className="lg:col-span-3 flex flex-col justify-start">
          <AnomalyPanel
            selectedSatellite={selectedSatellite}
            onClearSatellite={() => setSelectedSatellite(null)}
            anomalies={anomalies}
            riskMatrix={riskMatrix}
            shimmer={shimmer}
          />
        </section>
      </main>
    </div>
  );
}
