---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/analysis/linking_pipeline.py', 'tests/test_graph_api.py', 'PHASE_9_3_COMPLETION_SUMMARY.md', 'src/dashboard/unified_dashboard.py', 'PHASE_9.md', 'src/ai/dspy_programs.py', 'src/storage/pgvector_store.py', 'tests/test_linking_pipeline.py', 'docs/project_master_log.md', 'tests/test_rulego_dspy.py', 'src/analysis/rulego_bridge.py']
---

Great question. Based on everything we’ve shipped and validated, we’re ready for **Phase 9.3**.

* **9.1** (Models SSOT + wiring) — ✅ complete
* **9.2** (Multi‑source runner backend & UI integration) — ✅ plan in repo, core plumbing in place and master log working
* **Next**: **9.3 — Cross‑Document Linking & Evidence Graph (with deterministic + AI verification)**

Here’s a single, copy‑paste plan you can hand to Cursor.

````markdown
# PHASE_9_3_PLAN.md — Cross‑Document Linking & Evidence Graph (Deterministic + AI Verification)

## 🎯 Objectives
1) Extract entities & claims from each ingested document (multi‑source bundles).  
2) Link entities/claims across documents to form a cross‑doc evidence graph.  
3) Apply **Rulego** policies for deterministic checks; run **DSPy** programs for AI corroboration/contradiction.  
4) Expose read‑only APIs for graph/timeline that the UI can consume (no UI surgery beyond what's scoped below).  
5) Persist features & links in Postgres (pgvector + relational tables) for fast re‑query.

---

## 🔩 Technical Requirements

### Data model (Postgres)
- **Tables (schema `lte`)**
  - `documents(id, run_id, source_type, uri, title, published_at, shard_no, text_len, sha256, created_at)`
  - `entities(id, doc_id, type, value, span_start, span_end, conf, created_at)`  
  - `claims(id, doc_id, text, normalized, conf, created_at)`
  - `entity_links(id, left_entity_id, right_entity_id, link_type, score, method, created_at)`  
  - `claim_links(id, left_claim_id, right_claim_id, link_type, score, method, created_at)`
  - `doc_embeddings(doc_id, embedding vector(768), model, created_at)`  ← pgvector
  - `claim_embeddings(claim_id, embedding vector(768), model, created_at)` ← pgvector
  - `graph_snapshots(id, run_id, payload_json jsonb, created_at)`  (optional cache for UI)

> Provide `docker/initdb/003_graph.sql` with DDL + indexes (BTREE + IVFFLAT on vectors).

### Extraction & Linking pipeline
- **Module**: `src/analysis/linking_pipeline.py`
  - `extract_entities(doc)`: NER using SSOT config (`config/models.toml`)  
    - prefer GPU NER if configured; fallback CPU w/ logging (dev only).
  - `extract_claims(doc)`: LLM+pattern hybrid (DSPy prompt program) → sentences/atomic claims  
  - `embed_entities_claims(...)`: embeddings via LM Studio (GPU) → `doc_embeddings`, `claim_embeddings`
  - `link_entities_across_docs(run_id)`: candidate pairs via blocking (string + vector kNN) → score with reranker (GPU if available) → write `entity_links`
  - `link_claims_across_docs(run_id)`: same strategy → write `claim_links`
  - `snapshot_graph(run_id)`: build nodes/edges JSON (documents, entities, claims, link edges) → store in `graph_snapshots`

- **Deterministic policy checks (Rulego)**
  - `src/analysis/rulego_bridge.py` add `evaluate_graph(run_id)` which:
    - ensures minimum evidence per claim (configurable)
    - flags contradictions (e.g., same entity with incompatible attributes)
    - outputs `policy_findings: [{rule_id, severity, nodes, msg}]`

- **AI corroboration (DSPy)**
  - `src/ai/dspy_programs.py` add `CorroborationProgram` with:
    - verify top‑k evidence for each claim, returns `label ∈ {corroborated, weak, contradicted}`, `rationale`, `citations`
    - batch mode by run_id

### GPU/CPU allocation (9.3)
- **LLM** (Qwen 8B) → GPU (LM Studio), dynamic load/unload
- **Embeddings** → GPU (LM Studio)
- **Reranker** → GPU if free; fallback CPU **with log** (allowed)
- **NER** → GPU if model supports; else CPU
- Respect `config/models.toml` for model names/endpoints; hash surfaced in `/api/health/full`.

### APIs (envelope format)
- `GET /api/graph/{run_id}` → `{ nodes: [...], edges: [...], findings: {...} }`
- `POST /api/graph/{run_id}/build` → kicks linking pipeline; returns `{status:"ok", data:{run_id}}`
- `GET /api/claims/{run_id}` → flattened claims with link counts & corroboration labels
- `GET /api/entities/{run_id}` → flattened entities with link counts & types
- `GET /api/sources` (from 9.2) — unchanged; includes source registry snapshot

