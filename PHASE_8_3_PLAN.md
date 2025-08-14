---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/dashboard/unified_dashboard.py', 'test_no_fallbacks.py', 'manifest.json', 'ingestion_success_flow.cy.ts', 'test_health_gates.py', 'ingestion_error_surface.cy.ts', 'PHASE_8_1_COMPLETION_SUMMARY.md', 'config/tool_registry.json', 'metrics.json', 'tests/test_no_fallbacks.py', 'merkle.json', 'start_disabled_until_gates_pass.cy.ts', 'tests/test_ingestion_youtube_failures.py', 'QUICKSTART.md', 'PHASE_8.md', 'PHASE_8_2_PLAN.md', 'ROOT_OVERVIEW.md', 'tests/test_health_gates.py', 'tests/test_ingestion_youtube_happy_path.py', 'test_ingestion_youtube_failures.py', 'test_ingestion_youtube_happy_path.py']
---

The root problem is the system quietly “helping” via fallbacks, so failures don’t surface, Cursor assumes success, and we drift. We’ll fix that by **killing all fallbacks**, adding hard **health gates**, and making ingestion through **one source of truth (Veritas MCP)** the only path.

Below is a concrete **Phase 8.3 plan** tailored to your repo. I’ll show exactly where fallbacks exist in the docs, what we’ll remove, and how we’ll verify that pulling YouTube transcripts actually works before anything else proceeds.

# Phase 8.3 — No Fallbacks, Verified Ingestion, Cursor Discipline

## Principles (non-negotiable)

* **No fallbacks** anywhere in Dashboard/API/UI. If MCP/Veritas isn’t healthy, the UI must block with a red banner and a 503 reason. Your docs currently advertise filesystem & tool-registry fallbacks in multiple places; we will remove them.  &#x20;
* **Single ingestion path:** `/api/runs/youtube/start` must call the **Veritas MCP tool** (e.g., `start_veritas_youtube_channel_run`) and nothing else. If that tool isn’t reachable/healthy, fail immediately. The MCP tool set is already documented and should remain the only path.&#x20;
* **Fail fast, loud:** Cursor must see red tests/errors instead of “helpful” behavior. Phase 7’s guidelines already call out fail-fast; we’ll enforce it.&#x20;

---

## A. Remove all fallbacks (code, UI, and docs)

**Targets to change**

1. **Dashboard backend** `src/dashboard/unified_dashboard.py`

   * Delete filesystem fallbacks for:

     * `GET /api/runs` / `GET /api/runs/{id}` / `GET /api/runs/{id}/corpus` reading from `data/runs/*`.
     * `GET /api/tools` falling back to `config/tool_registry.json`.
   * When MCP hub is unavailable, return **HTTP 503** with `{status:"error", error:"MCP_UNAVAILABLE", details}`.

2. **Docs**

   * Remove fallback descriptions from:

     * `QUICKSTART.md` (“filesystem fallback enabled…”, “falls back to config/tool\_registry.json”).&#x20;
     * `ROOT_OVERVIEW.md` Fallbacks section.&#x20;
     * Phase 8.1 summary lines that tout fallbacks (update to “strict mode only”).&#x20;

3. **YouTube “autosubs” mention**

   * Remove “API → autosubs fallback” wording from Phase 8 docs; make missing transcripts a **hard error** with guidance. &#x20;

**Acceptance test (new)**

* `tests/test_no_fallbacks.py`

  * Stop MCP hub → call `/api/runs` → expect 503 with `MCP_UNAVAILABLE` (no results from filesystem).
  * Stop MCP hub → call `/api/tools` → expect 503 (no tool\_registry.json used).

---

## B. Health gates before any run can start

**New endpoint & UI**

* `GET /api/health/full` returns a **gate report**: MCP hub reachable, Veritas tools registered, Langflow 7860 ok, LM Studio model loaded (1234), Neo4j ok, Redis ok. (See existing health URLs). &#x20;
* Home “Start Analysis” button remains disabled until **all gates pass**. If any gate fails, show a red, sticky banner with exact failing service and a one-liner fix.

**Acceptance tests**

* `tests/test_health_gates.py`: simulate each dependency down and verify run cannot start and error explains which gate failed.

---

## C. Ingestion source of truth (Veritas MCP only)

**Contract**

* `/api/runs/youtube/start` → call `start_veritas_youtube_channel_run(...)` (no direct library calls). Phase 7 lists this tool suite.&#x20;
* The tool must return `{run_id, doc_count, bundle_dir}`; dashboard only reads from the returned bundle path—never from a fallback. (Phase 8 docs describe this contract.)&#x20;

**Hard checks**

* After tool returns, confirm bundle exists with **required files** (`manifest.json`, `corpus.jsonl`, `merkle.json`, `metrics.json`, `proofs/`) or surface a 500 with which file is missing. (Phase 8 bundle spec.)&#x20;

**YouTube transcript correctness gate**

