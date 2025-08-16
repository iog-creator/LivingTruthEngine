---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['suspects.json', 'config/tool_registry.json', 'manifest.json', 'src/ingestion_general/adapters/youtube_adapter.py', 'metrics.json', 'src/api/ai_activity.py', 'merkle.json']
---

Got it. I’ll do three things in one shot:

1. **Rewrite Phase 8.2** to explicitly include test coverage.
2. **Add minimal test-only emit endpoint** (guarded by `TEST_MODE`) so Cypress can drive WS updates.
3. **Provide runnable Cypress + pytest skeletons** you can paste straight into Cursor.

---

# Phase 8.2 Plan: MCP Tools Enhancement and Fallback Removal

## Status: ✅ COMPLETED

### Overview
Phase 8.2 focuses on enhancing MCP tools to create complete bundles with transcripts and removing fallback mechanisms to ensure proper error handling.

## ✅ Completed Tasks

### 1. MCP Tools Enhancement ✅
- **Status**: ✅ COMPLETED
- **Issue**: MCP tools were not creating complete bundles with transcripts
- **Solution**: Fixed YouTube Transcript API integration in `src/ingestion_general/adapters/youtube_adapter.py`
- **Changes Made**:
  - Updated `fetch_transcript()` method to use correct API: `api.fetch(video_id)` instead of `api.get_transcript(video_id)`
  - Fixed transcript parsing to use `entry.text` instead of `entry['text']` for `FetchedTranscriptSnippet` objects
  - Updated tool registry parameter schema to match actual implementation
- **Verification**: 
  - ✅ MCP tool successfully creates `.veritasrun` bundles with transcripts
  - ✅ Bundle contains: `corpus.jsonl`, `manifest.json`, `merkle.json`, `metrics.json`, `proofs/`, `suspects.json`
  - ✅ Transcript content properly extracted and included in bundle
  - ✅ MCP Hub Server integration working correctly
  - ✅ Tests passing: `test_phase8_mcp_tools` and `test_phase8_bundle_structure`

### 2. Tool Registry Update ✅
- **Status**: ✅ COMPLETED
- **Issue**: Tool registry had outdated parameter schema for `start_veritas_run`
- **Solution**: Updated `config/tool_registry.json` with correct parameter schema
- **Changes Made**:
  - Added missing parameters: `channel_url`, `selection`, `max_videos`, `crawl_depth`, `allow_domains`, `deny_domains`, `transcript_pref`, `ocr_mode`, `auto_retry_attempts`
  - Updated description to reflect Phase 8 capabilities
  - Ensured parameter types and requirements match actual implementation

### 3. Fallback Mechanism Removal ✅
- **Status**: ✅ COMPLETED
- **Issue**: System had fallback mechanisms that could mask MCP failures
- **Solution**: Removed fallback mechanisms to ensure proper error handling
- **Verification**:
  - ✅ Dashboard returns 503 when MCP services are unavailable
  - ✅ No fallback to filesystem or cached data
  - ✅ Proper error propagation through MCP Hub Server

## Technical Details

### YouTube Transcript API Fix
The main issue was in the YouTube adapter where the API usage was incorrect:

```python
# ❌ Old (incorrect)
transcript = YouTubeTranscriptApi.get_transcript(video_id)
text_content = " ".join([entry['text'] for entry in transcript])

# ✅ New (correct)
api = YouTubeTranscriptApi()
transcript = api.fetch(video_id)
text_content = " ".join([entry.text for entry in transcript])
```

### Bundle Structure
Each `.veritasrun` bundle now contains:
- `corpus.jsonl`: Complete transcript data with metadata
- `manifest.json`: Run metadata and parameters
- `merkle.json`: Cryptographic proof structure
- `metrics.json`: Processing metrics
- `proofs/`: Individual document proofs
- `suspects.json`: Suspect identification data

### MCP Hub Server Integration
- ✅ Tool properly registered in MCP Hub Server
- ✅ Parameter validation working correctly
- ✅ Execution through MCP Hub Server successful
- ✅ Performance monitoring active (warnings for >2s execution)

## Test Results

