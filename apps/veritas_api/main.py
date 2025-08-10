from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, redis, structlog
from schemas import RunRequest, JobStatus, JobResults
from store import create_job, read_status, read_results

log = structlog.get_logger(__name__)
app = FastAPI(title="Veritas API")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8501"], allow_methods=["*"], allow_headers=["*"])
r = redis.from_url(os.getenv("REDIS_URL","redis://living-truth-redis:6379/0"))

@app.on_event("startup")
def on_start():
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(20))
    log.info("api.startup")

@app.post("/jobs", response_model=JobStatus)
def create(req: RunRequest):
    job_id = create_job(req.model_dump())
    r.lpush("veritas:jobs", job_id)
    return JobStatus(job_id=job_id, state="queued", stage="queued", progress=0.0, metrics={})

@app.get("/jobs/{job_id}", response_model=JobStatus)
def status(job_id: str):
    st = read_status(job_id)
    if not st: raise HTTPException(404, "job not found")
    return JobStatus(job_id=job_id, **st)

@app.get("/jobs/{job_id}/results", response_model=JobResults)
def results(job_id: str):
    res = read_results(job_id)
    if not res: raise HTTPException(404, "results not available")
    return JobResults(**res)

