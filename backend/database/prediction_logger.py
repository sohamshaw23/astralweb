"""
database/prediction_logger.py

Project Zenith
Centralised Prediction Logger

Usage (inside any service method, after successful inference):
    from database.prediction_logger import log_prediction

    log_prediction(
        model="collision",
        prediction="High Risk",
        confidence=87.3,
        input_features=params,      # the dict passed to the model
        request=request,            # Flask request object (for user/IP)
    )

The call is fire-and-forget: if the database is unavailable the error
is printed to stderr and the API response is NOT affected.

NOTE: all database imports are deferred to call-time so that a missing
psycopg2 driver (or any other DB setup problem) never prevents Flask from
starting up.
"""

import sys
import traceback
from datetime import datetime

from flask import Request


# ---------------------------------------------------------------------------
# Human-readable action templates per model
# ---------------------------------------------------------------------------

_MISSION_ACTIONS = {
    "collision":      "Collision probability assessed",
    "hotspot":        "Wildfire hotspot prediction executed",
    "disaster":       "Disaster classification prediction executed",
    "satellite_risk": "Satellite risk assessment executed",
    "congestion":     "Orbital congestion prediction executed",
    "anomaly":        "Anomaly detection scan executed",
}


def log_prediction(
    model: str,
    prediction: str,
    confidence,
    input_features=None,
    request=None,
):
    """
    Persist one prediction to PostgreSQL and write a corresponding
    MissionLog entry.

    Parameters
    ----------
    model           : Model identifier string — one of:
                      collision / hotspot / disaster /
                      satellite_risk / congestion / anomaly
    prediction      : Primary label / result returned to the client.
    confidence      : Model confidence percentage (0-100), or None.
    input_features  : Dict of raw input parameters fed to the model.
    request         : Flask request object; used to extract the
                      requesting user (from JWT/session) or their IP.

    Returns
    -------
    The new PredictionLog.id on success, or None on failure.
    All imports and DB operations are deferred so a missing psycopg2
    driver or unavailable DB never crashes Flask startup.
    """
    try:
        # Lazy imports — only executed when a prediction actually happens
        from database.postgres import SessionLocal          # noqa: PLC0415
        from database.models import PredictionLog, MissionLog  # noqa: PLC0415
    except Exception:
        print(
            "[prediction_logger] WARNING: database unavailable — "
            "prediction will not be persisted.\n"
            f"{traceback.format_exc()}",
            file=sys.stderr,
        )
        return None

    db = SessionLocal()
    try:
        user = _resolve_user(request)
        now  = datetime.utcnow()

        # 1. Write PredictionLog row
        log_row = PredictionLog(
            model=model,
            prediction=str(prediction),
            confidence=(
                round(float(confidence), 4)
                if confidence is not None else None
            ),
            timestamp=now,
            input_features=input_features or {},
            user=user,
        )
        db.add(log_row)
        db.flush()   # get the auto-generated id without full commit

        # 2. Write MissionLog row (cross-reference)
        action = _MISSION_ACTIONS.get(model, f"{model} prediction executed")
        mission_row = MissionLog(
            action=action,
            status="success",
            details={
                "prediction_log_id": log_row.id,
                "model":             model,
                "prediction":        str(prediction),
                "confidence":        confidence,
                "user":              user,
                "timestamp":         now.isoformat() + "Z",
            },
            timestamp=now,
        )
        db.add(mission_row)
        db.flush()

        # Back-fill the soft reference on PredictionLog
        log_row.mission_log_id = mission_row.id

        db.commit()
        return log_row.id

    except Exception:
        db.rollback()
        print(
            f"[prediction_logger] WARNING: could not persist prediction "
            f"for model={model!r}. The API response is NOT affected.\n"
            f"{traceback.format_exc()}",
            file=sys.stderr,
        )
        return None

    finally:
        db.close()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resolve_user(request) -> str | None:
    """
    Extract the best available user identifier from the Flask request.
    Priority: JWT 'sub' claim → remote IP address.
    """
    if request is None:
        return None

    # Try JWT identity (works if flask-jwt-extended is installed)
    try:
        from flask_jwt_extended import get_jwt_identity   # noqa: PLC0415
        identity = get_jwt_identity()
        if identity:
            return str(identity)
    except Exception:
        pass

    # Fallback to IP address
    return (
        request.headers.get("X-Forwarded-For", request.remote_addr)
        or "unknown"
    )
