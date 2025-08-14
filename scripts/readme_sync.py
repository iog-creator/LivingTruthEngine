#!/usr/bin/env python
from datetime import date
import json, glob, os
inv = sorted(glob.glob("logs/repo_health/*.json"))[-1]
data = json.load(open(inv))
tools = [t["name"] for t in data.get("mcp_tools", [])][:50]
services = [s["name"] for s in data.get("docker_services", [])][:50]
template = f"""# Living Truth Engine — Phase 9

**Current focus:** 9.5.7 Resilience Dashboard UI  
**Last repo health run:** {date.today().isoformat()}

## Active MCP tools
{"".join(f"- {t}\n" for t in tools)}

## Active Docker services
{"".join(f"- {s}\n" for s in services)}

## How to run
- `docker compose -f docker/docker-compose.yml up -d --build`
- App: http://localhost:8050
- CI smoke: `bash scripts/resilience_dashboard_test.sh`
"""
open("README.md","w",encoding="utf-8").write(template)
print("README synced.")
