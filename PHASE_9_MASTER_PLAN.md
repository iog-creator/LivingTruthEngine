# PHASE_9_MASTER_PLAN.md — Living Truth Engine (Guided Incremental PRs)

> Source of truth for Phase 9 (9.3 → 9.5).  
> Cursor protocol: **one PR per sub‑phase**, following the order below.  
> For each PR:
> 1) Create/commit files under “Files” for that sub‑phase only.  
> 2) Add a short `PHASE_<subphase>_COMPLETION_SUMMARY.md` in repo root at merge time.  
> 3) Run smoke (provided) and `python build_master_log.py append`.

---

## ✅ Phase 9.3 (context: already complete)
**What’s done:** Entity/claim extraction, cross‑doc linking, Rulego checks, DSPy labels, `/api/graph/{run_id}`, basic Graph UI hook, pgvector tables (temporary), smoke/tests, completion summary & master log updates.

**Hindsight items identified:**  
- Embedding vector dimension must come from **SSOT** (no magic numbers like 768).  
- UI split caused drift; we will unify UI in Phase 9.4.  
- Health should surface `embedding_model` and `embedding_dim`.

---

## 🔧 Phase 9.3.1 — Hardening & Consistency (Hotfix) — *PR #1*

**Objectives**
- Fix completion summary generator & ensure `build_master_log.py` picks it up cleanly.
- Add a real `scripts/p9_3_smoke.sh` (idempotent).
- Make pgvector **dimension SSOT‑driven**; remove any hard‑coded dims.
- Health endpoint surfaces `embedding_model` + `embedding_dim`.

**Deliverables**
- `scripts/p9_3_smoke.sh` (prints node/edge counts; exits 0)
- `docker/initdb/003b_graph_dim.sql` (safe migration shell; app handles D at runtime)
- `src/storage/pgvector_store.py`: read embedding **D** from model registry; refuse mismatches; store `model_key`, `dim`.
- `/api/health/full`: add fields `embedding_model`, `embedding_dim`.
- Tests: `tests/test_pgvector_dim.py`, `tests/test_master_log.py`.

**Acceptance**
- Smoke passes; summary written; master log updated.
- `/api/health/full` shows correct model & dim.
- No magic dims left in code or DDL.

**Files**
- scripts/p9_3_smoke.sh
- docker/initdb/003b_graph_dim.sql
- src/storage/pgvector_store.py
- src/common/model_registry.py (expose dim if needed)
- tests/test_pgvector_dim.py
- tests/test_master_log.py

---

## 🌐 Phase 9.4.0 — DevOps Cutover Skeleton (Single Origin) — *PR #2*

**Objectives**
- Single origin: `/api/**` → FastAPI `:8050`; `/` → new UI shell.
- Keep `/status` for the legacy working state page.
- Add CORS toggle via env for local UI dev (if needed).

**Deliverables**
- Reverse proxy config (Traefik/Nginx, compose override or docs).
- CORS env in backend; keep envelope format unchanged.
- `/api/health/full` adds `{ reverse_proxy: true, ui_origin }`.

**Acceptance**
- `/` returns placeholder index.
- `/status` returns legacy page unchanged.
- `/api/health/full` lists `reverse_proxy: true`.

**Files**
- deploy/proxy/{nginx.conf, docker-compose.override.yml}
- src/dashboard/unified_dashboard.py (CORS env toggle)
- scripts/p9_4_0_smoke.sh

---

## 🧱 Phase 9.4.1 — UI Foundation & Scaffold (Next.js) — *PR #3*

**Objectives**
- New **Next.js 14 + TypeScript + Tailwind + shadcn/ui** app.
- API client + Zod envelope guards, React Query, global error boundary.
- Route: `/overview` with placeholder health cards.

**Deliverables**
- `ui/` Next.js App Router project.
- `ui/lib/{api.ts, schemas.ts, query.ts, state.ts}`.
- `ui/app/(dashboard)/layout.tsx`, `ui/app/(dashboard)/overview/page.tsx`.
- Scripts: `scripts/ui_dev.sh`, `scripts/ui_build.sh`.

