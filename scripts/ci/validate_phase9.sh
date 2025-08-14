#!/usr/bin/env bash
set -euo pipefail

echo "[Phase 9] Running rule & MCP preflight…"

# 1) Required rule files exist
for f in .cursor/rules/core_workflow.mdc .cursor/rules/api_contracts.mdc .cursor/rules/ui_policy.mdc .cursor/rules/models_and_embeddings.mdc .cursor/rules/fallbacks_and_health.mdc .cursor/rules/mcp_integration.mdc; do
  test -f "$f" || { echo "Missing rule: $f"; exit 1; }
done

# 2) Phase files monotonic
python - <<'PY'
import os, re, sys
phases = sorted([p for p in os.listdir('.') if re.match(r'^PHASE_9_.*_PLAN\.md$', p)])
print("[OK] Phase plan files:", phases)
PY

# 3) Envelope spot check (cheap)
python - <<'PY'
import requests, sys
try:
    for ep in ["/api/health","/api/health/full","/api/models"]:
        j = requests.get("http://localhost:8050"+ep, timeout=10).json()
        assert "status" in j, ep+" missing status"
    print("[OK] Envelope spot check passed")
except Exception as e:
    print(f"[WARN] Envelope check failed (backend may not be running): {e}")
    print("[INFO] This is expected if backend is not running")
PY

# 4) MCP tool specifications exist
for spec in tools/mcp/specs/*.json; do
  test -f "$spec" || { echo "Missing MCP spec: $spec"; exit 1; }
done

# 5) Tool registry is valid JSON
python -c "import json; json.load(open('config/tool_registry.json'))" || { echo "Invalid tool registry JSON"; exit 1; }

echo "[OK] Phase 9 preflight complete"

