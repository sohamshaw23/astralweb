"use client";

import React, { useState } from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { Flame, Wind, Droplets, AlertTriangle, Compass, ShieldAlert, Cpu, Check, X } from "lucide-react";

export interface DisasterEvent {
  id: string;
  type: "wildfire" | "cyclone" | "flood" | "storm";
  name: string;
  location: string;
  severity: number; // 1-5
  population: string;
  satellite: string;
  status: "ACTIVE" | "MONITORING" | "CONTAINED";
  coordinates: [number, number];
}

// --- SLIDE-IN INTELLIGENCE DRAWER ---
export function IntelligenceDrawer({ event, onClose }: { event: DisasterEvent; onClose: () => void }) {
  const pipeline = ["INGESTION", "CORRELATION", "TASKING", "MITIGATION"];
  const currentStage = 2; // TASKING

  const icons = {
    wildfire: Flame,
    cyclone: Wind,
    flood: Droplets,
    storm: AlertTriangle,
  };
  const Icon = icons[event.type];

  return (
    <div className="fixed inset-y-0 right-0 w-80 sm:w-96 bg-[#080b18]/95 border-l border-white/10 z-50 p-6 flex flex-col justify-between shadow-[0_0_50px_rgba(0,0,0,0.8)] font-mono select-none">
      
      {/* Header Info */}
      <div className="space-y-6">
        <div className="flex justify-between items-center border-b border-white/10 pb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-status-accent">
              <Icon className="w-5 h-5 text-status-accent" />
            </div>
            <div>
              <h3 className="text-white font-bold uppercase text-sm">{event.name}</h3>
              <p className="text-[9px] text-text-secondary uppercase">{event.location}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-text-secondary hover:text-white cursor-pointer">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Severity Gauge */}
        <div className="space-y-1">
          <div className="text-[9px] text-text-secondary uppercase">Severity Level</div>
          <div className="flex gap-1.5 text-status-warning">
            {Array.from({ length: 5 }).map((_, idx) => (
              <span key={idx} className={idx < event.severity ? "text-status-warning text-sm" : "text-text-muted text-sm"}>
                ★
              </span>
            ))}
          </div>
        </div>

        {/* Dynamic Trajectory Cone SVG */}
        <div className="space-y-2">
          <div className="text-[9px] text-text-secondary uppercase">Projected 48H Trajectory Cone</div>
          <div className="h-32 border border-white/5 bg-black/40 rounded-lg flex items-center justify-center overflow-hidden">
            <svg className="w-full h-full" viewBox="0 0 100 50">
              <defs>
                <linearGradient id="coneGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="rgba(0, 229, 255, 0.4)" />
                  <stop offset="100%" stopColor="rgba(0, 229, 255, 0.02)" />
                </linearGradient>
              </defs>
              {/* Cone shape */}
              <polygon points="10,25 90,5 90,45" fill="url(#coneGrad)" />
              {/* Actual timeline path */}
              <path d="M 10 25 Q 50 15 90 20" fill="none" stroke="var(--status-accent)" strokeWidth="1" />
              {/* Time stamps */}
              <circle cx="10" cy="25" r="2.5" fill="var(--status-accent)" />
              <circle cx="50" cy="20" r="2" fill="var(--status-accent)" />
              <circle cx="90" cy="20" r="2" fill="var(--status-accent)" />
              
              <text x="8" y="33" fill="var(--text-secondary)" fontSize="5">0H</text>
              <text x="45" y="28" fill="var(--text-secondary)" fontSize="5">24H</text>
              <text x="85" y="28" fill="var(--text-secondary)" fontSize="5">48H</text>
            </svg>
          </div>
        </div>

        {/* Observation Windows */}
        <div className="p-3 bg-white/2 border border-white/5 rounded-lg space-y-1.5 text-[10px]">
          <div className="text-white font-bold uppercase">Observation Windows</div>
          <div className="flex justify-between">
            <span>OBSERVER PAYLOAD:</span>
            <span className="text-status-accent font-bold">{event.satellite}</span>
          </div>
          <div className="flex justify-between">
            <span>NEXT DOCK EPOCH:</span>
            <span className="text-white">12:35:44 UTC</span>
          </div>
        </div>

        {/* Response status pipeline */}
        <div className="space-y-2">
          <div className="text-[9px] text-text-secondary uppercase">Response Workflow Pipeline</div>
          <div className="grid grid-cols-4 gap-1.5 text-center text-[8px]">
            {pipeline.map((stage, idx) => (
              <div
                key={stage}
                className={`py-1.5 border rounded font-bold transition-colors ${
                  idx === currentStage
                    ? "bg-status-accent/10 border-status-accent text-status-accent animate-pulse"
                    : idx < currentStage
                    ? "bg-status-safe/10 border-status-safe/30 text-status-safe"
                    : "bg-transparent border-white/5 text-text-muted"
                }`}
              >
                {stage}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Footer operations CTA */}
      <button className="w-full bg-status-accent hover:bg-status-accent/80 text-bg-void font-bold py-3 rounded-lg text-xs tracking-widest cursor-pointer transition-colors">
        RE-TASK CONSTELATION
      </button>

    </div>
  );
}

// --- DISASTER EVENT ROW HORIZONTAL CARDS ---
export function EventRow({
  events,
  onSelectEvent,
}: {
  events: DisasterEvent[];
  onSelectEvent: (event: DisasterEvent) => void;
}) {
  const icons = {
    wildfire: Flame,
    cyclone: Wind,
    flood: Droplets,
    storm: AlertTriangle,
  };

  return (
    <div className="w-full relative z-10 flex gap-4 overflow-x-auto pb-4 pt-2 select-none">
      {events.map((event) => {
        const Icon = icons[event.type];
        return (
          <div
            key={event.id}
            className="min-w-[260px] flex-shrink-0 bg-bg-surface/80 border border-white/8 rounded-xl p-4 flex flex-col justify-between space-y-4 hover:border-status-accent/40 hover:bg-bg-surface transition-all duration-300"
          >
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-2">
                <Icon className="w-4 h-4 text-status-accent" />
                <span className="font-mono text-xs font-bold text-white uppercase">{event.name}</span>
              </div>
              <span className={`px-1.5 py-0.5 rounded text-[8px] font-mono font-bold ${
                event.status === "ACTIVE"
                  ? "bg-status-critical/15 text-status-critical border border-status-critical/20"
                  : event.status === "MONITORING"
                  ? "bg-status-warning/15 text-status-warning border border-status-warning/20"
                  : "bg-status-safe/15 text-status-safe border border-status-safe/20"
              }`}>
                {event.status}
              </span>
            </div>

            <div className="font-mono text-[9px] text-text-secondary space-y-1">
              <div>LOCATION: {event.location}</div>
              <div>POPULATION: {event.population}</div>
              <div>SATELLITE: {event.satellite}</div>
            </div>

            <button
              onClick={() => onSelectEvent(event)}
              className="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-white font-mono text-[9px] font-bold py-2 rounded-lg cursor-pointer tracking-wider transition-colors"
            >
              VIEW INTELLIGENCE
            </button>
          </div>
        );
      })}
    </div>
  );
}

// --- WILDFIRE MONITOR SIDEBAR ---
export function WildfireMonitor() {
  const fires = [
    { name: "NSW-09", area: 12400, cont: 14, trend: "up" },
    { name: "QUEENSLAND-04", area: 8200, cont: 42, trend: "down" },
    { name: "ALBERTA-12", area: 6500, cont: 60, trend: "down" },
  ];

  return (
    <GlassCard glowColor="critical" className="space-y-4">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <Flame className="w-4 h-4 text-status-critical" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          WILDFIRE INTELLIGENCE MONITOR
        </h3>
      </div>

      <div className="space-y-3 font-mono text-[10px] text-text-secondary">
        {fires.map((fire, idx) => (
          <div key={idx} className="p-2.5 bg-white/2 border border-white/5 rounded-lg flex items-center justify-between">
            <div className="space-y-0.5">
              <span className="text-white font-bold">{fire.name}</span>
              <div>BURN: {fire.area.toLocaleString()} HA</div>
            </div>
            <div className="text-right">
              <div>CONTAINMENT</div>
              <span className="text-status-safe font-bold">{fire.cont}%</span>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

// --- CYCLONE TRACKER SIDEBAR ---
export function CycloneTracker() {
  return (
    <GlassCard glowColor="warning" className="space-y-4">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <Wind className="w-4 h-4 text-status-warning" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          CYCLONE TRACKER VECTORS
        </h3>
      </div>

      <div className="space-y-3 font-mono text-[10px] text-text-secondary">
        <div className="p-2.5 bg-white/2 border border-white/5 rounded-lg space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-white font-bold">CYCLONE-IND-04</span>
            <span className="bg-status-critical/10 text-status-critical border border-status-critical/20 px-1 rounded text-[8px]">
              CAT 3
            </span>
          </div>
          <div>WIND: 185 KM/H</div>
          <div>LANDFALL ETA: 12H 45M</div>
        </div>
      </div>
    </GlassCard>
  );
}

// --- FLOOD HEATMAP SIDEBAR ---
export function FloodHeatmap() {
  return (
    <GlassCard glowColor="primary" className="space-y-4">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <Droplets className="w-4 h-4 text-status-accent" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          RIVER BASIN RISK SCALES
        </h3>
      </div>

      <div className="space-y-3 font-mono text-[10px] text-text-secondary">
        <div className="p-2.5 bg-white/2 border border-white/5 rounded-lg space-y-2">
          <div className="text-white font-bold">MEKONG RIVER BASIN</div>
          <div className="space-y-1">
            <div className="flex justify-between">
              <span>WATER LEVEL:</span>
              <span className="text-status-critical font-bold">14.8M (CRITICAL)</span>
            </div>
            <div className="w-full h-1 bg-white/5 rounded overflow-hidden">
              <div className="w-4/5 h-full bg-status-critical" />
            </div>
          </div>
        </div>
      </div>
    </GlassCard>
  );
}
