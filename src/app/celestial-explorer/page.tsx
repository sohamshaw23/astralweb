"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { Navbar } from "@/components/layout/navbar";
import {
  CelestialObject,
  ObjectBrowser,
  SkyDomeVisualizer,
  DetailsPanel,
} from "@/components/celestial/sky-dome";
import { Moon, Star, Compass } from "lucide-react";

export default function CelestialExplorerPage() {
  const [utcTime, setUtcTime] = useState("");
  const [viewMode, setViewMode] = useState<"earth" | "sky" | "universe">("sky");
  const [selectedObject, setSelectedObject] = useState<CelestialObject | null>(null);

  useEffect(() => {
    const clock = setInterval(() => {
      setUtcTime(new Date().toUTCString());
    }, 1000);
    return () => clearInterval(clock);
  }, []);

  return (
    <div className="relative min-h-screen bg-[#030616] text-text-primary overflow-x-hidden flex flex-col pt-20 px-6 pb-24 select-none">
      
      {/* Background radial lights */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(139,92,246,0.04)_0%,transparent_75%)] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.01)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.01)_1px,transparent_1px)] bg-[size:6rem_6rem] pointer-events-none z-0" />

      {/* Top Header Comm */}
      <div className="border-b border-primary/20 bg-[#030616]/90 py-3 mb-4">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-4 px-4">
          <div className="flex items-center gap-3">
            <span className="font-mono text-xs font-bold text-primary-vivid uppercase tracking-widest">
              ASTRONOMY REFERENCE CALIBRATION MATRIX
            </span>
          </div>

          {/* View Mode Switcher pills */}
          <div className="flex items-center bg-white/5 border border-white/10 p-0.5 rounded-lg">
            {(["earth", "sky", "universe"] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setViewMode(mode)}
                className={`px-3 py-1.5 text-[9px] font-mono rounded uppercase cursor-pointer transition-colors ${
                  viewMode === mode
                    ? "bg-primary text-white shadow-md"
                    : "bg-transparent text-text-secondary hover:text-white"
                }`}
              >
                {mode} VIEW
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Core Layout grid */}
      <main className="max-w-7xl mx-auto w-full flex-grow grid grid-cols-1 lg:grid-cols-12 gap-6 relative z-10 pt-4 items-stretch">
        
        {/* Left Side Object Browser (25% / 3 cols) */}
        <section className="lg:col-span-3 flex flex-col justify-start">
          <ObjectBrowser onSelectObject={setSelectedObject} />
        </section>

        {/* Center/Right Sky View (75% / 9 cols) */}
        <section className="lg:col-span-9 flex flex-col h-full">
          <SkyDomeVisualizer mode={viewMode} onSelectObject={setSelectedObject} />
        </section>

      </main>

      {/* Bottom slide-up details drawer */}
      {selectedObject && (
        <DetailsPanel object={selectedObject} onClose={() => setSelectedObject(null)} />
      )}

    </div>
  );
}
