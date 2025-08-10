from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

Connector = Literal["youtube","web","pdf"]

class RunRequest(BaseModel):
    target: str
    connectors: List[Connector] = ["youtube"]
    max_items: int = 10
    crawl_depth: int = 1
    gates: Dict[str, float] = {"budget_usd_per_run": 0.0}
    order: Literal["oldest","newest"] = "oldest"
    video_ids: Optional[List[str]] = None  # optional manual override

class JobStatus(BaseModel):
    job_id: str
    state: Literal["queued","running","done","error","paused"]
    stage: Optional[str] = None
    progress: float = 0.0
    metrics: Dict[str, float] = {}
    message: Optional[str] = None

class JobResults(BaseModel):
    claims: List[dict]
    fracture_score: float
    unity_bridges: List[dict]
    run_folder: str
    notes: Optional[Dict] = None

