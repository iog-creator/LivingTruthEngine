---
phase: 8.3.2
title: Snapshot, Reconcile & Lock (Baseline = 8.3.1; Incorporates Revised System Spec)
owner: PM (Living Truth Engine)
status: Ready-to-run
created: 2025-08-11
applies: one-off
objectives:
  - Produce an auditable, reproducible snapshot of the *actual* running system.
  - Reconcile docs & code with the revised spec you provided (ports, services, tool counts, envelopes, no-fallbacks).
  - Lock invariants needed for Phase 9: stable health `service`, `{status,data?,error?}` envelopes, transcript call shape.
deliverables:
  - docs/snapshots/snapshot_<UTC>.md (generated evidence)
  - scripts/snapshot.sh (enhanced collector)
  - scripts/smoke_envelope.sh (envelope contract check)
  - Docs reconciled: Langflow→Langflow; port mappings; tool counts pinned to observed; health `service` labeled
  - (Optional) tests/test_transcript_api.py (API call-shape sanity)
success_criteria:
  - Snapshot shows green health, valid envelopes, tool categories visible, and service probes for Langflow/LM Studio/Neo4j/Postgres/Redis/Veritas API & Console.
  - Docs updated to reflect observed ports and tool counts; Langflow removed; transcript call fixed if needed.
  - Envelope smoke passes for /api/health, /api/health/full, /api/tools, /api/runs.
notes:
  - Treat your revised spec as the **desired** target; this phase pins docs to reality from the snapshot.
  - Keep edits surgical; no net-new features.
---

## 1) One-click snapshotter (enhanced)

Create **scripts/snapshot.sh** (chmod +x):

```bash
#!/usr/bin/env bash
set -euo pipefail

TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="docs/snapshots/snapshot_${TS}.md"
mkdir -p docs/snapshots

# Allow override via env
DASH_PORT="${DASH_PORT:-8050}"
LF_PORT="${LF_PORT:-7860}"
LM_PORT="${LM_PORT:-1234}"
NEO_HTTP="${NEO_HTTP:-7474}"
NEO_BOLT="${NEO_BOLT:-7687}"
PG_HOST_PORT="${PG_HOST_PORT:-5434}"
PG_CONT_PORT="${PG_CONT_PORT:-5432}"
REDIS_HOST_PORT="${REDIS_HOST_PORT:-6380}"
REDIS_CONT_PORT="${REDIS_CONT_PORT:-6379}"
VERITAS_API_PORT="${VERITAS_API_PORT:-8080}"
VERITAS_CONSOLE_PORT="${VERITAS_CONSOLE_PORT:-8501}"

w() { printf "%s\n" "$*" >> "$OUT"; }

w "# Living Truth Engine — System Snapshot (${TS} UTC)"
w ""
w "- Host: $(hostname)"
w "- Project: LivingTruthEngine"
w ""

w "## Containers"
w '```'
docker compose -f docker/docker-compose.yml ps || true
w '```'

w "## Dashboard Health"
w '```json'
curl -sf "http://localhost:${DASH_PORT}/api/health/full" | jq . || echo '{"status":"fail","error":"dashboard unreachable"}'
w '```'

w "## MCP Tools (categories + counts)"
w '```bash'
w "curl -s http://localhost:${DASH_PORT}/api/tools | jq '.data.categories | keys, map(.), length'"
w '```'
w '```json'
curl -sf "http://localhost:${DASH_PORT}/api/tools" | jq '.data.categories | keys, map(.), length' || echo '{"error":"unreachable"}'
w '```'

w "## Analyze API sanity (last run if present)"
RID=$(curl -sf "http://localhost:${DASH_PORT}/api/runs" | jq -r '.data[0].run_id // empty' || true)
if [[ -n "$RID" ]]; then
  w "- run_id: \`${RID}\`"
  for ep in summary claims; do
    w "### /api/analyze/${ep}"
    w '```json'
    curl -sf -X POST "http://localhost:${DASH_PORT}/api/analyze/${ep}" \
      -H 'Content-Type: application/json' -d "{\"run_id\":\"${RID}\"}" | jq . || echo '{"error":"fail"}'
    w '```'
  done
else
  w "_No runs found; skipping analyze endpoints._"
fi

w "## Envelope proofs (No Fallbacks contract)"
for ep in /api/health /api/health/full /api/tools /api/runs; do
  w "### GET $ep"
  w '```json'
  curl -sf "http://localhost:${DASH_PORT}${ep}" | jq '{status, has_data: has("data"), has_error: has("error")}' \
    || echo '{"status":"fail","has_data":false,"has_error":true}'
  w '```'
done

