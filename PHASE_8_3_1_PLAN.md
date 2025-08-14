---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['config/tool_registry.json']
---

# PHASE 8.3.1 PLAN

## Objective
Finalize Phase 8.2 deliverables, unblock Analyze feature, and lock in MCP-only gates and bring-up cycle.

---

## Bring-Up (Do First)
1. **Rebuild dashboard** (container does not bind-mount source):
```bash
docker compose -f docker/docker-compose.yml build dashboard
docker compose -f docker/docker-compose.yml up -d
```
2. **Health check**:
```bash
curl -s http://localhost:8050/api/health/full | jq .
```
3. **Tiny smoke run** (Limit=1, Depth=1 on Imagination Podcast channel) to confirm `.veritasrun` with corpus.

---

## Phase 8.2 Minimal Slice to Ship
- **AI Activity Panel**: WebSocket `/ws/ai-activity` emitting `{ai_type, status}`; UI shows live icons.
- **Chat Dock**: `POST /api/ai/chat` → MCP forward; collapsible drawer in UI.
- **Run Naming**: `human_name` at creation; PATCH for rename; visible in list.
- **Toggle Propagation Fix**: Ensure OCR/JS/HF toggles pass to `/api/runs/youtube/start`; add Cypress check.
- **Analyze Header Polish**: Pin Explain/Export buttons in Analyze tab header.

**Definition of Done**:
- Icons pulse on inference.
- Chat sends & receives actions.
- Human names visible + rename works.
- Toggles verified in API payload.
- Header buttons anchored.
- All tests green; docs updated.

---

## Known Risks
- Dashboard container must be rebuilt to pick up source changes.
- UI↔API shape/ID mismatches possible; verify with `/api/*` endpoints.
- Enforce “no silent fallbacks” and always run bring-up + smoke before claiming success.

---

## Quick References
- **Core tabs**: Home, Runs, Analyze, Advanced.
- **Endpoints**:
  - `GET /api/health/full`
  - `POST /api/runs/youtube/start`
  - `GET /api/runs`
  - `GET /api/runs/{id}`
  - `GET /api/runs/{id}/corpus`
  - `GET /api/tools`
  - `POST /api/execute`
- Standard response envelope: `{status, data, error}`.

---

## Smoke Test Recipe
```bash
# Health gates
curl -s http://localhost:8050/api/health/full | jq .

# Start tiny run
RID=<run_id>
curl -s http://localhost:8050/api/runs/$RID | jq .
curl -s http://localhost:8050/api/runs/$RID/corpus | jq '.documents | length'
```
Expect ≥1 transcript in `corpus.jsonl`.

---

## MCP Tool Fixes for Analyze
- `analyze_veritas_summary`: Reads run’s corpus.jsonl; returns `{title, uri, snippet, length}`.
- `analyze_veritas_claims`: Returns `{claims: []}` (stub until real extraction).
- Registered in `config/tool_registry.json` under `living_truth_fastmcp_server`.
- Hub registry loader patched to prefer primary registry.

---

## Tests to Add
- `test_summary_200`: POST `/api/analyze/summary` → 200, non-empty snippet.
- `test_claims_200`: POST `/api/analyze/claims` → 200, claims list.
- `test_envelope_shapes`: Endpoints return `{status,data,error}`.

---

## Acceptance Criteria
- Health gates pass.
- MCP tools visible in `/api/tools`.
- Analyze Summary returns snippet for latest run.
- Claims returns empty list (until implemented).
- Tiny smoke run passes.
- All tests green.
