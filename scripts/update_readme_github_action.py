#!/usr/bin/env python
from datetime import date
import json, glob, os, re

def update_readme():
    inv = sorted(glob.glob("logs/repo_health/*.json"))[-1]
    with open(inv) as f: 
        data = json.load(f)
    services = [s["name"] for s in data.get("docker_services", []) if s.get("name") not in (None, "services")]
    tools = [t["name"] for t in data.get("mcp_tools", [])]
    readme = "README.md"
    template = f"""# Living Truth Engine — Phase 9

**Current focus:** 9.5.7.1 Repo Health Completion  
**Last repo health run:** {date.today().isoformat()}

## Active MCP tools
{chr(10).join(f'- {t}' for t in tools[:50])}

## Active Docker services
{chr(10).join(f'- {s}' for s in services[:50])}

## How to run
- `docker compose -f docker/docker-compose.yml up -d --build`
- App: http://localhost:8050
- CI smoke: `bash scripts/resilience_dashboard_test.sh`
"""
    open(readme, "w", encoding="utf-8").write(template)
    print("README.md updated.")

if __name__ == "__main__":
    update_readme()
