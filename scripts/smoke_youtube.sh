#!/usr/bin/env bash
set -euo pipefail

echo "==> health"
curl -fsS http://localhost:8050/api/health | jq -r .status

echo "==> full health"
curl -fsS http://localhost:8050/api/health/full | jq .

echo "==> tools"
curl -fsS http://localhost:8050/api/tools | jq '.status,.data.categories | length'

echo "==> runs (ok if empty list)"
curl -fsS http://localhost:8050/api/runs | jq '.status, (.data|length)'

echo "==> models (SSOT)"
curl -fsS http://localhost:8050/api/models | jq '.data.llm,.data.embedding'

echo "==> rulego health"
curl -fsS http://localhost:9127/health | jq .

echo "PASS"
