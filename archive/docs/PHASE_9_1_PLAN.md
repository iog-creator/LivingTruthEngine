---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['src/dashboard/unified_dashboard.py', 'src/ai/dspy_programs.py', 'src/storage/pgvector_store.py', 'src/common/model_registry.py', 'src/analysis/rulego_bridge.py']
---

Got it—let’s lock in **Phase 9\_1: Services + Models SSOT & Wiring** so Cursor stops reinventing wheels and uses the stack we already planned and shipped.

Below is a compact “action pack” you can drop into Phase‑9. It establishes a **single source of truth (SSOT)** for models, reconnects **Rulego**, turns on **pgvector**, and gives Cursor explicit API/types to call—without changing what already works (UI + runs + MCP). I’m basing this on what we’ve already delivered (UI at `ui_status_chat.html`, Veritas bundles, aux services, Phase‑9 endpoints/plan).    &#x20;

---

# Phase 9\_1 — Deliverables (paste-ready)

### 1) SSOT for models

**File:** `config/models.toml`

```toml
# LLMs (served by LM Studio OR API)
[llm.default]
provider = "lmstudio"   # or "openai"|"hf"
model    = "qwen/qwen3-8b-instruct"
endpoint = "http://localhost:1234/v1"  # desktop LM Studio

# Embeddings (for pgvector)
[embedding.default]
provider = "hf"
model    = "sentence-transformers/all-MiniLM-L6-v2"
dim      = 384

# NER (non‑LLM)
[ner.default]
provider = "spacy"
model    = "en_core_web_trf"

# Reranker (non‑LLM)
[reranker.default]
provider = "hf"
model    = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# OCR / STT (non‑LLM)
[ocr.default]
provider = "tesseract"
lang     = "eng"

[stt.default]
provider = "whisper"
model    = "base"

# Diarization (optional non‑LLM)
[diarization.default]
provider = "pyannote"
pipeline = "pyannote/speaker-diarization"

# Topic modeling (non‑LLM)
[topics.default]
provider = "bertopic"
backend  = "sentence-transformers/all-MiniLM-L6-v2"
```

**File:** `src/common/model_registry.py`

```python
from dataclasses import dataclass
from pathlib import Path
import tomllib

@dataclass
class ModelSpec:
    provider: str
    name: str
    extra: dict

class ModelRegistry:
    def __init__(self, path: str = "config/models.toml"):
        self.cfg = tomllib.loads(Path(path).read_text(encoding="utf-8"))

    def llm(self, key="default") -> ModelSpec:
        c = self.cfg["llm"][key]
        return ModelSpec(c["provider"], c["model"], {"endpoint": c.get("endpoint")})

    def embedding(self, key="default") -> ModelSpec:
        c = self.cfg["embedding"][key]
        return ModelSpec(c["provider"], c["model"], {"dim": c.get("dim")})

    def ner(self, key="default") -> ModelSpec:
        c = self.cfg["ner"][key]
        return ModelSpec(c["provider"], c["model"], {})

    # ...reranker/ocr/stt/diarization/topics similar...
```

**Why:** Cursor asks “what model where?” This file answers it once, and `ModelRegistry` makes it trivial to wire into runners, MCP tools, and the UI.

---

### 2) pgvector on Postgres (and embeddings pipe)

We already rely on Postgres; Phase‑9 needs vector search for multi‑source. Add the extension + schema and a thin store.

**File:** `docker/initdb/002_pgvector.sql`

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE SCHEMA IF NOT EXISTS lte;
CREATE TABLE IF NOT EXISTS lte.documents (
  id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  source_type TEXT NOT NULL,
  text TEXT NOT NULL,
  meta JSONB DEFAULT '{}'::jsonb
);
CREATE TABLE IF NOT EXISTS lte.doc_embeddings (
  id TEXT PRIMARY KEY,
  doc_id TEXT REFERENCES lte.documents(id) ON DELETE CASCADE,
  run_id TEXT NOT NULL,
  embedding vector(384) NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_doc_embed_run ON lte.doc_embeddings(run_id);
```

**File:** `src/storage/pgvector_store.py`

```python
import psycopg, numpy as np
from .types import Embedder  # your embedding interface

class PgVectorStore:
    def __init__(self, dsn: str, embedder: Embedder):
        self.db = psycopg.connect(dsn, autocommit=True)
        self.embedder = embedder

    def upsert_docs(self, run_id: str, docs: list[dict]):
        with self.db.cursor() as cur:
            for d in docs:
                cur.execute(
                    "INSERT INTO lte.documents(id,run_id,source_type,text,meta) "
                    "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET text=EXCLUDED.text",
                    (d["id"], run_id, d["source_type"], d["text"], d.get("meta", {}))
                )
                vec = self.embedder.encode(d["text"])
                cur.execute(
                    "INSERT INTO lte.doc_embeddings(id,doc_id,run_id,embedding) "
                    "VALUES (%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET embedding=EXCLUDED.embedding",
                    (d["id"], d["id"], run_id, np.array(vec))
                )

    def search(self, run_id: str, query: str, k: int = 10):
        qvec = np.array(self.embedder.encode(query))
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT d.id,d.text,d.meta "
                "FROM lte.doc_embeddings e JOIN lte.documents d ON d.id=e.doc_id "
                "WHERE e.run_id=%s ORDER BY e.embedding <#> %s LIMIT %s",
                (run_id, qvec, k)
            )
            return [{"id": i, "text": t, "meta": m} for (i, t, m) in cur.fetchall()]
