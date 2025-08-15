import json
from types import SimpleNamespace
from pathlib import Path

import src.agents.ssot_langchain_agent as mod


class _MockResp:
    def __init__(self, payload):
        self._payload = payload
        self.status_code = 200

    def raise_for_status(self):  # pragma: no cover
        return

    def json(self):
        return self._payload


def test_deterministic_agent_monkeypatched(monkeypatch, tmp_path):
    # Arrange: monkeypatch requests.post to avoid real HTTP
    calls = []

    def _fake_post(url, json=None, timeout=30.0):
        calls.append((url, json))
        if url.endswith("/tools/verify_ssot"):
            return _MockResp({"result": "pass", "checks": {"bundle": True}})
        if url.endswith("/tools/read_ssot_report"):
            return _MockResp({"summary": {"ok": True}, "details": {"files": 5}})
        if url.endswith("/tools/draft_patches"):
            return _MockResp({"patches": [{"file": "README.md", "change": "add reference"}]})
        if url.endswith("/tools/run_repo_inventory"):
            return _MockResp({"files": 42})
        raise AssertionError(f"Unexpected URL: {url}")

    monkeypatch.setattr(mod.requests, "post", _fake_post)

    # Use client + agent (no LangChain needed)
    client = mod.SSOTBridgeClient("http://127.0.0.1:8756", timeout=5.0)
    agent = mod.DeterministicSSOTAgent(client)

    # Act
    envelope = agent.run()

    # Assert: envelope and structure
    assert envelope["status"] == "ok"
    data = envelope["data"]
    assert data["sequence"] == ["verify_ssot", "read_ssot_report", "draft_patches"]
    assert data["verify"]["result"] == "pass"
    assert "report" in data and "patches" in data

    # Persist (ensures writer is idempotent)
    out = tmp_path / "out.json"
    (tmp_path).mkdir(parents=True, exist_ok=True)
    # internal save function
    mod._save_report(envelope, out)
    saved = json.loads(out.read_text(encoding="utf-8"))
    assert saved["status"] == "ok"
