Alright — here’s a **Phase 9 plan** in the same structured format we’ve been using, ready for handoff to the next chat after Phase 8.2 wraps.

---

# **PHASE 9 PLAN — Multi-Source Expansion & Advanced Evidence Linking**

## **Objective**

Expand the system beyond a single YouTube channel to support **multiple simultaneous sources** (websites, PDFs, images, and other channels), add **cross-document linking and visualization**, and integrate more **AI-assisted verification workflows**.

---

## **Scope (What Ships)**

* **Multi-source ingestion**:

  * Ability to run from multiple YouTube channels, domain URLs, PDF repositories in one job.
  * Source list management from Dashboard.
* **Advanced link discovery**:

  * Detect named entities, claims, and references across different sources.
  * Link documents by people, places, events, and cited URLs.
* **Evidence graph view**:

  * Interactive 2D/3D graph showing connections between docs, entities, and claims.
  * Filter by source type, confidence, and date.
* **AI-assisted verification**:

  * Auto-flag suspicious or unverified claims.
  * Suggest corroborating or contradicting documents.
* **Flexible run configuration**:

  * Choose per-source parameters (max depth, OCR/JS toggles).
* **Improved run metadata**:

  * Store and display cross-source relationships in manifest.

---

## **Implementation Steps**

### **1) Multi-Source Runner Backend**

* Update `VeritasRunner`:

  * Accept multiple source configs in a single job.
  * Dispatch correct adapter per source type (`youtube_adapter`, `web_fetcher`, `pdf_extractor`).
  * Merge all docs into a unified corpus with per-source tags.

### **2) Source Registry**

* **File**: `config/source_registry.toml`

  * Define reusable source presets:

    ```toml
    [[source]]
    type = "youtube"
    url = "https://www.youtube.com/@imaginationpodcastofficial"
    limit = 10
    sort = "oldest"
    max_depth = 3
    ocr_required = false
    js_render = false

    [[source]]
    type = "web"
    url = "https://example.com/research-archive"
    max_depth = 2
    ```

### **3) Entity & Claim Linking**

* Enhance canonicalization to extract:

  * Named entities (via NER model)
  * Claims (subject-predicate-object triples)
* Create `links.json` in bundle:

  * Edges between docs by shared entities or claim references.

### **4) Evidence Graph**

* **Backend**: API route `/api/graph/{run_id}`

  * Returns nodes/edges for D3.js or Plotly.
* **Frontend**:

  * New tab in Analyze: "Evidence Graph"
  * Interactive zoom, filter by entity type, date, confidence.

### **5) AI-Assisted Verification**

* New MCP tool `verify_claims_in_run(run_id)`:

  * For each claim, check:

    * Is there corroborating evidence in corpus?
    * Is there contradictory evidence?
  * Add `verification.json` to bundle.

### **6) Dashboard Changes**

* "New Run" form:

  * Multiple source selection (from registry or manual entry).
  * Per-source parameter controls.
* Analyze:

  * Evidence Graph tab.
  * Claim verification panel.

### **7) Manifest & Metadata**

* Update `manifest.json` schema:

  * `sources`: array with type, url, params.
  * `links`: reference to `links.json`.
  * `verification`: reference to `verification.json`.

### **8) Tests**

* pytest:

  * Multi-source ingestion produces combined corpus.
  * Entities/claims extracted from all sources.
  * Graph API returns valid nodes/edges.
* Cypress:

  * Dashboard multi-source UI works.
  * Graph and claim panels display correctly.

---

## **Dependencies**

* `spacy` or `transformers` NER model for entity extraction.
* Graph library for frontend (D3.js or Plotly).
* If OCR/JS still optional, reuse Phase 8 flags.

---

## **Docs & Rules**

* README:

  * Multi-source run examples.
  * Evidence Graph usage.
  * Claim verification workflow.
* `.cursor/rules/current_working_state.mdc` updated for new features.
* Add `PHASE_9_COMPLETION_SUMMARY.md` (template below).

---

# **PHASE 9 COMPLETION SUMMARY — Template**

When complete, verify:

1. **Multi-source ingestion**:

   * Runs can ingest from ≥2 sources in one job.
   * Manifest lists all sources with params.
2. **Link discovery**:

   * `links.json` created with correct edges.
3. **Evidence Graph**:

   * Graph tab loads and is interactive.
4. **Claim verification**:

   * `verification.json` created with corroboration/contradiction results.
5. **Dashboard**:

   * Multi-source config form works.
   * Graph and verification panels display.
6. **Tests**:

   * All pytest & Cypress tests green.
7. **Docs & Rules**:

   * Updated for multi-source + graph + verification.

---

If we do Phase 8.2 → Phase 9 in order, you’ll end up with a **dashboard that not only runs YouTube ingestion but also maps cross-source evidence visually and verifies claims**.

Do you want me to also include **the AI activity visualization & chat control from 8.2** into this Phase 9 graph so that the user can see **which AI model worked on which part of the evidence**? That would make the graph dynamic.
