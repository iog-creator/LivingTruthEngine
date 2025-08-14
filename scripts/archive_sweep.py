#!/usr/bin/env python
import json, os, re, glob, shutil, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
INV = sorted(glob.glob(str(ROOT / "logs/repo_health/*.json")))[-1]
inv = json.loads(open(INV, encoding="utf-8").read())

# read reference texts to keep files that are explicitly linked
refs = ""
for p in ("README.md","MCP_REQUIREMENTS_REFERENCE.md","project_master_log.md"):
    fp = ROOT / p
    if fp.exists():
        refs += fp.read_text(encoding="utf-8", errors="ignore")

def mtime_days(path: pathlib.Path) -> int:
    try:
        age = (datetime.datetime.now() - datetime.datetime.fromtimestamp(path.stat().st_mtime)).days
        return age
    except FileNotFoundError:
        return 99999

docs = [d["file"] for d in inv.get("docs", []) if "/archive/" not in d["file"]]
phase_doc = re.compile(r"PHASE_[0-9_]+.*\.md$", re.I)
referenced = {d for d in docs if os.path.basename(d) in refs}
candidates = []
for d in docs:
    if phase_doc.search(d) and d not in referenced:
        age = mtime_days(ROOT / d)
        if age >= 120:
            candidates.append(d)

ARCH = ROOT / "archive" / "docs"
ARCH.mkdir(parents=True, exist_ok=True)
moved = []
for d in candidates:
    src = ROOT / d
    dst = ARCH / os.path.basename(d)
    if src.exists() and not dst.exists():
        shutil.move(str(src), str(dst))
        moved.append(d)

# update archive index
idx = ARCH / "README.md"
lines = ["# Archived Docs (auto-generated)\n", f"_Updated: {datetime.date.today().isoformat()}_\n\n"]
for d in sorted(moved):
    lines.append(f"- {os.path.basename(d)}\n")
idx.write_text("".join(lines), encoding="utf-8")

print(f"Archived {len(moved)} docs.")
