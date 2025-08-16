#!/usr/bin/env python
import json, os, subprocess, pathlib, difflib
from datetime import datetime, timezone

def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()

def git(*args): return run(["git", *args])

def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

root = pathlib.Path(git("rev-parse","--show-toplevel"))
reports = root/"reports"; reports.mkdir(parents=True, exist_ok=True)

bundle = {"generated_at_utc": now(), "results": {}}
# 1) MCP import
try:
    from src.mcp_servers.phase9_mcp_server import Phase9MCPServer
    s = Phase9MCPServer()
    for name in ("get_ssot_meta_index","get_rule_integrity_status","verify_ssot"):
        if hasattr(s, name):
            try:
                data = getattr(s, name)()
                bundle["results"][name] = {"status":"ok","data":data}
            except Exception as e:
                bundle["results"][name] = {"status":"error","error":str(e)}
except Exception as e:
    bundle["results"]["mcp_import"] = {"status":"warn","error":str(e)}

# 2) Compose snapshot
try:
    import yaml
    y=yaml.safe_load(open(root/"docker/docker-compose.yml"))
    svcs=y.get("services",{})
    snapshot={"services":[]}
    for k,v in sorted(svcs.items()):
        snapshot["services"].append({
            "name":k,
            "ports":v.get("ports",[]),
            "health":bool(v.get("healthcheck"))
        })
    bundle["compose"]=snapshot
except Exception as e:
    bundle["compose_error"]=str(e)

# 3) Write current snapshot
ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
cur = reports/f"ssot_snapshot_{ts}.json"
cur.write_text(json.dumps(bundle, indent=2), encoding="utf-8")

# 4) Diff vs previous
prev = None
for p in sorted(reports.glob("ssot_snapshot_*.json")):
    if p.name < cur.name:
        prev = p
log = reports/"ssot_watchdog_log.jsonl"
if not log.exists(): log.write_text("", encoding="utf-8")
try:
    diff_text=""
    if prev:
        a = prev.read_text(encoding="utf-8").splitlines(False)
        b = cur.read_text(encoding="utf-8").splitlines(False)
        diff_text = "".join(difflib.unified_diff(a,b,fromfile=prev.name,tofile=cur.name,n=3))
    entry = {
        "ts": now(),
        "git_head": git("rev-parse","--short","HEAD"),
        "snapshot": cur.name,
        "prev_snapshot": prev.name if prev else None,
        "diff_len": len(diff_text),
    }
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry)+"\n")
except Exception as e:
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts":now(),"error":str(e)})+"\n")

# 5) Update master log blocks
ml = root/"project_master_log.md"
ml_txt = ml.read_text(encoding="utf-8") if ml.exists() else ""

def upsert(text: str, start: str, end: str, body: str) -> str:
    import re
    if start in text and end in text:
        return re.sub(start+r".*?"+end, start+"\n"+body+"\n"+end, text, flags=re.S)
    return (text.rstrip()+"\n\n"+start+"\n"+body+"\n"+end) if text else start+"\n"+body+"\n"+end

stack_start, stack_end = "<!-- SSOT:STACK_STATUS START -->", "<!-- SSOT:STACK_STATUS END -->"
summary_start, summary_end = "<!-- MCP:SSOT_SUMMARY START -->", "<!-- MCP:SSOT_SUMMARY END -->"

lines=[f"## Stack Status Snapshot — {now()} (authoritative)",""]
for svc in bundle.get("compose",{}).get("services",[]):
    ports = ", ".join(svc["ports"]) if svc["ports"] else "—"
    lines.append(f"- **{svc['name']}** | ports: {ports} | healthcheck: {'yes' if svc['health'] else 'no'}")

lines2=[f"### MCP SSOT Summary — {now()}",""]
for k,v in bundle.get("results",{}).items():
    lines2.append(f"- **{k}**: {v.get('status','n/a')}")

ml1 = upsert(ml_txt, stack_start, stack_end, "\n".join(lines))
ml2 = upsert(ml1, summary_start, summary_end, "\n".join(lines2))
ml.write_text(ml2, encoding="utf-8")
print(f"✓ Snapshot: {cur.name}")
