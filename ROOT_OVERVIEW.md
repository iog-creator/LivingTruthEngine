# Living Truth Engine - Root Overview

This file gives another AI or developer everything needed to understand and run the project immediately.

## What it is
- Unified dashboard for survivor testimony analysis and evidence discovery
- Phase 8.1 complete with quick start UI and robust fallbacks

## Run it
```bash
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
docker compose -f docker/docker-compose.yml up -d
```

## Primary URL
- Dashboard: http://localhost:8050 (health at /api/health)

## Key endpoints (dashboard)
- POST /api/runs/youtube/start
- GET /api/runs
- GET /api/runs/{id}
- GET /api/runs/{id}/corpus
- GET /api/tools
- POST /api/execute
- GET /api/status
- GET /api/health

All endpoints return `{status, data, error}`.

## Defaults
- Channel: `https://www.youtube.com/@imaginationpodcastofficial`
- Limit: 10
- Depth: 3
- Sort: oldest
- Advanced toggles: OCR Required, JavaScript Render, HF Burst
- Optional: Run Label, Save To Directory

## Fallbacks
- Inside the container, if MCP tools are not reachable, the dashboard falls back to:
  - Listing runs from `data/runs/`
  - `status.json` for run details
  - `corpus.jsonl` for corpus data
  - `config/tool_registry.json` for tool listing

## Health & Service URLs
- Dashboard: http://localhost:8050/api/health
- Langflow: http://localhost:7860/health
- LM Studio: http://localhost:1234/v1/models
- Neo4j: http://localhost:7474/
- Redis: `redis-cli ping`

## Quick API examples
```bash
# List runs
curl -s http://localhost:8050/api/runs | jq .

# Run details
RID=<run_id>
curl -s http://localhost:8050/api/runs/$RID | jq .

# Corpus
echo $RID
curl -s http://localhost:8050/api/runs/$RID/corpus | jq .

# Tools
curl -s http://localhost:8050/api/tools | jq .

# Execute a tool
curl -s http://localhost:8050/api/execute -H 'Content-Type: application/json' \
  -d '{"tool_name":"get_status","params":{}}' | jq .
```

## Read next
- README.md (full project overview)
- PHASE_8_1_COMPLETION_SUMMARY.md (what shipped)
- .cursor/rules/ (rules AI should follow)
