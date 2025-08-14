---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/runners/multisource_runner.py', 'PHASE_9.md', 'pdf_adapter.py', 'web_adapter.py', 'PHASE_9_2_COMPLETION_SUMMARY.md', 'pgvector_store.py', 'youtube_adapter.py']
---

# **PHASE 9.2 PLAN — Multi-Source Runner Backend & UI Integration**
**Status:** Planned  
**Phase:** 9.2  
**Depends on:** Phase 9.1 completion (SSOT, pgvector, Rulego, DSPy integration)  
**Primary Goal:** Implement multi-source ingestion backend (YouTube, Web, PDF) with unified run handling, SSOT-driven configuration, GPU-aware model allocation, and targeted UI integration.

---

## **🎯 Objectives**
1. **Backend** — Build the **multi-source ingestion runner** that orchestrates jobs from multiple source types in a single run.
2. **UI (main dashboard `/`)** — Add controls for starting/viewing multi-source jobs in the **main dashboard home page** ONLY.
3. **SSOT Integration** — Use `config/models.toml` for all model calls (LLM, embeddings, reranker).
4. **GPU/CPU Model Allocation** — Offload LLM and embedding models to GPU (LM Studio), reranker to GPU if possible (fallback to CPU if GPU busy — allowed exception).
5. **Job Tracking** — Store metadata in Postgres (with pgvector for embeddings) and expose via `/api/multisource/jobs`.
6. **Strict API Envelope** — All endpoints must use `{status, data, error}` format.
7. **Smoke Testing** — Create `scripts/p9_2_smoke.sh` to validate ingestion + storage + retrieval.

---

## **🛠 Technical Requirements**

### **1. Backend Implementation**
- Create `src/runners/multisource_runner.py`:
  - Accepts JSON with:
    ```json
    {
      "sources": ["youtube", "web", "pdf"],
      "params": {
        "item_limit": 5,
        "crawl_depth": 1,
        "job_label": "Example Run"
      }
    }
    ```
  - Dispatches each source type to its adapter:
    - YouTube → existing `youtube_adapter.py`
    - Web → existing `web_adapter.py`
    - PDF → existing `pdf_adapter.py`
  - Merges output into **unified corpus** with per-source tags.

- Use `pgvector_store.py` for:
  - `upsert_docs()` to insert embeddings
  - `search()` for retrieval

- Model calls:
  - LLM → LM Studio (GPU)
  - Embeddings → LM Studio (GPU)
  - Reranker → GPU if possible, fallback to CPU only as per exception rules.

---

### **2. API Endpoints**
- Add `POST /api/multisource/start`:
  - Validates health gates (`pgvector`, `rulego`, `lmstudio`).
  - Starts job in background (thread or queue).
  - Returns job_id + status.

- Add `GET /api/multisource/jobs`:
  - Lists all multi-source jobs.
  - Includes job_id, label, status, sources, created_at, completed_at.

- Add `GET /api/multisource/jobs/{job_id}`:
  - Returns detailed job metadata + document counts.

- All responses in `{status, data, error}` format.  
  **DO NOT** return raw HTML.

---

### **3. UI Integration**
- **Target UI:** **main dashboard home page `/` ONLY**.
  - **DO NOT TOUCH** `static/ui_status_chat.html` (AI chat/status interface).
  - Add “Multi-Source Ingestion” card with:
    - Source type checkboxes (YouTube, Web, PDF)
    - Item limit (input)
    - Crawl depth (input)
    - Job label (input)
    - Start button
  - Below the form, show “Multi-Source Jobs” list with:
    - Job ID
    - Status (color-coded)
    - Refresh button

---

### **4. GPU/CPU Allocation Rules**
- Use GPU for:
  - All LLM inference.
  - All embeddings.
  - Reranker **if GPU free**.
- **Fallback Exception:** Reranker may run on CPU **only if GPU busy**, and must be logged as “CPU fallback allowed”.
- Ensure LM Studio can load/unload models dynamically.

---

### **5. SSOT Model Loading**
- Pull all model names + parameters from `config/models.toml`.
- Hash model config (`models_checksum`) and return in `/api/health/full`.

---

### **6. Fallback Exceptions**
The following are **approved and expected fallbacks** and are **NOT** to be flagged as “no fallback” violations:
1. **YouTube Captions/Transcripts** — If unavailable from MCP tool, fallback to YouTube-provided captions is allowed.
2. **Reranker CPU Execution** — If GPU is busy, reranker may run on CPU (must log this event).
3. **Local Data for Debugging** — When `ALLOW_FALLBACKS=true`, use local test data in `/data/debug_samples` for development smoke tests only.
4. **Non-blocking Search** — If pgvector is temporarily unavailable, return partial results from in-memory cache with warning (only in dev mode).

---

### **7. Testing**
- Create `scripts/p9_2_smoke.sh`:
  - Step 1: Health check (`/api/health/full`)
  - Step 2: Start test job with YouTube+PDF, item_limit=1.
  - Step 3: Poll `/api/multisource/jobs` until complete.
  - Step 4: Query pgvector to confirm embeddings stored.
  - Step 5: Run `search()` to confirm retrieval works.

---

## **📜 Workflow Safeguards**
- **UI edits** — Touch only main dashboard `/` for ingestion controls.
- **AI chat/status UI** — Never edit `static/ui_status_chat.html` unless explicitly instructed in that phase.
- **Strict envelope** — All API endpoints must conform to `{status, data, error}`.
- **No silent fallbacks** — Except the approved cases listed in **Fallback Exceptions**.

---

## **📋 Completion Summary Instructions**
At the end of this phase, create `PHASE_9_2_COMPLETION_SUMMARY.md` with:
1. ✅ Overview of all implemented features.
2. ✅ API endpoint list + sample responses.
3. ✅ Database changes (pgvector schema updates if any).
4. ✅ GPU/CPU allocation confirmation with sample logs.
5. ✅ UI screenshots (main dashboard ingestion form + job list).
6. ✅ Smoke test results (`scripts/p9_2_smoke.sh` run output).
7. ✅ Known issues + next phase recommendations.

---

## **📜 p9_2_smoke.sh Outline**
```bash
#!/bin/bash
set -e

echo "=== PHASE 9.2 SMOKE TEST START ==="

# Step 1: Health check
echo "[1/5] Checking health..."
curl -s http://localhost:8050/api/health/full | jq .

# Step 2: Start test job
echo "[2/5] Starting multi-source test job..."
JOB_ID=$(curl -s -X POST http://localhost:8050/api/multisource/start \
  -H "Content-Type: application/json" \
  -d '{"sources":["youtube","pdf"],"params":{"item_limit":1,"crawl_depth":1,"job_label":"p9_2_smoke"}}' | jq -r '.data.job_id')
echo "Started job: $JOB_ID"

# Step 3: Poll for completion
echo "[3/5] Waiting for job to complete..."
for i in {1..30}; do
  STATUS=$(curl -s http://localhost:8050/api/multisource/jobs/$JOB_ID | jq -r '.data.status')
  echo "Status: $STATUS"
  [[ "$STATUS" == "completed" ]] && break
  sleep 2
done

# Step 4: Verify pgvector contains embeddings
echo "[4/5] Checking embeddings in pgvector..."
psql -U postgres -d veritas -c "SELECT COUNT(*) FROM document_embeddings;"

# Step 5: Search test
echo "[5/5] Running search test..."
curl -s -X POST http://localhost:8050/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"test"}' | jq .

echo "=== PHASE 9.2 SMOKE TEST COMPLETE ==="
```
