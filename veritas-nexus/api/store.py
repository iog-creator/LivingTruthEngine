import json, uuid, os, pathlib

RUNS = pathlib.Path(os.getenv("RUNS_ROOT","/app/runs"))


def create_job(req: dict) -> str:
    job_id = uuid.uuid4().hex
    job_dir = RUNS / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "request.json").write_text(json.dumps(req))
    (job_dir / "status.json").write_text(json.dumps({"state":"queued","stage":"queued","progress":0.0,"metrics":{}}))
    return job_id


def read_status(job_id: str):
    p = RUNS / job_id / "status.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def update_status(job_id: str, patch: dict):
    st = read_status(job_id) or {}
    st.update(patch)
    (RUNS / job_id / "status.json").write_text(json.dumps(st))


def read_results(job_id: str):
    p = RUNS / job_id / "results.json"
    if not p.exists():
        return None
    return json.loads(p.read_text())


def write_results(job_id: str, data: dict):
    (RUNS / job_id / "results.json").write_text(json.dumps(data))
