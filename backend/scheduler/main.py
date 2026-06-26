"""
scheduler/main.py

Project Zenith
Centralised Background Scheduler

Runs inside the Flask process via APScheduler (BackgroundScheduler).
All jobs execute in daemon threads — a crash in any job is caught,
logged to stderr, and NEVER propagates to Flask.

Job schedule
────────────────────────────────────────────────────
  refresh_tle          every  6 h   TLE dataset from CelesTrak
  refresh_disasters    every  1 h   NASA EONET disaster events + ETL
  refresh_weather      every  1 h   Weather data from Open-Meteo API
  refresh_hotspots     every  2 h   Hotspot dataset reload + ETL
  refresh_redis        every  5 min Analytics cache warm-up
  maybe_retrain        every 24 h   Retrain models if .pkl > MAX_MODEL_AGE_DAYS
────────────────────────────────────────────────────

Usage in app.py:
    from scheduler.main import start_scheduler
    start_scheduler()          # call once inside create_app()
"""

import os
import sys
import time
import logging
import traceback
from datetime import datetime, timezone

logger = logging.getLogger("zenith.scheduler")

# ---------------------------------------------------------------------------
# Tunables
# ---------------------------------------------------------------------------

# How many days old a model .pkl must be before we retrain
MAX_MODEL_AGE_DAYS = int(os.getenv("ZENITH_RETRAIN_AFTER_DAYS", "7"))

# ---------------------------------------------------------------------------
# Individual Job Functions
# ---------------------------------------------------------------------------


def job_refresh_tle():
    """Download fresh TLE data from CelesTrak and hot-reload satellite service."""
    try:
        from scheduler.update_tle import update
        update()

        # Hot-reload the satellite service so live endpoints immediately use new TLEs
        from services.satellite_service import satellite_service
        satellite_service.refresh()

        logger.info("[scheduler] TLE refreshed and satellite service reloaded.")
    except Exception:
        logger.error(
            "[scheduler] TLE refresh FAILED:\n%s", traceback.format_exc()
        )


def job_refresh_disasters():
    """Download latest NASA EONET events and reload the disaster service dataset."""
    try:
        from scheduler.fetch_disasters import fetch
        fetch()

        from scheduler.process_raw_data import process
        process()

        # Hot-reload in-memory dataset so API responses immediately reflect new data
        from services.disaster_service import disaster_service
        disaster_service.load_processed_data()

        logger.info("[scheduler] Disaster data refreshed.")
    except Exception:
        logger.error(
            "[scheduler] Disaster refresh FAILED:\n%s", traceback.format_exc()
        )


def job_refresh_weather():
    """Download latest weather data from Open-Meteo API."""
    try:
        from scheduler.fetch_weather import fetch
        fetch()
        logger.info("[scheduler] Weather data refreshed.")
    except Exception:
        logger.error(
            "[scheduler] Weather refresh FAILED:\n%s", traceback.format_exc()
        )


def job_refresh_hotspots():
    """Process raw hotspots and reload hotspot dataset."""
    try:
        from scheduler.process_raw_data import process
        process()

        from services.hotspot_service import hotspot_service
        hotspot_service.refresh()

        logger.info("[scheduler] Hotspot dataset reloaded (%d records).",
                    hotspot_service.count())
    except Exception:
        logger.error(
            "[scheduler] Hotspot refresh FAILED:\n%s", traceback.format_exc()
        )



def job_refresh_redis():
    """
    Invalidate stale analytics cache keys and eagerly pre-warm them.
    Also resets the legacy in-memory CacheService with fresh snapshots.
    """
    try:
        from scheduler.refresh_cache import refresh
        refresh()

        logger.info("[scheduler] Redis / analytics cache refreshed.")
    except Exception:
        logger.error(
            "[scheduler] Redis refresh FAILED:\n%s", traceback.format_exc()
        )


def _model_needs_retrain(model_key: str, pkl_path: str) -> bool:
    """
    Return True if the .pkl file is older than MAX_MODEL_AGE_DAYS
    or does not exist yet.
    """
    if not os.path.exists(pkl_path):
        logger.warning("[scheduler] Model '%s' not found at %s — will retrain.",
                       model_key, pkl_path)
        return True

    mtime = os.path.getmtime(pkl_path)
    age_days = (time.time() - mtime) / 86_400
    if age_days >= MAX_MODEL_AGE_DAYS:
        logger.info("[scheduler] Model '%s' is %.1f days old — retraining.",
                    model_key, age_days)
        return True

    logger.debug("[scheduler] Model '%s' is %.1f days old — no retrain needed.",
                 model_key, age_days)
    return False


