---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/analysis/linking_pipeline.py', 'src/dashboard/unified_dashboard.py', 'src/ai/dspy_programs.py', 'src/storage/pgvector_store.py', 'apiClient.ts', 'src/analysis/rulego_bridge.py']
---

You’re right—the current setup is brittle. The root issues I’m hearing/seeing:

* Two front-end “homes” got edited in parallel (state page vs. 8050), so state and callbacks diverged.
* Dash callback wiring made basic button interactions fragile and opaque.
* No single source of truth for UI state, routes, or API contracts.

Let’s reset with a clean, modern stack and an opinionated scaffold that bakes in reliability.

# New Front‑End: What we’re building

**Goals**

* One client app. One state store. One API contract. No split-brain UI.
* Bulletproof buttons & forms (predictable loading/disabled/error states).
* Fast charts/graphs, accessible components, dark mode, and testable flows.
* Easy migration path from the current APIs and pages.

**Stack (decisive choice)**

* **Next.js 14 (App Router) + TypeScript** for routing, SSR/SSG, and code-splitting.
* **Tailwind CSS + shadcn/ui** for accessible, consistent components.
* **TanStack Query** for data fetching/cache, retries, request dedupe.
* **Zustand** for cross-page client state (lightweight, explicit).
* **Zod** for runtime type validation of API responses.
* **Recharts** for charts; **Cytoscape.js** (with cola layout) for 2D graphs; **3D (optional later):** three.js/force-graph.
* **Playwright** (E2E) + **Vitest** (unit) + **Testing Library** (component).
* **MSW** (mock service worker) for API mocks in dev/tests.
* **OpenAPI (generated types)** if we have a spec; else hand-rolled Zod schemas first.

---

# Information Architecture (routes you’ll see)

* `/` **Overview** — at-a-glance health, recent runs, quick actions.
* `/runs` **Job Runs** — start a run, list, view details, verify proofs.

  * `/runs/[runId]` details: manifest, metrics, Merkle root/leaf count, artifacts.
* `/graph` **Evidence Graph** — simple force graph (entities/claims/doc links).
* `/claims` **Claims** — table with status, corroboration, filters.
* `/entities` **Entities** — table + quick profile drawer and cross-doc links.
* `/models` **Models** — SSOT snapshot (what’s loaded, device, checksums).
* `/health` **Health** — gates, dependencies, errors, recent fallbacks.
* `/settings` **Flags** — OCR/PII/HF burst toggles (read-only until back-end supports writes).

> All pages consume the **same JSON envelope** the backend already uses:
> `{ status: "ok" | "error", data?: T, error?: { code, message, meta? } }`

---

# “Why buttons will just work” (interaction model)

* Every action button is a **single async mutation** via TanStack Query:

  * shows **loading** (spinner on the button),
  * **disabled** while in flight (prevents double-submit),
  * **toasts** on success/error,
  * **optimistic updates** where safe (e.g., “Start Run” adds placeholder row).
* All forms use **Zod schemas** for validation; submit is blocked with clear inline errors.
* Errors from the server surface through a **single apiClient** that respects the envelope and maps to typed results.

---

# High‑Level Project Structure

```
ui/
├─ app/                    # Next.js App Router
│  ├─ (dashboard)/         # Grouped routes
│  │  ├─ page.tsx          # Overview
│  │  ├─ runs/
│  │  │  ├─ page.tsx       # Runs list + Start Run
│  │  │  └─ [runId]/page.tsx
│  │  ├─ graph/page.tsx
│  │  ├─ claims/page.tsx
│  │  ├─ entities/page.tsx
│  │  ├─ models/page.tsx
│  │  ├─ health/page.tsx
│  │  └─ settings/page.tsx
│  └─ api/hello/route.ts   # (dev sanity)
├─ components/
│  ├─ ui/…                 # shadcn-generated primitives
│  ├─ charts/…             # Recharts wrappers
│  ├─ graph/GraphView.tsx  # Cytoscape wrapper
│  ├─ runs/…               # RunList, RunDetail, StartRunForm
│  └─ layout/…             # AppShell, Sidebar, Topbar
├─ lib/
│  ├─ apiClient.ts         # fetch wrapper w/ envelope + error mapping
│  ├─ query.ts             # TanStack Query client/provider
│  ├─ schemas.ts           # Zod schemas for API shapes
│  ├─ state.ts             # Zustand store (UI-only flags, ephemeral UI state)
│  └─ env.ts               # public runtime config (NEXT_PUBLIC_API_BASE etc.)
├─ styles/
│  └─ globals.css
├─ tests/                  # Vitest + Playwright
└─ next.config.mjs
```

