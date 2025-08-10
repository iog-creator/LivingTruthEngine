
---

# PHASE\_7\_PLAN.md

## Objective

1. Finish Phase‑6 cleanup (tests + Langflow write path).
2. Implement **Generalist Ingestion Runner** (web/pdf/YouTube) with provenance bundles.
3. Extend Dashboard with **Job Runs** tab (browse runs, open bundles, quick viz).
4. Keep MCP‑first, **local‑only** (no HF) unless explicitly toggled.

---

## Guardrails (must follow)

* **Local‑only** by default (LM Studio, CPU libs). No HF calls unless `HF_BURST=on`.
* **Model cap**: ≤ 10GB per model. Prefer Qwen 0.5–7B Q4 or Mistral 7B Q4; embedder small (e5‑small or MiniLM).
* **OCR default OFF**. PDF text only unless `OCR_REQUIRED=true`.
* **PII scrub**: standard policy ON.
* **Provenance**: SHA‑256 per doc + Merkle over bundle; store hashes in bundle.

---

## Branching

```bash
git checkout -b phase7-generalist-ingestion || git switch phase7-generalist-ingestion
```

---

## Part A — Phase‑6 Cleanup

### A1. Dashboard content assertion

* File: `scripts/testing/functional_tests.py`
* Fix: Align test with current `/health` JSON and root HTML title.

**Change**

* Update the dashboard test to hit `/health` and assert `{"status":"ok"}`; avoid brittle HTML text checks.

### A2. Langflow write endpoint (405)

* File: `src/mcp_servers/langflow_mcp_server.py`
* Action: Use supported endpoints (`/api/v1/project/export`, `/api/v1/flows/{id}` **GET/POST** as applicable) OR mock writes in CI.
* Add env flag `LANGFLOW_WRITE_ENABLED` (default `false`). In tests, skip write when false; only read/list/status.

**Acceptance for Part A**

* `pytest -q` passes the updated functional test.
* Manual `curl http://localhost:8050/health` → `{"status":"ok"}`.
* Hub tool `get_langflow_status` works; no 405 in CI logs.

---

## Part B — Generalist Ingestion Runner

### B1. Files to add

* `src/ingestion_general/__init__.py`
* `src/ingestion_general/runners.py`  ← orchestration & job state
* `src/ingestion_general/fetchers.py` ← web/yt/pdf adapters
* `src/ingestion_general/canonicalize.py`
* `src/ingestion_general/provenance.py` ← sha256 + merkle
* `src/ingestion_general/bundles.py`    ← write `.veritasrun/` bundle
* `tests/test_phase7_veritas.py`
* `config/veritas_flags.toml` (if not present) ← **source of truth** for flags
* Update: `src/mcp_servers/living_truth_fastmcp_server.py`
* Update: `config/tool_registry.json`

### B2. Runner contract

```python
# VeritasRunner.start(topic: str, max_docs: int, sources: list[str]) -> dict
# sources values: ["web", "pdf", "youtube"]
# Output directory: data/outputs/runs/<timestamp>_<slug>.veritasrun/
# Bundle contents:
#   manifest.json (topic, ts, doc list, gates, flags)
#   corpus.jsonl  (canonical docs; one JSON per line)
#   proofs/
#     <doc_id>.sha256
#   merkle.json  (root, leaves ordered by doc_id)
#   metrics.json (counts, timings, drift=0.0 placeholder)
```

### B3. Fetchers (local‑only)

* **Web**: `trafilatura` for text; fallback `readability-lxml`. No JS rendering in Phase 7.
* **PDF**: `PyMuPDF` text extraction. If text ratio < threshold and `OCR_REQUIRED=true`, skip with `suspect:true` tag (no OCR yet).
* **YouTube**: `yt-dlp --skip-download --write-auto-sub --write-sub --sub-lang en --convert-subs srt` to get subtitles; if missing, use `youtube_transcript_api` (no ASR).

### B4. Canonicalize

* Normalize to:

  ```json
  {
    "doc_id": "string",
    "source_type": "web|pdf|youtube",
    "uri": "string",
    "retrieved_at": "iso8601",
    "title": "string",
    "text": "string",
    "lang": "en",
    "suspect": false,
    "meta": { "extra": "…" }
  }
  ```

### B5. Provenance

* `sha256(text)` per doc → `proofs/<doc_id>.sha256`.
* Stable order by `doc_id`; build `merkle.json` with `root` and `leaves`.
* Store `manifest.json` with flags snapshot (exact TOML used).

