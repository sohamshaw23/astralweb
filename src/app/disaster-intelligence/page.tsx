"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useMissionData, DisasterAlert } from "@/hooks/useMissionData";
import { EarthGlobe } from "@/components/globe/earth-globe";
import {
  DisasterEvent,
  EventRow,
  IntelligenceDrawer,
  WildfireMonitor,
  CycloneTracker,
  FloodHeatmap,
} from "@/components/disaster/disaster-map";
import { Globe, AlertTriangle, ShieldAlert } from "lucide-react";

export default function DisasterIntelligencePage() {
  const { satellites } = useMissionData();
  const [utcTime, setUtcTime] = useState("");
  const [selectedEvent, setSelectedEvent] = useState<DisasterEvent | null>(null);

  // Layer toggles above map: wildfire | cyclone | flood | storm
  const [filterLayers, setFilterLayers] = useState({
    wildfire: true,
    cyclone: true,
    flood: true,
    storm: true,
  });

  const disasterEvents: DisasterEvent[] = [
    { id: "de-1", type: "wildfire", name: "NSW-WILDFIRE-09", location: "Australia, NSW", severity: 5, population: "145,000", satellite: "CARTOSAT-3", status: "ACTIVE", coordinates: [-33, 150] },
    { id: "de-2", type: "cyclone", name: "CYCLONE-IND-04", location: "India, Bay of Bengal", severity: 4, population: "1.2 Million", satellite: "RISAT-1A", status: "ACTIVE", coordinates: [15, 88] },
    { id: "de-3", type: "flood", name: "MEKONG-BASIN-FLOOD", location: "Southeast Asia", severity: 3, population: "840,000", satellite: "ZENITH-01", status: "MONITORING", coordinates: [10, 105] },
    { id: "de-4", type: "storm", name: "PACIFIC-TYPHOON-B", location: "West Pacific", severity: 2, population: "320,000", satellite: "ZENITH-02", status: "MONITORING", coordinates: [20, 130] },
  ];

  const countBadges = {
    wildfire: disasterEvents.filter((e) => e.type === "wildfire").length,
    cyclone: disasterEvents.filter((e) => e.type === "cyclone").length,
    flood: disasterEvents.filter((e) => e.type === "flood").length,
    storm: disasterEvents.filter((e) => e.type === "storm").length,
  };

  useEffect(() => {
    const clock = setInterval(() => {
      setUtcTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(clock);
  }, []);

  // Filtered disaster alert mapping for EarthGlobe component
  const mappedAlerts: DisasterAlert[] = disasterEvents
    .filter((e) => filterLayers[e.type])
    .map((e) => ({
      id: e.id,
      type: e.type,
      severity: e.severity >= 4 ? "critical" : e.severity >= 3 ? "warning" : "info",
      location: e.location,
      coordinates: e.coordinates,
    }));

  const mockGlobeLayers = {
    satellites: false,
    debris: false,
    orbits: false,
    disasters: true, // disasters layer enabled
    assets: false,
  };

  const handleToggleFilter = (key: keyof typeof filterLayers) => {
    setFilterLayers((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="relative min-h-screen bg-bg-void text-text-primary overflow-x-hidden flex flex-col pt-20 px-6 pb-6 select-none">
      
      {/* Background visual layers */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(0,229,255,0.02)_0%,transparent_75%)] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.012)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.012)_1px,transparent_1px)] bg-[size:5rem_5rem] pointer-events-none z-0" />

      {/* Header Bar */}
      <div className="border-b border-white/10 bg-bg-void/85 py-3 mb-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-4">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs font-bold text-status-accent uppercase tracking-widest">
              CRISIS VECTOR DATA INTERFACES
            </span>
          </div>

          <div className="flex items-center gap-2 bg-status-warning/10 border border-status-warning/30 px-3 py-1 rounded text-status-warning font-mono text-[10px] font-bold tracking-widest">
            <ShieldAlert className="w-3.5 h-3.5" /> HAZARD VECTOR STREAMS ACTIVE
          </div>
        </div>
      </div>

      {/* Main Panel Core Grid */}
      <main className="max-w-7xl mx-auto w-full flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10 pt-4 items-stretch">
        
        {/* Left Sidebars (25% / 3 cols) */}
        <section className="lg:col-span-3 flex flex-col space-y-6">
          <div className="p-4 bg-bg-surface/70 border border-white/10 rounded-xl space-y-4">
            <div className="font-display font-bold text-xs uppercase tracking-wider text-white">
              Hazard Layer Selector
            </div>
            <div className="space-y-2">
              {(Object.keys(filterLayers) as Array<keyof typeof filterLayers>).map((key) => {
                const active = filterLayers[key];
                return (
                  <button
                    key={key}
                    onClick={() => handleToggleFilter(key)}
                    className={`w-full flex justify-between items-center px-3 py-2 border rounded-lg font-mono text-xs uppercase tracking-wide cursor-pointer transition-all ${
                      active
                        ? "bg-status-accent/10 border-status-accent text-status-accent"
                        : "bg-transparent border-white/5 text-text-muted hover:text-text-secondary"
                    }`}
                  >
                    <span>{key}S</span>
                    <span className="bg-white/5 border border-white/10 px-1.5 py-0.5 rounded text-[9px]">
                      {countBadges[key]}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          <WildfireMonitor />
          <CycloneTracker />
          <FloodHeatmap />
        </section>

        {/* Center/Right Map and Cards (75% / 9 cols) */}
        <section className="lg:col-span-9 flex flex-col justify-between space-y-6">
          {/* Earth Globe view */}
          <div className="flex-grow flex items-center justify-center min-h-[400px] border border-white/5 bg-bg-surface/30 rounded-2xl relative overflow-hidden">
            <div className="absolute top-4 left-4 font-mono text-[9px] text-text-secondary">
              GLOBAL HAZARD THERMAL MAP OVERLAY
            </div>
            <EarthGlobe
              satellites={satellites}
              disasters={mappedAlerts}
              selectedSatellite={null}
              onSelectSatellite={() => {}}
              layers={mockGlobeLayers as any}
              onToggleLayer={() => {}}
            />
          </div>

          {/* Bottom Horizontal Card rows */}
          <div className="space-y-2">
            <div className="font-display font-bold text-xs uppercase text-white tracking-wider">
              Disaster Assessment Dossiers
            </div>
            <EventRow events={disasterEvents} onSelectEvent={setSelectedEvent} />
          </div>
        </section>
      </main>

      {/* Slide-in intelligence report panel */}
      {selectedEvent && (
        <IntelligenceDrawer event={selectedEvent} onClose={() => setSelectedEvent(null)} />
      )}

    </div>
  );
}