### Passing Tests
- ✅ `test_phase8_mcp_tools`: MCP tool registration and execution
- ✅ `test_phase8_bundle_structure`: Bundle creation and validation
- ✅ `test_veritas_mcp_tools`: Veritas MCP integration
- ✅ `test_bundle_structure`: Bundle structure validation

### Known Issues
- Some tests fail due to YouTube video availability (premieres, private videos)
- Langflow MCP tests failing due to write operations being disabled
- Dashboard health test expects "dashboard" but returns "unified_dashboard"

## Next Steps

Phase 8.2 is complete. The MCP tools are now working correctly and creating complete bundles with transcripts. The system properly handles errors without fallback mechanisms.

### Recommendations for Phase 8.3
1. Address remaining test failures
2. Optimize performance for large transcript processing
3. Add more robust error handling for YouTube API failures
4. Implement retry mechanisms for transient failures

---

**Phase 8.2 Status: ✅ COMPLETED**
- MCP tools enhanced and working correctly
- Complete bundles with transcripts being created
- Fallback mechanisms removed
- System properly handles errors

---

# 1) Rewrite — Phase 8.2 Plan (final)

```md
# Phase 8.2 — Dashboard AI Activity + Chat + UX polish (with tests)

## Goals
- Live **AI Activity** indicator (Embedder, Reranker, LLM, OCR, JS, Provenance) showing status + `model · provider`.
- Right-side **AI Chat** dock calling `/api/ai/chat` (non-streaming for 8.2; streaming can land in 9.0).
- **Run naming** improvements; **toggle propagation** (OCR/JS/HF Burst); **sticky Analyze header** (Explain/Export).
- **Test coverage:** Cypress E2E for UI, pytest for API + WS.

## Deliverables
- Backend: `src/api/ai_activity.py` (WS `/ws/ai-activity`, REST `/api/ai-activity/snapshot`), `POST /api/ai/chat`.
- **Test-only endpoint** (guarded by `TEST_MODE=1`): `POST /api/_test/ai-activity/emit` → publishes hub events to live WS (used by Cypress).
- Frontend: AI Activity strip injected in `base.html`, sticky header in Analyze, Chat dock (simple input + reply area).
- Docs update: README “AI Activity + Chat” section; Phase 8.2 completion note.

## Acceptance Criteria
1) **AI Activity**
   - Tiles render (6 kinds). Idle=gray; Working=amber pulse; Inference=green throb.
   - Page load paints from `/api/ai-activity/snapshot`.
   - WS pushes update tiles without reload.
2) **Chat Dock**
   - Sends `POST /api/ai/chat {message, context_run_id?, model?, provider?}`.
   - Returns `{status:"ok", data:{reply}, error:null}` and displays reply.
3) **Run Naming**
   - Human-readable name generated at start; appears in Runs list; PATCH rename allowed.
4) **Toggles**
   - OCR/JS/HF-burst values propagate to backend; visible in run manifest/log.
5) **Analyze Header**
   - Buttons anchored in sticky header; layout OK on mobile.
6) **Tests**
   - **Cypress (E2E)**: 
     - Snapshot paints tiles; WS event (triggered via test endpoint) updates status/model text.
     - Chat dock happy path (intercepted response) shows reply; LLM tile model shows configured label.
   - **pytest**:
     - `/api/ai/chat` returns shape & echoes message (stub).
     - WS: snapshot empty → emit → snapshot reflects; WS client receives event.

## Out of Scope
- Streaming chat, multi-source orchestration changes, claim verification.

## How to run tests
- **Cypress**: `npm run cypress:open` or `npx cypress run` (see config below).  
- **pytest**: `pytest -q`.

```

---

# 2) Backend patch — add test-only emit endpoint

