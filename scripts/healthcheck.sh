#!/usr/bin/env bash
set -Eeuo pipefail
CURL="curl -sf"
fail=0
check(){ name="$1"; url="$2"; if $CURL "$url" >/dev/null; then echo "✓ $name: $url"; else echo "❌ $name: $url"; fail=1; fi; }
check "dashboard" "http://127.0.0.1:8050/api/health"
check "langflow"  "http://127.0.0.1:7860/health"
check "devdocs"   "http://127.0.0.1:9126/health"
check "rulego"    "http://127.0.0.1:9127/health"
check "mcp-solver" "http://127.0.0.1:9128/health"
exit $fail
