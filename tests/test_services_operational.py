"""
Operational service tests with concrete, human-meaningful assertions.

Covers:
- DevDocs, Rulego, MCP Solver containers: health JSON shape and status
- LM Studio: models list presence and endpoint capability (embeddings or chat)
- MCP Hub: categories for documentation/workflow/solver and tool invocation
"""

from __future__ import annotations

import os
import json
import re
import requests
from typing import Any, Dict, List


BASES = {
    "devdocs": "http://localhost:9126",
    "rulego": "http://localhost:9127",
    "solver": "http://localhost:9128",
    "lm_studio": os.getenv("LM_STUDIO_ENDPOINT", "http://localhost:1234"),
}


def _assert_health(base: str, expected_service: str) -> Dict[str, Any]:
    resp = requests.get(f"{base}/health", timeout=5)
    assert resp.status_code == 200, f"{expected_service} /health not 200: {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "ok", f"{expected_service} status not ok: {data}"
    assert data.get("service") == expected_service, f"{expected_service} service mismatch: {data}"
    return data


def test_devdocs_health():
    data = _assert_health(BASES["devdocs"], "devdocs")
    # Human-usable output context
    assert set(data.keys()) >= {"status", "service"}


def test_rulego_health():
    data = _assert_health(BASES["rulego"], "rulego")
    assert set(data.keys()) >= {"status", "service"}


def test_solver_health():
    data = _assert_health(BASES["solver"], "mcp-solver")
    assert set(data.keys()) >= {"status", "service"}


def test_lm_studio_models_and_capabilities():
    # List models
    resp = requests.get(f"{BASES['lm_studio']}/v1/models", timeout=10)
    assert resp.status_code == 200, f"LM Studio /v1/models not 200: {resp.status_code}"
    payload = resp.json()
    models: List[Dict[str, Any]] = payload.get("data", [])
    assert isinstance(models, list), f"LM Studio models payload malformed: {payload}"
    assert len(models) >= 1, "LM Studio returned no models; add a model in LM Studio UI and rerun."

    # Try embeddings if an embedding model is present
    embedding_model = next((m.get("id") for m in models if re.search(r"embed|embedding", str(m.get("id", "")), re.I)), None)
    if embedding_model:
        e_resp = requests.post(
            f"{BASES['lm_studio']}/v1/embeddings",
            json={"input": "hello world", "model": embedding_model},
            timeout=15,
        )
        assert e_resp.status_code == 200, f"Embeddings endpoint failed: {e_resp.status_code} {e_resp.text}"
        e_json = e_resp.json()
        assert "data" in e_json, f"Embeddings response missing data: {e_json}"
        return

    # Otherwise, try chat completions if a likely chat model exists
    chat_model = next((m.get("id") for m in models if not re.search(r"embed|embedding", str(m.get("id", "")), re.I)), None)
    if chat_model:
        c_resp = requests.post(
            f"{BASES['lm_studio']}/v1/chat/completions",
            json={
                "model": chat_model,
                "messages": [{"role": "user", "content": "Say hello"}],
                "max_tokens": 8,
                "stream": False,
            },
            timeout=20,
        )
        assert c_resp.status_code == 200, f"Chat endpoint failed: {c_resp.status_code} {c_resp.text}"
        c_json = c_resp.json()
        assert "choices" in c_json, f"Chat response missing choices: {c_json}"
        return

    # If neither endpoint is available, at least models are listed; provide guidance
    assert False, (
        "LM Studio lists models but neither embeddings nor chat endpoints validated. "
        "Load an embedding or chat model compatible with LM Studio and rerun."
    )


def test_hub_categories_and_tools():
    # Import hub and validate categories + execute status tools
    from src.mcp_servers.mcp_hub_server import MCPHubServer

    hub = MCPHubServer()
    cats = hub.get_tool_categories()
    for cat, expected in {
        "documentation": ["crawl_docs", "retrieve_docs"],
        "workflow": ["query_rulego_chain", "list_rulego_chains"],
        "solver": ["solve_constraint", "route_llm"],
    }.items():
        tools = cats.get(cat, [])
        for name in expected:
            assert name in tools, f"Missing {name} in {cat} category"

    # Execute status tools through hub; assert healthy markers
    dd = hub.execute_tool("get_devdocs_status", {})
    rg = hub.execute_tool("get_rulego_status", {})
    sv = hub.execute_tool("get_solver_status", {})
    assert "✅" in dd and "http://" in dd, f"DevDocs status not healthy: {dd}"
    assert "✅" in rg and "http://" in rg, f"Rulego status not healthy: {rg}"
    assert "✅" in sv and "http://" in sv, f"Solver status not healthy: {sv}"