### B6. MCP Tools

Add to `living_truth_fastmcp_server.py`:

* `start_veritas_run(topic: str, max_docs: int = 10, sources: list[str] = None) -> dict`
* `get_veritas_run_status(run_id: str) -> dict`
* `list_veritas_runs(limit: int = 20) -> list`
* `open_veritas_bundle(run_id: str) -> dict`
  Register in `config/tool_registry.json`.

### B7. Flags & config

* `config/veritas_flags.toml` keys:

  * `HF_BURST="off"` (ignored in Phase 7)
  * `OCR_REQUIRED="false"`
  * `PII_SCRUB="standard"`
  * `MAX_DOCS_DEFAULT=10`
* Wire read‑only access in runner; **do not** auto‑toggle.

### B8. Minimal metrics

* `metrics.json`:

  * `docs_total`
  * `docs_by_source`
  * `bytes_total`
  * `duration_seconds`
  * `errors` (list of brief strings)

**Acceptance for Part B**

* MCP `start_veritas_run("imagination podcast smoke", 6, ["youtube"])` creates a bundle under `data/outputs/runs/…`.
* Bundle contains all artifacts; merkle root present; no external calls in logs.
* `list_veritas_runs` returns the new run; `open_veritas_bundle` loads its manifest.

---

## Part C — Dashboard: Job Runs tab

### C1. File

* `src/analysis/dash_app.py` (existing FastAPI+Dash hybrid)

### C2. Add tab “Job Runs”

* Left: run selector (reads `data/outputs/runs/*/*.veritasrun`).
* Middle: manifest & metrics panels.
* Right: provenance quick‑view (root hash + leaf count).
* Buttons: “Refresh”, “Open Folder”.

### C3. 3D Network interaction (non‑blocking)

* If a run has `entities.json` later (Phase 8), render; else hide control gracefully.

**Acceptance for Part C**

* Dashboard loads `/` and `/health` OK.
* “Job Runs” lists the new run; opening shows manifest + metrics + merkle root.
* No JS errors in console; 3D graph controls hidden if no data.

---

## Tests

### `tests/test_phase7_veritas.py`

* Start a YouTube‑only run with `max_docs=3`.
* Assert directory + files exist (manifest, corpus.jsonl, proofs/\*, merkle.json, metrics.json).
* Assert `manifest.flags.OCR_REQUIRED=="false"`.
* Assert MCP `list_veritas_runs` includes the run.

Run:

```bash
pytest -q tests/test_phase7_veritas.py
```

---

## Documentation updates

* `README.md` → add “Generalist Ingestion Runner” section.
* `docs/PROJECT_STRUCTURE.md` → describe `data/outputs/runs/…/*.veritasrun`.
* `.cursor/rules/@veritas_runs.mdc` → brief guide for Cursor to use MCP tools and file conventions.

---

## Commands (build & verify)

```bash
# Rebuild services that changed (dashboard shows new tab)
docker compose -f docker/docker-compose.yml up -d --build dashboard

# Health checks
curl -s http://localhost:8050/health
python -c "from src.mcp_servers.mcp_hub_server import MCPHub; print(MCPHub().get_tool_categories())"

# Start a smoke run via MCP tool (python shell or test)
python - <<'PY'
from src.mcp_servers.living_truth_fastmcp_server import LivingTruthFastMCP
m=LivingTruthFastMCP()
print(m.start_veritas_run(topic="imagination podcast smoke", max_docs=3, sources=["youtube"]))
PY
```

---

## PR checklist

* [ ] Part A fixes committed; tests updated.
* [ ] New ingestion files added; MCP tools registered.
* [ ] Dashboard tab implemented.
* [ ] `pytest -q` green for new tests.
* [ ] `PHASE_7_COMPLETION_SUMMARY.md` written.

---

## Out‑of‑scope (defer to Phase 8)

* OCR (Tesseract/RapidOCR).
* JS‑rendering pages (Playwright+stealth).
* Drift/coverage metrics and reranking.
* Entity/claims extraction bundle enrichments.

---

### Notes to Cursor

* Prefer small, single‑purpose functions with type hints.
* Fail fast on network or parsing errors; record brief error string in `metrics.json`.
* No network calls to HF unless `HF_BURST=="on"` (Phase 8).
* Keep dependencies minimal; pin versions.

---

If you want, I’ll also generate a **`PHASE_7_COMPLETION_SUMMARY.md`** template now so Cursor knows what to produce when it’s done.