**Acceptance**
- `npm run dev` → `/overview` renders.
- API client validates `{status,data,error}` (MSW mock ok).

**Files**
- ui/**
- scripts/ui_dev.sh
- scripts/ui_build.sh

---

## ▶️ Phase 9.4.2 — Runs Flow (Start/List/Detail/Verify) — *PR #4*

**Objectives**
- `/runs` + `/runs/[runId]`.
- StartRunForm (loading/disabled/toasts), RunList, RunDetail (manifest, metrics, merkle), Verify Proofs.

**Deliverables**
- Components: `StartRunForm.tsx`, `RunList.tsx`, `RunDetail.tsx`.
- E2E: `tests/e2e/runs.spec.ts`.

**Acceptance**
- E2E: start → list refresh → open → manifest & merkle visible.
- Envelope errors become toasts; no dead buttons.

**Files**
- ui/app/(dashboard)/runs/**
- ui/components/runs/**
- tests/e2e/runs.spec.ts

---

## 🕸️ Phase 9.4.3 — Evidence Graph (MVP) — *PR #5*

**Objectives**
- `/graph` renders force graph from `/api/graph/{run_id}`.
- Stats bar (node/edge counts), findings list, search; **fallback list** if WebGL missing.

**Deliverables**
- `GraphView.tsx` (Cytoscape or force-graph).
- E2E: `tests/e2e/graph.spec.ts`.

**Acceptance**
- Given a `run_id`, graph renders without JS errors; fallback list triggers when needed.

**Files**
- ui/app/(dashboard)/graph/page.tsx
- ui/components/graph/GraphView.tsx
- tests/e2e/graph.spec.ts

---

## 📑 Phase 9.4.4 — Claims & Entities Tables — *PR #6*

**Objectives**
- `/claims` and `/entities` with filters, pagination, row drawer (details + source links).
- Claim badges: `corroborated|weak|contradicted`.

**Deliverables**
- Tables using TanStack Table + faceted filter controls.

**Acceptance**
- Tables load for a `run_id`; filters/pagination work; drawer shows metadata.

**Files**
- ui/app/(dashboard)/claims/page.tsx
- ui/app/(dashboard)/entities/page.tsx
- ui/components/tables/**
- tests/e2e/tables.spec.ts

---

## 🧰 Phase 9.4.5 — Models, Health, Settings (Read‑only) — *PR #7*

**Objectives**
- `/models`: model names, device, endpoint, checksum.
- `/health`: gates + recent fallbacks.
- `/settings`: flags read‑only mirrored from server.

**Deliverables**
- Pages wired to `/api/models` and `/api/health/full`.

**Acceptance**
- Live data displayed; no writes yet.

**Files**
- ui/app/(dashboard)/models/page.tsx
- ui/app/(dashboard)/health/page.tsx
- ui/app/(dashboard)/settings/page.tsx

---

## 🧯 Phase 9.4.6 — Client Observability & Reliability — *PR #8*

**Objectives**
- Global error boundary w/ copyable error details.
- Minimal client metrics (pageview + API timings).
- Retry policy: GETs only; never retry POST.

**Deliverables**
- `ui/components/system/ErrorBoundary.tsx`
- `ui/lib/api.ts` retry/backoff rules
- Unit tests for api client behavior.

**Acceptance**
- Forced error triggers boundary; timings visible in logs; POSTs never auto‑retry.

**Files**
- ui/components/system/ErrorBoundary.tsx
- ui/lib/api.ts
- tests/unit/apiClient.test.ts

---

## 🧪 Phase 9.4.7 — Test & Contract Suite — *PR #9*

**Objectives**
- Zod schemas for all envelopes used by the UI.
- Playwright smoke for Status/Run/Graph; local CI script.

**Deliverables**
- `ui/lib/schemas.ts`
- E2E specs: `status`, `ingest`, `graph`.

**Acceptance**
- All unit + e2e tests pass locally.

**Files**
- ui/lib/schemas.ts
- tests/e2e/{status,ingest,graph}.spec.ts
- package.json (scripts for CI)

---

## 📥 Phase 9.5.0 — Real Adapters (YouTube/Web/PDF) — *PR #10*

**Objectives**
- Production adapters: normalize() → DocumentLike.
- Dedupe by `sha256(text)`; min text length enforced.
- Persist YouTube transcript mode.

**Deliverables**
- `src/adapters/{youtube,web,pdf}.py`
- Runner integration; adapter tests.

**Acceptance**
- Multi‑source run yields ≥1 doc per selected source (sample inputs).
- Smoke validates adapter paths; envelopes OK.

**Files**
- src/adapters/*
- src/runners/multisource_runner.py (wire adapters)
- tests/test_adapters_*.py
- scripts/p9_5_0_smoke.sh

---

## 🧭 Phase 9.5.1 — Embedding Storage: Model‑Aware Dimensions — *PR #11*

**Objectives**
- No magic dims; enforce **dim from SSOT**; allow multiple models safely.
- Partition (or view) by `(model_key, dim)`; ANN indexes per partition.
- Backfill/move script.

**Deliverables**
- Migration: `docker/initdb/004_embeddings.sql`.
- Store writes tagged with `model_key`, `dim`, `version`.
- Health shows `embedding_model`, `embedding_dim`, `dim_mismatch: false`.

**Acceptance**
- Inserts land in correct partition; KNN works with ANN index.

**Files**
- docker/initdb/004_embeddings.sql
- src/storage/pgvector_store.py
- scripts/migrations/move_embeddings_by_model.py
- tests/test_pgvector_dim.py

---

## 🖥️ Phase 9.5.2 — GPU Scheduler + Health Upgrades — *PR #12*

**Objectives**
- VRAM probing + per‑model reservations.
- Lazy model load/unload; fallback logging.
- Health exposes GPU info and recent fallbacks.

**Deliverables**
- `src/common/gpu_scheduler.py`
- `/api/health/full` adds `gpu:{present,vram_total,active_allocations}` and `fallbacks[]`.

**Acceptance**
- Force low VRAM → CPU fallback logged and visible in health.

**Files**
- src/common/gpu_scheduler.py
- src/dashboard/unified_dashboard.py (health fields)
- tests/test_gpu_scheduler.py

---

## 🕰️ Phase 9.5.3 — Timeline API + Graph Polish — *PR #13*

**Objectives**
- `GET /api/timeline/{run_id}` items `{id,type,label,ts_first,ts_last,refs}`.
- Graph filters, pinning, selection drawer polish.

**Deliverables**
- Timeline API + UI view (in Graph page).
- Timeline test; Graph polish.

**Acceptance**
- Timeline renders <1s on sample; smooth interactions.

**Files**
- src/dashboard/unified_dashboard.py (timeline endpoint)
- ui/app/(dashboard)/graph/page.tsx (polish)
- tests/test_timeline_api.py

---

## 🚀 Phase 9.5.4 — Performance Gates & Hardening — *PR #14*

**Objectives**
- Perf harness for `/api/graph`/Timeline; LCP and bundle size budgets.
- Optional CI gates (warn/fail on regression).

**Deliverables**
- `scripts/perf_harness.py`
- Tests asserting p95 API latencies; Next.js bundle analyzer.

**Acceptance**
- `/api/graph` p95 ≤ 1.5s on demo corpus; Timeline ≤ 1.0s.
- UI initial JS ≤ 250KB; LCP ≤ 2.5s (dev box).

**Files**
- scripts/perf_harness.py
- tests/perf/test_perf_targets.py
- ui/next.config.mjs (analyze)

---

# Cursor Working Protocol (strict)

- **One PR per sub‑phase** in the order above.  
- **Commit format**: `phase<subphase>: <short summary> [verified]`.  
- On each PR merge:
  1) Create/update `PHASE_<subphase>_COMPLETION_SUMMARY.md` in repo root (brief: what shipped, evidence of acceptance).  
  2) Run the sub‑phase smoke script (if present).  
  3) `python build_master_log.py append`.

# Ground Rules

- No changes to API envelope `{status,data?,error?}` without plan amendments.  
- No edits to the legacy `home.html`; keep `/status` page functional.  
- Embedding dimension must come from SSOT (model registry/env).  
- If health detects a schema/model mismatch, return a clear 5xx with remediation steps.

---
