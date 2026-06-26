# 🌌 Project Zenith — Space Situational Awareness & Disaster Intelligence Platform

<div align="center">

![Project Zenith](https://img.shields.io/badge/Project-Zenith-0a0a2e?style=for-the-badge&logo=satellite&logoColor=00e5ff)
![Next.js](https://img.shields.io/badge/Next.js-16.2.9-black?style=for-the-badge&logo=next.js)
![Flask](https://img.shields.io/badge/Flask-3.0.2-000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776ab?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46e3b7?style=for-the-badge&logo=render&logoColor=white)

**Orbit-Scale Spatial Analytics & Safety Engine**

[🌐 Live Website](https://zenith-frontend-xwzt.onrender.com) • [⚙️ Backend API](https://zenith-backend-api-uisr.onrender.com) • [📊 Dashboard](https://zenith-frontend-xwzt.onrender.com/dashboard)

</div>

---

## 📖 Overview

**Project Zenith** is a full-stack, real-time space situational awareness and disaster intelligence platform. It fuses live satellite telemetry, machine learning–powered risk analysis, and geospatial disaster intelligence into a single command centre — accessible from any browser.

The platform enables operators to monitor orbital objects, detect collision risks, identify congestion in low-earth orbit (LEO), assess ground-level disaster hotspots, and query an AI Mission Assistant — all through a premium, animated dark-mode interface.

---

## 🖥️ Pages & Modules

| Page | Route | Description |
|---|---|---|
| **Landing** | `/` | Animated hero with live 3D Earth globe, typewriter telemetry feed, stats counters |
| **Dashboard** | `/dashboard` | Mission control HQ — satellite grid, risk matrix, anomaly feed, system logs |
| **SSA** | `/ssa` | Space Situational Awareness — orbital tracking, debris, collision alerts |
| **Celestial Explorer** | `/celestial-explorer` | Interactive sky-dome with celestial body positions using Skyfield |
| **Disaster Intelligence** | `/disaster-intelligence` | Real-time disaster heatmap with severity scoring and hotspot analysis |
| **Guardian Mode** | `/guardian-mode` | Asset protection view — satellite coverage over strategic ground targets |

---

## ✨ Website Functionality & Unique Features

### 🛰️ Real-Time Orbital Tracking
- Tracks live satellites using **TLE (Two-Line Element)** data ingested and propagated via the **Skyfield** astrodynamics library.
- Propagates satellite positions every refresh cycle to produce accurate latitude, longitude, and altitude in real time.
- Satellites are visualised on a rotating, interactive **3D Earth globe** powered by `react-globe.gl` and `Three.js`.

### 🤖 AI Mission Assistant
- An embedded chat assistant (`/api/ai/chat`) trained on mission context that answers questions about orbital safety, disaster events, and satellite status.
- Generates automated mission summaries, space weather narratives, and disaster analysis reports.
- Falls back gracefully to a Python-based contextual intelligence engine if external AI services are unavailable.

### ☄️ Proprietary ML-Powered Analytics Engine
Nine modular machine learning APIs power the analytics layer:

| ML Module | Capability |
|---|---|
| **Collision** | Predicts probability of collision between tracked objects using XGBoost |
| **Congestion** | Scores orbital band congestion in LEO, MEO, and GEO shells |
| **Anomaly Detection** | Flags anomalous telemetry patterns with severity trending |
| **Satellite Risk** | Multi-factor risk scoring per satellite — debris, solar weather, signal |
| **Disaster Score** | Ground-level disaster risk scoring with wildfire, flood, and cyclone sub-scores |
| **Hotspot Detection** | Identifies thermal and seismic hotspot zones on Earth's surface |
| **Orbital Prediction** | Predicts future orbital positions and decay timelines |
| **Coverage Analysis** | Evaluates ground coverage footprints for asset protection |
| **Visibility** | Computes satellite visibility windows over specific ground coordinates |

### 🌍 Disaster Intelligence
- Fetches live natural disaster data (wildfires, floods, cyclones, volcanic events) from external geospatial APIs.
- Displays disaster events on a global heatmap with severity classification: **Critical / Warning / Info**.
- Provides coordinate-level disaster analysis and AI-narrated summaries.

### 🌌 Celestial Explorer
- Renders the current position of celestial bodies (Sun, Moon, planets) for any location on Earth using the **Skyfield** and **de421 ephemeris** dataset.
- Interactive sky-dome component built with `Three.js` and `react-globe.gl`.

### 🛡️ Guardian Mode
- Monitors strategic assets on the ground and identifies which satellites currently provide coverage.
- Designed for defence, agriculture, and infrastructure monitoring use-cases.

### 🎨 Premium UI/UX Design
- **Glassmorphism** cards with subtle backdrop blur and luminous borders.
- **Animated starfield canvas** background with parallax drift and twinkling stars.
- **Typewriter effect** telemetry readout on the landing page.
- **Animated counters** that count up when scrolled into view.
- **Framer Motion** page transitions and micro-animations throughout.
- **Live telemetry simulation** — satellite positions, signal strengths, and anomaly scores update automatically every 5 seconds even without a backend connection, powered by the `useMissionData` hook.

### ♻️ Resilient Data Architecture
- The frontend is designed for **graceful degradation** — it always shows realistic mock telemetry data and falls back silently if the backend API is unreachable. Users always see a working interface.
- The background scheduler (APScheduler) continuously refreshes satellite TLE data and disaster feeds in the background.

---

## 🚀 Installation & Setup Instructions

### Prerequisites
Make sure you have the following installed:
- **Node.js** `>= 18.x` and **npm** `>= 9.x`
- **Python** `>= 3.11`
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/sohamshaw23/astralweb.git
cd astralweb
```

---

### 2. Frontend Setup (Next.js)

Install dependencies and start the development server:

```bash
# Install all npm packages
npm install

# Start the Next.js dev server
npm run dev
```

The frontend will be available at **http://localhost:3000**.

---

### 3. Backend Setup (Flask)

Navigate to the backend directory and set up a Python virtual environment:

```bash
cd backend

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all Python dependencies
pip install -r requirements.txt
```

#### Environment Variables

Create a `.env` file inside the `backend/` directory with the following:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@localhost:5432/project_zenith
PORT=5001
```

> **Note**: The `DATABASE_URL` is optional. If omitted or if the database is unreachable, the platform will start without database features and will log a warning.

#### Start the Backend Server

```bash
python3 app.py
```

The Flask API will be available at **http://localhost:5001**.

---

### 4. Connect Frontend to Backend

Create a `.env.local` file in the **root** of the project (next to `package.json`):

```env
NEXT_PUBLIC_API_URL=http://localhost:5001
```

Restart the Next.js dev server if it is already running.

---

### 5. (Optional) PostgreSQL Database Setup

If you want to use the full database features, install PostgreSQL and create the database:

```sql
CREATE DATABASE project_zenith;
```

Then run the database initialisation (automatically handled on startup by `init_database()`).

---

## 🌐 Live Deployment (Render)

The entire stack is deployed on **Render** using a Blueprint (`render.yaml`):

| Service | Type | URL |
|---|---|---|
| `zenith-frontend` | Static Site (Next.js) | https://zenith-frontend-xwzt.onrender.com |
| `zenith-backend-api` | Python Web Service | https://zenith-backend-api-uisr.onrender.com |
| `zenith-db` | PostgreSQL 18 | Internal (connected via `DATABASE_URL`) |

To deploy your own instance:
1. Push the repository to GitHub.
2. Go to [dashboard.render.com](https://dashboard.render.com) → **New** → **Blueprint**.
3. Connect your repository and apply the `render.yaml` blueprint.

---

## 📦 Dependencies

### Frontend (Node.js)

| Package | Version | Purpose |
|---|---|---|
| `next` | 16.2.9 | React framework for SSR/SSG/Static Export |
| `react` | 19.2.4 | UI library |
| `react-dom` | 19.2.4 | DOM rendering |
| `three` | ^0.184.0 | 3D rendering engine (WebGL) |
| `@types/three` | ^0.184.1 | TypeScript types for Three.js |
| `react-globe.gl` | ^2.38.0 | Interactive 3D globe component |
| `framer-motion` | ^12.40.0 | Animations and page transitions |
| `lucide-react` | ^1.18.0 | SVG icon library |
| `clsx` | ^2.1.1 | Conditional class name utility |
| `class-variance-authority` | ^0.7.1 | Component variant management |
| `tailwind-merge` | ^3.6.0 | Tailwind class conflict resolution |
| `tailwindcss` | ^4 | Utility-first CSS framework |
| `typescript` | ^5 | Static type checking |

### Backend (Python)

| Package | Purpose |
|---|---|
| `flask` | Web framework for the REST API |
| `flask-cors` | Cross-Origin Resource Sharing (CORS) support |
| `skyfield` | Astrodynamics — satellite propagation, celestial positions |
| `pandas` | Data manipulation and analysis |
| `numpy` | Numerical computing |
| `xgboost` | Gradient boosting ML for collision & risk prediction |
| `scikit-learn` | Machine learning utilities and preprocessing |
| `matplotlib` | Plotting and data visualisation |
| `seaborn` | Statistical data visualisation |
| `requests` | HTTP client for external API calls |
| `transformers` | HuggingFace model loading (AI assistant NLP) |
| `sqlalchemy` | ORM for PostgreSQL database |
| `python-dotenv` | Environment variable loading from `.env` files |
| `APScheduler` | Background scheduler for TLE data refresh jobs |
| `psycopg2-binary` | PostgreSQL database adapter for Python |
| `gunicorn` | Production WSGI server for Flask |

---

## 🗂️ Project Structure

```
astralweb/
├── src/
│   ├── app/
│   │   ├── page.tsx                  # Landing page
│   │   ├── dashboard/page.tsx        # Mission control dashboard
│   │   ├── ssa/page.tsx              # Space Situational Awareness
│   │   ├── celestial-explorer/       # Celestial body viewer
│   │   ├── disaster-intelligence/    # Disaster heatmap & alerts
│   │   └── guardian-mode/            # Asset protection monitor
│   ├── components/
│   │   ├── globe/                    # 3D Earth globe component
│   │   ├── layout/                   # Navbar, layout wrappers
│   │   ├── ui/                       # GlassCard, buttons, etc.
│   │   ├── celestial/                # Sky-dome component
│   │   ├── disaster/                 # Disaster UI widgets
│   │   └── mission/                  # Mission panel components
│   ├── hooks/
│   │   └── useMissionData.ts         # Live + simulated telemetry hook
│   └── lib/
│       └── api.ts                    # Unified backend API client
├── backend/
│   ├── app.py                        # Flask app factory & entry point
│   ├── config.py                     # App configuration
│   ├── requirements.txt              # Python dependencies
│   ├── routes/                       # Flask route blueprints
│   ├── api/                          # ISS, ISRO, health endpoint handlers
│   ├── services/                     # Business logic services
│   ├── ml/                           # ML models (collision, anomaly, etc.)
│   ├── proprietary_apis/             # 9 analytics API endpoints
│   ├── scheduler/                    # Background data refresh jobs
│   ├── database/                     # PostgreSQL ORM setup
│   └── utils/                        # Shared utilities
├── render.yaml                       # Render cloud deployment blueprint
├── next.config.ts                    # Next.js configuration (static export)
└── package.json                      # Frontend package manifest
```

---

## 👥 Team

**Team Zenith** — Built for the AstralWeb Innovate competition.

---

<div align="center">
Made with ❤️ for the cosmos
</div>
