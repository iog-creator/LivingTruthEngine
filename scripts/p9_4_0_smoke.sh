#!/usr/bin/env bash
set -euo pipefail

echo "== Phase 9.4.0 Smoke =="

# Check if services are running
echo "Checking if services are running..."

# Check if API is accessible directly
if curl -s http://localhost:8050/api/health > /dev/null 2>&1; then
    echo "✅ API service (port 8050) is running"
else
    echo "❌ API service (port 8050) is not accessible"
    exit 1
fi

# Check if UI is accessible directly
if curl -s http://localhost:4173 > /dev/null 2>&1; then
    echo "✅ UI service (port 4173) is running"
else
    echo "❌ UI service (port 4173) is not accessible"
    exit 1
fi

# Check if proxy is running on port 80
if curl -s http://localhost:80 > /dev/null 2>&1; then
    echo "✅ Proxy service (port 80) is running"
else
    echo "❌ Proxy service (port 80) is not accessible"
    exit 1
fi

# 1) Root serves UI shell (HTML)
echo "Testing root route serves UI shell..."
if curl -sS http://localhost/ | grep -qi "Living Truth Engine"; then
    echo "✅ UI shell OK"
else
    echo "❌ UI shell not found"
    exit 1
fi

# 2) API routes still reachable via same origin
echo "Testing API routes via proxy..."
for ep in /api/health /api/health/full /api/models; do
    echo "Testing $ep..."
    status=$(curl -sS "http://localhost${ep}" | jq -r .status 2>/dev/null || echo "error")
    if [ "$status" = "ok" ]; then
        echo "✅ API $ep OK"
    else
        echo "❌ API $ep FAILED (status: $status)"
        exit 1
    fi
done

echo "All good."