> All endpoints must use `{status, data?, error?}` and 502/503/500 codes per core rules.

### Minimal UI scope (allowed this phase)
- **Main dashboard `/` only**: add a new **“Graph”** tab that fetches `/api/graph/{run_id}` and renders a simple force graph (or basic list view if you prefer to defer viz polish).
- **Do not modify** `src/dashboard/static/ui_status_chat.html`.

---

## 🧪 Testing & Verification

### Unit/Integration
- `tests/test_linking_pipeline.py`
  - Asserts: entity extraction yield > 0 on sample docs
  - Claims extracted with normalized form
  - Embeddings stored (doc + claim) and retrievable
  - Linking creates edges with scores and `method ∈ {"block+rerank"}`

- `tests/test_graph_api.py`
  - `/api/graph/{run_id}` returns nodes/edges with counts > 0 after build
  - Envelope and error code policy enforced
  - Health gates must be OK prior to build

- `tests/test_rulego_dspy.py`
  - Rulego returns findings array (can be empty)
  - DSPy returns labels ∈ {corroborated, weak, contradicted} with citations

### Smoke script
- `scripts/p9_3_smoke.sh`
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  bash scripts/proof_of_life.sh
  python - <<'PY'
from httpx import Client
c = Client(timeout=20)
rid = c.post("http://localhost:8050/api/graph/test-run/build").json()["data"]["run_id"]
g  = c.get (f"http://localhost:8050/api/graph/{rid}").json()
assert "nodes" in g["data"] and "edges" in g["data"]
print("OK graph:", len(g["data"]["nodes"]), "nodes,", len(g["data"]["edges"]), "edges")
PY
  pytest -q
````

---

## 🚦 Workflow Safeguards (carry‑over)

* **No silent fallbacks** beyond approved list:

  * YouTube captions fallback
  * Reranker CPU fallback
  * Dev‑only: in‑memory search when pgvector down
* Log every fallback in server logs and expose a short summary in `/api/health/full`.

---

## 📁 Files to Add/Modify

* `docker/initdb/003_graph.sql` (new)
* `src/analysis/linking_pipeline.py` (new)
* `src/analysis/rulego_bridge.py` (extend with `evaluate_graph`)
* `src/ai/dspy_programs.py` (extend with `CorroborationProgram`)
* `src/storage/pgvector_store.py` (extend: claim embeddings ops)
* `src/dashboard/unified_dashboard.py` (add graph endpoints)
* `src/dashboard/templates/` (optional: add Graph tab page)
* `config/models.toml` (ensure NER/reranker entries and tags)
* `tests/test_linking_pipeline.py`, `tests/test_graph_api.py`, `tests/test_rulego_dspy.py`
* `scripts/p9_3_smoke.sh` (new)

---

## ✅ Acceptance Criteria

* Running `scripts/p9_3_smoke.sh` prints “OK graph: N nodes, M edges” and exits 0.
* `/api/graph/{run_id}` returns nodes & edges with at least one cross‑document link.
* Rulego `findings` present (even if empty) and embedded in `/api/graph/{run_id}` response.
* DSPy corroboration labels included for claims with top‑k evidence & citations.
* Envelope & error code policy enforced across all new endpoints.
* pgvector contains doc + claim embeddings for the run.
* No edits to `ui_status_chat.html`.

---

## 🧱 Fallback Exceptions (explicit for 9.3)

* Reranker CPU fallback if GPU is occupied (log it, include in `/api/health/full`).
* YouTube captions fallback for missing MCP transcripts.
* Dev‑only in‑memory search if pgvector unavailable (`ALLOW_FALLBACKS=true` required).

---

## 🧭 MCP‑First Operations

Before coding:

* `validate_cursor_rules()`

After coding:

* `fix_cursor_rule_frontmatter()`
* `ruleset_archive_outdated()` (if any)

On completion:

* `generate_phase_completion_summary()` → `PHASE_9_3_COMPLETION_SUMMARY.md`

---

## 🧾 Completion Summary Instructions (MANDATORY)

Create `PHASE_9_3_COMPLETION_SUMMARY.md` including:

* ✅ Features implemented (bullets)
* ✅ API samples (`/api/graph/{run_id}` success + error)
* ✅ DB changes: list tables/indexes from `003_graph.sql`
* ✅ GPU/CPU allocation notes + any fallback logs excerpt
* ✅ Smoke output and `pytest` summary (copy/paste)
* ✅ Known issues & next steps (9.4)
* ✅ Master log updated: `scripts/rebuild_master_log.sh` (paste first 10 lines of `docs/project_master_log.md`)

Commit message:

```
phase9.3: cross‑doc linking + evidence graph [verified]
```

```

If you want, I can also generate stub files (empty but compilable) for the new modules and tests so Cursor fills them in without guesswork.
::contentReference[oaicite:0]{index=0}
```
