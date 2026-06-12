"use client";

import React from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { Cpu, TrendingUp, TrendingDown, ArrowRight, ShieldCheck, Compass } from "lucide-react";
import { SatelliteInfo, AnomalyInfo } from "@/hooks/useMissionData";

interface AnomalyPanelProps {
  selectedSatellite: SatelliteInfo | null;
  onClearSatellite: () => void;
  anomalies: AnomalyInfo[];
  riskMatrix: { name: string; prob: number; imp: number; quad: number }[];
  shimmer: boolean;
}

export function AnomalyPanel({
  selectedSatellite,
  onClearSatellite,
  anomalies,
  riskMatrix,
  shimmer,
}: AnomalyPanelProps) {
  
  const aiInsights = [
    { text: "Adjust zenith payload orbit s3 angle by -0.4° to clear debris corridor.", conf: 96 },
    { text: "Schedule antenna sync with Ground Station Polar-2 within 4 mins.", conf: 89 },
    { text: "Emergency coolant throttle for Guardian constellation recommended.", conf: 74 },
  ];

  const recommendedActions = [
    { text: "Verify Space Debris Shield Link", priority: "HIGH" },
    { text: "Calibrate GEO telemetry alignment", priority: "MED" },
    { text: "Sweep sector LEO-2 conjunction", priority: "LOW" },
  ];

  return (
    <div className="flex flex-col space-y-6 overflow-y-auto max-h-[calc(100vh-140px)] pr-2 select-none">
      
      {/* Section 1: Active Selection Details */}
      <GlassCard glowColor="accent" className="space-y-4">
        <div className="flex items-center justify-between border-b border-white/10 pb-2">
          <div className="flex items-center gap-2">
            <Compass className="w-4 h-4 text-status-accent" />
            <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
              TACTICAL ASSIGNED UNIT
            </h3>
          </div>
          {selectedSatellite && (
            <button
              onClick={onClearSatellite}
              className="text-[9px] font-mono text-status-critical border border-status-critical/30 bg-status-critical/5 px-2 py-0.5 rounded hover:bg-status-critical/15 transition-colors cursor-pointer"
            >
              DESELECT
            </button>
          )}
        </div>

        {selectedSatellite ? (
          <div className={`space-y-3 font-mono text-[10px] text-text-secondary transition-opacity duration-300 ${shimmer ? "opacity-60" : "opacity-100"}`}>
            <div className="flex justify-between">
              <span>DESIGNATOR:</span>
              <span className="text-white font-bold">{selectedSatellite.name}</span>
            </div>
            <div className="flex justify-between">
              <span>STATUS:</span>
              <span className={`font-bold ${
                selectedSatellite.status === "nominal"
                  ? "text-status-safe"
                  : selectedSatellite.status === "warning"
                  ? "text-status-warning"
                  : "text-status-critical animate-pulse"
              }`}>
                {selectedSatellite.status.toUpperCase()}
              </span>
            </div>
            <div className="flex justify-between">
              <span>POSITION:</span>
              <span className="text-white">
                {selectedSatellite.latitude.toFixed(2)}°N, {selectedSatellite.longitude.toFixed(2)}°E
              </span>
            </div>
            <div className="flex justify-between">
              <span>ALTITUDE:</span>
              <span className="text-white">{selectedSatellite.altitude} KM</span>
            </div>
            <div className="flex justify-between">
              <span>VELOCITY:</span>
              <span className="text-white">{selectedSatellite.velocity} KM/S</span>
            </div>
            <div className="flex justify-between">
              <span>LINK QUALITY:</span>
              <span className="text-status-accent font-bold">{selectedSatellite.signalStrength}%</span>
            </div>
          </div>
        ) : (
          <div className="py-4 text-center text-[10px] font-mono text-text-muted italic">
            SELECT A SATELLITE MARKER ON THE GLOBE TO MOUNT LINK DATA
          </div>
        )}
      </GlassCard>

      {/* Section 2: AI Insights */}
      <GlassCard glowColor="primary" className="space-y-4">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <Cpu className="w-4 h-4 text-primary-vivid" />
          <h3 className="font-display font-bold text-xs tracking-wider uppercase text-white">
            AI OPERATIVE ADVISORY
          </h3>
        </div>

        <div className="space-y-3">
          {aiInsights.map((insight, idx) => (
            <div key={idx} className="p-2.5 bg-white/2 border border-white/5 rounded-lg text-[10px] space-y-1 font-mono leading-relaxed">
              <p className="text-white">{insight.text}</p>
              <div className="flex items-center gap-1.5 justify-end">
                <span className="text-text-muted text-[8px]">CONFIDENCE:</span>
                <span className="text-status-accent font-bold text-[9px]">{insight.conf}%</span>
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Section 3: Risk Matrix */}
      <GlassCard glowColor="warning" className="space-y-4">
        <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
          RISK PROJECTION MATRIX
        </div>

        {/* 4 Quadrants visual representation */}
        <div className="relative w-full h-32 border border-white/15 bg-black/40 rounded-lg flex flex-col justify-between p-2 font-mono text-[8px] overflow-hidden">
          {/* Grid lines */}
          <div className="absolute top-1/2 left-0 right-0 h-px border-t border-dashed border-white/10" />
          <div className="absolute left-1/2 top-0 bottom-0 w-px border-l border-dashed border-white/10" />

          {/* Quadrant labels */}
          <div className="absolute top-1 left-2 text-text-muted">HI-P / LO-I</div>
          <div className="absolute top-1 right-2 text-status-critical/60">HI-P / HI-I</div>
          <div className="absolute bottom-1 left-2 text-text-muted">LO-P / LO-I</div>
          <div className="absolute bottom-1 right-2 text-text-muted">LO-P / HI-I</div>

          {/* Plotting points */}
          {riskMatrix.map((point, idx) => {
            const bottom = point.prob * 100;
            const left = point.imp * 100;
            return (
              <div
                key={idx}
                style={{ bottom: `calc(${bottom}% - 4px)`, left: `calc(${left}% - 4px)` }}
                className="absolute w-2 h-2 rounded-full bg-status-warning shadow-[0_0_6px_var(--status-warning)] group cursor-pointer"
              >
                <div className="absolute bottom-3 left-1/2 -translate-x-1/2 bg-bg-surface border border-white/10 rounded px-1 text-[7px] text-white hidden group-hover:block whitespace-nowrap z-20">
                  {point.name}
                </div>
              </div>
            );
          })}
        </div>
      </GlassCard>

      {/* Section 4: Anomaly Alerts */}
      <GlassCard glowColor="critical" className="space-y-4">
        <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
          ORBITAL ANOMALIES REGISTER
        </div>

        <div className={`space-y-2 font-mono text-[10px] text-text-secondary transition-opacity duration-300 ${shimmer ? "opacity-60" : "opacity-100"}`}>
          {anomalies.map((anom) => (
            <div key={anom.id} className="p-2 bg-white/2 border border-white/5 rounded-lg flex items-center justify-between">
              <div className="space-y-0.5">
                <span className="text-white font-bold">{anom.source}</span>
                <div className="text-text-muted text-[8px]">{anom.timestamp} UTC</div>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="text-[8px] text-text-muted">SCORE</div>
                  <div className="font-bold text-white">{anom.score}</div>
                </div>
                {anom.trend === "up" ? (
                  <TrendingUp className="w-4 h-4 text-status-critical" />
                ) : anom.trend === "down" ? (
                  <TrendingDown className="w-4 h-4 text-status-safe" />
                ) : (
                  <div className="w-4 h-0.5 bg-text-secondary" />
                )}
              </div>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Section 5: Recommended Actions */}
      <GlassCard glowColor="primary" className="space-y-4">
        <div className="font-display font-bold text-xs tracking-wider uppercase text-white border-b border-white/10 pb-2">
          RECOMMENDED ACTUATION
        </div>

        <div className="space-y-2">
          {recommendedActions.map((act, idx) => (
            <div key={idx} className="p-2.5 bg-bg-void/50 border border-white/5 rounded-lg flex items-center justify-between text-[10px] font-mono hover:border-status-accent/30 transition-colors">
              <span className="text-white flex items-center gap-2">
                <ShieldCheck className="w-3.5 h-3.5 text-status-safe" />
                {act.text}
              </span>
              <span className={`px-1.5 py-0.5 rounded text-[8px] font-bold ${
                act.priority === "HIGH"
                  ? "bg-status-critical/10 text-status-critical border border-status-critical/20"
                  : act.priority === "MED"
                  ? "bg-status-warning/10 text-status-warning border border-status-warning/20"
                  : "bg-status-accent/10 text-status-accent border border-status-accent/20"
              }`}>
                {act.priority}
              </span>
            </div>
          ))}
        </div>
      </GlassCard>

    </div>
  );
}
export default AnomalyPanel;
