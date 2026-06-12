"use client";

import React, { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { motion, useMotionValue, useTransform, useSpring, useInView } from "framer-motion";
import {
  Shield,
  Activity,
  Globe,
  Radio,
  Compass,
  Cpu,
  ArrowRight,
  Database,
  Layers,
  Zap,
  CheckCircle2,
} from "lucide-react";
import { Navbar } from "@/components/layout/navbar";
import { GlassCard } from "@/components/ui/glass-card";

// --- STARRY BACKGROUND COMPONENT ---
function StarryBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let stars: { x: number; y: number; size: number; speed: number; opacity: number }[] = [];

    const handleResize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initStars();
    };

    const initStars = () => {
      stars = [];
      const numStars = 800;
      for (let i = 0; i < numStars; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 1.5,
          speed: Math.random() * 0.05 + 0.01,
          opacity: Math.random(),
        });
      }
    };

    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#ffffff";

      // Draw two parallax layers
      stars.forEach((star) => {
        // Slow vertical drift
        star.y -= star.speed * 1.2;
        if (star.y < 0) {
          star.y = canvas.height;
          star.x = Math.random() * canvas.width;
        }

        // Pulse opacity slightly for twinkle
        star.opacity += (Math.random() - 0.5) * 0.04;
        if (star.opacity < 0.1) star.opacity = 0.1;
        if (star.opacity > 0.9) star.opacity = 0.9;

        ctx.globalAlpha = star.opacity;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.size, 0, Math.PI * 2);
        ctx.fill();
      });

      animationFrameId = requestAnimationFrame(animate);
    };

    window.addEventListener("resize", handleResize);
    handleResize();
    animate();

    return () => {
      window.removeEventListener("resize", handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none z-0" />;
}

// --- TYPEWRITER DESCRIPTOR COMPONENT ---
function TypewriterEffect() {
  const messages = [
    "Tracking 47,832 orbital objects...",
    "Monitoring 6 active disaster zones...",
    "Protecting 847 strategic assets...",
  ];
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [currentText, setCurrentText] = useState("");
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    const fullText = messages[currentMessageIndex];
    const typingSpeed = isDeleting ? 30 : 60;

    if (!isDeleting && currentText === fullText) {
      timer = setTimeout(() => setIsDeleting(true), 2500);
    } else if (isDeleting && currentText === "") {
      setIsDeleting(false);
      setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
    } else {
      timer = setTimeout(() => {
        setCurrentText(
          isDeleting
            ? fullText.substring(0, currentText.length - 1)
            : fullText.substring(0, currentText.length + 1)
        );
      }, typingSpeed);
    }

    return () => clearTimeout(timer);
  }, [currentText, isDeleting, currentMessageIndex]);

  return (
    <span className="font-mono text-status-accent drop-shadow-[0_0_8px_rgba(0,229,255,0.4)]">
      {currentText}
      <span className="animate-pulse">|</span>
    </span>
  );
}

// --- ANIMATED COUNTER COMPONENT ---
function AnimatedCounter({ value, duration = 2 }: { value: number; duration?: number }) {
  const [count, setCount] = useState(0);
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true });

  useEffect(() => {
    if (!isInView) return;

    let start = 0;
    const end = value;
    const totalMiliseconds = duration * 1000;
    const incrementTime = 30;
    const totalSteps = totalMiliseconds / incrementTime;
    const increment = end / totalSteps;

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, incrementTime);

    return () => clearInterval(timer);
  }, [isInView, value, duration]);

  return <span ref={ref}>{count.toLocaleString()}</span>;
}

