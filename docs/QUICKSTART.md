---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: []
---

# Quick Start

This is the fastest way to run the Living Truth Engine and get your first result in under 60 seconds.

**Note**: This documentation is part of the Living Truth Engine's Single Source of Truth (SSOT) system. For the complete project overview, see the main [README.md](../README.md) and [project_master_log.md](../project_master_log.md).

## Requirements
- Docker + Docker Compose
- Python 3.13 (optional for local tooling)

## Start all services
```bash
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
docker compose -f docker/docker-compose.yml up -d
```

## URLs
- Dashboard: http://localhost:8050
- Langflow: http://localhost:7860
- Neo4j: http://localhost:7474
- LM Studio: http://localhost:1234

## First analysis (dashboard)
1. Open http://localhost:8050
2. Use prefilled channel `https://www.youtube.com/@imaginationpodcastofficial`
3. Defaults: limit 10, depth 3, sort oldest
4. Optional: Add "Run Label" and a "Save To Directory" path
5. Click Start Analysis

The run appears in Recent Runs and the Runs tab. Analyze tab lets you view results (Summary, Entities, Claims, Graph, Timeline).

## Health checks
```bash
curl -f http://localhost:8050/api/health        # Dashboard
curl -f http://localhost:7860/health            # Langflow
curl -f http://localhost:1234/v1/models         # LM Studio
curl -f http://localhost:7474/                  # Neo4j
redis-cli -p 6380 ping                          # Redis
```

## Minimal API examples
```bash
# List runs (strict MCP-only mode)
curl -s http://localhost:8050/api/runs | jq .

# Get run details
RUN_ID=<your_run_id>
curl -s http://localhost:8050/api/runs/$RUN_ID | jq .

# Get run corpus
echo $RUN_ID
curl -s http://localhost:8050/api/runs/$RUN_ID/corpus | jq .

# List MCP tools (strict MCP-only mode)
curl -s http://localhost:8050/api/tools | jq .

# Execute a tool via dashboard
curl -s http://localhost:8050/api/execute \
  -H 'Content-Type: application/json' \
  -d '{"tool_name":"get_status","params":{}}' | jq .
```

## Troubleshooting
- Use Ctrl+Shift+R to hard-refresh dashboard after updates
- All dashboard endpoints return `{status,data,error}`
- System requires all health gates to pass before starting runs
- Check `/api/health/full` for detailed health status