---

# API contracts we will honor (typed)

```ts
// lib/schemas.ts
import { z } from "zod";

export const Envelope = <T extends z.ZodTypeAny>(data: T) =>
  z.object({
    status: z.enum(["ok", "error"]),
    data: data.optional(),
    error: z
      .object({ code: z.string(), message: z.string(), meta: z.record(z.any()).optional() })
      .optional(),
  });

export const RunManifest = z.object({
  run_id: z.string(),
  topic: z.string(),
  started_at: z.string(),
  flags: z.record(z.any()),
  documents: z.array(z.string()),
});

export const RunsList = Envelope(
  z.array(
    z.object({
      run_id: z.string(),
      created_at: z.string(),
      completed_at: z.string().optional(),
      job_label: z.string().optional(),
      status: z.enum(["pending", "running", "completed", "failed"]),
    }),
  ),
);

export const RunOpen = Envelope(
  z.object({
    manifest: RunManifest,
    metrics: z.object({
      docs_total: z.number(),
      docs_by_source: z.record(z.number()),
      duration_seconds: z.number().optional(),
    }),
    merkle: z.object({ root: z.string(), leaves: z.number() }),
  }),
);

export const StartRunResponse = Envelope(
  z.object({ run_id: z.string(), status: z.string() }),
);

export const GraphSnapshot = Envelope(
  z.object({
    nodes: z.array(z.object({ id: z.string(), label: z.string(), type: z.string() })),
    edges: z.array(z.object({ id: z.string(), source: z.string(), target: z.string(), kind: z.string() })),
    findings: z.any().optional(),
  }),
);
```

> These schemas strictly match the “envelope” pattern used across your backend; they’ll fail fast if anything drifts.

---

# Key Pages & Components

### 1) Job Runs

* **StartRunForm**: topic, sources (web/pdf/youtube), max\_docs; calls `/api/.../start` or MCP proxy; shows disable/loading.
* **RunsTable**: paginated list; status chips; click → detail.
* **RunDetail**: manifest, metrics, merkle root; **Verify Proofs** button (calls verify endpoint when available).

### 2) Graph

* **GraphView** (Cytoscape): groups by entity/claim/document; edge filter by link type; search; hover tooltips.
* Handles large graphs with WebGL renderer; falls back gracefully with message.

### 3) Claims / Entities

* Smart tables with column filters, quick link to source doc (opens drawer), status badges (corroborated/weak/contradicted).

### 4) Models / Health / Settings

* Read-only SSOT and health gates (from `/api/health/full` & `/api/models`).
* Settings mirrors flags from the repo; if write isn’t supported yet, disables the toggles but still shows values.

---

# Design system & UX rules (baked in)

* **Layout**: AppShell with left sidebar (icons + labels), sticky topbar (env badge, search), main content.
* **States**: Every async component must implement `idle → loading → success/error` with skeletons; no silent failures.
* **A11y**: shadcn/ui primitives, focus rings, keyboard nav, prefers‑reduced‑motion respected.
* **Themes**: system, light, dark (persisted to `localStorage`).
* **Charts**: Recharts with responsive containers; alt text & table fallback button.

---

# Observability & reliability

* **Client metrics**: minimal pageview + API timing (e.g., tiny custom logger; optional to wire to your server logs).
* **Global error boundary**: user-safe crash screen plus “copy error details” (no secrets).
* **Network policy**: all fetches go through `apiClient` with:

  * base URL `NEXT_PUBLIC_API_BASE` (staging/prod via env),
  * envelope parsing + Zod validation,
  * retries/backoff only for GETs (never for POST actions).

---

# DevOps & migration (no big-bang)

1. **Reverse proxy** (Traefik/Nginx) at one hostname:

   * `/api/**` → your current FastAPI/8050
   * `/**` → the new Next.js UI
   * Keeps ports invisible and ends the “8050 vs state page” split.
2. **Incremental parity**:

   * First deliver **Overview**, **Runs**, **Health** (reads only).
   * Add **Graph**, **Claims**, **Entities**.
   * Keep the old Dash pages available at a legacy path until we’re confident.
