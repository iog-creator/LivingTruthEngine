from pydantic import BaseModel
from typing import List, Dict, Optional

class RunRequest(BaseModel):
    target: str
    connectors: List[str]
    max_items: int
    crawl_depth: int
    gates: Dict[str, float]
    video_ids: Optional[List[str]] = None

class JobStatus(BaseModel):
    job_id: str
    state: str
    stage: str
    progress: float
    metrics: Dict[str, float]

class JobResults(BaseModel):
    claims: List[Dict] = []
    fracture_score: float
    unity_bridges: List[Dict]
    run_folder: str
