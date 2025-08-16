#!/usr/bin/env python3
"""
Validate reports/ssot_meta_index.json:
 - JSON presence & parse
 - Basic schema for rules/docs entries
 - Per-block "SSOT Meta" schema (owner/severity/tags/dependsOn/autofixAllowed/phase)
 - Freshness: index mtime >= latest mtime of rules/docs (with sensible excludes)

Exit codes:
 0  OK
 1  Validation error (schema/freshness/missing)
"""
from __future__ import annotations
import json, sys, time, re
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(".").resolve()
IDX = ROOT / "reports" / "ssot_meta_index.json"
EXCLUDES = {".git","node_modules","venv",".venv","__pycache__",".ruff_cache",".mypy_cache","dist","build"}
PHASE_RE = re.compile(r"^\d+(?:\.\d+)*$")
SEVERITIES = {"low","medium","high","critical"}

def err(code: str, msg: str, details: Optional[dict]=None) -> int:
    out = {"status":"error","error":{"code":code,"message":msg}}
    if details: out["error"]["details"]=details
    print(json.dumps(out, indent=2))
    return 1

def ok(data: dict) -> int:
    print(json.dumps({"status":"ok","data":data}, indent=2))
    return 0

def latest_src_mtime() -> float:
    latest = 0.0
    # rules
    rdir = ROOT/".cursor"/"rules"
    if rdir.exists():
        for p in rdir.glob("*.mdc"):
            latest = max(latest, p.stat().st_mtime)
    # core docs (if present)
    docs = [
        "README.md","project_master_log.md","MCP_REQUIREMENTS_REFERENCE.md",
        "SERVICES_MANIFEST.md","LM_STUDIO_INTEGRATION.md"
    ]
    for d in docs:
        p = ROOT/d
        if p.exists():
            latest = max(latest, p.stat().st_mtime)
    # phase summaries
    for p in ROOT.glob("PHASE_*_COMPLETION_SUMMARY.md"):
        latest = max(latest, p.stat().st_mtime)
    return latest

def valid_ssot_block(block: Dict[str, Any]) -> Optional[str]:
    # owner: str optional
    if "owner" in block and not isinstance(block["owner"], str):
        return "owner_must_be_string"
    # severity: optional enum
    if "severity" in block:
        sv = str(block["severity"]).lower()
        if sv not in SEVERITIES:
            return f"severity_invalid:{sv}"
    # tags: list[str]
    if "tags" in block:
        tags = block["tags"]
        if not isinstance(tags, list) or not all(isinstance(t,str) for t in tags):
            return "tags_must_be_list_of_strings"
    # dependsOn: list[str]
    if "dependsOn" in block:
        dp = block["dependsOn"]
        if not isinstance(dp, list) or not all(isinstance(t,str) for t in dp):
            return "dependsOn_must_be_list_of_strings"
    # autofixAllowed: bool
    if "autofixAllowed" in block and not isinstance(block["autofixAllowed"], bool):
        return "autofixAllowed_must_be_bool"
    # phase: string like 9.5.7.4.10
    if "phase" in block and (not isinstance(block["phase"], str) or not PHASE_RE.match(block["phase"])):
        return "phase_must_be_dotted_numbers"
    return None

def validate_index() -> int:
    if not IDX.exists():
        return err("missing_index","reports/ssot_meta_index.json not found. Run `make meta-index`.")
    try:
        data = json.loads(IDX.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return err("json_parse_error", "Invalid JSON in ssot_meta_index.json", {"exception": str(e)})
    # top-level keys
    if "rules" not in data or "docs" not in data:
        return err("schema_top", "Index must contain 'rules' and 'docs' arrays.")
    rules = data.get("rules") or []
    docs = data.get("docs") or []
    if not isinstance(rules, list) or not isinstance(docs, list):
        return err("schema_top_types", "'rules' and 'docs' must be arrays.")
    # per-rule checks
    r_errors = []
    for r in rules:
        if not isinstance(r, dict):
            r_errors.append("rule_not_object"); continue
        if not isinstance(r.get("file",""), str): r_errors.append("rule_file_invalid")
        if "description" in r and not isinstance(r["description"], str): r_errors.append("rule_description_invalid")
        if "globs" in r and r["globs"] is not None and not (isinstance(r["globs"], str) or isinstance(r["globs"], list)): r_errors.append("rule_globs_invalid")
        if "alwaysApply" in r and not isinstance(r["alwaysApply"], bool): r_errors.append("rule_alwaysApply_invalid")
        # SSOT meta blocks
        blks = r.get("ssot_meta") or []
        if not isinstance(blks, list): r_errors.append("ssot_meta_blocks_invalid"); continue
        for b in blks:
            if not isinstance(b, dict):
                r_errors.append("ssot_meta_block_not_object"); continue
            why = valid_ssot_block(b)
            if why: r_errors.append(why)
    if r_errors:
        return err("schema_rules", "Rule entries invalid", {"issues": r_errors[:25]})
    # freshness: index must be newer than src
    idx_mtime = IDX.stat().st_mtime
    src_mtime = latest_src_mtime()
    if idx_mtime + 1 < src_mtime:  # 1 second slack
        return err("stale_index","Meta index is older than rules/docs. Re-run `make meta-index`.",
                   {"index_mtime": idx_mtime, "latest_source_mtime": src_mtime})
    return ok({"rules": len(rules), "docs": len(docs), "fresh": True})

if __name__ == "__main__":
    sys.exit(validate_index())
