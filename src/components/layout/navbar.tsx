"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { Cpu, Terminal, Shield, Globe2, Moon, Clock, Sparkles } from "lucide-react";

export function Navbar() {
  const pathname = usePathname();
  const [clockTime, setClockTime] = useState("");

  useEffect(() => {
    const timer = setInterval(() => {
      const date = new Date();
      setClockTime(date.toLocaleTimeString("en-US", { hour12: false }));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Hide Navbar completely on the Landing Page (/)
  if (pathname === "/") {
    return null;
  }

  const navLinks = [
    { label: "Mission Control", href: "/dashboard", icon: Terminal },
    { label: "Guardian Mode", href: "/guardian-mode", icon: Shield },
    { label: "Disaster Intel", href: "/disaster-intelligence", icon: Globe2 },
    { label: "Celestial", href: "/celestial-explorer", icon: Moon },
  ];

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-bg-void/70 backdrop-blur-md border-b border-white/10 py-3 shadow-[0_4px_30px_rgba(0,0,0,0.5)] font-mono text-xs select-none">
      <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
        
        {/* Left: Logo + wordmark */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <Cpu className="w-5 h-5 text-status-accent group-hover:rotate-90 transition-transform duration-500" />
          <span className="font-display font-bold text-sm tracking-wider text-white group-hover:text-status-accent transition-colors duration-300">
            ZENITH OS
          </span>
        </Link>

        {/* Center: Route pills */}
        <nav className="hidden md:flex items-center gap-1 bg-white/5 border border-white/10 p-0.5 rounded-lg">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`relative px-3.5 py-1.5 rounded-md font-medium transition-colors ${
                  isActive ? "text-white" : "text-text-secondary hover:text-white"
                }`}
              >
                <span className="relative z-10 flex items-center gap-1.5">
                  {link.label}
                </span>

                {/* Sliding background pill */}
                {isActive && (
                  <motion.div
                    layoutId="active-pill"
                    className="absolute inset-0 bg-primary/45 border border-primary/40 rounded-md -z-0"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Right cluster: AI button | Simulate | system clock | alert count badge */}
        <div className="flex items-center gap-4">
          
          {/* AI Trigger */}
          <button
            onClick={() => window.dispatchEvent(new CustomEvent("trigger-ai"))}
            className="flex items-center gap-1 border border-primary-vivid/30 bg-primary/10 text-primary-vivid px-2.5 py-1.5 rounded hover:bg-primary/20 cursor-pointer transition-colors"
            title="Open AI Command Operative"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">AI COMMAND</span>
          </button>

          {/* Simulate Trigger */}
          <button
            onClick={() => window.dispatchEvent(new CustomEvent("trigger-simulation"))}
            className="flex items-center gap-1 border border-status-accent/30 bg-status-accent/10 text-status-accent px-2.5 py-1.5 rounded hover:bg-status-accent/20 cursor-pointer transition-colors"
            title="Launch Future Simulation"
          >
            <Clock className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">SIMULATE</span>
          </button>

          {/* Clock */}
          <span className="text-text-secondary font-mono hidden sm:inline">{clockTime}</span>

          {/* Alert Badge */}
          <span className="bg-status-critical/15 text-status-critical border border-status-critical/30 font-bold px-2 py-1 rounded-full text-[10px] animate-pulse">
            6 ALERTS
          </span>
        </div>

      </div>
    </header>
  );
}
export default Navbar;