* After bundle write, parse `corpus.jsonl` and assert:

  * ≥1 transcript item with non-empty `text`
  * `source_type: "youtube"` present
  * Count equals (or reasonably matches) the requested `limit` unless the channel truly has fewer items (warn, don’t hide). (Phase 8 validation mentions transcripts in corpus).&#x20;

**Acceptance tests**

* `tests/test_ingestion_youtube_happy_path.py`: channel → transcripts present in `corpus.jsonl`, non-empty, expected count.
* `tests/test_ingestion_youtube_failures.py`: bad channel id → 400; private/unavailable transcript → 502 with explicit cause; zero transcripts → 502 “NO\_TRANSCRIPTS\_RETURNED”.

---

## D. Observability that makes failures obvious

**Backend**

* Add structured logs: one **trace id** per run; log MCP request/response status, file writes, and post-write validation failures.

**UI**

* A small **“Ingestion Trace”** panel (collapsed by default) that shows each gate & step (Discover → Fetch transcripts → Canonicalize → Bundle write → Verify bundle). If any step fails, the panel expands automatically with the exact reason.

---

## E. Tests you can trust (pytest + Cypress)

**pytest (backend)**

* `test_no_fallbacks.py` (A)
* `test_health_gates.py` (B)
* `test_ingestion_youtube_happy_path.py`, `test_ingestion_youtube_failures.py` (C)

**Cypress (frontend)**

* `start_disabled_until_gates_pass.cy.ts` → start button disabled, then enabled after `/api/health/full` returns green.
* `ingestion_error_surface.cy.ts` → disconnect MCP → UI shows red banner & refuses to run.
* `ingestion_success_flow.cy.ts` → run completes, “Trace” shows steps; Analyze tab loads transcript docs.

(Phase 8.2 already planned Cypress & pytest coverage; we’ll hook into that scaffolding.)&#x20;

---

## F. Tighten Cursor discipline so it can’t go off the rails

**Add/Update** `.cursor/rules/current_working_state.mdc` with hard rules:

1. **Always read these before coding:** `ROOT_OVERVIEW.md`, `QUICKSTART.md`, `PHASE_8_1_COMPLETION_SUMMARY.md`, `PHASE_8_2_PLAN.md`. (They define endpoints, architecture, and the 8.2 expectations like chat/activity toggles.)  &#x20;
2. **E2E checklist before any change:**

   * Run `docker compose … up -d` and confirm **all** service health checks first.&#x20;
   * Call `/api/health/full` and paste the JSON into the PR description.
   * Call `/api/tools` and include the exact tool name used for ingestion.
3. **No assumptions:** If a test passes via a fallback path, **fail the PR**.

   * Add a guard test that intentionally shuts off MCP and expects 503. (A)
4. **PR template must include:**

   * What files changed and why (single source of truth = Veritas MCP).
   * Repro steps (curl commands copied from **ROOT\_OVERVIEW** quick examples).&#x20;
5. **Never bypass MCP** for YouTube, transcripts, or corpus writes. (Cites: Phase 7/8 tool contracts & bundle spec). &#x20;

---

## G. 8.2 features that remain (after ingest is stable)

We’ll continue 8.2 polish **only after** ingestion gates are green:

* **AI Activity Panel** and **Chat With AI dock** (already specified in the 8.2 plan). We’ll hold these behind a **feature flag** until ingestion is reliable. &#x20;

---

## H. What we’ll deliver in 8.3

* **Code**: Fallback removal + 503 errors; `/api/health/full`; strict MCP ingestion; structured logs.
* **Tests**: 4 pytest + 3 Cypress suites above.
* **Docs**: Updated `QUICKSTART.md`, `ROOT_OVERVIEW.md`, Phase 8 summaries to remove fallback language and add strict-mode notes. (Citations above.)
* **UX**: Ingestion Trace panel; Start button gating.

**Done =**

1. Start is disabled until gates pass.
2. `/api/runs/youtube/start` fails if MCP/Veritas isn’t healthy (no silent workarounds).
3. Successful run yields bundle with verified transcripts in `corpus.jsonl`.
4. All new pytest & Cypress tests green.

---

## Quick operator commands (to reproduce clearly)

```bash
# 1) Bring services up
docker compose -f docker/docker-compose.yml up -d

# 2) Verify gates BEFORE any run
curl -s http://localhost:8050/api/health/full | jq .
curl -sf http://localhost:7860/health      # Langflow
curl -sf http://localhost:1234/v1/models   # LM Studio
curl -sf http://localhost:7474/            # Neo4j
redis-cli ping

# 3) Start a run (strict mode; will 503 if gates fail)
curl -s -X POST http://localhost:8050/api/runs/youtube/start \
  -H 'Content-Type: application/json' \
  -d '{"channel_url":"https://www.youtube.com/@imaginationpodcastofficial","limit":3,"sort":"oldest","max_depth":0}' | jq .

# 4) Inspect bundle strictly via MCP-returned path only (no filesystem shortcuts)
```