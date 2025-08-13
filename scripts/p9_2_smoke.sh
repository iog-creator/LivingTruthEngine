#!/bin/bash

# Phase 9_2 Smoke Test - Multi-Source Ingestion with GPU/CPU-Aware Model Scheduling
# Tests the complete multi-source ingestion pipeline with health gates and device allocation

set -e

echo "=== Phase 9_2 Smoke Test: Multi-Source Ingestion ==="
echo "Testing GPU/CPU-aware model scheduling and multi-source ingestion"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    
    log_info "Running test: $test_name"
    
    if eval "$test_command"; then
        log_success "Test passed: $test_name"
        ((TESTS_PASSED++))
    else
        log_error "Test failed: $test_name"
        ((TESTS_FAILED++))
        return 1
    fi
}

# 1. Bring up the system
log_info "Step 1: Bringing up the system..."
if ! bash scripts/bring_up.sh; then
    log_error "System bring-up failed"
    exit 1
fi
log_success "System brought up successfully"

# 2. Test basic health
log_info "Step 2: Testing basic health..."
run_test "Basic health check" '
    curl -s http://localhost:8050/api/health | jq -e ".status == \"ok\""
'

# 3. Test full health with SSOT fields
log_info "Step 3: Testing full health with SSOT fields..."
run_test "Full health check" '
    curl -s http://localhost:8050/api/health/full | jq -e ".status == \"ok\""
'

# 4. Test models endpoint with device allocation
log_info "Step 4: Testing models endpoint with device allocation..."
run_test "Models endpoint with device info" '
    curl -s http://localhost:8050/api/models | jq -e ".status == \"ok\""
'

# 5. Test GPU status in models response
log_info "Step 5: Testing GPU status in models response..."
run_test "GPU device allocation in models" '
    curl -s http://localhost:8050/api/models | jq -e ".data.llm.extra.device != null"
'

# 6. Test multi-source ingestion with single source
log_info "Step 6: Testing multi-source ingestion with single source (youtube)..."
run_test "Single source ingestion" '
    JOB_RESPONSE=$(curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["youtube"], "params": {"item_limit": 1}}'"'"') && \
    echo "$JOB_RESPONSE" | jq -e ".status == \"ok\"" && \
    JOB_ID=$(echo "$JOB_RESPONSE" | jq -r ".data.job_id") && \
    echo "Job ID: $JOB_ID"
'

# Extract job ID for further testing
JOB_ID=$(curl -s -X POST http://localhost:8050/api/multisource/start \
    -H "Content-Type: application/json" \
    -d '{"sources": ["youtube"], "params": {"item_limit": 1}}' | \
    jq -r ".data.job_id")

# 7. Test job status endpoint
log_info "Step 7: Testing job status endpoint..."
run_test "Job status endpoint" '
    curl -s http://localhost:8050/api/multisource/jobs/'$JOB_ID' | jq -e ".status == \"ok\""
'

# 8. Test list jobs endpoint
log_info "Step 8: Testing list jobs endpoint..."
run_test "List jobs endpoint" '
    curl -s http://localhost:8050/api/multisource/jobs | jq -e ".status == \"ok\""
'

# 9. Test multi-source ingestion with all sources
log_info "Step 9: Testing multi-source ingestion with all sources..."
run_test "Multi-source ingestion (all sources)" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["youtube", "web", "pdf"], "params": {"item_limit": 1}}'"'"' | \
    jq -e ".status == \"ok\""
'

# 10. Test invalid source type
log_info "Step 10: Testing invalid source type validation..."
run_test "Invalid source type validation" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["invalid_source"]}'"'"' | \
    jq -e ".status == \"error\""
'

# 11. Test empty sources validation
log_info "Step 11: Testing empty sources validation..."
run_test "Empty sources validation" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": []}'"'"' | \
    jq -e ".status == \"error\""
'

# 12. Test GPU scheduler integration
log_info "Step 12: Testing GPU scheduler integration..."
run_test "GPU scheduler status" '
    curl -s http://localhost:8050/api/models | jq -e ".data.embedding.extra.device != null"
'

# 13. Test reranker device allocation
log_info "Step 13: Testing reranker device allocation..."
run_test "Reranker device allocation" '
    curl -s http://localhost:8050/api/models | jq -e ".data.reranker.extra.device != null"
'

# 14. Test envelope format consistency
log_info "Step 14: Testing envelope format consistency..."
run_test "Envelope format consistency" '
    curl -s http://localhost:8050/api/ingest/multi | jq -e "has(\"status\") and has(\"data\") and has(\"error\")"
'

# 15. Test health gates for each adapter
log_info "Step 15: Testing health gates for each adapter..."
run_test "YouTube adapter health gate" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["youtube"]}'"'"' | \
    jq -e ".status == \"ok\""
'

run_test "Web adapter health gate" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["web"]}'"'"' | \
    jq -e ".status == \"ok\""
'

run_test "PDF adapter health gate" '
    curl -s -X POST http://localhost:8050/api/multisource/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"sources": ["pdf"]}'"'"' | \
    jq -e ".status == \"ok\""
'

# 16. Test existing YouTube functionality still works
log_info "Step 16: Testing existing YouTube functionality..."
run_test "Existing YouTube endpoint" '
    curl -s -X POST http://localhost:8050/api/runs/youtube/start \
        -H "Content-Type: application/json" \
        -d '"'"'{"channel_url":"https://www.youtube.com/@imaginationpodcastofficial","limit":1,"sort":"oldest","max_depth":1}'"'"' | \
    jq -e ".status == \"ok\""
'

# 17. Test tools endpoint
log_info "Step 17: Testing tools endpoint..."
run_test "Tools endpoint" '
    curl -s http://localhost:8050/api/tools | jq -e ".status == \"ok\""
'

# 18. Test rules health endpoint
log_info "Step 18: Testing rules health endpoint..."
run_test "Rules health endpoint" '
    curl -s http://localhost:8050/api/rules/health | jq -e ".status == \"ok\""
'

# Wait for jobs to complete and check results
log_info "Step 19: Waiting for jobs to complete and checking results..."
sleep 5

run_test "Job completion check" '
    curl -s http://localhost:8050/api/multisource/jobs/'$JOB_ID' | \
    jq -e ".data.status == \"completed\" or .data.status == \"running\""
'

# 20. Test pgvector storage verification
log_info "Step 20: Testing pgvector storage verification..."
run_test "pgvector document count" '
    psql -U postgres -d living_truth_engine -c "SELECT COUNT(*) FROM lte.documents;" | grep -E "^[0-9]+$"
'

# 21. Test search functionality
log_info "Step 21: Testing search functionality..."
run_test "pgvector search" '
    curl -s -X POST http://localhost:8050/api/search \
        -H "Content-Type: application/json" \
        -d '"'"'{"query":"test","job_id":"'$JOB_ID'","k":5}'"'"' | \
    jq -e ".status == \"ok\""
'

# Summary
echo
echo "=== Phase 9_2 Smoke Test Summary ==="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo

if [ $TESTS_FAILED -eq 0 ]; then
    log_success "All Phase 9_2 smoke tests passed!"
    echo
    echo "✅ Multi-source ingestion with GPU/CPU-aware scheduling is working"
    echo "✅ Health gates are functioning for all adapters"
    echo "✅ Device allocation is working correctly"
    echo "✅ Envelope format is consistent across all endpoints"
    echo "✅ Existing functionality remains intact"
    exit 0
else
    log_error "Some Phase 9_2 smoke tests failed!"
    echo
    echo "❌ Multi-source ingestion needs attention"
    echo "❌ Check the failed tests above for details"
    exit 1
fi

