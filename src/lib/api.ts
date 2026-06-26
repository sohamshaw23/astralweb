/**
 * src/lib/api.ts
 * Unified API client for Astral backend integration
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000";

// --- Type Definitions ---

export interface LiveSatelliteData {
  name: string;
  latitude: number;
  longitude: number;
  altitude_km: number;
}

export interface TelemetryData {
  velocity_kmh: number;
  altitude_km: number;
  orbital_period_minutes: number;
  orbits_per_day: number;
}

export interface ActiveHotspotsBreakdown {
  total: number;
  high: number;
  medium: number;
  low: number;
  extreme: number;
}

export interface DisastersBreakdown {
  total: number;
  wildfires: number;
  floods: number;
  cyclones: number;
  landslides: number;
  volcanoes: number;
  status: string;
}

export interface WeatherSummary {
  condition: string;
  visibility_km: number;
  cloud_cover_pct: number;
  wind_speed_kmh: number;
  temperature_c: number;
  humidity_pct: number;
  trend: string;
  coverage_assets: string[];
  last_pass_utc: string;
}

export interface SpaceWeather {
  kp_index: number;
  geomagnetic_storm: string;
  solar_flux_f107: number;
  sunspot_count: number;
  proton_flux_pfu: number;
  xray_class: string;
  aurora_visible: boolean;
  satellite_impact: "Low" | "Moderate" | "High" | "Critical";
  source: string;
}

export interface DashboardAnalytics {
  total_satellites: number;
  average_risk: number;
  collision_alerts: number;
  collision_status: string;
  congestion_score: number;
  global_risk: {
    score: number;
    level: string;
  };
  active_hotspots: ActiveHotspotsBreakdown;
  disasters: DisastersBreakdown;
  weather_summary: WeatherSummary;
  space_weather: SpaceWeather;
  generated: string;
}

export interface CollisionAlert {
  satellite: string;
  risk: "Low" | "Moderate" | "High" | "Critical";
  distance_km: number;
}

export interface CollisionAlertsResponse {
  alerts: CollisionAlert[];
}

export interface AnomalyInfo {
  id: string;
  source: string;
  score: number;
  trend: "up" | "down" | "stable";
  timestamp: string;
}

export interface ChatResponse {
  response?: string;
  reply?: string;
  prompt?: string;
  insights?: string[];
  status?: string;
}

export interface HealthResponse {
  status: string;
  project: string;
  version: string;
  timestamp: string;
  services: Record<string, string>;
}

// --- Helper Fetch Function ---

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_URL}${path}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText} at ${path}`);
  }

  return response.json() as Promise<T>;
}

// --- Client Functions ---

/**
 * Fetches live tracked satellites from the backend
 */
export async function getSatellites(): Promise<LiveSatelliteData[]> {
  return apiFetch<LiveSatelliteData[]>("/api/satellites/live");
}

/**
 * Fetches real-time ISS telemetry
 */
export async function getTelemetry(): Promise<TelemetryData> {
  return apiFetch<TelemetryData>("/api/iss/telemetry");
}

/**
 * Fetches unified dashboard analytics
 */
export async function getAnalytics(): Promise<DashboardAnalytics> {
  return apiFetch<DashboardAnalytics>("/api/analytics/dashboard");
}

/**
 * Fetches active collision warnings/alerts
 */
export async function getPredictions(): Promise<CollisionAlertsResponse> {
  return apiFetch<CollisionAlertsResponse>("/api/analytics/collision/alerts");
}

/**
 * Fetches space weather parameters
 */
export async function getSpaceWeather(): Promise<SpaceWeather> {
  return apiFetch<SpaceWeather>("/api/ai/space-weather");
}

/**
 * Fetches backend readiness and service health
 */
export async function getMissionStatus(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>("/api/health");
}

/**
 * Sends a chat query to the AI Mission Assistant
 */
export async function postChat(prompt: string): Promise<ChatResponse> {
  return apiFetch<ChatResponse>("/api/ai/chat", {
    method: "POST",
    body: JSON.stringify({ prompt }),
  });
}
