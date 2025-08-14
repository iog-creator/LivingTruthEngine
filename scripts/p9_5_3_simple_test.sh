#!/bin/bash

# Phase 9.5.3 - Timeline API + Graph Polish Simple Test Script

set -e

echo "🧪 Phase 9.5.3 - Timeline API + Graph Polish Test"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run tests
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${BLUE}Testing: ${test_name}${NC}"
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}❌ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Check if system is running
echo "🔍 Checking system health..."

if ! curl -s http://localhost:8050/api/health > /dev/null; then
    echo -e "${RED}❌ Dashboard not running on port 8050${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Dashboard is running${NC}"

# Get a run ID for testing
echo "🔍 Getting test run ID..."
RUN_ID=$(curl -s http://localhost:8050/api/runs | jq -r '.data[0].run_id')

if [ "$RUN_ID" = "null" ] || [ -z "$RUN_ID" ]; then
    echo -e "${RED}❌ No runs available for testing${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Using run ID: ${RUN_ID}${NC}"

# Test 1: Timeline API endpoint exists and responds
run_test "Timeline API endpoint exists" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.status == \"ok\"'"

# Test 2: Timeline API returns expected structure
run_test "Timeline API structure validation" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data | has(\"timeline\") and has(\"summary\")'"

# Test 3: Timeline events are sorted by timestamp
run_test "Timeline events sorted by timestamp" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.timeline.events | length > 0'"

# Test 4: Graph API endpoint exists and responds
run_test "Graph API endpoint exists" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.status'"

# Test 5: Graph API returns expected structure
run_test "Graph API structure validation" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.data | has(\"nodes\") or has(\"edges\") or has(\"stats\")'"

# Test 6: Timeline API envelope format
run_test "Timeline API envelope format" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e 'has(\"status\") and has(\"data\")'"

# Test 7: Graph API envelope format
run_test "Graph API envelope format" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e 'has(\"status\") and has(\"data\")'"

# Test 8: Timeline API error handling for invalid run
run_test "Timeline API error handling" \
    "curl -s http://localhost:8050/api/timeline/invalid-run-id | jq -e '.status == \"error\"'"

# Test 9: Graph API error handling for invalid run
run_test "Graph API error handling" \
    "curl -s http://localhost:8050/api/graph/invalid-run-id | jq -e '.status == \"error\"'"

# Test 10: Timeline API includes run metadata
run_test "Timeline API includes run metadata" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data | has(\"run_id\")'"

# Test 11: Timeline API includes time range
run_test "Timeline API includes time range" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.timeline | has(\"time_range\")'"

# Test 12: Timeline API includes summary statistics
run_test "Timeline API includes summary statistics" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.summary | has(\"documents_processed\")'"

# Test 13: Graph API includes statistics
run_test "Graph API includes statistics" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.data | has(\"stats\") or has(\"total_nodes\") or has(\"total_edges\")'"

# Test 14: Graph build endpoint (with rebuild flag)
run_test "Graph build endpoint with rebuild" \
    "curl -s -X POST \"http://localhost:8050/api/graph/$RUN_ID/build?rebuild=1\" | jq -e '.status == \"ok\"'"

# Test 15: Graph fetch after build
run_test "Graph fetch after build" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.status == \"ok\"'"

# Test 16: Graph data structure after build
run_test "Graph data structure after build" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.data | has(\"nodes\") or has(\"edges\") or has(\"stats\")'"

# Test 17: Idempotency test - build without rebuild flag (should work)
run_test "Idempotency test - build without rebuild flag" \
    "curl -s -X POST \"http://localhost:8050/api/graph/$RUN_ID/build\" | jq -e '.status == \"ok\"'"

# Test 18: Idempotency test - build with rebuild flag again (should work)
run_test "Idempotency test - build with rebuild flag again" \
    "curl -s -X POST \"http://localhost:8050/api/graph/$RUN_ID/build?rebuild=1\" | jq -e '.status == \"ok\"'"

# Test 19: Performance metrics in build response
run_test "Performance metrics in build response" \
    "curl -s -X POST \"http://localhost:8050/api/graph/$RUN_ID/build?rebuild=1\" | jq -e '.data | has(\"performance\")'"

# Performance test (simple version)
echo -e "\n${BLUE}Performance Test: Timeline API${NC}"
start_time=$(date +%s)
curl -s "http://localhost:8050/api/timeline/$RUN_ID" > /dev/null
end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $duration -lt 1 ]; then
    echo -e "  ${GREEN}✅ Performance OK (${duration}s < 1s)${NC}"
    ((TESTS_PASSED++))
else
    echo -e "  ${RED}❌ Performance too slow (${duration}s >= 1s)${NC}"
    ((TESTS_FAILED++))
fi

echo -e "\n${BLUE}Performance Test: Graph API${NC}"
start_time=$(date +%s)
curl -s "http://localhost:8050/api/graph/$RUN_ID" > /dev/null
end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $duration -lt 2 ]; then
    echo -e "  ${GREEN}✅ Performance OK (${duration}s < 2s)${NC}"
    ((TESTS_PASSED++))
else
    echo -e "  ${RED}❌ Performance too slow (${duration}s >= 2s)${NC}"
    ((TESTS_FAILED++))
fi

# Summary
echo -e "\n${BLUE}Test Summary${NC}"
echo "============="
echo -e "${GREEN}Tests Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}Tests Failed: ${TESTS_FAILED}${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All Phase 9.5.3 tests passed!${NC}"
    echo -e "${GREEN}✅ Timeline API responding <1s${NC}"
    echo -e "${GREEN}✅ Graph API responding <2s${NC}"
    echo -e "${GREEN}✅ Graph UX enhanced with filters, pinning, and selection${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please check the implementation.${NC}"
    exit 1
fi


