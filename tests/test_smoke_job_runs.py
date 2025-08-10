from __future__ import annotations

import json
from pathlib import Path

import requests

from src.ingestion_general.runners import VeritasRunner


DASHBOARD = "http://localhost:8050"


def test_dashboard_health() -> None:
    r = requests.get(f"{DASHBOARD}/health", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "healthy", f"health={data}"
    assert data.get("service") == "dashboard"


def test_dashboard_root_contains_job_runs() -> None:
    # Prefer server-exposed metadata if available (less brittle than HTML search)
    r = requests.get(f"{DASHBOARD}/meta", timeout=5)
    if r.status_code == 200:
        data = r.json()
        tabs = data.get("tabs", [])
        assert any(t in ("Job Runs", "Veritas Runs") for t in tabs), f"tabs={tabs}"
    else:
        r = requests.get(DASHBOARD, timeout=10)
        assert r.status_code == 200
        html = r.text
        assert "Job Runs" in html or "Veritas Runs" in html, "Job Runs tab label not found in HTML"


def test_start_run_and_bundle_exists(tmp_path: Path) -> None:
    # Use project runner to create a run (dashboard button triggers the same code path)
    runner = VeritasRunner()
    status = runner.start(topic="SmokeRun", max_docs=1, sources=["web"])  # writes bundle

    bundle = Path(status.bundle_dir)
    assert bundle.exists(), f"missing bundle: {bundle}"
    assert (bundle / "manifest.json").exists(), "manifest missing"
    assert (bundle / "metrics.json").exists(), "metrics missing"
    assert (bundle / "proofs" / "merkle_roots.json").exists(), "proofs missing"

    # Open bundle through API to ensure readable structure
    opened = runner.open_bundle(status.run_id)
    assert opened["manifest"]["run_id"] == status.run_id