```diff
*** Begin Patch
*** Update File: src/api/ai_activity.py
@@
-from fastapi import APIRouter, WebSocket, WebSocketDisconnect
+from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Body
+import os
@@
 async def get_snapshot():
     return {"status": "ok", "data": hub._snapshot, "error": None}
 
 async def emit(ev: AIEvent):
     """Manual emit from any code path."""
     await hub.publish(ev)
+
+# --- TEST-ONLY: allow Cypress/pytest to trigger hub events over HTTP ---
+@router.post("/api/_test/ai-activity/emit")
+async def _test_emit_event(
+    payload: dict = Body(...),
+):
+    """
+    Guarded by TEST_MODE=1. Payload shape:
+    {
+      "kind": "llm", "status": "inference",
+      "run_id": "dev", "model": "qwen3-8b", "provider": "LM Studio", "detail": "test"
+    }
+    """
+    if os.getenv("TEST_MODE", "0") != "1":
+        return {"status": "forbidden", "data": None, "error": "TEST_MODE not enabled"}
+    try:
+        ev = AIEvent(
+            kind=AIKind(payload.get("kind", "llm")),
+            status=Status(payload.get("status", "working")),
+            run_id=payload.get("run_id"),
+            model=payload.get("model"),
+            provider=payload.get("provider"),
+            detail=payload.get("detail"),
+        )
+        await hub.publish(ev)
+        return {"status":"ok", "data": ev.json(), "error": None}
+    except Exception as e:
+        return {"status":"error", "data": None, "error": str(e)}
*** End Patch
```

> To enable: set `TEST_MODE=1` in your `.env` or the compose service for the dashboard during E2E runs.

---

# 3) pytest skeletons

```
*** Begin Patch
*** Add File: tests/pytest.ini
+[pytest]
+asyncio_mode = auto
*** End Patch
```

```
*** Begin Patch
*** Add File: tests/conftest.py
+import os
+import pytest
+from fastapi.testclient import TestClient
+
+# Ensure test mode endpoints are available
+os.environ.setdefault("TEST_MODE", "1")
+
+# Import the FastAPI app from your dashboard entrypoint
+from src.dashboard.unified_dashboard import app
+
+@pytest.fixture(scope="session")
+def client():
+    return TestClient(app)
*** End Patch
```

```
*** Begin Patch
*** Add File: tests/test_ai_chat.py
+def test_ai_chat_basic(client):
+    payload = {"message": "hello 8.2", "context_run_id": "test-run", "model": "qwen3-8b", "provider": "LM Studio"}
+    r = client.post("/api/ai/chat", json=payload)
+    assert r.status_code == 200
+    body = r.json()
+    assert body["status"] == "ok"
+    assert "reply" in body["data"]
+    # Stub currently echoes
+    assert "hello 8.2" in body["data"]["reply"]
*** End Patch
```

```
*** Begin Patch
*** Add File: tests/test_ai_activity_ws.py
+from contextlib import contextmanager
+
+def test_snapshot_and_emit(client):
+    # 1) initial snapshot
+    snap = client.get("/api/ai-activity/snapshot").json()
+    assert snap["status"] == "ok"
+    assert isinstance(snap["data"], dict)
+
+    # 2) emit an event (test-only endpoint)
+    emit = {
+        "kind":"llm","status":"inference",
+        "run_id":"ws-test","model":"qwen3-8b","provider":"LM Studio","detail":"pytest"
+    }
+    r = client.post("/api/_test/ai-activity/emit", json=emit).json()
+    assert r["status"] == "ok"
+
+    # 3) snapshot should reflect last event for that kind
+    snap2 = client.get("/api/ai-activity/snapshot").json()
+    last_llm = snap2["data"]["llm"]
+    assert last_llm["status"] == "inference"
+    assert last_llm["model"] == "qwen3-8b"
+
+def test_websocket_receives_events(client):
+    with client.websocket_connect("/ws/ai-activity") as ws:
+        # On connect, snapshot arrives first
+        initial = ws.receive_json()
+        assert initial["type"] in ("snapshot", "event")
+
+        # Fire an event via test endpoint
+        payload = {"kind":"embedder","status":"working","model":"bge-m3","provider":"LM Studio","run_id":"x"}
+        r = client.post("/api/_test/ai-activity/emit", json=payload)
+        assert r.status_code == 200
+
+        # WS should receive the event
+        msg = ws.receive_json()
+        assert msg["type"] == "event"
+        data = msg["data"]
+        assert data["kind"] == "embedder"
+        assert data["status"] == "working"
*** End Patch
```

---

# 4) Cypress config + specs

```
*** Begin Patch
*** Add File: cypress.config.ts
+import { defineConfig } from 'cypress'
+
+export default defineConfig({
+  e2e: {
+    baseUrl: 'http://localhost:8050',
+    specPattern: 'cypress/e2e/**/*.cy.{js,ts}',
+    supportFile: 'cypress/support/e2e.ts',
+    video: false,
+  },
+})
*** End Patch
```

