#!/usr/bin/env python
import yaml, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
compose = yaml.safe_load(open("docker/docker-compose.yml"))
docs_dir = ROOT / "docs" / "services"; docs_dir.mkdir(parents=True, exist_ok=True)
for name, spec in (compose.get("services") or {}).items():
    md = docs_dir / f"{name}.md"
    ports = "\n".join(f"- {p}" for p in (spec.get("ports") or []))
    envs = spec.get("environment") or {}
    if isinstance(envs, dict):
        env = "\n".join(f"- `{k}`: `{v}`" for k,v in envs.items())
    elif isinstance(envs, list):
        env = "\n".join(f"- `{e}`" for e in envs)
    else:
        env = "- (none)"
    health = spec.get("healthcheck") or {}
    content = f"""---
phase: 9.5.7
status: active
last_reviewed: {datetime.date.today().isoformat()}
related_files: []
---

# Service: {name}

## Role
(brief)

## Ports
{ports or "- (none)"}

## Environment
{env or "- (none)"}

## Healthcheck
- Test: `{health.get('test', '(none)')}`

## Code Paths
- (link to src/* if applicable)

## Tests
- (list tests referencing this service)
"""
    md.write_text(content, encoding="utf-8")
print("Service docs scaffolded/updated.")
