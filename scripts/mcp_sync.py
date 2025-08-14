#!/usr/bin/env python
import os, json, glob, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOLS = []
for p in glob.glob("src/mcp_servers/**/*.py", recursive=True):
    s = open(p, encoding="utf-8", errors="ignore").read()
    if "@mcp.tool" in s or ".tool(" in s:
        TOOLS.append({"name": pathlib.Path(p).stem, "file": pathlib.Path(p).as_posix()})
specs_dir = ROOT / "specs"; specs_dir.mkdir(exist_ok=True)
now = datetime.datetime.utcnow().isoformat()
# create/update spec files
for t in TOOLS:
    spec = {"name": t["name"], "version": "1.0.0", "updated": now, "envelope": {"status":"ok|error","data?":{},"error?":{"code":"STRING","message":"STRING"}}}
    path = specs_dir / f"{t['name']}.json"
    open(path, "w", encoding="utf-8").write(json.dumps(spec, indent=2))
# update MCP_REQUIREMENTS_REFERENCE.md
ref = ROOT / "MCP_REQUIREMENTS_REFERENCE.md"
lines = ["# MCP Requirements Reference (auto)\n\n", f"_updated: {now}_\n\n"]
for t in sorted(TOOLS, key=lambda x: x["name"]):
    lines.append(f"- **{t['name']}** — `specs/{t['name']}.json` (src: `{t['file']}`)\n")
open(ref, "w", encoding="utf-8").write("".join(lines))
# archive orphaned specs
spec_paths = { (specs_dir/f"{t['name']}.json").as_posix() for t in TOOLS }
orph = [p for p in glob.glob("specs/*.json") if p not in spec_paths]
if orph:
    arch = ROOT / "archive" / "specs"; arch.mkdir(parents=True, exist_ok=True)
    for p in orph:
        os.replace(p, arch / pathlib.Path(p).name)
print(f"Synced {len(TOOLS)} tools; archived {len(orph)} orphans.")