3. **Contracts**:

   * Lock the envelope + endpoints we rely on (we already match your Phase docs).
   * If an endpoint is unfinished, we **stub with MSW** so UI is testable today.

---

# Testing (acceptance baked in)

* **E2E** (Playwright):

  * Start Run → shows “running” → list refresh → open run → sees manifest & merkle root.
  * Buttons disabled during request; errors surface in toast.
* **Contract tests** (Vitest):

  * Each endpoint validated by Zod (schemas above).
* **Visual tests**:

  * Storybook (optional) for StartRunForm, GraphView with sample JSON.

---

# Non‑negotiables to prevent regressions

* One front-end repo only; no editing UI in the API repo.
* All API calls **must** use `apiClient` (enforces envelope + zod).
* No “just a fetch in a component”.
* No hidden global state; only TanStack Query (server state) + a tiny Zustand store for UI bits.
* Lint rules: disallow `fetch` outside `apiClient.ts`.

---

# Initial folder scaffold (ready to paste)

```
ui
├─ app
│  ├─ (dashboard)
│  │  ├─ layout.tsx
│  │  ├─ page.tsx
│  │  ├─ runs/page.tsx
│  │  ├─ runs/[runId]/page.tsx
│  │  ├─ graph/page.tsx
│  │  ├─ claims/page.tsx
│  │  ├─ entities/page.tsx
│  │  ├─ models/page.tsx
│  │  └─ health/page.tsx
│  └─ globals.css
├─ components
│  ├─ layout/AppShell.tsx
│  ├─ runs/RunList.tsx
│  ├─ runs/RunDetail.tsx
│  ├─ runs/StartRunForm.tsx
│  ├─ graph/GraphView.tsx
│  └─ ui/* (shadcn)
├─ lib
│  ├─ apiClient.ts
│  ├─ query.ts
│  ├─ schemas.ts
│  ├─ state.ts
│  └─ env.ts
├─ tests
│  ├─ e2e/start-run.spec.ts
│  └─ unit/apiClient.test.ts
├─ tailwind.config.ts
├─ tsconfig.json
└─ package.json
```

---

# How we’ll reflect “hind‑sight” learnings

* **Single source of truth** for flags & models: surface SSOT (from `/api/models`, `/api/health/full`) as read-only panels so drift is obvious.
* **Job Runs** is first-class (not a buried tab): you told me it’s essential—so it’s a top-level route with its own list/detail flow.
* **Proof verification** is a button with explicit result states (pass/fail + leaf diffs) instead of a silent log line.
* **Graph** ships with filters and safe defaults; if the dataset is big or missing, we show a helpful empty state, not a broken canvas.
* **No more dead buttons**: every actionable control is tested in E2E with loading/disabled expectations.

---
Awesome — taking that as a green light to kick off Phase 9.3 scaffolding now. Here’s a ready‑to‑drop starter pack so you can paste into your repo and run smoke right away.

# Files to add

## `docker/initdb/003_graph.sql`