w "## Service Probes (from your spec)"
# Langflow
w "### Langflow ${LF_PORT}"; w '```'; curl -sf "http://localhost:${LF_PORT}/health" || echo "unreachable"; w '```'
# LM Studio
w "### LM Studio ${LM_PORT}"; w '```'; curl -sf "http://localhost:${LM_PORT}/v1/models" || echo "unreachable"; w '```'
# Neo4j (HTTP)
w "### Neo4j ${NEO_HTTP} (HTTP)"; w '```'; curl -sf "http://localhost:${NEO_HTTP}/" | head -n 3 || echo "unreachable"; w '```'
# Postgres (TCP check)
w "### Postgres ${PG_HOST_PORT}->${PG_CONT_PORT} (TCP)"; w '```'; (echo > /dev/tcp/localhost/${PG_HOST_PORT}) >/dev/null 2>&1 && echo "open" || echo "closed"; w '```'
# Redis (TCP check)
w "### Redis ${REDIS_HOST_PORT}->${REDIS_CONT_PORT} (TCP)"; w '```'; (echo > /dev/tcp/localhost/${REDIS_HOST_PORT}) >/dev/null 2>&1 && echo "open" || echo "closed"; w '```'
# Veritas API / Console (if present)
w "### Veritas API ${VERITAS_API_PORT}"; w '```'; curl -sf "http://localhost:${VERITAS_API_PORT}/health" || echo "unreachable"; w '```'
w "### Veritas Console ${VERITAS_CONSOLE_PORT}"; w '```'; curl -sf "http://localhost:${VERITAS_CONSOLE_PORT}/" | head -n 3 || echo "unreachable"; w '```'

w "## Dashboard code hash vs container (prove rebuild)"
w '```bash'
w "sha256sum src/dashboard/unified_dashboard.py || true"
sha256sum src/dashboard/unified_dashboard.py 2>/dev/null || true
DASH_CONT=$(docker ps --format '{{.Names}}' | grep -E 'dashboard|dash' | head -n1 || true)
if [[ -n "${DASH_CONT}" ]]; then
  w "# container hash"
  docker exec -i "$DASH_CONT" /bin/sh -lc 'sha256sum src/dashboard/unified_dashboard.py || true'
else
  w "<dashboard container not found>"
fi
w '```'

w "## Compose ports (scan)"
w '```'
sed -n '1,240p' docker/docker-compose.yml | sed -n '/ports:/,/environment:/p' || true
w '```'

w "## Langflow remnants check"
w '```'
git grep -n -i Langflow || true
w '```'

w "## YouTubeTranscript API call shape (static check)"
w '```'
grep -n "YouTubeTranscriptApi" -n src/ingestion_general/adapters/youtube_adapter.py || true
w '```'

echo "Wrote $OUT"
```

## 2) Envelope smoke

Create **scripts/smoke_envelope.sh** (chmod +x):

```bash
#!/usr/bin/env bash
set -euo pipefail
DASH_PORT="${DASH_PORT:-8050}"

check() {
  local ep="$1"
  echo "==> $ep"
  curl -sf "http://localhost:${DASH_PORT}${ep}" \
    | jq -e 'has("status") and (has("data") or has("error"))' >/dev/null
}

check /api/health
check /api/health/full
check /api/tools
check /api/runs
echo "Envelope OK"
```

## 3) Reconcile (surgical edits)

* **Health `service` string** → set exactly to `"unified_dashboard"` across code & tests (what the runtime already returns).&#x20;
* **Transcript call** → use `YouTubeTranscriptApi.get_transcript(video_id)` (class method).&#x20;
* **Langflow→Langflow** → purge/rename in docs/config.&#x20;
* **Ports normalization** → docs reflect compose: Postgres **5434→5432**, Redis **6380→6379**.&#x20;
* **Tool counts in docs** → snapshot + `config/tool_registry.json` decide canonical numbers and we pin them (no more 63 vs 99 confusion).&#x20;

## 4) Optional tiny test (only if you run pytest)

Create **tests/test_transcript_api.py**:

```python
import pytest
def test_youtube_transcript_api_call_shape():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception:
        pytest.skip("youtube_transcript_api not installed")
    assert hasattr(YouTubeTranscriptApi, "get_transcript")
```

## 5) Operator runbook (Cursor)

1. Bring up services:

```
docker compose -f docker/docker-compose.yml up -d --build
```

2. Generate snapshot:

```
./scripts/snapshot.sh
```

3. Envelope check:

```
./scripts/smoke_envelope.sh
```

4. Make the surgical edits (service label, transcript call, Langflow purge, port docs, tool counts).
5. (Optional) Re-run snapshot to capture the reconciled state.

## 6) Acceptance checklist

* [ ] Snapshot file exists and includes: green health/full, tools categories summary, service probes, envelope proofs
* [ ] Docs contain **no** "Langflow" mentions
* [ ] Docs show compose host-port mappings (5434→5432, 6380→6379)
* [ ] Docs list tool counts that match snapshot
* [ ] Transcript API call shape corrected (if needed)
* [ ] Envelope smoke exits 0
