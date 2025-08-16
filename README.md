# Living Truth Engine — Phase 9

**Current focus:** 9.5.7 Resilience Dashboard UI  
**Last repo health run:** 2025-08-14

## Active MCP tools
- devdocs_mcp_server.py
- living_truth_fastmcp_server.py
- langflow_mcp_server.py
- mcp_solver_server.py
- github_mcp_server.py
- huggingface_mcp_server.py
- rulego_mcp_server.py
- mcp_hub_server.py
- phase9_mcp_server.py
- postgresql_mcp_server.py


## Active Docker services
- langflow
- lm-studio
- postgres
- neo4j
- redis
- living-truth-engine
- devdocs
- rulego
- mcp-solver
- dashboard
- veritas_api
- veritas_worker
- veritas_console


## How to run
- `docker compose -f docker/docker-compose.yml up -d --build`
- App: http://localhost:8050
- CI smoke: `bash scripts/resilience_dashboard_test.sh`

## Development Tools
- **Consolidate Cursor Rules**: `python scripts/consolidate_cursor_rules.py` - Creates a consolidated view of all MDC rules for refactoring

---

### SSOT Policy
This repository enforces a Single Source of Truth (SSOT) for critical docs: `README.md`, `project_master_log.md`, `MCP_REQUIREMENTS_REFERENCE.md`, `SERVICES_MANIFEST.md`, and all `PHASE_*_COMPLETION_SUMMARY.md` in root. CI runs `scripts/verify_ssot_bundle.py` on PRs and nightly.

### Cursor Rules
All Cursor rules from `.cursor/rules/` have been consolidated into `CURSOR_RULES_CONSOLIDATED.md` for refactoring and reorganization purposes. This file contains all 34 active rules with metadata and full content for analysis.
