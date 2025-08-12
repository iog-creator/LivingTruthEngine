from __future__ import annotations

import os
from fastapi.testclient import TestClient

from src.dashboard.unified_dashboard import main


def test_ai_activity_snapshot_and_emit() -> None:
    # Ensure test mode for emit helper
    os.environ.setdefault("TEST_MODE", "1")

    app = main()
    client = TestClient(app)

    # Initial snapshot is empty
    snap0 = client.get("/api/ai-activity/snapshot").json()
    assert snap0["status"] == "ok"
    assert isinstance(snap0["data"], dict)

    # Emit a test event
    payload = {
        "kind": "llm",
        "status": "inference",
        "model": "qwen3-8b",
        "provider": "LM Studio",
        "run_id": "pytest",
    }
    emit = client.post("/api/_test/ai-activity/emit", json=payload).json()
    assert emit["status"] == "ok"

    # Snapshot should reflect last event
    snap1 = client.get("/api/ai-activity/snapshot").json()
    assert snap1["status"] == "ok"
    llm = snap1["data"].get("llm")
    assert llm and llm["status"] == "inference"
    assert llm.get("model") == "qwen3-8b"


def test_ai_activity_websocket_receives_events() -> None:
    os.environ.setdefault("TEST_MODE", "1")
    app = main()
    client = TestClient(app)

    with client.websocket_connect("/ws/ai-activity") as ws:
        # Trigger an event
        payload = {
            "kind": "embedder",
            "status": "working",
            "model": "bge-m3",
            "provider": "LM Studio",
        }
        r = client.post("/api/_test/ai-activity/emit", json=payload)
        assert r.status_code == 200

        # WS should receive the event
        msg = ws.receive_json()
        assert msg["ai_type"] == "embedder"
        assert msg["status"] == "working"

