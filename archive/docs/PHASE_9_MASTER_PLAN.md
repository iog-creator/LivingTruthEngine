---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['linking_pipeline.py']
---

# Phase 9 Master Plan
**Plans Only — Incorporates All Lessons Learned to Allow Full Replay from Scratch**

---

## 9.3.0 – Graph Extraction & Linking Pipeline
**Objectives**
- Implement entity & claim extraction pipeline across ingested documents.
- Link entities and claims across documents to form an evidence graph.
- Integrate deterministic policy checks (Rulego).
- Integrate AI corroboration (DSPy).
- Expose read-only APIs for graph/timeline consumption.
- Persist features & links in Postgres (pgvector + relational tables).

**Key Steps**
1. Create `003_graph.sql` schema with required tables & indexes.
2. Implement `linking_pipeline.py` for extraction, linking, and snapshotting.
3. Add CPU/GPU model fallback support.
4. Add `/api/graph/{run_id}` and `/api/timeline/{run_id}` endpoints.
5. Add minimal UI Graph tab to view output.
6. Write smoke test `p9_3_smoke.sh`.
7. **MCP/RULES Enforcement:**  
   - Update MCP tools for graph/timeline APIs.  
   - Update Cursor rules for graph build, validation, and smoke tests.  
   - Validate with MCP server gates.

**Acceptance Criteria**
- APIs return `{status,data,error}` envelope.
- End-to-end smoke script passes.
- MCP validation passes with updated tool definitions.

---

## 9.3.1 – Hardening & Consistency
**Objectives**
- Enforce schema constraints and envelope consistency.
- Add idempotency and rebuild support for graph builds.
- Improve error handling for extraction/linking.

**Key Steps**
1. Add `?rebuild=1` option to graph build.
2. Wrap builds in transactions with `ON CONFLICT` upserts.
3. Add detailed error messages with remediation hints.
4. Expand smoke tests to cover rebuild.
5. **MCP/RULES Enforcement:**  
   - Update MCP tools for rebuild option and constraints.  
   - Update Cursor rules for idempotent builds & DB validation.  

**Acceptance Criteria**
- No constraint violations on repeated builds.
- MCP server health passes.

---

## 9.4.0 – DevOps Cutover Skeleton
**Objectives**
- Single origin server: `/api/**` via FastAPI, `/` via new UI shell.
- Reverse proxy configuration.
- Dev environment parity for API/UI.

**Key Steps**
1. Configure dashboard to serve both API & UI.
2. Add reverse proxy for API routing.
3. Update Docker Compose for single origin deployment.
4. Add CI test to verify routing works.
5. **MCP/RULES Enforcement:**  
   - Update MCP tool for health check across reverse proxy.  
   - Add Cursor rule to block merges if proxy health fails.

**Acceptance Criteria**
- UI and API accessible under same origin.
- Reverse proxy health passes in MCP tests.

---

## 9.4.1 – CI Build & Phase Gate
**Objectives**
- Add per-phase build & deploy gates.
- Integrate MCP validation into CI.

**Key Steps**
1. Add `scripts/ci/validate_phase9.sh` with per-phase checks.
2. Add CI pipeline step for MCP validation.
3. Enforce MCP ruleset sync before build.
4. **MCP/RULES Enforcement:**  
   - Add MCP tool for CI status reporting.  
   - Update Cursor rules to run MCP before merge.

**Acceptance Criteria**
- MCP server passes in CI.
- Merge blocked on validation failure.

---

## 9.4.2 – UI Integration Gate
**Objectives**
- Standardize UI component integration process.
- Enforce UI health in MCP validation.

**Key Steps**
1. Define UI build test in MCP.
2. Update MCP server with `/ui/health` check.
3. Add Cursor rule for UI build success gate.
4. Add UI smoke test script.
5. **MCP/RULES Enforcement:**  
   - Update tools for UI validation & smoke run.  

**Acceptance Criteria**
- MCP UI health passes before deploy.

---

## 9.4.3 – Graph API Expansion
**Objectives**
- Add filters, search, and metadata to graph API.
- Prepare for advanced UI graph interactions.

**Key Steps**
1. Extend `/api/graph/{run_id}` with filters & search params.
2. Add node/edge metadata in API.
3. Update MCP tools for expanded graph API.
4. **MCP/RULES Enforcement:**  
   - Update Cursor rules for expanded API validation.  