// --- 3D EARTH GLOBE SIMULATION COMPONENT ---
function EarthGlobe() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  const springConfig = { stiffness: 100, damping: 20 };
  const rotateX = useSpring(useTransform(mouseY, [-300, 300], [15, -15]), springConfig);
  const rotateY = useSpring(useTransform(mouseX, [-300, 300], [-15, 15]), springConfig);

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      mouseX.set(x);
      mouseY.set(y);
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, [mouseX, mouseY]);

  return (
    <div ref={containerRef} className="relative w-72 h-72 sm:w-96 sm:h-96 md:w-[450px] md:h-[450px] flex items-center justify-center select-none">
      {/* Atmosphere Glow */}
      <div className="absolute inset-0 rounded-full bg-radial from-status-accent/15 via-primary/5 to-transparent blur-2xl scale-110 pointer-events-none" />
      <div className="absolute inset-0 rounded-full border border-status-accent/20 shadow-[0_0_50px_rgba(0,229,255,0.15)] pointer-events-none scale-105" />

      {/* Orbit paths */}
      <svg className="absolute inset-[-40px] w-[calc(100%+80px)] h-[calc(100%+80px)] pointer-events-none" viewBox="0 0 100 100">
        {/* LEO Orbit */}
        <ellipse
          cx="50"
          cy="50"
          rx="47"
          ry="18"
          fill="none"
          stroke="rgba(0, 229, 255, 0.2)"
          strokeWidth="0.25"
          strokeDasharray="2 3"
          className="origin-center animate-orbit-rotate"
        />
        {/* MEO Orbit */}
        <ellipse
          cx="50"
          cy="50"
          rx="52"
          ry="32"
          fill="none"
          stroke="rgba(139, 92, 246, 0.25)"
          strokeWidth="0.25"
          className="origin-center animate-orbit-rotate-reverse"
        />
      </svg>

      {/* Interactive Rotatable Globe */}
      <motion.div
        style={{ rotateX, rotateY, transformStyle: "preserve-3d" }}
        className="w-full h-full rounded-full relative overflow-hidden bg-gradient-to-br from-[#0c1435] via-[#050816] to-[#01030a] shadow-[inset_-30px_-30px_70px_rgba(0,0,0,0.95),inset_20px_20px_50px_rgba(255,255,255,0.08)] border border-white/10"
      >
        {/* Repeating grid representation of earth landmass */}
        <div className="absolute inset-0 opacity-40 bg-[linear-gradient(to_right,rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:16px_16px]" />

        {/* Dynamic sliding landmass */}
        <motion.div
          animate={{ x: [0, -1000] }}
          transition={{ repeat: Infinity, duration: 40, ease: "linear" }}
          className="absolute inset-0 flex w-[2000px] h-full pointer-events-none"
        >
          {/* Mock Futuristic Map Structure */}
          <div className="w-[1000px] h-full relative opacity-60">
            <svg viewBox="0 0 1000 400" className="w-full h-full fill-status-accent/25">
              {/* Simplistic stylized map paths for Sci-Fi rendering */}
              <rect x="150" y="80" width="160" height="120" rx="30" />
              <rect x="420" y="50" width="220" height="160" rx="40" />
              <rect x="700" y="120" width="180" height="140" rx="35" />
              <rect x="250" y="240" width="100" height="90" rx="20" />
              <circle cx="100" cy="180" r="40" />
              <circle cx="340" cy="100" r="50" />
              <circle cx="580" cy="190" r="60" />
              <circle cx="820" cy="90" r="45" />
            </svg>
          </div>
          <div className="w-[1000px] h-full relative opacity-60">
            <svg viewBox="0 0 1000 400" className="w-full h-full fill-status-accent/25">
              <rect x="150" y="80" width="160" height="120" rx="30" />
              <rect x="420" y="50" width="220" height="160" rx="40" />
              <rect x="700" y="120" width="180" height="140" rx="35" />
              <rect x="250" y="240" width="100" height="90" rx="20" />
              <circle cx="100" cy="180" r="40" />
              <circle cx="340" cy="100" r="50" />
              <circle cx="580" cy="190" r="60" />
              <circle cx="820" cy="90" r="45" />
            </svg>
          </div>
        </motion.div>

        {/* Terminator line (Day/Night dividing gradient) */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-black/40 to-black/90 pointer-events-none" />

        {/* Atmosphere rim light overlay */}
        <div className="absolute inset-0 shadow-[inset_15px_15px_30px_rgba(0,229,255,0.25),inset_-15px_-15px_30px_rgba(0,0,0,0.85)] rounded-full pointer-events-none" />
      </motion.div>

      {/* Orbiting Satellite 1 marker */}
      <motion.div
        animate={{
          rotate: 360,
        }}
        transition={{ repeat: Infinity, duration: 25, ease: "linear" }}
        className="absolute w-[calc(100%+30px)] h-[calc(100%+30px)] pointer-events-none origin-center"
      >
        <div className="absolute top-1/2 left-0 -translate-y-1/2 flex flex-col items-center">
          <div className="w-2.5 h-2.5 rounded-full bg-status-accent shadow-[0_0_10px_var(--status-accent)] animate-pulse" />
          <span className="font-mono text-[8px] text-status-accent mt-1 bg-bg-void/80 border border-status-accent/30 px-1 rounded">
            ISS-MOCK
          </span>
        </div>
      </motion.div>

      {/* Orbiting Satellite 2 marker (Counter rotate) */}
      <motion.div
        animate={{
          rotate: -360,
        }}
        transition={{ repeat: Infinity, duration: 35, ease: "linear" }}
        className="absolute w-[calc(100%+60px)] h-[calc(100%+60px)] pointer-events-none origin-center"
      >
        <div className="absolute top-1/4 right-0 -translate-y-1/2 flex flex-col items-center">
          <div className="w-2.5 h-2.5 rounded-full bg-primary-vivid shadow-[0_0_10px_var(--primary-vivid)] animate-pulse" />
          <span className="font-mono text-[8px] text-primary-vivid mt-1 bg-bg-void/80 border border-primary-vivid/30 px-1 rounded">
            NAV-ZENITH
          </span>
        </div>
      </motion.div>
    </div>
  );
}

