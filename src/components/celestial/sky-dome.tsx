"use client";

import React, { useState } from "react";
import { GlassCard } from "@/components/ui/glass-card";
import { Moon, Star, Compass, Info, Users, Clock, Globe2, X } from "lucide-react";

export interface CelestialObject {
  id: string;
  name: string;
  category: "iss" | "planet" | "constellation" | "moon" | "dso";
  classification: string;
  distance: string;
  magnitude: string;
  discovery: string;
  description: string;
  // ISS specific
  crew?: string[];
  experiment?: string;
  resupply?: string;
  // Constellation specific
  mythology?: string;
  bestMonths?: string;
}

// --- OBJECT DETAILS PANEL (BOTTOM SLIDE UP) ---
export function DetailsPanel({ object, onClose }: { object: CelestialObject; onClose: () => void }) {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-[#070b22]/95 border-t border-primary/30 z-50 p-6 shadow-[0_-10px_40px_rgba(79,70,229,0.2)] font-mono text-xs select-none">
      <div className="max-w-7xl mx-auto relative">
        <button onClick={onClose} className="absolute -top-2 right-0 text-text-secondary hover:text-white cursor-pointer">
          <X className="w-5 h-5" />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
          {/* Main Info */}
          <div className="md:col-span-4 space-y-3">
            <div className="inline-flex items-center gap-2 px-2 py-0.5 bg-primary/10 border border-primary/20 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-status-accent animate-pulse" />
              <span className="text-[9px] text-status-accent uppercase tracking-wider">{object.category}</span>
            </div>
            <h3 className="font-display font-bold text-xl text-white tracking-widest">{object.name.toUpperCase()}</h3>
            <p className="text-text-secondary text-[10px] leading-relaxed">{object.description}</p>
          </div>

          {/* Core Specs */}
          <div className="md:col-span-4 grid grid-cols-2 gap-4 border-l border-white/5 pl-0 md:pl-8">
            <div>
              <span className="text-text-muted block text-[8px] uppercase">Classification</span>
              <span className="text-white font-bold">{object.classification}</span>
            </div>
            <div>
              <span className="text-text-muted block text-[8px] uppercase">Distance</span>
              <span className="text-white font-bold">{object.distance}</span>
            </div>
            {object.magnitude && (
              <div>
                <span className="text-text-muted block text-[8px] uppercase">Visual Mag</span>
                <span className="text-status-accent font-bold">{object.magnitude}</span>
              </div>
            )}
            {object.discovery && (
              <div>
                <span className="text-text-muted block text-[8px] uppercase">Discovery</span>
                <span className="text-white font-bold">{object.discovery}</span>
              </div>
            )}
          </div>

          {/* Category specific info */}
          <div className="md:col-span-4 border-l border-white/5 pl-0 md:pl-8 space-y-4">
            {object.category === "iss" && (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-status-accent" />
                  <span className="text-white font-bold uppercase text-[9px]">Crew Manifest (7)</span>
                </div>
                <div className="text-[10px] text-text-secondary leading-relaxed">
                  {object.crew?.join(" // ")}
                </div>
                <div className="text-[9px] text-text-muted">
                  CURRENT EXPERIMENT: {object.experiment}
                </div>
              </div>
            )}

            {object.category === "constellation" && (
              <div className="space-y-2">
                <div className="text-white font-bold uppercase text-[9px]">Mythology & Visibility</div>
                <p className="text-text-secondary text-[10px] leading-relaxed">{object.mythology}</p>
                <div className="text-[9px] text-status-accent font-bold">BEST VIEWING MONTHS: {object.bestMonths}</div>
              </div>
            )}

            {object.category === "planet" && (
              <div className="space-y-2">
                <div className="text-white font-bold uppercase text-[9px]">Planetary Diagnostics</div>
                <div className="flex justify-between">
                  <span>VISIBILITY STATUS:</span>
                  <span className="text-status-safe font-bold">OPTIMAL</span>
                </div>
                <div className="flex justify-between">
                  <span>ORBIT VELOCITY:</span>
                  <span className="text-white">24.1 KM/S</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// --- OBJECT BROWSER SIDEBAR ---
export function ObjectBrowser({
  onSelectObject,
}: {
  onSelectObject: (obj: CelestialObject) => void;
}) {
  const moonInfo = {
    phase: "Waxing Gibbous",
    illumination: "78%",
    rise: "14:42 UTC",
    set: "03:12 UTC",
  };

  const issInfo = {
    alt: 408,
    vel: "27,600 km/h",
    crew: ["S. Williams", "B. Wilmore", "M. Barratt", "M. Dominick", "J. Epps", "A. Grebenkin", "N. Kononenko"],
  };

  const categories: Record<string, any[]> = {
    planets: [
      { id: "p-mars", name: "Mars", category: "planet", classification: "Terrestrial Planet", distance: "225M KM", magnitude: "-1.5", discovery: "Ancient", description: "The fourth planet from the Sun and the second-smallest planet in the Solar System." },
      { id: "p-jupiter", name: "Jupiter", category: "planet", classification: "Gas Giant", distance: "778M KM", magnitude: "-2.7", discovery: "Ancient", description: "The fifth planet from the Sun and the largest in the Solar System." },
    ],
    constellations: [
      { id: "c-orion", name: "Orion", category: "constellation", classification: "Constellation", distance: "1,344 LY", magnitude: "0.4", discovery: "Ancient", description: "A prominent constellation located on the celestial equator and visible throughout the world.", mythology: "Named after Orion, a hunter in Greek mythology.", bestMonths: "DECEMBER - FEBRUARY" },
    ],
    dsos: [
      { id: "d-andromeda", name: "Andromeda Galaxy", category: "dso", classification: "Spiral Galaxy", distance: "2.537M LY", magnitude: "3.4", discovery: "964 AD", description: "A barred spiral galaxy approximately 2.5 million light-years from Earth and the nearest major galaxy to the Milky Way." },
    ],
  };

  return (
    <div className="space-y-6 overflow-y-auto max-h-[calc(100vh-160px)] pr-2 font-mono text-xs select-none">
      
      {/* Moon Phase Widget */}
      <GlassCard glowColor="accent" className="space-y-3">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <Moon className="w-4 h-4 text-status-accent" />
          <h3 className="font-display font-bold text-xs uppercase text-white">LUNAR DIAL</h3>
        </div>
        <div className="space-y-1 text-[10px] text-text-secondary">
          <div className="flex justify-between">
            <span>PHASE:</span>
            <span className="text-white font-bold">{moonInfo.phase}</span>
          </div>
          <div className="flex justify-between">
            <span>RISE/SET:</span>
            <span className="text-white">{moonInfo.rise} / {moonInfo.set}</span>
          </div>
        </div>
      </GlassCard>

      {/* ISS Live Tracker */}
      <GlassCard glowColor="primary" className="space-y-3">
        <div className="flex items-center gap-2 border-b border-white/10 pb-2">
          <Globe2 className="w-4 h-4 text-primary-vivid animate-pulse" />
          <h3 className="font-display font-bold text-xs uppercase text-white">ISS LIVE STATS</h3>
        </div>
        <div className="space-y-2 text-[10px] text-text-secondary">
          <div className="flex justify-between">
            <span>ALTITUDE:</span>
            <span className="text-status-accent font-bold">{issInfo.alt} KM</span>
          </div>
          <div className="flex justify-between">
            <span>VELOCITY:</span>
            <span className="text-white">{issInfo.vel}</span>
          </div>
          <button
            onClick={() => onSelectObject({
              id: "iss",
              name: "ISS Tracker",
              category: "iss",
              classification: "Space Station",
              distance: "408 KM",
              magnitude: "-5.0",
              discovery: "1998",
              description: "The International Space Station is a co-operative space laboratory orbiting Earth.",
              crew: issInfo.crew,
              experiment: "Microgravity plant biology and fluid dynamics sync.",
            })}
            className="w-full bg-white/5 border border-white/10 hover:bg-white/10 text-white py-1.5 rounded text-[8px] font-bold cursor-pointer transition-colors"
          >
            VIEW CREW & EXP
          </button>
        </div>
      </GlassCard>

      {/* Object listings categories */}
      {Object.keys(categories).map((catName) => (
        <GlassCard key={catName} glowColor="accent" className="space-y-3">
          <div className="font-display font-bold text-xs uppercase text-white border-b border-white/10 pb-1">
            {catName}
          </div>
          <div className="space-y-1.5">
            {categories[catName].map((obj) => (
              <button
                key={obj.id}
                onClick={() => onSelectObject(obj)}
                className="w-full text-left py-1 text-text-secondary hover:text-white hover:pl-1 transition-all flex items-center justify-between text-[10px]"
              >
                <span>{obj.name}</span>
                <span className="text-text-muted text-[8px]">{obj.classification}</span>
              </button>
            ))}
          </div>
        </GlassCard>
      ))}

    </div>
  );
}

// --- MAIN VISUALIZATION PANEL ---
export function SkyDomeVisualizer({
  mode,
  onSelectObject,
}: {
  mode: "earth" | "sky" | "universe";
  onSelectObject: (obj: CelestialObject) => void;
}) {
  const [hoveredConst, setHoveredConst] = useState<string | null>(null);

  return (
    <div className="w-full h-full min-h-[420px] flex items-center justify-center relative rounded-2xl overflow-hidden border border-white/5 bg-bg-surface/30">
      
      {/* EARTH VIEW */}
      {mode === "earth" && (
        <div className="relative flex flex-col items-center justify-center font-mono">
          <span className="absolute top-4 left-4 text-[9px] text-text-secondary">EARTH CONSTELLATION OVERLAY</span>
          
          <div className="w-72 h-72 rounded-full bg-gradient-to-br from-[#0c1b40] to-[#04081c] border border-primary/30 flex items-center justify-center relative overflow-hidden shadow-[inset_0_0_30px_rgba(79,70,229,0.3)]">
            {/* Simple Earth grid meridians */}
            <div className="absolute inset-0 opacity-20 bg-[linear-gradient(to_right,rgba(255,255,255,0.05)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.05)_1px,transparent_1px)] bg-[size:20px_20px]" />
            {/* ISS Orbit line representation */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 100 100">
              <ellipse cx="50" cy="50" rx="46" ry="18" fill="none" stroke="rgba(0, 229, 255, 0.4)" strokeWidth="0.5" className="origin-center animate-orbit-rotate" />
              {/* Moon orbit */}
              <ellipse cx="50" cy="50" rx="60" ry="24" fill="none" stroke="rgba(139, 92, 246, 0.2)" strokeWidth="0.5" />
            </svg>
            <div className="w-2.5 h-2.5 bg-status-accent rounded-full animate-ping" />
          </div>
        </div>
      )}

      {/* SKY VIEW (SKY DOME VECTORS) */}
      {mode === "sky" && (
        <div className="relative w-full h-full flex flex-col items-center justify-center font-mono">
          <span className="absolute top-4 left-4 text-[9px] text-text-secondary">CELESTIAL SKY DOME</span>

          {/* Semicircular dome */}
          <div className="w-80 h-80 rounded-full border border-primary/30 bg-gradient-to-t from-[#020514] via-[#0b061e] to-[#140b2b] relative overflow-hidden shadow-[inset_0_0_50px_rgba(139,92,246,0.3)] flex items-center justify-center">
            
            {/* Constellation Star dots */}
            <svg className="absolute inset-0 w-full h-full cursor-pointer" viewBox="0 0 100 100">
              {/* Stars representation */}
              <circle cx="30" cy="30" r="1.5" fill="#fff" className="animate-pulse" />
              <circle cx="70" cy="40" r="1.2" fill="#fff" />
              <circle cx="50" cy="65" r="1" fill="#fff" />
              <circle cx="20" cy="60" r="2.2" fill="#fff" className="animate-pulse" />
              <circle cx="80" cy="70" r="1.8" fill="#fff" />

              {/* Orion constellation lines on hover */}
              <g
                className="group/orion pointer-events-auto"
                onMouseEnter={() => setHoveredConst("Orion")}
                onMouseLeave={() => setHoveredConst(null)}
                onClick={() => onSelectObject({
                  id: "c-orion",
                  name: "Orion",
                  category: "constellation",
                  classification: "Constellation",
                  distance: "1,344 LY",
                  magnitude: "0.4",
                  discovery: "Ancient",
                  description: "A prominent constellation named after Orion the Greek hunter.",
                  mythology: "Named after Orion, a hunter in Greek mythology.",
                  bestMonths: "DECEMBER - FEBRUARY",
                })}
              >
                {/* Connecting stars */}
                <line x1="40" y1="20" x2="60" y2="20" stroke="rgba(0, 229, 255, 0.1)" strokeWidth="0.5" className="group-hover/orion:stroke-status-accent group-hover/orion:stroke-1 transition-all" />
                <line x1="60" y1="20" x2="55" y2="45" stroke="rgba(0, 229, 255, 0.1)" strokeWidth="0.5" className="group-hover/orion:stroke-status-accent group-hover/orion:stroke-1 transition-all" />
                <line x1="55" y1="45" x2="35" y2="45" stroke="rgba(0, 229, 255, 0.1)" strokeWidth="0.5" className="group-hover/orion:stroke-status-accent group-hover/orion:stroke-1 transition-all" />
                <line x1="35" y1="45" x2="40" y2="20" stroke="rgba(0, 229, 255, 0.1)" strokeWidth="0.5" className="group-hover/orion:stroke-status-accent group-hover/orion:stroke-1 transition-all" />
                
                {/* Stars of Orion */}
                <circle cx="40" cy="20" r="2" fill="#fff" />
                <circle cx="60" cy="20" r="2.5" fill="#fff" />
                <circle cx="55" cy="45" r="2" fill="#fff" />
                <circle cx="35" cy="45" r="2.2" fill="#fff" />
              </g>
            </svg>

            {hoveredConst && (
              <div className="absolute top-4 bg-bg-surface border border-status-accent/30 rounded px-2 py-1 text-[8px] text-white">
                CONSTELLATION: {hoveredConst} (CLICK TO DETAIL)
              </div>
            )}
          </div>
        </div>
      )}

      {/* UNIVERSE VIEW */}
      {mode === "universe" && (
        <div className="relative w-full h-full flex flex-col items-center justify-center font-mono">
          <span className="absolute top-4 left-4 text-[9px] text-text-secondary">SOLAR SCHEMATIC LOOP</span>

          <div className="relative w-80 h-80 flex items-center justify-center">
            {/* Center Sun */}
            <div className="w-8 h-8 rounded-full bg-status-warning shadow-[0_0_20px_var(--status-warning)] z-10" />

            {/* Orbit pathways */}
            <div className="absolute w-28 h-28 border border-white/5 rounded-full" />
            <div className="absolute w-44 h-44 border border-white/5 rounded-full" />
            <div className="absolute w-60 h-60 border border-white/5 rounded-full" />

            {/* Planet Earth */}
            <div
              onClick={() => onSelectObject({
                id: "earth-cel",
                name: "Earth",
                category: "planet",
                classification: "Terrestrial Planet",
                distance: "0 KM",
                magnitude: "N/A",
                discovery: "Ancient",
                description: "Our home planet, third from the Sun, and the only known harbor of life.",
              })}
              className="absolute left-[calc(50%+45px)] w-3 h-3 bg-status-accent border border-status-accent rounded-full cursor-pointer animate-pulse"
            />

            {/* Planet Mars */}
            <div
              onClick={() => onSelectObject({
                id: "p-mars",
                name: "Mars",
                category: "planet",
                classification: "Terrestrial Planet",
                distance: "225M KM",
                magnitude: "-1.5",
                discovery: "Ancient",
                description: "The fourth planet from the Sun, and a primary destination for deep-space science.",
              })}
              className="absolute top-[calc(50%-80px)] w-2.5 h-2.5 bg-status-critical rounded-full cursor-pointer"
            />
          </div>
        </div>
      )}

    </div>
  );
}