**Acceptance Criteria**
- Expanded graph API responds within 500 ms.
- MCP graph tests pass.

---

## 9.4.4 – API Envelope Enforcement
**Objectives**
- Validate API envelope format across all endpoints.
- Automate enforcement in CI.

**Key Steps**
1. Add MCP tool for envelope validation.
2. Update Cursor rules to block on envelope failures.
3. Integrate into `validate_phase9.sh`.
4. **MCP/RULES Enforcement:**  
   - Tool for bulk API validation.  

**Acceptance Criteria**
- 100% envelope compliance.

---

## 9.4.5 – Health Gates Expansion
**Objectives**
- Expand `/api/health/full` with all phase metrics.
- MCP tool for full health validation.

**Key Steps**
1. Add metrics: GPU, embedding model/dim, recent fallbacks.
2. Update MCP server to parse and validate health metrics.
3. **MCP/RULES Enforcement:**  
   - Cursor rules updated to require all health gates pass.

**Acceptance Criteria**
- Health gates fully cover system readiness.

---

## 9.4.6 – Error Handling & Observability
**Objectives**
- Centralize error handling.
- Improve observability via structured logging.

**Key Steps**
1. Add error codes and categories.
2. Add structured logging to all APIs.
3. Update MCP tools for error log scraping.
4. **MCP/RULES Enforcement:**  
   - Cursor rule requiring error budget compliance.

**Acceptance Criteria**
- All errors logged with code/category.
- MCP detects no unclassified errors.

---

## 9.4.7 – CI/CD Auto-Remediation Hooks
**Objectives**
- Auto-remediate common failures in CI/CD.
- Integrate MCP-triggered fixes.

**Key Steps**
1. Add remediation scripts for known errors.
2. Update MCP tools to trigger remediation hooks.
3. **MCP/RULES Enforcement:**  
   - Cursor rule blocks if remediation fails.

**Acceptance Criteria**
- CI/CD can auto-fix predefined failure modes.

---

## 9.5.0 – Real Adapters
**Objectives**
- Implement real YouTube, Web, and PDF adapters.
- Deduplicate by SHA256.
- Persist transcript mode.

**Key Steps**
1. Implement adapters in `src/adapters/`.
2. Add enhanced multi-source runner.
3. Integrate into API.
4. Smoke test `p9_5_0_smoke.sh`.
5. **MCP/RULES Enforcement:**  
   - Update MCP tools for adapter tests.

**Acceptance Criteria**
- ≥1 doc/source in multi-source run.
- MCP adapter tests pass.

---

## 9.5.0a – Adapter Internals Upgrade
**Objectives**
- Upgrade Web/PDF adapters with high-quality extraction libraries.

**Key Steps**
1. Web: Trafilatura + readability + JS render fallback.
2. PDF: PyMuPDF + pdfplumber + OCR fallback.
3. Add robust fallback chain.
4. Update smoke tests.
5. **MCP/RULES Enforcement:**  
   - MCP tool for extraction quality metrics.

**Acceptance Criteria**
- Enhanced extraction quality.
- MCP extraction tests pass.

---

## 9.5.1 – Model-Aware Embedding Storage
**Objectives**
- Remove magic dimensions.
- Partition by `(model_key, dim)`.
- Backfill embeddings.

**Key Steps**
1. Schema migration.
2. Update embedding store ops.
3. Health gate for dim mismatch.
4. **MCP/RULES Enforcement:**  
   - Tool for embedding validation.

**Acceptance Criteria**
- No dim mismatches.
- MCP embedding test passes.

---

## 9.5.2 – Embedding Backfill & Verification
**Objectives**
- Backfill missing embeddings.
- Verify all embeddings match model/dim.

---

## 9.5.3 – Timeline API + Graph Polish
**Objectives**
- `/api/timeline/{run_id}` endpoint.
- Graph UX filters/pinning polish.

---

## 9.5.4 – Performance Gates
**Objectives**
- p95 latency measurement.
- LCP budget enforcement.
- Bundle size optimization.
- CI gates for regressions.

---

## 9.5.5 – Error Budgeting & Recovery Automation
**Objectives**
- Error budget enforcement.
- Automated recovery workflows.

---

## 9.6.x – Full GPU / Real Model Integration
**Objectives**
- GPU model serving for embeddings, reranking, LLM tasks.

---

## 9.7.x – Advanced Evidence Graph & UI Overhaul
**Objectives**
- New UI with real-time graph interactions and advanced filters.
