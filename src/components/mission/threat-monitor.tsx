"use client";

import React, { useState, useEffect } from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { Shield, ShieldCheck, AlertTriangle, Play, HelpCircle, X } from "lucide-react";

// Types
export interface CollisionPair {
  id: string;
  satA: string;
  satB: string;
  mass: number; // kg
  velocity: number; // km/s
  timeToApproach: number; // seconds
  risk: number; // %
}

// --- COLLISION MODAL COMPONENT ---
export function CollisionModal({ pair, onClose }: { pair: CollisionPair; onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 p-4 font-mono select-none">
      <div className="bg-[#0f0714] border border-status-critical/40 rounded-xl p-6 max-w-lg w-full relative shadow-[0_0_50px_rgba(255,77,77,0.25)]">
        <button onClick={onClose} className="absolute top-4 right-4 text-text-secondary hover:text-white cursor-pointer">
          <X className="w-5 h-5" />
        </button>

        <h3 className="font-display font-bold text-lg text-white mb-2 tracking-widest text-status-critical uppercase">
          CONJUNCTION ASSESSMENT DIRECTIVE
        </h3>
        <p className="text-[10px] text-text-secondary border-b border-white/10 pb-3 mb-4">
          SECTOR CONVERGENCE CONE // REF: {pair.id}
        </p>

        {/* Converging Path SVG visualizer */}
        <div className="relative w-full h-44 border border-white/5 bg-black/60 rounded-lg flex items-center justify-center overflow-hidden mb-6">
          <svg className="w-full h-full" viewBox="0 0 200 100">
            {/* Grid background */}
            <defs>
              <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                <path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255, 255, 255, 0.03)" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />

            {/* Path A */}
            <path
              d="M 20 20 L 100 50"
              fill="none"
              stroke="var(--status-safe)"
              strokeWidth="1.5"
              strokeDasharray="2 2"
              className="animate-pulse"
            />
            {/* Path B */}
            <path
              d="M 20 80 L 100 50"
              fill="none"
              stroke="var(--status-critical)"
              strokeWidth="1.5"
            />

            {/* Projected Drift cones */}
            <polygon points="100,50 150,30 150,70" fill="rgba(255, 77, 77, 0.15)" stroke="rgba(255, 77, 77, 0.3)" strokeWidth="0.5" />

            {/* Danger Impact Hub */}
            <circle cx="100" cy="50" r="10" fill="none" stroke="var(--status-critical)" strokeWidth="1" className="animate-ping" style={{ animationDuration: '2s' }} />
            <circle cx="100" cy="50" r="4" fill="var(--status-critical)" />

            {/* Satellite Icons */}
            <circle cx="40" cy="27.5" r="3" fill="var(--status-safe)" />
            <circle cx="40" cy="72.5" r="3" fill="var(--status-critical)" />

            {/* Labels */}
            <text x="45" y="26" fill="var(--text-secondary)" fontSize="6">{pair.satA}</text>
            <text x="45" y="77" fill="var(--text-secondary)" fontSize="6">{pair.satB}</text>
            <text x="105" y="47" fill="var(--status-critical)" fontSize="7" fontWeight="bold">CONJUNCTION POINT</text>
          </svg>
        </div>

        <div className="grid grid-cols-2 gap-4 text-xs text-text-secondary mb-6">
          <div>
            <div>CLOSING VELOCITY</div>
            <div className="font-bold text-white text-sm mt-0.5">{pair.velocity} KM/S</div>
          </div>
          <div>
            <div>COMBINED MASS</div>
            <div className="font-bold text-white text-sm mt-0.5">{pair.mass.toLocaleString()} KG</div>
          </div>
          <div>
            <div>ETA TO CLOSEST</div>
            <div className="font-bold text-status-critical text-sm mt-0.5">{pair.timeToApproach} SEC</div>
          </div>
          <div>
            <div>COLLISION PROBABILITY</div>
            <div className={`font-bold text-sm mt-0.5 ${pair.risk > 30 ? "text-status-critical" : "text-status-warning"}`}>
              {pair.risk}%
            </div>
          </div>
        </div>

        <div className="flex gap-3">
          <button className="flex-1 bg-status-critical hover:bg-status-critical/80 text-white font-bold py-2.5 rounded-lg text-xs tracking-wider transition-colors cursor-pointer">
            TRIGGER ESCAPE MANEUVER
          </button>
          <button onClick={onClose} className="flex-1 bg-white/5 border border-white/10 hover:bg-white/10 text-white py-2.5 rounded-lg text-xs font-bold transition-colors cursor-pointer">
            DISMISS ALERT
          </button>
        </div>
      </div>
    </div>
  );
}

