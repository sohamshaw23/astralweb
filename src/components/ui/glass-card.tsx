"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface GlassCardProps extends React.HTMLAttributes<HTMLDivElement> {
  glowColor?: "primary" | "critical" | "safe" | "warning" | "accent";
  hoverEffect?: boolean;
}

export function GlassCard({
  children,
  className,
  glowColor,
  hoverEffect = true,
  ...props
}: GlassCardProps) {
  const glowClasses = {
    primary: "hover:shadow-[0_0_30px_rgba(79,70,229,0.25)] hover:border-primary/40",
    critical: "hover:shadow-[0_0_30px_rgba(255,77,77,0.25)] hover:border-status-critical/40",
    safe: "hover:shadow-[0_0_30px_rgba(0,255,200,0.25)] hover:border-status-safe/40",
    warning: "hover:shadow-[0_0_30px_rgba(255,200,87,0.25)] hover:border-status-warning/40",
    accent: "hover:shadow-[0_0_30px_rgba(0,229,255,0.25)] hover:border-status-accent/40",
  };

  return (
    <div
      className={cn(
        "glass-panel rounded-xl p-6 transition-all duration-300 ease-out text-text-primary backdrop-blur-xl relative overflow-hidden",
        hoverEffect && "hover:-translate-y-1.5 holo-panel hover:bg-bg-surface/80",
        glowColor && glowClasses[glowColor],
        className
      )}
      {...props}
    >
      {/* Background radial gradient overlay on hover */}
      <div className="absolute inset-0 bg-radial from-white/2 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
      {children}
    </div>
  );
}
export default GlassCard;
