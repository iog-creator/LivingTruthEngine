#!/usr/bin/env bash
set -euo pipefail
DASH_PORT="${DASH_PORT:-8050}"

check() {
  local ep="$1"
  echo "==> $ep"
  response=$(curl -sf "http://localhost:${DASH_PORT}${ep}")
  if [[ $? -ne 0 ]]; then
    echo "❌ Failed to reach $ep"
    exit 1
  fi
  
  # Check for status field
  if ! echo "$response" | jq -e 'has("status")' >/dev/null; then
    echo "❌ $ep missing 'status' field"
    exit 1
  fi
  
  # All endpoints now use envelope format: status + data + error
  if ! echo "$response" | jq -e 'has("data")' >/dev/null; then
    echo "❌ $ep missing 'data' field"
    exit 1
  fi
  
  # Health endpoints should have service field in data
  if [[ "$ep" == "/api/health" || "$ep" == "/api/health/full" ]]; then
    if ! echo "$response" | jq -e '.data | has("service")' >/dev/null; then
      echo "❌ $ep missing 'service' field in data"
      exit 1
    fi
  fi
}

check /api/health
check /api/health/full
check /api/tools
check /api/runs
echo "Envelope OK"