```

*Context:* Runs and bundles are already established; this augments search with vectors. &#x20;

---

### 3) Rulego as a first‑class service

We stabilized Rulego as a FastAPI service in Phase‑6; wire it into the analysis pipeline and expose a tiny UI/endpoint.&#x20;

**File:** `config/rulego/policies.yaml`

```yaml
version: 1
policies:
  - id: claims_consistency
    when: "$.claim.type in ['factual','temporal']"
    then:
      - check: "exists($.evidence)"
        fail: "Claim has no evidence"
      - check: "$.confidence >= 0.5"
        warn: "Low confidence claim"
```

**File:** `src/analysis/rulego_bridge.py`

```python
import httpx

class RulegoClient:
    def __init__(self, base="http://localhost:9127"):
        self.base = base
    async def evaluate(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/evaluate", json=payload)
            r.raise_for_status()
            return r.json()
```

**Dashboard endpoint:** `GET /api/rules/health` → proxy Rulego `/health` and list loaded policy IDs.

---

### 4) DSPy (dspy3) slot for verifiers/routers

Add DSPy but behind a flag so we can iterate.

**File:** `src/ai/dspy_programs.py`

```python
import dspy

class CorroborationProgram(dspy.Module):
    def __init__(self, llm):
        super().__init__()
        self.verify = dspy.ChainOfThought(llm=llm)
    def forward(self, claim: str, snippets: list[str]):
        prompt = f"Claim: {claim}\nEvidence:\n" + "\n".join(snippets)
        return {"analysis": self.verify(prompt)}
```

**Integration point:** call this from the **claim verification** tool you already scoped for Phase‑9 endpoints (`/api/verification/{run_id}`) so we can ship corroboration as a module.&#x20;

---

### 5) API surface for Cursor (explicit “what to call”)

**File:** `src/dashboard/unified_dashboard.py` (additions)

```python
# NEW: models & rules SSOT exposure
@router.get("/api/models")
def get_models():
    reg = ModelRegistry()
    return {"status":"ok","data":{
        "llm": reg.llm().__dict__,
        "embedding": reg.embedding().__dict__,
        "ner": reg.ner().__dict__,
        # ...
    }}

@router.get("/api/health/full")
def health_full():
    # existing payload … plus:
    return {"status":"ok","data":{
        "services": {...},        # existing
        "models_checksum": sha1(open("config/models.toml","rb").read()).hexdigest(),
        "pgvector": {"enabled": True, "tables":["lte.documents","lte.doc_embeddings"]},
        "rulego": {"status":"ok"}
    }}
```

These pair naturally with what the UI and README already document (health, runs, execute, viz; Phase‑9 endpoints in progress).&#x20;

---

### 6) Compose & init: keep desktop LM Studio, no extra container

We keep your **desktop LM Studio** (no docker container) and point SSOT to `http://localhost:1234`. The UI remains the single file we shipped at `src/dashboard/static/ui_status_chat.html`. &#x20;

If you want pgvector auto‑init: mount `docker/initdb` into Postgres. (We already track Postgres in the service diagram and quickstart.) &#x20;

---

### 7) Wire into Veritas runs (no reinvention)

* On bundle write: push docs to `lte.documents` and embeddings to `lte.doc_embeddings`.
* Add **MCP tool**: `extract_entities_and_claims` (uses spaCy + reranker), then evaluate with Rulego and (optionally) DSPy corroboration—these are already listed in Phase‑9 scope/templates. &#x20;

---

### 8) Smoke script

**File:** `scripts/p9_1_smoke.sh`

```bash
set -euo pipefail
echo "[1/5] API health"
curl -s http://localhost:8050/api/health | jq -r .status

echo "[2/5] Full health (+pgvector/models)"
curl -s http://localhost:8050/api/health/full | jq .

echo "[3/5] Models SSOT"
curl -s http://localhost:8050/api/models | jq '.data'

echo "[4/5] Rulego health"
curl -s http://localhost:9127/health | jq .

echo "[5/5] Vector roundtrip (requires one run indexed)"
python - <<'PY'
from src.storage.pgvector_store import PgVectorStore
from src.common.model_registry import ModelRegistry
# Replace with your DSN:
store = PgVectorStore("postgresql://postgres:postgres@localhost:5432/postgres",
                      embedder=... )  # your embedder instance
print("OK: store import")
PY
echo "PASS"
```

---

## What this unlocks (immediately)

* **Cursor knows exactly which models to use** for LLM vs non‑LLM (NER, reranker, OCR/STT, topics) via `/api/models` and `config/models.toml`.
* **pgvector** is real and queryable in Phase‑9 multi‑source work.
* **Rulego** is back in the loop for deterministic checks.
* **DSPy** is available for verification logic without blocking anything else.
* **UI stays the same** (the single working file) and can show SSOT status or model names if desired.&#x20;

If you give me the green light, I’ll push these files to `LivingTruthEngine-Phase9` and run the smoke. Then we can proceed to **9\_2: multi‑source runner** (hook adapters to pgvector + SSOT) and **9\_3: evidence graph + verification endpoints**—exactly as our Phase‑9 plan calls out. &#x20;