```sql
-- lte evidence graph schema
CREATE SCHEMA IF NOT EXISTS lte;

-- documents
CREATE TABLE IF NOT EXISTS lte.documents (
  id            UUID PRIMARY KEY,
  run_id        TEXT NOT NULL,
  source_type   TEXT NOT NULL,
  uri           TEXT,
  title         TEXT,
  published_at  TIMESTAMPTZ,
  shard_no      INT DEFAULT 0,
  text_len      INT DEFAULT 0,
  sha256        TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

-- entities
CREATE TABLE IF NOT EXISTS lte.entities (
  id          UUID PRIMARY KEY,
  doc_id      UUID REFERENCES lte.documents(id) ON DELETE CASCADE,
  type        TEXT NOT NULL,
  value       TEXT NOT NULL,
  span_start  INT,
  span_end    INT,
  conf        REAL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- claims
CREATE TABLE IF NOT EXISTS lte.claims (
  id          UUID PRIMARY KEY,
  doc_id      UUID REFERENCES lte.documents(id) ON DELETE CASCADE,
  text        TEXT NOT NULL,
  normalized  TEXT,
  conf        REAL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- links
CREATE TABLE IF NOT EXISTS lte.entity_links (
  id               UUID PRIMARY KEY,
  left_entity_id   UUID REFERENCES lte.entities(id) ON DELETE CASCADE,
  right_entity_id  UUID REFERENCES lte.entities(id) ON DELETE CASCADE,
  link_type        TEXT NOT NULL,      -- e.g., same-as, coref, alias
  score            REAL NOT NULL,
  method           TEXT NOT NULL,      -- e.g., "block+rerank"
  created_at       TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lte.claim_links (
  id              UUID PRIMARY KEY,
  left_claim_id   UUID REFERENCES lte.claims(id) ON DELETE CASCADE,
  right_claim_id  UUID REFERENCES lte.claims(id) ON DELETE CASCADE,
  link_type       TEXT NOT NULL,       -- support | contradict | duplicate
  score           REAL NOT NULL,
  method          TEXT NOT NULL,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- vector embeddings
CREATE TABLE IF NOT EXISTS lte.doc_embeddings (
  doc_id     UUID PRIMARY KEY REFERENCES lte.documents(id) ON DELETE CASCADE,
  embedding  VECTOR(768),
  model      TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lte.claim_embeddings (
  claim_id   UUID PRIMARY KEY REFERENCES lte.claims(id) ON DELETE CASCADE,
  embedding  VECTOR(768),
  model      TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- graph cache
CREATE TABLE IF NOT EXISTS lte.graph_snapshots (
  id          UUID PRIMARY KEY,
  run_id      TEXT NOT NULL,
  payload_json JSONB NOT NULL,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- indexes
CREATE INDEX IF NOT EXISTS idx_docs_runid ON lte.documents(run_id);
CREATE INDEX IF NOT EXISTS idx_entities_doc ON lte.entities(doc_id);
CREATE INDEX IF NOT EXISTS idx_claims_doc   ON lte.claims(doc_id);

-- pgvector indexes (requires pgvector extension already enabled)
CREATE INDEX IF NOT EXISTS idx_doc_embed_ivf
  ON lte.doc_embeddings USING ivfflat (embedding vector_l2_ops) WITH (lists=100);

CREATE INDEX IF NOT EXISTS idx_claim_embed_ivf
  ON lte.claim_embeddings USING ivfflat (embedding vector_l2_ops) WITH (lists=200);
```

## `src/analysis/linking_pipeline.py`

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from uuid import uuid4

# NOTE: wire these to your existing SSOT + stores
from src.storage.pgvector_store import PgVectorStore  # extend as needed
from src.analysis.rulego_bridge import evaluate_graph
from src.ai.dspy_programs import CorroborationProgram

@dataclass
class ExtractedEntity:
    id: str
    doc_id: str
    type: str
    value: str
    span: Tuple[int, int]
    conf: float

@dataclass
class ExtractedClaim:
    id: str
    doc_id: str
    text: str
    normalized: str
    conf: float

class LinkingPipeline:
    def __init__(self, store: PgVectorStore):
        self.store = store

    # --- Extraction ---------------------------------------------------------
    def extract_entities(self, doc: Dict[str, Any]) -> List[ExtractedEntity]:
        """
        TODO: replace with real NER (GPU if available per models.toml).
        For now, emit a trivial entity from title if present.
        """
        ents: List[ExtractedEntity] = []
        title = (doc.get("title") or "").strip()
        if title:
            ents.append(ExtractedEntity(
                id=str(uuid4()), doc_id=doc["id"], type="TITLE", value=title,
                span=(0, len(title)), conf=0.6
            ))
        return ents

    def extract_claims(self, doc: Dict[str, Any]) -> List[ExtractedClaim]:
        """
        TODO: DSPy-powered atomic claim extraction.
        """
        text = (doc.get("text") or "")[:400]
        if not text:
            return []
        return [ExtractedClaim(
            id=str(uuid4()), doc_id=doc["id"], text=text,
            normalized=text.lower().strip(), conf=0.55
        )]

    # --- Embeddings ---------------------------------------------------------
    def embed_entities_claims(self, run_id: str, entities: List[ExtractedEntity],
                              claims: List[ExtractedClaim]) -> None:
        """
        TODO: call LM Studio embedding model per SSOT; persist into pgvector tables.
        """
        self.store.bulk_upsert_claim_embeddings([(c.id, [0.0]*768, "mock") for c in claims])
        # document-level embeddings left as is for now

    # --- Linking ------------------------------------------------------------
    def link_entities_across_docs(self, run_id: str) -> int:
        """
        TODO: blocking (string match + kNN) then rerank; write lte.entity_links.
        """
        # Minimal stub: no cross-links yet.
        return 0

    def link_claims_across_docs(self, run_id: str) -> int:
        """
        TODO: kNN on claim_embeddings + rerank; write lte.claim_links.
        """
        return 0

    # --- Snapshot -----------------------------------------------------------
    def snapshot_graph(self, run_id: str) -> Dict[str, Any]:
        nodes, edges = self.store.build_graph_snapshot(run_id)
        findings = evaluate_graph(run_id, nodes, edges)
        payload = {"nodes": nodes, "edges": edges, "findings": findings}
        self.store.save_graph_snapshot(run_id, payload)
        return payload

