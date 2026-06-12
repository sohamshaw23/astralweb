"use client";

import React, { useState, useEffect, useRef } from "react";
import { Terminal, Cpu, Play, Pause, FastForward, Sparkles, X, ChevronRight, MessageSquare, AlertCircle, Clock } from "lucide-react";
import { GlassCard } from "@/components/ui/glass-card";

export function GlobalOverlays() {
  const [isAiOpen, setIsAiOpen] = useState(false);
  const [isSimOpen, setIsSimOpen] = useState(false);

  // AI Assistant States
  const [aiInput, setAiInput] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [confidence, setConfidence] = useState<number | null>(null);

  // Simulation States
  const [simHour, setSimHour] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [simSpeed, setSimSpeed] = useState(1);
  const [chromaticEffect, setChromaticEffect] = useState(false);

  useEffect(() => {
    // Listen for custom trigger from Navbar Launch or Command centers
    const handleTriggerSim = () => setIsSimOpen(true);
    const handleTriggerAi = () => setIsAiOpen(true);
    window.addEventListener("trigger-simulation", handleTriggerSim);
    window.addEventListener("trigger-ai", handleTriggerAi);
    return () => {
      window.removeEventListener("trigger-simulation", handleTriggerSim);
      window.removeEventListener("trigger-ai", handleTriggerAi);
    };
  }, []);

  // Playback Auto-Advance
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (isPlaying) {
      timer = setInterval(() => {
        setSimHour((prev) => {
          if (prev >= 72) {
            setIsPlaying(false);
            return 72;
          }
          // Brief distortion aberration effect on hour shifts
          setChromaticEffect(true);
          setTimeout(() => setChromaticEffect(false), 200);
          return prev + 1;
        });
      }, 1500 / simSpeed);
    }
    return () => clearInterval(timer);
  }, [isPlaying, simSpeed]);

  const presetQueries = [
    "Which satellites need immediate review?",
    "Show me current threat distribution",
    "Summarize today's disaster intelligence",
  ];

  const handleRunAi = (query: string) => {
    if (isProcessing) return;
    setIsProcessing(true);
    setAiResponse("");
    setConfidence(null);

    // Mock processing streams
    const mockResponses: Record<string, string> = {
      "Which satellites need immediate review?": "ANALYSIS DIRECTIVE: SAT-ZENITH-ALERT (ID: s3) registers an active inclination drift of +1.2°. Conjunction window in LEO sector 4A overlaps with debris segment COSMOS-2251. Relocation thrust recommended.",
      "Show me current threat distribution": "THREAT DISTRIBUTION OVERVIEW: Elevated spatial warnings are clustered within LEO bands (altitude 300-600km) due to debris swarm shifting. National communications lines are secure. Threat rating currently ELEVATED.",
      "Summarize today's disaster intelligence": "DISASTER BRIEFING: Active Cyclone VEGA in Bay of Bengal moving NNW at 185 km/h. Expected landfall in 18h. Emergency observation satellite CARTOSAT-3 tasking scheduled for orbit sweep.",
    };

    const answer = mockResponses[query] || `SYNTHESIS: Custom command evaluation executed for query: "${query}". Satellite telemetry layers show nominal operation. No critical drift warnings registered on active sectors.`;
    
    let index = 0;
    const interval = setInterval(() => {
      setAiResponse((prev) => prev + answer.charAt(index));
      index++;
      if (index >= answer.length) {
        clearInterval(interval);
        setIsProcessing(false);
        setConfidence(Math.floor(Math.random() * 15) + 85); // 85-99%
      }
    }, 15);
  };

  return (
    <>
      {/* 1. FLOATING ACTION TRIGGER TRIGGER BUTTON (Bottom-Right) */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
        <button
          onClick={() => {
            // Dispatch event to activate simulation
            setIsSimOpen(true);
          }}
          className="bg-bg-surface/90 border border-status-accent/30 hover:border-status-accent hover:shadow-[0_0_15px_rgba(0,229,255,0.4)] text-status-accent rounded-full p-3.5 backdrop-blur-md cursor-pointer transition-all duration-300 flex items-center justify-center shadow-lg"
          title="Simulate Future States"
        >
          <Clock className="w-5 h-5" />
        </button>
        <button
          onClick={() => setIsAiOpen(true)}
          className="bg-primary hover:bg-primary-vivid hover:shadow-[0_0_20px_rgba(139,92,246,0.6)] text-white rounded-full p-4 cursor-pointer transition-all duration-300 flex items-center justify-center shadow-lg"
          title="AI Operational Assistant"
        >
          <Cpu className="w-5 h-5 animate-pulse" />
        </button>
      </div>

      {/* 2. AI COMMAND ASSISTANT SLIDE-UP DOME */}
      {isAiOpen && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-end justify-center font-mono select-none">
          <div className="bg-[#040816] border-t-2 border-primary w-full max-w-3xl rounded-t-2xl p-6 flex flex-col space-y-6 shadow-[0_-15px_40px_rgba(79,70,229,0.3)] max-h-[85vh] overflow-y-auto">
            
            {/* Header info */}
            <div className="flex justify-between items-center border-b border-white/10 pb-3">
              <div className="flex items-center gap-2">
                <Terminal className="text-primary-vivid w-5 h-5" />
                <span className="text-white font-bold tracking-widest text-sm uppercase">ZENITH AI OPERATIVE</span>
                <span className="w-2 h-2 rounded-full bg-status-safe animate-ping" />
              </div>
              <button onClick={() => setIsAiOpen(false)} className="text-text-secondary hover:text-white cursor-pointer">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Assessment Panel */}
            <div className="p-4 bg-white/2 border border-white/5 rounded-xl space-y-2">
              <div className="text-[10px] text-text-secondary uppercase">OPERATIVE LIVE ASSESSMENT</div>
              <ul className="text-[11px] text-white space-y-1">
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-status-critical" />
                  3 satellites inside high-risk collision corridors.
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-status-warning" />
                  1 anomalous orbital signature detected.
                </li>
                <li className="flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-status-accent" />
                  Cyclone VEGA landfall predicted within 18h.
                </li>
              </ul>
            </div>

            {/* Presets query commands */}
            <div className="space-y-2">
              <div className="text-[10px] text-text-secondary uppercase">RECOMMENDED DEEP QUERY OVERLAYS</div>
              <div className="flex flex-col gap-2">
                {presetQueries.map((query) => (
                  <button
                    key={query}
                    onClick={() => handleRunAi(query)}
                    className="w-full text-left bg-white/2 hover:bg-white/5 border border-white/5 p-2.5 rounded-lg text-xs text-text-secondary hover:text-white flex items-center justify-between transition-colors cursor-pointer"
                  >
                    <span>&gt; {query}</span>
                    <ChevronRight className="w-4 h-4 text-text-muted" />
                  </button>
                ))}
              </div>
            </div>

            {/* Response Console */}
            {(aiResponse || isProcessing) && (
              <div className="p-4 bg-black/50 border border-white/10 rounded-xl space-y-3 min-h-[100px] relative">
                {isProcessing && (
                  <div className="absolute top-4 right-4 flex items-center gap-1.5">
                    {/* Pulsing voice wave bars */}
                    {[1, 2, 3].map((bar) => (
                      <span key={bar} className="w-1 h-3 bg-status-accent rounded animate-bounce" style={{ animationDelay: `${bar * 0.1}s` }} />
                    ))}
                  </div>
                )}
                
                <div className="text-xs text-white leading-relaxed whitespace-pre-wrap">
                  {aiResponse}
                </div>

                {confidence !== null && (
                  <div className="flex items-center justify-between border-t border-white/5 pt-2 text-[10px] text-text-secondary">
                    <span>SOURCE VERIFICATION: MOCK-DATA-FEED // CONST-OVERWATCH</span>
                    <span className="text-status-safe font-bold">CONFIDENCE: {confidence}%</span>
                  </div>
                )}
              </div>
            )}

            {/* Custom Input */}
            <div className="flex gap-2">
              <input
                type="text"
                value={aiInput}
                onChange={(e) => setAiInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleRunAi(aiInput)}
                placeholder="Submit manual overwatch query..."
                className="flex-grow bg-white/5 border border-white/10 rounded-lg py-2 px-4 text-xs text-white focus:outline-none focus:border-primary"
              />
              <button
                onClick={() => handleRunAi(aiInput)}
                className="bg-primary hover:bg-primary-vivid px-6 py-2 rounded-lg text-xs font-bold text-white cursor-pointer transition-colors"
              >
                RUN
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 3. FUTURE SIMULATION TAKE-OVER SCREEN */}
      {isSimOpen && (
        <div
          className={`fixed inset-0 bg-[#020512]/95 backdrop-blur-md z-50 p-6 flex flex-col justify-between font-mono select-none transition-all duration-300 ${
            chromaticEffect ? "blur-[1.5px] saturate-200" : ""
          }`}
        >
          {/* Header indicator */}
          <div className="flex justify-between items-center border-b border-white/10 pb-4">
            <div className="flex items-center gap-3">
              <Clock className="w-6 h-6 text-status-accent animate-spin" style={{ animationDuration: '12s' }} />
              <span className="font-display font-black text-lg tracking-widest text-white uppercase">
                FUTURE SIMULATION — TEMPORAL PROJECTION ENGINE
              </span>
            </div>
            <button onClick={() => setIsSimOpen(false)} className="text-text-secondary hover:text-white cursor-pointer">
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Timeline slider representation */}
          <div className="max-w-4xl mx-auto w-full p-6 bg-white/2 border border-white/5 rounded-2xl space-y-4">
            <div className="flex justify-between text-xs text-text-secondary font-bold">
              <span>NOW (T+0H)</span>
              <span className="text-status-accent">SIMULATED HOURS: T+{simHour}H</span>
              <span>PROJECTION CAP: T+72H</span>
            </div>

            <input
              type="range"
              min="0"
              max="72"
              value={simHour}
              onChange={(e) => {
                setChromaticEffect(true);
                setTimeout(() => setChromaticEffect(false), 200);
                setSimHour(Number(e.target.value));
              }}
              className="w-full accent-status-accent bg-white/10 rounded-lg cursor-pointer appearance-none h-1.5"
            />
          </div>

          {/* Earth Visual state & Projection feeds */}
          <div className="max-w-6xl mx-auto w-full grid grid-cols-1 md:grid-cols-2 gap-8 items-center flex-grow py-8 overflow-y-auto">
            {/* Left simulated Earth projection */}
            <div className="flex flex-col items-center space-y-4">
              <div className="text-[10px] text-text-secondary uppercase">PROJECTED GEOCENTRIC COORDINATE VECTOR</div>
              <div className="w-64 h-64 rounded-full bg-gradient-to-br from-[#0b1b40] to-[#04081c] border border-status-accent/30 flex items-center justify-center relative overflow-hidden shadow-[0_0_30px_rgba(0,229,255,0.15)]">
                {/* Visual coordinate orbits shifting */}
                <div
                  style={{ transform: `rotate(${simHour * 5}deg)` }}
                  className="absolute inset-4 rounded-full border border-dashed border-status-accent/30 transition-transform duration-500"
                />
                <div
                  style={{ transform: `rotate(-${simHour * 3}deg)` }}
                  className="absolute inset-12 rounded-full border border-dashed border-primary-vivid/20 transition-transform duration-500"
                />
                <div className="w-4 h-4 bg-status-accent rounded-full animate-ping" />
              </div>
            </div>

            {/* Right log projection feed */}
            <GlassCard glowColor="primary" className="space-y-4 h-80 flex flex-col justify-start">
              <div className="text-xs text-white font-bold border-b border-white/10 pb-2">
                TEMPORAL PROJECTION OVERWATCH REPORT
              </div>
              <div className="space-y-3 overflow-y-auto text-[10px] leading-relaxed text-text-secondary">
                <div className={simHour >= 12 ? "text-status-warning font-bold transition-all" : "opacity-35 transition-all"}>
                  &gt; T+12h: IRNSS-1G collision warning alert triggered in LEO band. Conjunction threshold 12%.
                </div>
                <div className={simHour >= 24 ? "text-status-critical font-bold transition-all" : "opacity-35 transition-all"}>
                  &gt; T+24h: Cyclone VEGA makes coastal landfall. Heavy flood warnings in Southeast Asia.
                </div>
                <div className={simHour >= 48 ? "text-white transition-all" : "opacity-35 transition-all"}>
                  &gt; T+48h: Debris field shift corridor sweeps GEO belt coordinate sector 99-A.
                </div>
                <div className={simHour >= 72 ? "text-status-safe font-bold transition-all" : "opacity-35 transition-all"}>
                  &gt; T+72h: All coordinates updated. Simulation prediction projections finalized.
                </div>
              </div>
            </GlassCard>
          </div>

          {/* Controls actions bar */}
          <div className="max-w-4xl mx-auto w-full flex flex-col sm:flex-row gap-4 items-center justify-between bg-bg-surface/80 border border-white/5 p-4 rounded-2xl">
            <div className="flex gap-2">
              <button
                onClick={() => setIsPlaying(!isPlaying)}
                className="bg-primary hover:bg-primary-vivid px-6 py-2.5 rounded-lg text-xs font-bold text-white flex items-center gap-2 cursor-pointer transition-colors"
              >
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                {isPlaying ? "PAUSE" : "PLAY SIMULATION"}
              </button>
            </div>

            <div className="flex items-center gap-1.5 bg-white/5 border border-white/10 p-0.5 rounded-lg">
              {[1, 2, 4].map((speed) => (
                <button
                  key={speed}
                  onClick={() => setSimSpeed(speed)}
                  className={`px-3 py-1.5 text-[9px] font-mono rounded cursor-pointer transition-colors ${
                    simSpeed === speed ? "bg-status-accent text-bg-void font-bold" : "text-text-secondary hover:text-white"
                  }`}
                >
                  {speed}X
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
export default GlobalOverlays;