// --- COLLISION FEED LISTING COMPONENT ---
export function CollisionFeed({ pairs, onAssess }: { pairs: CollisionPair[]; onAssess: (p: CollisionPair) => void }) {
  return (
    <GlassCard glowColor="critical" className="space-y-4 h-full flex flex-col justify-start">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <AlertTriangle className="w-4 h-4 text-status-critical animate-pulse" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          CONJUNCTION FORECAST MATRIX
        </h3>
      </div>

      <div className="overflow-x-auto flex-grow">
        <table className="w-full text-left font-mono text-[10px] text-text-secondary border-collapse">
          <thead>
            <tr className="border-b border-white/5 text-text-muted">
              <th className="py-2">UNIT PAIR</th>
              <th className="py-2">ETA TO IMPACT</th>
              <th className="py-2">VELOCITY</th>
              <th className="py-2">RISK %</th>
              <th className="py-2 text-right">ACTION</th>
            </tr>
          </thead>
          <tbody>
            {pairs.map((pair) => (
              <tr key={pair.id} className="border-b border-white/5 hover:bg-white/2 transition-colors">
                <td className="py-3 font-bold text-white">
                  {pair.satA} <span className="text-text-muted font-normal">v/s</span> {pair.satB}
                </td>
                <td className="py-3 text-status-warning font-semibold">
                  {pair.timeToApproach} SEC
                </td>
                <td className="py-3">{pair.velocity} km/s</td>
                <td className={`py-3 font-bold ${
                  pair.risk > 30 ? "text-status-critical animate-pulse" : "text-status-warning"
                }`}>
                  {pair.risk}%
                </td>
                <td className="py-3 text-right">
                  <button
                    onClick={() => onAssess(pair)}
                    className="bg-status-critical/10 border border-status-critical/30 hover:bg-status-critical/20 px-2 py-1 rounded text-[8px] font-bold text-status-critical tracking-widest cursor-pointer transition-all"
                  >
                    ASSESS
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassCard>
  );
}

// --- ORBITAL ANOMALY DEVIATION COMPONENT ---
export function AnomalyDetection() {
  const anomalies = [
    { id: "an-01", name: "UNIDENTIFIED-CONSTELLATION-D", exp: "540km (LEO)", dev: 12.4, score: 89, status: "CONFIRMED" },
    { id: "an-02", name: "SAT-NAV-SHUFFLE", exp: "20,180km (MEO)", dev: 4.8, score: 62, status: "INVESTIGATING" },
  ];

  return (
    <GlassCard glowColor="critical" className="space-y-4">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <HelpCircle className="w-4 h-4 text-status-critical" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          ORBITAL ANOMALIES & DEVIATIONS
        </h3>
      </div>

      <div className="space-y-4 font-mono text-[10px]">
        {anomalies.map((anom, idx) => (
          <div key={idx} className="p-3 bg-white/2 border border-white/5 rounded-lg space-y-3">
            <div className="flex justify-between items-start">
              <div>
                <div className="text-white font-bold">{anom.name}</div>
                <div className="text-[8px] text-text-muted mt-0.5">DEV: {anom.dev}% // TARGET ALT: {anom.exp}</div>
              </div>
              <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                anom.status === "CONFIRMED"
                  ? "bg-status-critical/15 text-status-critical border border-status-critical/20"
                  : "bg-status-warning/15 text-status-warning border border-status-warning/20"
              }`}>
                {anom.status}
              </span>
            </div>

            {/* Mini SVG path comparison */}
            <div className="h-10 border border-white/5 bg-black/40 rounded flex items-center justify-center overflow-hidden">
              <svg className="w-full h-full" viewBox="0 0 100 20">
                {/* Reference Path */}
                <path d="M 10 10 Q 50 2 90 10" fill="none" stroke="rgba(0, 229, 255, 0.4)" strokeWidth="0.75" strokeDasharray="2 2" />
                {/* Deviated actual Path */}
                <path d="M 10 10 Q 50 16 90 10" fill="none" stroke="var(--status-critical)" strokeWidth="1" />
                {/* Pulse Warning Node */}
                <circle cx="50" cy="13" r="2.5" fill="var(--status-critical)" className="animate-ping" />
              </svg>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

// --- DEBRIS MONITORING HEAT-RING GAUGE ---
export function DebrisMonitoring() {
  const bands = [
    { name: "LEO", density: 87, status: "critical", color: "text-status-critical" },
    { name: "MEO", density: 43, status: "warning", color: "text-status-warning" },
    { name: "GEO", density: 29, status: "safe", color: "text-status-safe" },
  ];

  return (
    <GlassCard glowColor="warning" className="space-y-4">
      <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
        DEBRIS DENSITY BY ORBITAL BAND
      </div>

      <div className="grid grid-cols-3 gap-4 font-mono text-center">
        {bands.map((band) => (
          <div key={band.name} className="p-3 bg-white/2 border border-white/5 rounded-lg space-y-2">
            <div className="text-[10px] text-text-secondary">{band.name} BAND</div>
            <div className={`text-xl font-bold ${band.color}`}>{band.density}%</div>
            <div className="text-[8px] text-text-muted">TREND: +2.1%</div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

// --- STRATEGIC ASSET TRACKING COMPONENT ---
export function StrategicAssetTracking() {
  const assets = [
    { name: "NavIC-1A", type: "NAVIGATION", health: 98, status: "SHIELD ACTIVE" },
    { name: "CARTOSAT-2E", type: "IMAGING", health: 94, status: "SHIELD ACTIVE" },
    { name: "RISAT-1A", type: "RADAR", health: 96, status: "SHIELD ACTIVE" },
    { name: "GSAT-31", type: "COMM", health: 82, status: "VULNERABLE" },
  ];

  return (
    <GlassCard glowColor="safe" className="space-y-4">
      <div className="flex items-center gap-2 border-b border-white/10 pb-2">
        <Shield className="w-4 h-4 text-status-safe" />
        <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
          NATIONAL Constellation OVERWATCH
        </h3>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {assets.map((asset, idx) => (
          <div key={idx} className="p-3 bg-white/2 border border-white/5 rounded-lg flex flex-col justify-between font-mono text-[9px] relative overflow-hidden">
            {/* Asset header */}
            <div className="space-y-1">
              <span className="text-white font-bold text-[10px]">{asset.name}</span>
              <div className="text-text-muted">{asset.type}</div>
            </div>

            {/* Health indicators */}
            <div className="mt-4 flex items-center justify-between">
              <span className={asset.status === "SHIELD ACTIVE" ? "text-status-safe font-semibold" : "text-status-warning font-semibold"}>
                {asset.status}
              </span>
              <div className="relative w-8 h-8 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90">
                  <circle cx="16" cy="16" r="12" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="2" />
                  <circle
                    cx="16"
                    cy="16"
                    r="12"
                    fill="none"
                    stroke={asset.status === "SHIELD ACTIVE" ? "var(--status-safe)" : "var(--status-warning)"}
                    strokeWidth="2"
                    strokeDasharray={`${2 * Math.PI * 12}`}
                    strokeDashoffset={`${2 * Math.PI * 12 * (1 - asset.health / 100)}`}
                    className={asset.status === "SHIELD ACTIVE" ? "animate-spin origin-center" : ""}
                    style={{ animationDuration: '10s' }}
                  />
                </svg>
                <span className="absolute text-[7px] text-white font-bold">{asset.health}%</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}

// --- NATIONAL ASSET HEALTH SCORE ---
export function NationalAssetScore() {
  return (
    <GlassCard glowColor="safe" className="flex items-center gap-6 py-4">
      {/* Large radial progress */}
      <div className="relative w-16 h-16 flex items-center justify-center shrink-0">
        <svg className="w-full h-full transform -rotate-90">
          <circle cx="32" cy="32" r="26" fill="none" stroke="rgba(0, 255, 200, 0.1)" strokeWidth="4" />
          <circle
            cx="32"
            cy="32"
            r="26"
            fill="none"
            stroke="var(--status-safe)"
            strokeWidth="4"
            strokeDasharray={`${2 * Math.PI * 26}`}
            strokeDashoffset={`${2 * Math.PI * 26 * (1 - 0.97)}`}
          />
        </svg>
        <span className="absolute font-mono text-sm font-extrabold text-white">97%</span>
      </div>

      <div className="space-y-1 font-mono text-[10px]">
        <div className="text-white font-bold uppercase text-xs">ASSET HEALTH INDEX</div>
        <div className="text-text-secondary">NOMINAL SATELLITES OPERATIONAL</div>
        <div className="text-text-muted">LAST SWEEP CALIBRATION: 2S AGO</div>
      </div>
    </GlassCard>
  );
}

// --- SPACE HEALTH COMPOSITE INDEX CHART ---
export function SpaceHealthIndex() {
  const metrics = [
    { label: "Debris Density", weight: 35, val: 87, color: "bg-status-critical" },
    { label: "Collision Risk", weight: 30, val: 68, color: "bg-status-warning" },
    { label: "Anomaly Count", weight: 20, val: 41, color: "bg-status-accent" },
    { label: "Congestion Index", weight: 15, val: 92, color: "bg-status-safe" },
  ];

  return (
    <GlassCard glowColor="primary" className="space-y-4">
      <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
        SPACE ENVIRONMENTAL INDEX BREAKDOWN
      </div>

      <div className="space-y-3 font-mono text-[9px] text-text-secondary">
        {metrics.map((met) => (
          <div key={met.label} className="space-y-1">
            <div className="flex justify-between">
              <span>{met.label} (w: {met.weight}%)</span>
              <span className="text-white font-bold">{met.val}%</span>
            </div>
            <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
              <div style={{ width: `${met.val}%` }} className={`h-full ${met.color}`} />
            </div>
          </div>
        ))}
      </div>
    </GlassCard>
  );
}