# Convenience function used by API
def build_graph_for_run(run_id: str, store: PgVectorStore) -> Dict[str, Any]:
    lp = LinkingPipeline(store)
    docs = store.get_documents_by_run(run_id)
    all_ents, all_claims = [], []
    for d in docs:
        all_ents += lp.extract_entities(d)
        all_claims += lp.extract_claims(d)
    store.upsert_entities(all_ents)
    store.upsert_claims(all_claims)
    lp.embed_entities_claims(run_id, all_ents, all_claims)
    lp.link_entities_across_docs(run_id)
    lp.link_claims_across_docs(run_id)
    return lp.snapshot_graph(run_id)
```

## `src/analysis/rulego_bridge.py`

```python
from typing import List, Dict, Any

def evaluate_graph(run_id: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Deterministic checks placeholder. Wire to Rulego later.
    Return shape:
      { "policy_findings": [ { "rule_id": "...", "severity": "info|warn|error", "nodes": [...], "msg": "..." } ] }
    """
    findings = []
    if not edges:
        findings.append({
            "rule_id": "MIN_EVIDENCE",
            "severity": "warn",
            "nodes": [],
            "msg": "No cross-document links found; evidence graph is sparse."
        })
    return {"policy_findings": findings}
```

## `src/ai/dspy_programs.py`

```python
from typing import Dict, Any, List

class CorroborationProgram:
    """
    Stub for DSPy corroboration.
    Later: label in {'corroborated','weak','contradicted'} with rationale + citations.
    """
    def run_batch(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        out = []
        for c in claims:
            out.append({
                "claim_id": c["id"],
                "label": "weak",
                "rationale": "Placeholder rationale (DSPy not wired yet).",
                "citations": []
            })
        return out
```

## `src/storage/pgvector_store.py` (add/extend minimal methods)

```python
from __future__ import annotations
from typing import List, Dict, Any, Tuple
import json, uuid

class PgVectorStore:
    # assume you already have a connection pool; pseudocode here
    def __init__(self, conn):
        self.conn = conn

    # --- documents ----------------------------------------------------------
    def get_documents_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        q = "SELECT id::text, run_id, source_type, title, '' AS text FROM lte.documents WHERE run_id=%s"
        with self.conn.cursor() as cur:
            cur.execute(q, (run_id,))
            rows = cur.fetchall()
        return [dict(id=r[0], run_id=r[1], source_type=r[2], title=r[3], text=r[4]) for r in rows]

    # --- entities/claims ----------------------------------------------------
    def upsert_entities(self, ents) -> None:
        if not ents: return
        with self.conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO lte.entities(id, doc_id, type, value, span_start, span_end, conf) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
                [(e.id, e.doc_id, e.type, e.value, e.span[0], e.span[1], e.conf) for e in ents]
            )
        self.conn.commit()

    def upsert_claims(self, claims) -> None:
        if not claims: return
        with self.conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO lte.claims(id, doc_id, text, normalized, conf) "
                "VALUES(%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
                [(c.id, c.doc_id, c.text, c.normalized, c.conf) for c in claims]
            )
        self.conn.commit()

    # --- embeddings ---------------------------------------------------------
    def bulk_upsert_claim_embeddings(self, items: List[Tuple[str, List[float], str]]):
        if not items: return
        with self.conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO lte.claim_embeddings(claim_id, embedding, model) VALUES(%s,%s,%s) "
                "ON CONFLICT (claim_id) DO UPDATE SET embedding=EXCLUDED.embedding, model=EXCLUDED.model",
                [(cid, item[1], item[2]) for cid, *item in [(i[0], i[1], i[2]) for i in items]]
            )
        self.conn.commit()

    # --- graph snapshot -----------------------------------------------------
    def build_graph_snapshot(self, run_id: str):
        # Minimal node/edge projection
        with self.conn.cursor() as cur:
            cur.execute("SELECT id::text, title FROM lte.documents WHERE run_id=%s", (run_id,))
            docs = [{"id": r[0], "type": "document", "title": r[1]} for r in cur.fetchall()]

            cur.execute("SELECT id::text, doc_id::text, type, value FROM lte.entities "
                        "JOIN lte.documents d ON d.id=doc_id WHERE d.run_id=%s", (run_id,))
            ents = [{"id": r[0], "type": "entity", "doc_id": r[1], "entity_type": r[2], "value": r[3]} for r in cur.fetchall()]

            cur.execute("SELECT id::text, doc_id::text, text FROM lte.claims "
                        "JOIN lte.documents d ON d.id=doc_id WHERE d.run_id=%s", (run_id,))
            claims = [{"id": r[0], "type": "claim", "doc_id": r[1], "text": r[2]} for r in cur.fetchall()]

            cur.execute("SELECT left_entity_id::text, right_entity_id::text, link_type, score FROM lte.entity_links")
            elinks = [{"source": r[0], "target": r[1], "type": r[2], "score": r[3]} for r in cur.fetchall()]

            cur.execute("SELECT left_claim_id::text, right_claim_id::text, link_type, score FROM lte.claim_links")
            clinks = [{"source": r[0], "target": r[1], "type": r[2], "score": r[3]} for r in cur.fetchall()]

        nodes = docs + ents + claims
        edges = elinks + clinks
        return nodes, edges

    def save_graph_snapshot(self, run_id: str, payload: Dict[str, Any]) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.graph_snapshots(id, run_id, payload_json) VALUES(%s,%s,%s)",
                (str(uuid.uuid4()), run_id, json.dumps(payload))
            )
        self.conn.commit()
```

## `src/dashboard/unified_dashboard.py` (add endpoints)

```python
# ...existing imports...
from fastapi import APIRouter, HTTPException
from src.storage.pgvector_store import PgVectorStore
from src.analysis.linking_pipeline import build_graph_for_run

router = APIRouter(prefix="/api")

@router.post("/graph/{run_id}/build")
def api_graph_build(run_id: str):
    try:
        store = get_pg_store()  # your existing factory
        data = build_graph_for_run(run_id, store)
        return {"status": "ok", "data": {"run_id": run_id, **data}, "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "error": str(e)})

@router.get("/graph/{run_id}")
def api_graph_get(run_id: str):
    try:
        store = get_pg_store()
        nodes, edges = store.build_graph_snapshot(run_id)
        from src.analysis.rulego_bridge import evaluate_graph
        findings = evaluate_graph(run_id, nodes, edges)
        return {"status": "ok", "data": {"nodes": nodes, "edges": edges, "findings": findings}, "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail={"status": "error", "data": None, "error": str(e)})

@router.get("/claims/{run_id}")
def api_claims(run_id: str):
    # minimal placeholder: return claim rows with zero link counts
    store = get_pg_store()
    # implement a proper view later
    nodes, _ = store.build_graph_snapshot(run_id)
    claims = [n for n in nodes if n.get("type") == "claim"]
    for c in claims:
        c["link_count"] = 0
        c["label"] = "weak"
    return {"status": "ok", "data": claims, "error": None}

@router.get("/entities/{run_id}")
def api_entities(run_id: str):
    store = get_pg_store()
    nodes, _ = store.build_graph_snapshot(run_id)
    ents = [n for n in nodes if n.get("type") == "entity"]
    for e in ents:
        e["link_count"] = 0
    return {"status": "ok", "data": ents, "error": None}
```

## `scripts/p9_3_smoke.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
from httpx import Client
c = Client(timeout=30)
rid = "test-run"
# trigger build
resp = c.post("http://localhost:8050/api/graph/{}/build".format(rid))
j = resp.json()
assert j["status"] == "ok"
g = c.get("http://localhost:8050/api/graph/{}".format(rid)).json()
assert "nodes" in g["data"] and "edges" in g["data"]
print("OK graph:", len(g["data"]["nodes"]), "nodes,", len(g["data"]["edges"]), "edges")
PY
```

---

Want me to also add a super‑simple “Graph” tab on `/` that fetches `/api/graph/{run_id}` and renders a basic force layout, or keep UI changes for later?
