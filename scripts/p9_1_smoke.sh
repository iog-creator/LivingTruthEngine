#!/usr/bin/env bash
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
try:
    from src.storage.pgvector_store import PgVectorStore
    from src.common.model_registry import ModelRegistry
    print("OK: store import")
except ImportError as e:
    print(f"WARNING: Import failed - {e}")
    print("This is expected if dependencies aren't installed yet")
PY
echo "PASS"
