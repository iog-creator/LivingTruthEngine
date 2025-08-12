#!/usr/bin/env bash
set -euo pipefail

echo "==> docker compose up -d"
docker compose -f docker/docker-compose.yml up -d

echo "==> wait for dashboard :8050"
for i in {1..40}; do
  if curl -fsS http://localhost:8050/api/health >/dev/null; then
    echo "dashboard ok"
    break
  fi
  sleep 1
done

echo "==> wait for aux services (optional)"
for svc in 9126 9127 9128; do
  curl -fsS "http://localhost:${svc}/health" >/dev/null || true
done

echo "READY"

