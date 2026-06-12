"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useMissionData, SatelliteInfo } from "@/hooks/useMissionData";
import {
  CollisionFeed,
  CollisionModal,
  CollisionPair,
  AnomalyDetection,
  DebrisMonitoring,
  StrategicAssetTracking,
  NationalAssetScore,
  SpaceHealthIndex,
} from "@/components/mission/threat-monitor";
import { EarthGlobe } from "@/components/globe/earth-globe";
import { Shield, Eye, AlertOctagon, Terminal } from "lucide-react";

export default function GuardianModePage() {
  const { satellites, disasters } = useMissionData();
  const [utcTime, setUtcTime] = useState("");
  const [selectedSatellite, setSelectedSatellite] = useState<SatelliteInfo | null>(null);
  const [activeCollisionPair, setActiveCollisionPair] = useState<CollisionPair | null>(null);

  // Filter out disasters for Guardian Earth View (Satellites only, no disasters)
  const emptyDisasters: any[] = [];

  const [layers, setLayers] = useState({
    satellites: true,
    debris: false,
    orbits: false,
    disasters: false,
    assets: false,
  });

  const mockCollisionPairs: CollisionPair[] = [
    { id: "c-091", satA: "ZENITH-02", satB: "COSMOS-2251", mass: 1850, velocity: 14.2, timeToApproach: 84, risk: 42 },
    { id: "c-104", satA: "ZENITH-ALERT", satB: "DEBRIS-491A", mass: 900, velocity: 11.8, timeToApproach: 192, risk: 18 },
    { id: "c-312", satA: "GUARDIAN-EYE-1", satB: "METEOR-DEBRIS", mass: 2400, velocity: 15.6, timeToApproach: 312, risk: 8 },
  ];

  useEffect(() => {
    const clock = setInterval(() => {
      setUtcTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(clock);
  }, []);

  const handleAssessPair = (pair: CollisionPair) => {
    setActiveCollisionPair(pair);
  };

  const handleToggleLayer = (layer: keyof typeof layers) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  return (
    <div className="relative min-h-screen bg-[#07030c] text-text-primary overflow-x-hidden flex flex-col pt-20 px-6 pb-6 select-none border-t-4 border-status-critical/60">
      
      {/* 4% Scanlines CRT feel */}
      <div className="absolute inset-0 pointer-events-none z-30 opacity-[0.04] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[size:100%_4px,6px_100%] mix-blend-screen" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(255,77,77,0.04)_0%,transparent_80%)] pointer-events-none z-0" />
      
      {/* Top Header Command */}
      <div className="border-b border-status-critical/20 bg-[#07030c]/90 py-3 mb-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-4">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs font-bold text-status-critical uppercase tracking-widest">
              GUARDIAN DEFENSE SYSTEM OVERRIDE
            </span>
          </div>

          <div className="flex items-center gap-2 bg-status-critical/10 border border-status-critical/30 px-3 py-1 rounded text-status-critical font-mono text-[10px] font-bold tracking-widest animate-pulse">
            <AlertOctagon className="w-3.5 h-3.5" /> OVERWATCH LEVEL: ALPHA
          </div>
        </div>
      </div>

      {/* Main Core Layout grid */}
      <main className="max-w-7xl mx-auto w-full flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch relative z-10 pt-4">
        
        {/* Left Diagnostics stack (30% of viewport / 3 cols L-grid) */}
        <section className="lg:col-span-4 flex flex-col space-y-6">
          <NationalAssetScore />
          <StrategicAssetTracking />
          <AnomalyDetection />
          <DebrisMonitoring />
          <SpaceHealthIndex />
        </section>

        {/* Center Space View (Satellites only, no disasters) (40% / 5 cols) */}
        <section className="lg:col-span-4 flex flex-col items-center justify-center min-h-[400px]">
          <div className="font-mono text-[9px] text-status-critical/60 uppercase border border-status-critical/20 bg-status-critical/5 px-2 py-0.5 rounded mb-4">
            GUARDIAN SPACE TRACK ARRAY
          </div>
          <EarthGlobe
            satellites={satellites}
            disasters={emptyDisasters}
            selectedSatellite={selectedSatellite}
            onSelectSatellite={setSelectedSatellite}
            layers={layers}
            onToggleLayer={handleToggleLayer}
          />
        </section>

        {/* Right Collision Threat Matrix (30% / 4 cols) */}
        <section className="lg:col-span-4 flex flex-col">
          <CollisionFeed pairs={mockCollisionPairs} onAssess={handleAssessPair} />
        </section>

      </main>

      {/* Assessment vector path overlay modal */}
      {activeCollisionPair && (
        <CollisionModal pair={activeCollisionPair} onClose={() => setActiveCollisionPair(null)} />
      )}

    </div>
  );
}
