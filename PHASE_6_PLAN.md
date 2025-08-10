# Phase 6 Plan — Service Stabilization, MCP Usage, and Validation

## Objective
Stabilize optional services (DevDocs, Rulego, MCP Solver) and ensure they are actively integrated and validated through the MCP Hub (documentation, workflow, and solver categories). Expand tests and docs to lock in behavior and maintain the MCP-first policy.

## Scope
- Replace fragile, clone-at-start containers with lightweight internal services exposing `/health`.
- Ensure MCP adapters for DevDocs, Rulego, and Solver use those services via the Hub.
- Update functional tests to validate hub categories and tool execution.
- Update project docs to reflect the new architecture and usage.

## Deliverables
- Stable containers for `devdocs`, `rulego`, `mcp-solver` (healthy, with `/health`).
- MCP Hub exposes categories: `documentation`, `workflow`, `solver` with tools discoverable.
- Functional tests covering hub categories and runtime execution of status tools.
- Documentation updates in `README.md`, `docs/PROJECT_SETUP.md`, `docs/PROJECT_STRUCTURE.md`.
- Phase 6 summary in the project root (`PHASE_6_COMPLETION_SUMMARY.md`).

## Work Items
1. Container stabilization
   - Implement FastAPI stubs: `src/aux_services/devdocs_server.py`, `rulego_server.py`, `solver_server.py`.
   - Update `docker/docker-compose.yml` to run uvicorn services with healthchecks.
   - Verify host endpoints: 9126 (devdocs), 9127 (rulego), 9128 (solver).

2. MCP usage integration
   - Ensure `src/mcp_servers/devdocs_mcp_server.py`, `rulego_mcp_server.py`, `mcp_solver_server.py` point to the above endpoints and provide status tools.
   - Confirm categories in Hub: `documentation`, `workflow`, `solver` include expected tools.

3. Testing and validation
   - Extend `scripts/testing/functional_tests.py` to validate hub categories and call status tools via the hub.
   - Run full test suite; keep non-related failures tracked as Known Issues.

4. Documentation
   - Update `README.md`, `docs/PROJECT_SETUP.md`, `docs/PROJECT_STRUCTURE.md` with the new service model.
   - Note that these optional services are internal health backends used by MCP adapters.

## Acceptance Criteria
- All three containers start healthy and respond to `/health`.
- Hub `get_tool_categories()` includes documentation/workflow/solver entries.
- Hub `execute_tool()` successfully calls `get_devdocs_status`, `get_rulego_status`, `get_solver_status`.
- Functional test `test_hub_additional_categories` passes.
- Docs reflect the new approach and ports.

## Test Plan
- docker: `docker compose ps` shows services up and healthy.
- curl: `http://localhost:9126/health`, `:9127/health`, `:9128/health` should return JSON status ok.
- pytest: run `pytest tests/` and `python scripts/testing/functional_tests.py`.
- Manual hub sanity: invoke category listing and tool execution.

## Risks & Mitigations
- Upstream API mismatches (Langflow write endpoints): keep tests read-only where needed; track as Known Issues for follow-up.
- Overreach of optional services: keep them minimal and health-focused; expand capabilities later.

## Timeline
- Day 1: Implement stubs, compose updates, and health validation.
- Day 2: Test integration via Hub, add/adjust functional tests.
- Day 3: Documentation and final verification; produce Phase 6 summary.

## Known Issues to Triage Post-Phase 6
- Dashboard content assertion needs aligning to current HTML; test is failing on content check.
- Langflow write endpoints (`/api/v1/flows`) return 405; adjust to supported endpoints or update API usage.


Origional: Got it. Here are the decisions and the exact instructions Cursor needs to keep Phase 6 moving—no guesswork.

# Phase 6 — Decisions You Can Treat As Final

* **Branch**: keep working on `phase6-generalist-ingestion`. We’ll PR to `main` after tests pass.
* **Model policy (local‑first)**: **Use LM Studio only**. No HF burst in Phase 6.
* **OCR**: **OFF by default**. Auto‑enable only when a PDF extractor yields **<1200 chars** or is image‑only.
* **PII scrubbing**: **Standard** by default. Add a UI toggle for **Strict** (hash emails/phones, redact names).
* **Redis host**: `living-truth-redis` (compose service name).
* **Dashboard**: reuse the existing container at **port 8050** (`src.analysis.dash_app:fastapi_app`). Health: `/health`.
* **Run bundles**: write under `data/outputs/runs/<timestamp>_<slug>.veritasrun/`.
* **Max docs**: default **10**.
* **Sources allowed**: `"web"`, `"pdf"`, `"youtube"`. (YouTube uses existing ChannelArchiver path.)
* **Proofs**: SHA‑256 per chunk + Merkle root per source. **Required** for a run to be “green”.

---

# 1) Config files to add/update

## `config/veritas_flags.toml` (new)

```toml
[hf]
burst_enabled = false
burst_cap_usd = 0.00
reranker = "qwen-reranker"   # placeholder; not used while burst_enabled=false

[ocr]
enabled_default = false
auto_trigger_min_chars = 1200

[pii]
mode = "standard"            # "standard" | "strict"

[ingestion]
max_docs_default = 10
sources_allowed = ["web", "pdf", "youtube"]

[paths]
runs_dir = "data/outputs/runs"
```

## `src/config/living_truth_config.py`

