#!/usr/bin/env python
import os, json, datetime, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

def _list(paths, exts):
    for p in paths:
        p = (ROOT / p)
        if not p.exists():
            continue
        for dirpath, _, files in os.walk(p):
            for f in files:
                if any(f.endswith(e) for e in exts):
                    full = pathlib.Path(dirpath) / f
                    rel = full.relative_to(ROOT).as_posix()
                    yield rel

def _compose_services():
    compose = ROOT / "docker" / "docker-compose.yml"
    if not compose.exists():
        return []
    y = yaml.safe_load(compose.read_text())
    out = []
    for name, spec in (y.get("services") or {}).items():
        ports = spec.get("ports") or []
        labels = (spec.get("labels") or {})
        out.append({
            "name": name,
            "ports": [str(p) for p in ports],
            "labels": {str(k): str(v) for k, v in labels.items()},
            "profile": ",".join(spec.get("profiles", []) or []),
        })
    return out

def _mcp_tools():
    out = []
    for rel in _list(["src"], [".py"]):
        if "/mcp_servers/" in rel:
            try:
                s = (ROOT / rel).read_text(encoding="utf-8", errors="ignore")
                if "@mcp.tool" in s or ".tool(" in s:
                    out.append({"name": pathlib.Path(rel).name, "file": rel})
            except Exception:
                pass
    return out

def main():
    docs = []
    for rel in _list([".", "docs", "rules"], [".md", ".mdc"]):
        docs.append({"name": pathlib.Path(rel).name, "file": rel})
    specs = [{"name": pathlib.Path(rel).name, "file": rel} for rel in _list(["specs"], [".json"])]
    inventory = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "docs": docs,
        "specs": specs,
        "mcp_tools": _mcp_tools(),
        "docker_services": _compose_services(),
        "schema_version": 2
    }
    outdir = ROOT / "logs" / "repo_health"
    outdir.mkdir(parents=True, exist_ok=True)
    outfile = outdir / f"{datetime.date.today()}.json"
    outfile.write_text(json.dumps(inventory, indent=2))
    print(f"Inventory saved to {outfile}")

if __name__ == "__main__":
    main()