def job_maybe_retrain():
    """
    Check each model's .pkl age; retrain only those that are stale.
    After retraining, evict the cached model from ModelManager so
    the next inference call picks up the fresh weights automatically.
    """
    import subprocess

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ml_dir   = os.path.join(base_dir, "ml")

    models = {
        "collision":     ("collision",    os.path.join(ml_dir, "collision",    "model.pkl")),
        "anomaly":       ("anomaly",      os.path.join(ml_dir, "models",       "anomaly_model.pkl")),
        "hotspot":       ("hotspot",      os.path.join(ml_dir, "models",       "hotspot_model.pkl")),
        "disaster":      ("disaster",     os.path.join(ml_dir, "models",       "disaster_model.pkl")),
        "satellite_risk":("satellite_risk",os.path.join(ml_dir, "models",      "satellite_risk_model.pkl")),
        "congestion":    ("congestion",   os.path.join(ml_dir, "models",       "congestion_model.pkl")),
    }

    retrained = []
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir

    for key, (subdir, pkl_path) in models.items():
        if not _model_needs_retrain(key, pkl_path):
            continue

        train_dir = os.path.join(ml_dir, subdir)
        train_script = os.path.join(train_dir, "train.py")

        if not os.path.exists(train_script):
            logger.warning("[scheduler] No train.py for '%s' — skipping.", key)
            continue

        try:
            logger.info("[scheduler] Retraining '%s' …", key)
            result = subprocess.run(
                [sys.executable, "train.py"],
                cwd=train_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=600,    # 10 min max per model
            )
            if result.returncode != 0:
                logger.error(
                    "[scheduler] Retrain of '%s' exited %d:\n%s",
                    key, result.returncode, result.stderr
                )
            else:
                logger.info("[scheduler] '%s' retrained successfully.", key)
                retrained.append(key)

                # Evict from ModelManager in-memory cache so next request
                # loads the fresh .pkl automatically
                try:
                    from ml.model_manager import model_manager
                    model_manager._models.pop(key, None)
                    logger.info("[scheduler] ModelManager cache cleared for '%s'.", key)
                except Exception:
                    pass

        except subprocess.TimeoutExpired:
            logger.error("[scheduler] Retrain of '%s' timed out.", key)
        except Exception:
            logger.error(
                "[scheduler] Retrain of '%s' FAILED:\n%s",
                key, traceback.format_exc()
            )

    if retrained:
        # Warm cache so new models are immediately exercised
        try:
            job_refresh_redis()
        except Exception:
            pass

    logger.info("[scheduler] Retrain cycle done. Retrained: %s",
                retrained if retrained else "none")


# ---------------------------------------------------------------------------
# Scheduler Bootstrap
# ---------------------------------------------------------------------------

_scheduler = None


def start_scheduler():
    """
    Create and start the APScheduler BackgroundScheduler.
    Safe to call multiple times — only the first call starts the scheduler.
    Degrades gracefully if APScheduler is not installed.
    """
    global _scheduler
    if _scheduler is not None:
        return _scheduler   # already running

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.interval import IntervalTrigger
    except ImportError:
        logger.warning(
            "[scheduler] APScheduler not installed — background jobs disabled. "
            "Install with:  pip install APScheduler"
        )
        return None

    _scheduler = BackgroundScheduler(
        daemon=True,
        job_defaults={
            "coalesce":    True,   # skip missed runs (don't pile up)
            "max_instances": 1,    # never run the same job twice in parallel
        },
    )

    # ── TLE: every 6 hours ───────────────────────────────────────────────
    _scheduler.add_job(
        job_refresh_tle,
        trigger=IntervalTrigger(hours=6),
        id="refresh_tle",
        name="TLE Refresh (CelesTrak)",
        replace_existing=True,
    )

    # ── Disasters: every 1 hour ───────────────────────────────────────────
    _scheduler.add_job(
        job_refresh_disasters,
        trigger=IntervalTrigger(hours=1),
        id="refresh_disasters",
        name="Disaster Data Refresh (NASA EONET)",
        replace_existing=True,
    )

    # ── Weather: every 1 hour ─────────────────────────────────────────────
    _scheduler.add_job(
        job_refresh_weather,
        trigger=IntervalTrigger(hours=1),
        id="refresh_weather",
        name="Weather Data Refresh (Open-Meteo)",
        replace_existing=True,
    )

    # ── Hotspots: every 2 hours ───────────────────────────────────────────
    _scheduler.add_job(
        job_refresh_hotspots,
        trigger=IntervalTrigger(hours=2),
        id="refresh_hotspots",
        name="Hotspot Dataset Reload",
        replace_existing=True,
    )

    # ── Redis / analytics cache: every 5 minutes ─────────────────────────
    _scheduler.add_job(
        job_refresh_redis,
        trigger=IntervalTrigger(minutes=5),
        id="refresh_redis",
        name="Redis Cache Warm-up",
        replace_existing=True,
    )

    # ── Conditional retrain: every 24 hours (02:00 UTC) ──────────────────
    from apscheduler.triggers.cron import CronTrigger
    _scheduler.add_job(
        job_maybe_retrain,
        trigger=CronTrigger(hour=2, minute=0, timezone="UTC"),
        id="maybe_retrain",
        name="Conditional Model Retrain (nightly)",
        replace_existing=True,
    )

    _scheduler.start()
    logger.info(
        "[scheduler] Started with jobs: %s",
        [j.id for j in _scheduler.get_jobs()],
    )
    return _scheduler


def stop_scheduler():
    """Gracefully shut down the scheduler (call at app teardown)."""
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("[scheduler] Stopped.")
    _scheduler = None


def scheduler_status():
    """Return a dict summary of all scheduled jobs (used by health endpoint)."""
    if _scheduler is None or not _scheduler.running:
        return {"status": "stopped", "jobs": []}

    jobs = []
    for job in _scheduler.get_jobs():
        jobs.append({
            "id":         job.id,
            "name":       job.name,
            "next_run":   (
                job.next_run_time.isoformat()
                if job.next_run_time else None
            ),
            "trigger":    str(job.trigger),
        })

    return {
        "status":   "running",
        "jobs":     jobs,
        "job_count": len(jobs),
        "generated": datetime.now(timezone.utc).isoformat(),
    }
