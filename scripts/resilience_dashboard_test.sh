#!/bin/bash
# Resilience Dashboard Test Script
# Tests the Phase 9.5.7 resilience dashboard API endpoints

set -e

echo "🧪 Testing Resilience Dashboard API endpoints..."

# Test resilience score endpoint
echo "Testing /api/resilience/score..."
curl -s http://localhost:8050/api/resilience/score | jq '.status' | grep -q "ok" || {
    echo "❌ Resilience score endpoint failed"
    exit 1
}

# Test chaos endpoint
echo "Testing /api/resilience/chaos..."
curl -s http://localhost:8050/api/resilience/chaos | jq '.status' | grep -q "ok" || {
    echo "❌ Chaos endpoint failed"
    exit 1
}

# Test anomalies endpoint
echo "Testing /api/resilience/anomalies..."
curl -s http://localhost:8050/api/resilience/anomalies | jq '.status' | grep -q "ok" || {
    echo "❌ Anomalies endpoint failed"
    exit 1
}

# Test resilience score threshold (should be >= 80%)
SCORE=$(curl -s http://localhost:8050/api/resilience/score | jq '.data.score')
if (( $(echo "$SCORE >= 80" | bc -l) )); then
    echo "✅ Resilience score: $SCORE (passes threshold)"
else
    echo "❌ Resilience score: $SCORE (below threshold of 80)"
    exit 1
fi

echo "✅ All resilience dashboard tests passed!"
