---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['scripts/perf_harness.py']
---

# PHASE 9.5.1 MASTER PLAN — Post-UI Series, Pre-Adapter Implementation

This plan supersedes the 9.4.x series and continues directly into Phase 9.5.x.  
It includes:
- All completed work from 9.3.1 → 9.4.7 (summarized)
- Updated MCP rules, gates, and enforcement
- Remaining 9.5.x objectives

---

## ✅ Summary of Completed Work (9.3.1 → 9.4.7)

- **9.3.1 Hardening** — Fixed completion summaries, master log rebuild, pgvector SSOT dims.
- **9.4.0 DevOps Cutover** — Single-origin routing via reverse proxy, decoupled API/UI.
- **9.4.1 UI Scaffold** — Next.js + TS + Tailwind + shadcn/ui foundation.
- **9.4.2 Runs Flow** — Runs list/detail, start form, proof verification.
- **9.4.3 Evidence Graph MVP** — Graph rendering, stats, fallback list view.
- **9.4.4 Claims & Entities Tables** — Searchable tables, details drawer.
- **9.4.5 Models/Health/Settings** — Live API data integration for system views.
- **9.4.6 Observability** — Global error boundary, client metrics, retries.
- **9.4.7 Test Suite** — Zod envelope schemas, Playwright E2E tests.

All MCP Gates for these phases passed, and system rules are enforced.

---

## 🚀 Next Phases (9.5.x Series)

### Phase 9.5.0 — Real Adapters
**Objectives**
- Implement adapters for YouTube, Web, PDF.
- Deduplicate sources by `sha256`.
- Persist transcript mode in DB.

**Acceptance Criteria**
- Multi-source run yields ≥1 doc/source.

**MCP Gates**
- Exit: `mcp.lte.adapters.test_sources`, `mcp.lte.smoke.run_phase` (`scripts/p9_5_0_smoke.sh`)

---

### Phase 9.5.1 — Model-Aware Embedding Storage
**Objectives**
- Remove all magic dims from DB.
- Partition embeddings by `(model_key, dim)`.
- Backfill existing embeddings.

**Acceptance Criteria**
- `/api/health/full` reports no dim mismatch.
- KNN search works post-migration.

**MCP Gates**
- Exit: `mcp.lte.pgvector.db_dim`, `mcp.lte.models.assert_embedding_dim`, `mcp.lte.pgvector.reindex_ann`

---

### Phase 9.5.2 — GPU Scheduler + Health Upgrades
**Objectives**
- GPU VRAM probing & reservation logic.
- Health endpoint shows GPU info & recent fallbacks.

**Acceptance Criteria**
- Forcing low VRAM triggers CPU fallback in health logs.

**MCP Gates**
- Exit: `mcp.lte.gpu.status`, `mcp.lte.gpu.simulate_low_vram`

---

### Phase 9.5.3 — Timeline API + Graph Polish
**Objectives**
- `/api/timeline/{run_id}` endpoint.
- Graph filters, pinning, and selection polish.

**Acceptance Criteria**
- Timeline API responds <1s for sample run.
- Graph UX smooth under load.

**MCP Gates**
- Exit: `mcp.lte.timeline.preview`

---

### Phase 9.5.4 — Performance Gates & Hardening
**Objectives**
- Perf harness to track p95 API latency, LCP budget, bundle size.
- CI gates for regressions.

**Acceptance Criteria**
- `/api/graph` p95 ≤ 1.5s
- JS bundle ≤ 250KB
- LCP ≤ 2.5s

**MCP Gates**
- Exit: Run `scripts/perf_harness.py`, attach results, confirm budgets.

---

## 🔒 Global Enforcement (Rules + System)

**Cursor Rules**
- core_workflow.mdc — PR protocol & MCP hooks.
- api_contracts.mdc — Envelope schema enforcement.
- ui_policy.mdc — Single-origin UI, no legacy edits.
- models_and_embeddings.mdc — SSOT dims, health surfacing.
- fallbacks_and_health.mdc — Allowed fallbacks only, logged.
- mcp_ops.mdc / mcp_integration.mdc — MCP usage protocol.

**System Rules**
- `/api/health/full` shows embedding model/dim, GPU info, fallbacks.
- Reverse proxy routing enforced post-9.4.0.
- No hard-coded dims; DB validated at runtime.
- Legacy UI protected from edits.
- Only approved fallbacks allowed.

**CI Validation**
- `scripts/ci/validate_phase9.sh` checks:
  - Rule existence
  - Phase file monotonicity
  - Envelope spot checks

---

## 📦 Embedded MCP Specs (Abbreviated)
*(Full JSON specs remain in `tools/mcp/specs/` — see repo for detail)*

Namespaces:  
- `mcp.project.rules`  
- `mcp.lte.health`  
- `mcp.lte.models`  
- `mcp.lte.pgvector`  
- `mcp.lte.proxy`  
- `mcp.lte.ui.contracts`  
- `mcp.lte.adapters`  
- `mcp.lte.gpu`  
- `mcp.lte.timeline`  
- `mcp.lte.smoke`

---

**End of 9.5.1 Master Plan**