export default function Home() {
  const capabilities = [
    {
      icon: Radio,
      title: "Orbital Threat Analysis",
      desc: "Track real-time debris clustering, potential intercept vectors, and micrometeoroid streams with predictive spatial risk analysis.",
      glow: "accent",
    },
    {
      icon: Activity,
      title: "Collision Prediction Engine",
      desc: "Automated conjunction analysis algorithms calculations projecting proximity events across deep-space asset paths.",
      glow: "critical",
    },
    {
      icon: Globe,
      title: "Disaster Intelligence Feed",
      desc: "Synthesize global climatic risks, wildfire progress, flood heatmaps, and seismic events with direct satellite visual overlays.",
      glow: "warning",
    },
    {
      icon: Shield,
      title: "National Asset Protection",
      desc: "Guarding critical communication constellations and sovereign infrastructure through automated defense protocols.",
      glow: "safe",
    },
    {
      icon: Compass,
      title: "Celestial Navigation",
      desc: "Stellar reference calibration mapping and celestial object categorization mapped to astronomical coordinates.",
      glow: "primary",
    },
    {
      icon: Cpu,
      title: "AI Mission Command",
      desc: "Large Action Models orchestrating multi-constellation task assignment and response optimization.",
      glow: "accent",
    },
  ];

  const workflowSteps = [
    {
      step: "01",
      title: "Constellation Integration",
      desc: "Ingesting live sensor sweeps, telemetry lines, and satellite payloads into our centralized browser operating system.",
    },
    {
      step: "02",
      title: "Autonomous Risk Evaluation",
      desc: "Running local and cloud prediction models calculating spatial interference and hazard escalations.",
    },
    {
      step: "03",
      title: "Mission Directives Executed",
      desc: "Orchestrate response vectors, emergency orbital shifts, and direct ground station alerts.",
    },
  ];

  return (
    <div className="relative min-h-screen bg-bg-void overflow-hidden flex flex-col">
      {/* Ambient background grid layer */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(79,70,229,0.05)_0%,transparent_70%)] pointer-events-none z-0" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.015)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.015)_1px,transparent_1px)] bg-[size:4rem_4rem] pointer-events-none z-0" />
      
      {/* Star Field Parallax Canvas */}
      <StarryBackground />

      {/* Navigation Header */}
      <Navbar />

      {/* Hero Section */}
      <main className="flex-grow flex flex-col justify-center pt-32 pb-20 px-6 max-w-7xl mx-auto w-full z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center min-h-[calc(100vh-250px)]">
          
          {/* Hero Left Content */}
          <div className="lg:col-span-7 flex flex-col justify-center space-y-8 text-left">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full w-fit">
              <span className="w-2 h-2 rounded-full bg-status-accent animate-ping" />
              <span className="font-mono text-xs text-text-secondary tracking-widest uppercase">
                OPERATIONAL STATUS: READY
              </span>
            </div>

            <div className="space-y-4">
              <h1 className="font-display text-4xl sm:text-6xl md:text-7xl font-bold tracking-tight text-white leading-none">
                PROJECT <span className="bg-gradient-to-r from-primary via-primary-vivid to-status-accent bg-clip-text text-transparent">ZENITH</span>
              </h1>
              <h2 className="font-interface text-xl sm:text-2xl text-text-secondary font-light max-w-xl">
                AI-Powered Space Situational Awareness & Disaster Intelligence Platform.
              </h2>
            </div>

            {/* Typewriter terminal section */}
            <div className="h-8 flex items-center font-mono text-sm sm:text-base border-l-2 border-status-accent pl-4">
              <TypewriterEffect />
            </div>

            {/* CTA Group */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Link
                href="/dashboard"
                className="flex items-center justify-center gap-2 bg-primary hover:bg-primary-vivid text-white font-interface font-medium px-8 py-4 rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.4)] hover:shadow-[0_0_30px_rgba(139,92,246,0.6)] transition-all duration-300 transform hover:-translate-y-0.5 group"
              >
                Launch Mission Control
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link
                href="/guardian-mode"
                className="flex items-center justify-center gap-2 border border-status-accent/50 hover:border-status-accent hover:bg-status-accent/5 text-status-accent font-interface font-medium px-8 py-4 rounded-xl shadow-[0_0_15px_rgba(0,229,255,0.15)] transition-all duration-300 transform hover:-translate-y-0.5"
              >
                <Shield className="w-5 h-5" />
                Enter Guardian Mode
              </Link>
            </div>
          </div>

          {/* Hero Right Content (Interactive Globe) */}
          <div className="lg:col-span-5 flex justify-center items-center">
            <EarthGlobe />
          </div>
        </div>
      </main>

      {/* Statistics Strip */}
      <section className="border-y border-white/10 bg-bg-surface/50 backdrop-blur-md relative z-10 py-10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div className="space-y-1">
              <p className="font-mono text-3xl md:text-4xl font-bold text-status-accent">
                <AnimatedCounter value={47832} />
              </p>
              <p className="text-xs font-interface uppercase tracking-widest text-text-secondary">
                Tracked Satellites
              </p>
            </div>
            <div className="space-y-1">
              <p className="font-mono text-3xl md:text-4xl font-bold text-status-critical">
                <AnimatedCounter value={23} />
              </p>
              <p className="text-xs font-interface uppercase tracking-widest text-text-secondary">
                Collision Alerts
              </p>
            </div>
            <div className="space-y-1">
              <p className="font-mono text-3xl md:text-4xl font-bold text-status-warning">
                <AnimatedCounter value={6} />
              </p>
              <p className="text-xs font-interface uppercase tracking-widest text-text-secondary">
                Active Disasters
              </p>
            </div>
            <div className="space-y-1">
              <p className="font-mono text-3xl md:text-4xl font-bold text-status-safe">
                <AnimatedCounter value={847} />
              </p>
              <p className="text-xs font-interface uppercase tracking-widest text-text-secondary">
                Protected Assets
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Capabilities Sections */}
      <section className="py-24 px-6 max-w-7xl mx-auto w-full z-10 relative">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="font-display text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-wide">
            Next-Gen Intelligence Capabilities
          </h2>
          <p className="text-text-secondary font-interface">
            Engineered to process real-time orbital telemetry, geospatial environmental maps, and celestial alignments under one workspace context.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {capabilities.map((cap, i) => {
            const Icon = cap.icon;
            return (
              <GlassCard key={i} glowColor={cap.glow as any} className="flex flex-col space-y-4">
                <div className="w-12 h-12 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-status-accent">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="font-display text-xl font-bold text-white">{cap.title}</h3>
                <p className="text-text-secondary text-sm font-interface leading-relaxed">
                  {cap.desc}
                </p>
              </GlassCard>
            );
          })}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-24 border-t border-white/5 bg-bg-surface/20 backdrop-blur-sm z-10">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
            <h2 className="font-display text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-wide">
              How It Works
            </h2>
            <p className="text-text-secondary font-interface">
              Zenith consolidates planetary threat vectors, computing complex spatial intersections at the edge.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 relative">
            {workflowSteps.map((step, i) => (
              <div key={i} className="flex flex-col space-y-4 relative z-10 bg-bg-void/50 p-6 rounded-2xl border border-white/5">
                <div className="font-mono text-5xl font-extrabold text-white/10">{step.step}</div>
                <h3 className="font-display text-xl font-bold text-white">{step.title}</h3>
                <p className="text-text-secondary text-sm font-interface leading-relaxed">
                  {step.desc}
                </p>
              </div>
            ))}
            
            {/* Connecting line for design system details */}
            <div className="absolute top-1/2 left-0 right-0 h-0.5 border-t border-dashed border-white/10 -z-0 hidden md:block" />
          </div>
        </div>
      </section>

      {/* Technology Philosophy Section */}
      <section className="py-24 px-6 max-w-7xl mx-auto w-full z-10">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-5 space-y-6">
            <h2 className="font-display text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-wide leading-tight">
              Operational Precision.
              <br />
              Zero Compromises.
            </h2>
            <p className="text-text-secondary font-interface">
              Zenith's technical philosophy is rooted in sub-millisecond query delivery, visual density, and unified operating layers. We do not design wrappers — we code mission systems.
            </p>
          </div>
          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div className="p-6 bg-white/2 bg-opacity-30 border border-white/5 rounded-2xl space-y-2">
              <Database className="w-8 h-8 text-status-accent mb-2" />
              <h4 className="font-display font-bold text-white">CesiumJS Native Layer</h4>
              <p className="text-xs text-text-secondary">Fully compatible coordinate-mapping engines designed for seamless rendering of satellite coordinate matrices.</p>
            </div>
            <div className="p-6 bg-white/2 bg-opacity-30 border border-white/5 rounded-2xl space-y-2">
              <Layers className="w-8 h-8 text-primary-vivid mb-2" />
              <h4 className="font-display font-bold text-white">Multi-Payload Datasets</h4>
              <p className="text-xs text-text-secondary">Optimized to read combined feeds, uniting climate hazard nodes and telemetry arrays.</p>
            </div>
            <div className="p-6 bg-white/2 bg-opacity-30 border border-white/5 rounded-2xl space-y-2">
              <Zap className="w-8 h-8 text-status-safe mb-2" />
              <h4 className="font-display font-bold text-white">Sub-100ms Ingestion</h4>
              <p className="text-xs text-text-secondary">Real-time alerts processed at the client edge, minimizing command latency during risk escalation.</p>
            </div>
            <div className="p-6 bg-white/2 bg-opacity-30 border border-white/5 rounded-2xl space-y-2">
              <CheckCircle2 className="w-8 h-8 text-status-critical mb-2" />
              <h4 className="font-display font-bold text-white">Asset Security Protocols</h4>
              <p className="text-xs text-text-secondary">End-to-end telemetry verification, protecting strategic communications systems.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer CTA */}
      <footer className="border-t border-white/10 bg-bg-surface/40 py-16 px-6 text-center z-10">
        <div className="max-w-4xl mx-auto space-y-8">
          <h3 className="font-display text-2xl sm:text-3xl md:text-4xl font-bold text-white">
            The mission begins now.
          </h3>
          <p className="text-text-secondary font-interface max-w-lg mx-auto">
            Acquire tactical awareness of sovereign assets and earth anomalies. Get started with Project Zenith.
          </p>
          <div className="flex justify-center">
            <Link
              href="/dashboard"
              className="flex items-center gap-2 bg-gradient-to-r from-primary via-primary-vivid to-status-accent hover:from-primary-vivid hover:to-status-accent text-white font-interface font-medium px-10 py-5 rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all duration-300 transform hover:-translate-y-1"
            >
              Launch Mission Control
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
          <div className="pt-8 text-[10px] font-mono text-text-muted">
            PROJECT ZENITH © 2026 // CLASSIFIED SECURE OPERATING ENGINE // ALL RIGHTS RESERVED
          </div>
        </div>
      </footer>
    </div>
  );
}