```
*** Begin Patch
*** Add File: cypress/support/e2e.ts
+// Global Cypress hooks can go here
*** End Patch
```

```
*** Begin Patch
*** Add File: cypress/fixtures/ai_snapshot.json
+{
+  "status": "ok",
+  "data": {
+    "llm": { "kind":"llm", "status":"idle", "model":"qwen3-8b", "provider":"LM Studio" },
+    "embedder": { "kind":"embedder", "status":"idle", "model":"bge-m3", "provider":"LM Studio" }
+  },
+  "error": null
+}
*** End Patch
```

```
*** Begin Patch
*** Add File: cypress/e2e/ai_activity.cy.ts
+describe('AI Activity strip', () => {
+  it('paints from snapshot and updates via WS emit', () => {
+    // Stub the initial snapshot so tiles render immediately
+    cy.intercept('GET', '/api/ai-activity/snapshot', { fixture: 'ai_snapshot.json' }).as('snapshot')
+    cy.visit('/')
+    cy.wait('@snapshot')
+
+    // Check that LLM pill shows model/provider text
+    cy.get('#ai-activity [data-kind="llm"] .ai-model')
+      .should('contain.text', 'qwen3-8b')
+      .and('contain.text', 'LM Studio')
+
+    // Trigger a live event through the test endpoint; the page has an open WS connection
+    cy.request('POST', '/api/_test/ai-activity/emit', {
+      kind: 'llm',
+      status: 'inference',
+      model: 'qwen3-8b',
+      provider: 'LM Studio',
+      run_id: 'cypress'
+    }).its('status').should('eq', 200)
+
+    // Assert the LLM pill flips to "inference" (green class sets data-status attr)
+    cy.get('#ai-activity [data-kind="llm"]').should('have.attr', 'data-status', 'inference')
+  })
+})
*** End Patch
```

```
*** Begin Patch
*** Add File: cypress/e2e/ai_chat.cy.ts
+describe('AI Chat dock', () => {
+  it('sends a message and shows reply', () => {
+    // Intercept chat call and return stubbed reply
+    cy.intercept('POST', '/api/ai/chat', (req) => {
+      expect(req.body.message).to.contain('ping')
+      req.reply({
+        status: 'ok',
+        data: { reply: 'pong: ' + req.body.message },
+        error: null
+      })
+    }).as('chat')
+
+    cy.visit('/')
+
+    // Open the chat dock (adjust selector to your UI)
+    cy.get('[data-test="open-chat"]').click()
+
+    // Type and send
+    cy.get('[data-test="chat-input"]').type('ping from cypress{enter}')
+
+    cy.wait('@chat')
+    cy.get('[data-test="chat-reply"]').should('contain.text', 'pong: ping from cypress')
+  })
+})
*** End Patch
```

> UI selectors (`[data-test="open-chat"]`, `[data-test="chat-input"]`, `[data-test="chat-reply"]`) are placeholders—add `data-test` attributes in your chat dock markup for stable tests.

---

# 5) NPM scripts (if you want one-liners)

```
*** Begin Patch
*** Update File: package.json
@@
   "scripts": {
+    "cypress:open": "cypress open",
+    "cypress:run": "cypress run",
+    "test": "pytest -q"
   }
*** End Patch
```

---

# 6) Compose/test env hint (enable TEST\_MODE)

If you run Cypress against Docker, add `TEST_MODE=1` to the dashboard service:

```diff
*** Begin Patch
*** Update File: docker/docker-compose.yml
@@
   dashboard:
     environment:
+      - TEST_MODE=1
*** End Patch
```

(Or export `TEST_MODE=1` before `uvicorn` locally.)

---

## What you’ll see

* `pytest` will verify the chat endpoint shape and that WS broadcasts are received.
* Cypress will confirm the snapshot paints the strip and that a WS event (triggered via the test-only endpoint) updates the UI, plus a happy-path chat send/receive.

If you want, I can also drop `data-test` attributes into your chat dock HTML and provide a tiny React/HTMX snippet for the dock so the Cypress selectors match exactly.
