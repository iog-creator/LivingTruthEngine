---
phase: 9.5.7.2
status: active
last_reviewed: 2025-08-14
related_files:
  - docker/docker-compose.yml
  - scripts/service_feature_map.py
  - scripts/verify_service_docs_complete.py
  - scripts/verify_compose_healthchecks.py
  - scripts/gen_service_docs.py
  - scripts/readme_sync.py
---

# Living Truth Engine — Service Manifest

This document is the **single source of truth** for all services used in Phase 9.5.7.2. It replaces individual files in `docs/services/*`. CI will fail if any required section is missing.

## Legend
- **Core**: must be UP for 9.5.7 dashboard to be complete.
- **Optional**: enabled via profiles; not required for 9.5.7 baseline.

---

## Core Services

### 1) dashboard (core)
**Role**: Primary web app — serves REST `/api/*`, WebSocket `/ws/*`, and the Resilience Dashboard UI.  
**Ports**: `8050:8050`  
**Environment**: 
- `PYTHONPATH=/app:/app/src`
- `LM_STUDIO_ENDPOINT=http://host.docker.internal:1234/v1`
**Healthcheck**: `GET http://localhost:8050/api/health` → 200  
**Code Paths**:
- `src/api/health.py`, `src/api/resilience.py`
- `ui/components/resilience/ResilienceDashboard.tsx`  
**Tests**:
- `tests/api/test_resilience_api.py`
- `tests/ui/resilience_dashboard.spec.ts`
- `scripts/resilience_dashboard_test.sh`

---

### 2) postgres (core)
**Role**: Datastore for resilience scores, anomalies, chaos results, error budgets.  
**Ports**: `5434:5432`  
**Healthcheck**: `pg_isready` → 0  
**Migrations**: `docker/initdb/004_error_budget.sql`, `docker/initdb/005_resilience.sql`  
**Tests**:
- Exercised indirectly by API schema tests (reads series).

---

### 3) mcp‑solver (core)
**Role**: MCP tool host used to trigger chaos, compute resilience scores, export reports.  
**Ports**: `9128:3000`  
**Healthcheck**: `GET http://localhost:3000/health` → 200  
**Code Paths**: `src/mcp_servers/phase9_mcp_server.py`  
**Tests**: `tests/mcp/test_resilience_dashboard_tools.py`

---

### 4) redis (core)
**Role**: Queue/cache for chaos, predictive monitoring, proactive recovery.  
**Ports**: `6380:6379`  
**Healthcheck**: `redis-cli ping` → `PONG`  
**Tests**: `tests/services/test_redis_smoke.py`

---

### 5) veritas_worker (core, i.e., "worker")
**Role**: Executes jobs, writes results to Postgres.  
**Ports**: none (exposes health server on 8090 internally)  
**Healthcheck**: `GET http://localhost:8090/health` → 200  
**Code Paths**: `src/services/veritas_worker/health_server.py`  
**Tests**: `tests/services/test_veritas_worker_smoke.py`

---

## Supporting/Optional Services

### lm‑studio (optional)
**Role**: Local LLM/embedding runtime for dev profile.  
**Ports**: `1235:1234`  
**Healthcheck**: TCP on `:1234`  
**Tests**: `tests/services/test_lm_studio_smoke.py`

### devdocs (optional)
**Role**: Dev docs MCP endpoint / static docs host.  
**Ports**: `9126:24125`  
**Environment**: (none)  
**Healthcheck**: `GET http://localhost:24125/health` → 200  
**Tests**: `tests/services/test_devdocs_smoke.py`

### langflow (optional)
**Role**: Workflow UI/orchestrator; not required for 9.5.7 baseline.  
**Ports**: `7860:7860`  
**Environment**: 
- `LANGFLOW_DATABASE_URL=postgresql://langflow:langflow@postgres:5432/langflow`
- `LANGFLOW_CONFIG_DIR=/app/langflow`
- `PYTHONPATH=/app/langflow_source:/app/langchain_source`
**Healthcheck**: `GET http://localhost:7860/health` → 200  
**Tests**: `tests/services/test_langflow_smoke.py` (skipped if profile off)

### neo4j (optional)
**Role**: Graph storage for entity relationships.  
**Ports**: `7474:7474`, `7687:7687`  
**Healthcheck**: `cypher-shell 'RETURN 1'` → 1  
**Tests**: `tests/services/test_neo4j_smoke.py` (optional)

### rulego (optional)
**Role**: Policy engine for guardrails.  
**Ports**: `9127:8080`  
**Healthcheck**: `GET http://localhost:8080/health` → 200  
**Tests**: `tests/services/test_rulego_smoke.py`

### veritas_api (supporting)
**Role**: Domain API consumed by console & workers.  
**Ports**: `8080:8080`  
**Healthcheck**: `GET http://localhost:8080/health` → 200  
**Code Paths**: `src/services/veritas_api/main.py`  
**Tests**: `tests/services/test_veritas_api_smoke.py`

### veritas_console (supporting)
**Role**: Thin UI that talks to `veritas_api`.  
**Ports**: `8501:8501`  
**Healthcheck**: `GET http://localhost:8501/health` → 200  
**Code Paths**: `src/services/veritas_console/main.py`  
**Tests**: `tests/services/test_veritas_console_smoke.py`
