from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json, subprocess, pathlib, signal
from schemas import RunRequest, JobStatus, JobResults
from store import create_job, read_status, update_status, read_results
import redis

app = FastAPI(title="Veritas Nexus API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
r = redis.from_url(os.getenv("REDIS_URL","redis://redis:6379/0"))
MCP = {}

def launch_mcp():
    root = pathlib.Path(os.getenv("MCP_REGISTRY","/app/mcp"))
    servers = ["web","pdf","llm_local","embeddings","reranker","provenance","graph"]
    for s in servers:
        p = subprocess.Popen(["python", str(root/s/"server.py")])
        MCP[s]=p

@app.on_event("startup")
def on_start():
    launch_mcp()

@app.on_event("shutdown")
def on_stop():
    for p in MCP.values():
        try: p.send_signal(signal.SIGTERM)
        except: pass

@app.post("/jobs", response_model=JobStatus)
def create(req: RunRequest):
    job_id = create_job(req.dict())
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
