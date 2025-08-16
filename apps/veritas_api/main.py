from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

import redis
import structlog
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from schemas import JobResults, JobStatus, RunRequest
from store import create_job, read_results, read_status

log = structlog.get_logger(__name__)
app = FastAPI(title="Veritas API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for React UI
try:
    app.mount("/react", StaticFiles(directory="static", html=True), name="react")
except Exception as e:
    log.warning(f"Could not mount React UI: {e}")

# SPA fallback for client-side routes under /react/*
@app.get("/react/{path:path}", include_in_schema=False)
def react_spa_fallback(path: str):
    index = Path("static/index.html")
    if index.exists():
        return HTMLResponse(index.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>React app not built</h1>", status_code=503)

r = redis.from_url(os.getenv("REDIS_URL", "redis://living-truth-redis:6379/0"))


@app.on_event("startup")
def on_start():
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(20))
    log.info("api.startup")


@app.get("/health")
def health():
    try:
        # Simple ping to redis to confirm connectivity
        r.ping()
        return {"status": "ok", "service": "veritas_api"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.post("/jobs", response_model=JobStatus)
def create(req: RunRequest):
    job_id = create_job(req.model_dump())
    r.lpush("veritas:jobs", job_id)
    return JobStatus(
        job_id=job_id, state="queued", stage="queued", progress=0.0, metrics={}
    )


@app.get("/jobs/{job_id}", response_model=JobStatus)
def status(job_id: str):
    st = read_status(job_id)
    if not st:
        raise HTTPException(404, "job not found")
    return JobStatus(job_id=job_id, **st)


@app.get("/jobs/{job_id}/results", response_model=JobResults)
def results(job_id: str):
    res = read_results(job_id)
    if not res:
        raise HTTPException(404, "results not available")
    return JobResults(**res)
