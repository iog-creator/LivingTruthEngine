# Phase 8.1 Plan — Unified Guided Dashboard

## Objective
Redesign the Living Truth Dashboard into a single, coherent, step-by-step interface that integrates ingestion, run management, and analysis into one place. Preserve all Phase 8 functionality but make it beginner-friendly while keeping advanced tools accessible.

## Scope
- Navigation overhaul with clear sections: Home (Quick Start), Runs, Analyze, Tools.
- Step-by-step guided ingestion workflow with sensible defaults.
- Centralized run management with progress tracking and quick access to artifacts.
- Integrated analysis panels with consistent controls and contextual help.
- Power user section for advanced toggles and MCP tool access.
- Minimal backend changes — reuse existing Phase 8 endpoints where possible.

---

## Implementation Steps (Cursor executes in order)

### 1) **Navigation overhaul**
- Add a top navbar with tabs: **Home**, **Runs**, **Analyze**, **Tools**.
- Remove redundant or hidden pages; consolidate into the 4-tab structure.

### 2) **Home tab (Quick Start)**
- Pre-fill channel URL with `https://www.youtube.com/@imaginationpodcastofficial`.
- Show limit (default 10), sort (default oldest), depth (default 3).
- Place OCR/JS toggles inside a collapsible “More options” section.
- Add a prominent **Start Run** button.
- On run start: show progress toast + add to activity sidebar.

### 3) **Runs tab**
- Display table: Run ID, created_at, doc_count, status.
- Clicking a run → slide-in drawer with:
  - manifest.json
  - metrics.json
  - Merkle root
  - Download buttons for corpus.jsonl, proofs/, metrics.json
- Show “No runs yet” empty state with link to Quick Start.

### 4) **Analyze tab**
- Left column: bundle/doc picker (list of docs in selected bundle).
- Right column: tabs for:
  - **Summary**: textual overview
  - **Entities**: named entity list
  - **Claims**: extracted claims + verification status
  - **Graph**: network visualization
  - **Timeline**: chronological events
- Consistent toolbar (zoom, export, refresh).
- “Explain this result” link in each panel → calls LLM for explanation.

### 5) **Tools tab**
- Toggles for OCR required, JS render, HF burst, depth override.
- Buttons for raw MCP tool calls (start_veritas_youtube_channel_run, list_veritas_runs, etc.).
- Display MCP tool results in JSON viewer.

### 6) **Global UI improvements**
- Progress toasts for all long operations.
- Right-rail activity feed for recent actions.
- Contextual help icons (`?`) beside each control with inline descriptions.
- Unified spacing grid, typography scale, and consistent button styles.

### 7) **Backend/API**
- Add `/ui/runs` endpoint returning `{runs: [run_info...]}`.
- Add `/ui/runs/{id}` endpoint returning `{manifest, metrics, proofs, corpus_path}`.
- Add `/ui/analyze/entities` and `/ui/analyze/claims` endpoints wrapping existing analyzers.
- Standardize API responses to `{status, data, error}`.

### 8) **Testing**
- Verify “start run → see bundle → analyze doc” flow works in ≤ 60 seconds.
- Verify toggles update manifest flags in `.veritasrun`.
- Confirm mobile + desktop layouts work.
- Confirm all endpoints return data without errors.

---

## Deliverables
1. Updated `src/analysis/dash_app.py` with new layout and UI components.
2. New API endpoints in `src/api/ui_routes.py` (or equivalent).
3. Updated CSS/styling for consistent UI.
4. Tests covering:
   - UI workflow (mocked where possible)
   - API responses for new `/ui/*` routes
5. Updated README with screenshots of the new dashboard and usage instructions.
6. PHASE_8_1_COMPLETION_SUMMARY.md in root.

