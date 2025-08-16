#!/usr/bin/env python3
"""
Pre-commit guard:
- If any .cursor/rules/*.mdc or SSOT core docs changed in the index, regenerate
  reports/ssot_meta_index.json and validate it.
- Auto-stage the refreshed artifacts so commits stay coherent.
"""
from __future__ import annotations
import subprocess, sys
from pathlib import Path

ROOT = Path(".").resolve()
REPORTS = ROOT / "reports"
TARGET = REPORTS / "ssot_meta_index.json"

SSOT_DOCS = {
    "README.md",
    "project_master_log.md",
    "MCP_REQUIREMENTS_REFERENCE.md",
    "SERVICES_MANIFEST.md",
    "LM_STUDIO_INTEGRATION.md",
}

def changed_files():
    # Use --cached to inspect staged content; fall back to unstaged if needed
    try:
        out = subprocess.check_output(["git","diff","--name-only","--cached"], text=True)
    except Exception:
        out = ""
    files = [f.strip() for f in out.splitlines() if f.strip()]
    return files

def relevant(paths):
    for p in paths:
        if p.startswith(".cursor/rules/") and p.endswith(".mdc"):
            return True
        if Path(p).name in SSOT_DOCS:
            return True
        if Path(p).name.startswith("PHASE_") and p.endswith("_COMPLETION_SUMMARY.md"):
            return True
    return False

def run(cmd):
    subprocess.check_call(cmd, cwd=str(ROOT))

def main():
    files = changed_files()
    if not files or not relevant(files):
        return 0
    REPORTS.mkdir(parents=True, exist_ok=True)
    # regenerate + validate; fail-fast on error
    run([sys.executable, "scripts/collect_yaml_meta.py", "--out", str(TARGET)])
    run([sys.executable, "scripts/validate_ssot_meta_index.py"])
    # auto-stage
    run(["git","add", str(TARGET)])
    latest = TARGET.with_name("ssot_meta_index_latest.json")
    if latest.exists():
        run(["git","add", str(latest)])
    print("✓ meta index refreshed & staged (pre-commit guard)")
    return 0

if __name__ == "__main__":
    sys.exit(main())

