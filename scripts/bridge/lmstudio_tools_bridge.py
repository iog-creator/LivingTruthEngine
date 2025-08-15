#!/usr/bin/env python3
"""
LM Studio Tools Bridge (local-only):
- Exposes a minimal OpenAI-tools-compatible HTTP API with *safe* functions:
    verify_ssot()         : run comprehensive SSOT check (no --fix)
    read_ssot_report()    : return JSON report (if exists)
    draft_patches()       : propose tiny, safe edits (read-only draft)
    run_repo_inventory()  : optional repo scan summary (lightweight)
- Never writes to repo; never runs --fix. Cursor remains executor of changes.

For MCP: LM Studio can also connect to our existing MCP server
(src/mcp_servers/phase9_mcp_server.py). This bridge is for "OpenAI tools" style.
"""
from __future__ import annotations
import os, json, subprocess
from pathlib import Path
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports" / "ssot_report.json"
app = FastAPI(title="LM Studio Tools Bridge")

class ToolRequest(BaseModel):
    params: Dict[str, Any] = {}

def run(cmd: str) -> tuple[int, str]:
    p = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "") + (f"\nSTDERR:\n{p.stderr}" if p.stderr else "")
    return p.returncode, out.strip()

@app.post("/tools/verify_ssot")
def verify_ssot(_: ToolRequest):
    os.environ["CI"] = "true"  # force non-AI mode
    code, out = run('python scripts/verify_complete_ssot_system.py --scope fast --json reports/ssot_report.json --sarif reports/ssot_report.sarif')
    return {"status": "ok" if code == 0 else "fail", "output": out}

@app.post("/tools/read_ssot_report")
def read_ssot_report(_: ToolRequest):
    if REPORT.exists():
        try:
            return {"status": "ok", "data": json.loads(REPORT.read_text())}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    return {"status": "ok", "data": {}}

@app.post("/tools/draft_patches")
def draft_patches(req: ToolRequest):
    """Return suggested minimal edits (specs only), never apply."""
    # Simple heuristic: suggest normalizing SSOT terms in README if inconsistent
    suggestions = []
    readme = ROOT / "README.md"
    if readme.exists():
        t = readme.read_text(encoding="utf-8", errors="ignore")
        if "Single Source of Truth" not in t and "SSOT" in t:
            suggestions.append({
                "file": "README.md",
                "spec": "README.md|SSOT -> Single Source of Truth (SSOT)",
                "rationale": "Normalize terminology"
            })
    return {"status": "ok", "suggestions": suggestions}

@app.post("/tools/run_repo_inventory")
def run_repo_inventory(_: ToolRequest):
    code, out = run("python scripts/repo_inventory.py || true")
    return {"status": "ok", "output": out}

# uvicorn entry
def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=int(os.getenv("LMSTUDIO_TOOLS_PORT","8756")))

if __name__ == "__main__":
    main()
