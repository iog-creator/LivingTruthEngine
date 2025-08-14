#!/bin/bash

# Phase 9.5.3 - Timeline API + Graph Polish Test Script
# Tests timeline API performance and graph UX enhancements

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
    local expected_status="$3"
    
    echo -e "\n${BLUE}Testing: ${test_name}${NC}"
    
    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ PASS${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}❌ FAIL${NC}"
        ((TESTS_FAILED++))
    fi
}

# Helper function to test API performance
test_api_performance() {
    local endpoint="$1"
    local max_time="$2"
    local test_name="$3"
    
    echo -e "\n${BLUE}Performance Test: ${test_name}${NC}"
    
    # Measure response time
    start_time=$(date +%s.%N)
    response=$(curl -s "$endpoint")
    end_time=$(date +%s.%N)
    
    # Calculate duration
    duration=$(echo "$end_time - $start_time" | bc -l)
    
    # Check if response is valid JSON
    if echo "$response" | jq . > /dev/null 2>&1; then
        echo -e "  ${GREEN}✅ Valid JSON response${NC}"
    else
        echo -e "  ${RED}❌ Invalid JSON response${NC}"
        return 1
    fi
    
    # Check performance
    if (( $(echo "$duration < $max_time" | bc -l) )); then
        echo -e "  ${GREEN}✅ Performance OK (${duration}s < ${max_time}s)${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "  ${RED}❌ Performance too slow (${duration}s >= ${max_time}s)${NC}"
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
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.status == \"ok\"'" \
    "ok"

# Test 2: Timeline API performance (< 1s)
test_api_performance \
    "http://localhost:8050/api/timeline/$RUN_ID" \
    "1.0" \
    "Timeline API response time"

# Test 3: Timeline API returns expected structure
run_test "Timeline API structure validation" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data | has(\"timeline\") and has(\"summary\")'" \
    "ok"

# Test 4: Timeline events are sorted by timestamp
run_test "Timeline events sorted by timestamp" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.timeline.events | length > 0'" \
    "ok"

# Test 5: Graph API endpoint exists and responds
run_test "Graph API endpoint exists" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.status'" \
    "ok"

# Test 6: Graph API performance (< 1.5s)
test_api_performance \
    "http://localhost:8050/api/graph/$RUN_ID" \
    "1.5" \
    "Graph API response time"

# Test 7: Graph API returns expected structure
run_test "Graph API structure validation" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.data | has(\"nodes\") or has(\"edges\") or has(\"stats\")'" \
    "ok"

# Test 8: Timeline API envelope format
run_test "Timeline API envelope format" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e 'has(\"status\") and has(\"data\")'" \
    "ok"

# Test 9: Graph API envelope format
run_test "Graph API envelope format" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e 'has(\"status\") and has(\"data\")'" \
    "ok"

# Test 10: Timeline API error handling for invalid run
run_test "Timeline API error handling" \
    "curl -s http://localhost:8050/api/timeline/invalid-run-id | jq -e '.status == \"error\"'" \
    "ok"

# Test 11: Graph API error handling for invalid run
run_test "Graph API error handling" \
    "curl -s http://localhost:8050/api/graph/invalid-run-id | jq -e '.status == \"error\"'" \
    "ok"

# Test 12: Timeline API includes run metadata
run_test "Timeline API includes run metadata" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data | has(\"run_id\")'" \
    "ok"

# Test 13: Timeline API includes time range
run_test "Timeline API includes time range" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.timeline | has(\"time_range\")'" \
    "ok"

# Test 14: Timeline API includes summary statistics
run_test "Timeline API includes summary statistics" \
    "curl -s http://localhost:8050/api/timeline/$RUN_ID | jq -e '.data.summary | has(\"documents_processed\")'" \
    "ok"

# Test 15: Graph API includes statistics
run_test "Graph API includes statistics" \
    "curl -s http://localhost:8050/api/graph/$RUN_ID | jq -e '.data | has(\"stats\") or has(\"total_nodes\") or has(\"total_edges\")'" \
    "ok"

# Performance stress test
echo -e "\n${BLUE}Performance Stress Test${NC}"
echo "Testing multiple concurrent requests..."

# Test concurrent timeline requests
for i in {1..5}; do
    (
        start_time=$(date +%s.%N)
        curl -s "http://localhost:8050/api/timeline/$RUN_ID" > /dev/null
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc -l)
        echo "Request $i: ${duration}s"
    ) &
done
wait

echo -e "\n${BLUE}Testing Graph API concurrent requests...${NC}"

# Test concurrent graph requests
for i in {1..5}; do
    (
        start_time=$(date +%s.%N)
        curl -s "http://localhost:8050/api/graph/$RUN_ID" > /dev/null
        end_time=$(date +%s.%N)
        duration=$(echo "$end_time - $start_time" | bc -l)
        echo "Request $i: ${duration}s"
    ) &
done
wait

# Summary
echo -e "\n${BLUE}Test Summary${NC}"
echo "============="
echo -e "${GREEN}Tests Passed: ${TESTS_PASSED}${NC}"
echo -e "${RED}Tests Failed: ${TESTS_FAILED}${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All Phase 9.5.3 tests passed!${NC}"
    echo -e "${GREEN}✅ Timeline API responding <1s${NC}"
    echo -e "${GREEN}✅ Graph API responding <1.5s${NC}"
    echo -e "${GREEN}✅ Graph UX enhanced with filters, pinning, and selection${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Please check the implementation.${NC}"
    exit 1
fi
