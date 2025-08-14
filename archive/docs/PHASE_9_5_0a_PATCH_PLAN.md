---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/adapters/pdf_adapter.py', 'PHASE_9.md', 'src/adapters/web_adapter.py', 'src/mcp_tools/adapters.py']
---

# PHASE_9_5_0a_PATCH_PLAN.md — Adapter Internals Upgrade

## 🎯 Objective
Upgrade Web and PDF adapters to use high-quality, modern extraction libraries instead of legacy fetchers, while **preserving the current adapter API, MCP gates, and multi-source runner integration** delivered in Phase 9.5.0.

---

## 📋 Tasks

### 1. **PDF Adapter Upgrade**
- Replace legacy PDF fetch logic with **existing internal PDF extraction module** (preferred) or integrate **pdfplumber** as fallback.
- Preserve `PDFAdapter` public method signatures.
- Ensure text extraction preserves layout, tables, and metadata.
- Maintain `DocumentLike` output format and SHA256 deduplication.

### 2. **Web Adapter Upgrade**
- Replace legacy HTML fetcher with **Trafilatura** (for text extraction) or **Crawlee** (for JS-heavy sites).
- Add optional `js_render` flag that switches between lightweight and headless extraction.
- Preserve `WebAdapter` public method signatures and `DocumentLike` output.

### 3. **Testing Enhancements**
- Extend `scripts/p9_5_0_smoke.sh` to:
  - Test PDF extraction against a known sample PDF with structured content.
  - Test Web extraction against a simple HTML page and a JS-rendered page.
- Update MCP tool `mcp.lte.adapters.test_sources` to run new adapter tests.

### 4. **Fallback & Error Handling**
- Add try/fallback to existing adapter code:
  1. Attempt enhanced extraction (internal module / Trafilatura / pdfplumber).
  2. If fails, fallback to legacy fetcher with warning log.
- Log all fallbacks to `/api/health/full` under `recent_fallbacks`.

---

## ✅ Acceptance Criteria
1. `PDFAdapter` extracts full structured text from sample PDF with ≥95% fidelity.
2. `WebAdapter` extracts clean article text from:
   - Static HTML
   - JS-rendered content
3. SHA256 deduplication still functional across upgraded adapters.
4. All MCP gates from Phase 9.5.0 still pass.
5. Smoke script returns ≥1 document for PDF and Web in addition to YouTube.

---

## 🛠 MCP Gates
- **Preflight:** `mcp.project.rules.validate`, `mcp.lte.health.get_full`
- **Exit:** `mcp.lte.adapters.test_sources`, `mcp.lte.smoke.run_phase` (updated smoke script)

---

## 📁 Files to Modify
- `src/adapters/pdf_adapter.py`
- `src/adapters/web_adapter.py`
- `scripts/p9_5_0_smoke.sh`
- `src/mcp_tools/adapters.py` (update test_sources tool)
- Optionally: `requirements.txt` (add Trafilatura, pdfplumber)

---

## 🔒 Constraints
- **Do not change** API endpoint paths or payload formats.
- **Do not remove** legacy fetchers — keep as fallback.
- All upgrades must be Docker-buildable and pass CI in existing pipelines.

---

**End of Phase 9.5.0a Patch Plan**
