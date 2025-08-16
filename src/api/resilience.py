# src/api/resilience.py
from fastapi import APIRouter, Query
from datetime import datetime, timedelta
from ._envelope import ok, err

router = APIRouter(prefix="/api/resilience", tags=["resilience"])


def _series(hours=24, base=85.0):
    now = datetime.utcnow()
    step = []
    for i in range(hours):
        step.append(
            {
                "t": (now - timedelta(hours=(hours - 1 - i))).isoformat(),
                "score": base + (i % 5 - 2),
            }
        )
    return step


@router.get("/score")
def score(window_hours: int = Query(24, ge=1, le=168)):
    base = 86.0
    series = _series(window_hours, base)
    components = {
        "chaos_recovery": 0.88,
        "anomaly_detection": 0.90,
        "proactive_recovery": 0.87,
        "error_budget": 0.92,
    }
    ci = {"floor": 80, "pass": (sum(p["score"] for p in series) / len(series)) >= 80}
    return ok(
        {
            "now": datetime.utcnow().isoformat(),
            "score": base,
            "components": components,
            "series": series,
            "ci": ci,
        }
    )


@router.get("/chaos")
def chaos(
    from_: str | None = None,
    to: str | None = None,
    scenario: str | None = None,
    service: str | None = None,
    blast: str | None = None,
):
    items = [
        {
            "id": "demo-1",
            "scenario": "cpu_pressure",
            "blast": "small",
            "service": "dashboard",
            "started_at": datetime.utcnow().isoformat(),
            "duration_s": 25,
            "recovery_s": 9,
            "status": "recovered",
        }
    ]
    return ok({"items": items, "count": len(items)})


@router.get("/anomalies")
def anomalies(
    from_: str | None = None, to: str | None = None, severity: str | None = None
):
    items = [
        {
            "id": "a-1",
            "metric": "latency_p95",
            "severity": "high",
            "delta": 1.7,
            "predicted_breach_in_min": 12,
        }
    ]
    return ok({"items": items, "count": len(items)})
