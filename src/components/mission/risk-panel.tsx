"use client";

import React, { useState, useEffect } from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { Shield, ShieldAlert, Radio, AlertTriangle } from "lucide-react";
import { DisasterAlert } from "@/hooks/useMissionData";

interface RiskPanelProps {
  satelliteCount: {
    active: number;
    warning: number;
    critical: number;
  };
  disasters: DisasterAlert[];
  logs: string[];
  shimmer: boolean;
}

export function RiskPanel({ satelliteCount, disasters, logs, shimmer }: RiskPanelProps) {
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    const start = Date.now() - 3254000; // Mock started ~54 mins ago
    const timer = setInterval(() => {
      setElapsedTime(Math.floor((Date.now() - start) / 1000));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const formatElapsed = (sec: number) => {
    const h = Math.floor(sec / 3600).toString().padStart(2, "0");
    const m = Math.floor((sec % 3600) / 60).toString().padStart(2, "0");
    const s = (sec % 60).toString().padStart(2, "0");
    return `${h}:${m}:${s}`;
  };

  // Threat Needle angle map: Minimal (-60), Low (-30), Elevated (0), High (30), Critical (60)
  const needleRotation = 0; // ELEVATED is vertical pointer center

  return (
    <div className="flex flex-col space-y-6 overflow-y-auto max-h-[calc(100vh-140px)] pr-2 select-none">
      
      {/* Section 1: Mission Status */}
      <GlassCard glowColor="primary" className="space-y-4">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <Shield className="w-4 h-4 text-primary-vivid" />
          <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
            MISSION STATUS
          </h3>
        </div>

        <div className="space-y-3 font-mono text-xs text-text-secondary">
          <div className="flex justify-between">
            <span>OPERATION:</span>
            <span className="text-white font-bold">ALPHA SHIELD</span>
          </div>
          <div className="flex justify-between">
            <span>PHASE:</span>
            <span className="text-status-accent font-bold">ORBIT SECURE II</span>
          </div>
          <div className="flex justify-between">
            <span>ELAPSED:</span>
            <span className="text-white font-bold">{formatElapsed(elapsedTime)}</span>
          </div>
        </div>
      </GlassCard>

      {/* Section 2: Threat Level Gauge */}
      <GlassCard glowColor="warning" className="space-y-4 flex flex-col items-center">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2 w-full justify-start">
          <ShieldAlert className="w-4 h-4 text-status-warning" />
          <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
            THREAT LEVEL
          </h3>
        </div>

        {/* Semi-circular dial gauge */}
        <div className="relative w-40 h-24 mt-2 flex items-end justify-center overflow-hidden">
          <svg className="w-40 h-40 absolute bottom-0" viewBox="0 0 100 100">
            {/* Color Arc Sections */}
            {/* Minimal */}
            <path d="M 15 50 A 35 35 0 0 1 85 50" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
            <path d="M 15 50 A 35 35 0 0 1 29 25" fill="none" stroke="var(--status-safe)" strokeWidth="8" opacity="0.3" />
            <path d="M 29 25 A 35 35 0 0 1 50 15" fill="none" stroke="rgba(0, 229, 255, 0.7)" strokeWidth="8" opacity="0.4" />
            <path d="M 50 15 A 35 35 0 0 1 71 25" fill="none" stroke="var(--status-warning)" strokeWidth="8" />
            <path d="M 71 25 A 35 35 0 0 1 85 50" fill="none" stroke="var(--status-critical)" strokeWidth="8" opacity="0.3" />
          </svg>

          {/* Gauge Needle */}
          <div
            style={{ transform: `rotate(${needleRotation}deg)` }}
            className="w-1 h-16 bg-status-warning origin-bottom rounded-full transition-transform duration-1000 ease-out z-10 relative bottom-0"
          />
          {/* Central Cap */}
          <div className="w-4 h-4 bg-bg-surface border-2 border-status-warning rounded-full absolute bottom-0 z-20" />
        </div>

        <div className="font-mono text-sm font-bold text-status-warning tracking-widest mt-2 uppercase">
          ELEVATED THREAT
        </div>
      </GlassCard>

      {/* Section 3: Satellite Count Telemetry */}
      <GlassCard glowColor="accent" className="space-y-4">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <Radio className="w-4 h-4 text-status-accent" />
          <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
            SATELLITE TELEMETRY
          </h3>
        </div>

        <div className={`space-y-2 font-mono text-xs transition-opacity duration-300 ${shimmer ? "opacity-60" : "opacity-100"}`}>
          <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
            <span className="text-text-secondary">ACTIVE</span>
            <span className="text-status-safe font-bold">{satelliteCount.active.toLocaleString()}</span>
          </div>
          <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
            <span className="text-text-secondary">WARNINGS</span>
            <span className="text-status-warning font-bold">{satelliteCount.warning}</span>
          </div>
          <div className="flex justify-between items-center bg-white/2 p-2 rounded border border-white/5">
            <span className="text-text-secondary">CRITICAL</span>
            <span className="text-status-critical font-bold animate-pulse">{satelliteCount.critical}</span>
          </div>
        </div>
      </GlassCard>

      {/* Section 4: Disaster Alerts */}
      <GlassCard glowColor="critical" className="space-y-4">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <AlertTriangle className="w-4 h-4 text-status-critical" />
          <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
            HAZARD BULLETINS
          </h3>
        </div>

        <div className="space-y-2">
          {disasters.map((dist) => (
            <div key={dist.id} className="p-2.5 bg-bg-void/50 border border-white/5 rounded-lg flex items-center justify-between text-[10px] font-mono">
              <div className="space-y-0.5">
                <div className="text-white font-bold">{dist.type}</div>
                <div className="text-text-muted uppercase">{dist.location}</div>
              </div>
              <span className={`px-2 py-0.5 rounded text-[8px] font-bold uppercase ${
                dist.severity === "critical"
                  ? "bg-status-critical/15 text-status-critical border border-status-critical/20"
                  : dist.severity === "warning"
                  ? "bg-status-warning/15 text-status-warning border border-status-warning/20"
                  : "bg-status-accent/15 text-status-accent border border-status-accent/20"
              }`}>
                {dist.severity}
              </span>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Section 5: Recent Events Feed */}
      <GlassCard glowColor="primary" className="space-y-4">
        <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
          LOG OVERWATCHSTREAM
        </div>
        <div className="space-y-2 h-44 overflow-y-auto pr-1 font-mono text-[9px] text-text-secondary">
          {logs.map((log, idx) => (
            <div key={idx} className="p-1 border-b border-white/5 leading-normal">
              {log}
            </div>
          ))}
        </div>
      </GlassCard>

    </div>
  );
}
export default RiskPanel;