* Read `veritas_flags.toml` and expose:

  * `flags.hf.burst_enabled`
  * `flags.ocr.enabled_default`, `flags.ocr.auto_trigger_min_chars`
  * `flags.pii.mode`
  * `flags.ingestion.max_docs_default`, `flags.ingestion.sources_allowed`
  * `paths.runs_dir`
* Set `REDIS_URL` to `redis://living-truth-redis:6379/0` if not already.

---

# 2) Runner + MCP wiring

## Files to create (or finish) under `src/ingestion_general/`

* `__init__.py`
* `web_fetcher.py` — trafilatura fetch + canonicalize URL.
* `pdf_extractor.py` — PyMuPDF extract; return `needs_ocr=True` based on char count or no text.
* `yt_adapter.py` — thin wrapper around `ChannelArchiver` to emit transcript docs (no downloads).
* `canonicalize.py` — sentence spans with stable IDs (`doc_id:chunk_id:sentence_id`).
* `provenance.py` — SHA‑256 per sentence chunk; Merkle per document; write `proofs/`.
* `bundle.py` — writer for `.veritasrun/` structure:

  * `manifest.json` (topic, created\_at, sources, counts)
  * `corpus.jsonl` (canonicalized sentences)
  * `proofs/` (per‑doc `hashes.json`, `merkle.json`)
  * `metrics.json` (counts, drift=0.0 placeholder)
* `runners.py` — exposes `VeritasRunner().start(topic, max_docs, sources)` and returns `run_id`.

## Update MCP server: `src/mcp_servers/living_truth_fastmcp_server.py`

Add/complete tools:

* `start_veritas_run(topic: str, max_docs: int = None, sources: list[str] = None) -> dict`
* `get_veritas_run_status(run_id: str) -> dict`
* `list_veritas_runs(limit: int = 20) -> list`
* `open_veritas_bundle(run_id: str) -> dict`  (returns manifest + head of corpus)
* `reanalyze_with_gates(run_id: str, gates: dict) -> dict`  (stub for Phase 7)

Register these in `config/tool_registry.json`.

---

# 3) Dashboard updates (Job Runs tab)

File: `src/analysis/dash_app.py`

Add/keep the **Job Runs** tab with:

* **Start Run** form: topic (text), sources (multi), max\_docs (int).
* **Runs list** (poll every 5 s): calls `list_veritas_runs`.
* **Run details panel**: `manifest.json`, proof verification button, head of `corpus.jsonl`.
* **Flags** panel:

  * `HF burst` (disabled/greyed when `burst_enabled=false`)
  * `OCR auto` (reflects `ocr.enabled_default`)
  * `PII mode` selector (`standard`/`strict`) — writes to a small store in `data/outputs/runs/<run>/_ui_flags.json` for now.

No work needed on 3D graph now (you already fixed it).

---

# 4) Tests to add

## `tests/test_phase6_veritas.py`

Implement these four:

```python
def test_merkle_roundtrip(tmp_path): ...
def test_bundle_manifest(tmp_path): ...
def test_mcp_list_open(monkeypatch): ...
def test_dashboard_job_runs_tab_imports(): ...
```

**Expectations**

* Corrupting any sentence chunk makes proof verify fail.
* `manifest.json`, `corpus.jsonl`, `proofs/*`, `metrics.json` exist and parse.
* MCP list/open returns recent run and opens manifest head.
* Importing `src.analysis.dash_app` exposes a layout containing “Job Runs”.

Run:

```bash
pytest -q tests/test_phase6_veritas.py
```

---

# 5) Commands Cursor should run (in order)

```bash
# 1) Create/checkout branch
git checkout -B phase6-generalist-ingestion

# 2) Add files per sections 1–3 above

# 3) Install deps (if missing)
pip install trafilatura==1.8.0 pymupdf==1.24.7

# 4) Rebuild dashboard only
docker compose -f docker/docker-compose.yml up -d --build dashboard
curl -sf http://localhost:8050/health

# 5) Quick runner smoke
python - <<'PY'
from src.ingestion_general.runners import VeritasRunner
rid = VeritasRunner().start(topic="Phase6 smoke", max_docs=1, sources=["web"])
print("RID", rid)
PY

# 6) Verify bundle exists
ls -la data/outputs/runs | tail -n 5

# 7) Run tests
pytest -q tests/test_phase6_veritas.py

# 8) Commit
git add -A
git commit -m "Phase 6: generalist ingestion runner, MCP tools, dashboard Job Runs, proofs, tests"

# 9) Optional: push & open PR
git push -u origin phase6-generalist-ingestion
```

---

# 6) Acceptance criteria (Phase 6)

A run is **green** when:

* A bundle folder is created with `manifest.json`, `corpus.jsonl`, `proofs/`, `metrics.json`.
* Merkle verifies for all docs; deliberate corruption fails verification.
* Dashboard Job Runs tab can:

  * Start a run,
  * List runs,
  * Open a run and show manifest + corpus head,
  * Verify proofs successfully.
* No HF calls (confirm via logs). OCR only triggers if <1200 chars from PDF.

---

# 7) Open questions Cursor had (answered)

* **Branch v. main?** Stay on `phase6-generalist-ingestion`; PR when green.
* **Where does Dash run?** Inside the existing **dashboard** service on **8050**; UVicorn app `src.analysis.dash_app:fastapi_app`.
* **HF usage now?** Disabled in Phase 6 (local‑only).
* **OCR default?** Off. Auto‑trigger under 1200 chars or image‑only PDFs.
* **PII default?** Standard; Strict is a UI toggle.

If Cursor hits anything ambiguous beyond this, have it stop and ask *exactly one* yes/no question, then proceed.
