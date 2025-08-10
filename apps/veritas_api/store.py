import json, uuid, threading
from pathlib import Path

ROOT = Path("/app/data/runs")
LOCK = threading.Lock()

def create_job(payload:dict)->str:
    job_id = str(uuid.uuid4())
    d = ROOT / job_id
    d.mkdir(parents=True, exist_ok=True)
    (d/"request.json").write_text(json.dumps(payload), encoding="utf-8")
    update_status(job_id, {"state":"queued","stage":"queued","progress":0.0,"metrics":{}})
    return job_id

def update_status(job_id:str, status:dict):
    (ROOT / job_id / "status.json").write_text(json.dumps(status), encoding="utf-8")

def read_status(job_id:str)->dict:
    f = ROOT / job_id / "status.json"
    return json.loads(f.read_text()) if f.exists() else {}

def write_results(job_id:str, results:dict):
    (ROOT / job_id / "results.json").write_text(json.dumps(results), encoding="utf-8")

def read_results(job_id:str)->dict:
    f = ROOT / job_id / "results.json"
    return json.loads(f.read_text()) if f.exists() else {}

