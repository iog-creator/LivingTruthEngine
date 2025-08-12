from __future__ import annotations

from pathlib import Path
import json
from fastapi.testclient import TestClient

from src.dashboard.unified_dashboard import main
import os


def write_fake_run(tmp_dir: Path) -> str:
    run_id = "testnorm"
    run_dir = tmp_dir / f"{run_id}.veritasrun"
    run_dir.mkdir(parents=True, exist_ok=True)
    # Minimal manifest with doc_count
    (run_dir / "manifest.json").write_text(json.dumps({"doc_count": 1}), encoding="utf-8")
    # corpus with non-standard keys (url + sentences)
    corpus = {
        "doc_id": "x",
        "url": "https://example.com/x",
        "title": "Example Doc",
        "sentences": [{"text": "Hello world."}, {"text": "More text."}],
        "meta": {},
    }
    with open(run_dir / "corpus.jsonl", "w", encoding="utf-8") as f:
        f.write(json.dumps(corpus) + "\n")
    return run_id


def test_corpus_normalization(tmp_path: Path, monkeypatch) -> None:
    # Point runs dir to temp data dir
    base = tmp_path / "data" / "outputs" / "runs"
    base.mkdir(parents=True, exist_ok=True)

    # Monkeypatch filesystem root used by the app by chdir into repo root-like structure
    # We simulate project root by creating the expected path layout in tmp_path and chdir there.
    run_id = write_fake_run(base)
    # Point the dashboard to our temp runs dir
    os.environ["VERITAS_RUNS_DIR"] = str(base)

    app = main()
    client = TestClient(app)

    # Validate list runs shows 1 doc
    runs = client.get("/api/runs").json()
    assert runs["status"] == "ok"
    found = any(item["run_id"] == run_id for item in runs["data"])
    assert found

    # Fetch corpus and ensure text/url normalized
    cp = client.get(f"/api/runs/{run_id}/corpus").json()
    assert cp["status"] == "ok"
    docs = cp["data"]["documents"]
    assert len(docs) == 1
    d0 = docs[0]
    assert "uri" in d0 and d0["uri"].startswith("https://example.com")
    assert "text" in d0 and "Hello world" in d0["text"]

