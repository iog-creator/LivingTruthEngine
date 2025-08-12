#!/usr/bin/env bash
set -euo pipefail
DASH_PORT="${DASH_PORT:-8050}"
echo "==> GET /api/health";        curl -sf "http://localhost:${DASH_PORT}/api/health"        | jq '.status'
echo "==> GET /api/health/full";   curl -sf "http://localhost:${DASH_PORT}/api/health/full"   | jq '.status'
echo "==> GET /api/runs";          curl -sf "http://localhost:${DASH_PORT}/api/runs"          | jq '.status'
RID=$(curl -sf "http://localhost:${DASH_PORT}/api/runs" | jq -r '.data[0].run_id // empty')
if [[ -n "$RID" ]]; then
  echo "==> POST /api/analyze/summary"; curl -sf -X POST "http://localhost:${DASH_PORT}/api/analyze/summary" -H 'Content-Type: application/json' -d "{\"run_id\":\"${RID}\"}" | jq '.status'
  echo "==> POST /api/analyze/claims";  curl -sf -X POST "http://localhost:${DASH_PORT}/api/analyze/claims"  -H 'Content-Type: application/json' -d "{\"run_id\":\"${RID}\"}" | jq '.status'
fi
echo "==> GET /api/tools";         curl -sf "http://localhost:${DASH_PORT}/api/tools"         | jq '.status'
echo "Proof-of-Life PASS"
