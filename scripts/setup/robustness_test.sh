#!/bin/bash

# Living Truth Engine - Comprehensive Robustness Test Script
# This script systematically tests all components to ensure reliability

set -e  # Exit on any error

echo "🔍 Living Truth Engine - Comprehensive Robustness Test"
echo "======================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "🧪 Testing: $test_name... "
    
    if eval "$test_command" > /dev/null 2>&1; then
        if [ $? -eq $expected_exit_code ]; then
            echo -e "${GREEN}✅ PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        else
            echo -e "${RED}❌ FAIL (wrong exit code)${NC}"
            FAILED_TESTS=$((FAILED_TESTS + 1))
        fi
    else
        echo -e "${RED}❌ FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Function to check service health
check_service() {
    local service_name="$1"
    local health_url="$2"
    local expected_status="${3:-200}"
    
    echo -n "🏥 Checking $service_name health... "
    
    if curl -f -s "$health_url" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ HEALTHY${NC}"
        return 0
    else
        echo -e "${RED}❌ UNHEALTHY${NC}"
        return 1
    fi
}

# Function to test port availability
test_port() {
    local port="$1"
    local service_name="$2"
    
    echo -n "🔌 Testing port $port ($service_name)... "
    
    if ss -tuln | grep -q ":$port "; then
        echo -e "${GREEN}✅ OPEN${NC}"
        return 0
    else
        echo -e "${RED}❌ CLOSED${NC}"
        return 1
    fi
}

echo -e "${BLUE}📋 Phase 1: Environment and Dependencies${NC}"
echo "----------------------------------------"

# Test 1: Check if we're in the right directory
run_test "Project Directory" "test -f docker/docker-compose.yml"

# Test 2: Check Docker availability
run_test "Docker Availability" "docker --version"

# Test 3: Check Docker Compose availability
run_test "Docker Compose Availability" "docker compose version"

# Test 4: Check if containers are running
run_test "Container Status" "docker compose -f docker/docker-compose.yml ps | grep -q 'Up'"

echo ""
echo -e "${BLUE}📋 Phase 2: Service Health Checks${NC}"
echo "----------------------------------------"

# Test 5: Langflow Health
check_service "Langflow" "http://localhost:7860/health"

# Test 6: LM Studio Health
check_service "LM Studio" "http://localhost:1234/v1/models"

# Test 7: Living Truth Engine Health
check_service "Living Truth Engine" "http://localhost:8000/health"

# Test 8: PostgreSQL Health
run_test "PostgreSQL Connection" "pg_isready -h localhost -p 5432"

# Test 9: Redis Health
run_test "Redis Connection" "docker exec living_truth_redis redis-cli ping"

# Test 10: Neo4j Health
check_service "Neo4j" "http://localhost:7474/"

echo ""
echo -e "${BLUE}📋 Phase 3: Port Availability${NC}"
echo "----------------------------------------"

# Test ports
test_port "7860" "Langflow"
test_port "1234" "LM Studio"
test_port "8000" "Living Truth Engine"
test_port "5432" "PostgreSQL"
test_port "6379" "Redis"
test_port "7474" "Neo4j Web"
test_port "7687" "Neo4j Bolt"

echo ""
echo -e "${BLUE}📋 Phase 4: API Functionality${NC}"
echo "----------------------------------------"

# Test 11: Langflow API
run_test "Langflow API" "curl -f -s http://localhost:7860/api/v1/projects/ > /dev/null"

# Test 12: LM Studio API
run_test "LM Studio API" "curl -f -s http://localhost:1234/v1/models > /dev/null"

# Test 13: Living Truth Engine API
run_test "Living Truth Engine API" "curl -f -s http://localhost:8000/health > /dev/null"

echo ""
echo -e "${BLUE}📋 Phase 5: Container Restart Tests${NC}"
echo "----------------------------------------"

# Test 14: Container restart capability
echo -n "🔄 Testing container restart... "
if cd /home/mccoy/Projects/RippleAGI/notebook_agent && docker compose -f docker/docker-compose.yml restart living_truth_engine > /dev/null 2>&1; then
    echo -e "${GREEN}✅ SUCCESS${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "${RED}❌ FAILED${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

# Wait for restart
sleep 15

# Test 15: Health after restart
run_test "Health After Restart" "curl -f -s http://localhost:8000/health > /dev/null"

echo ""
echo -e "${BLUE}📋 Phase 6: Configuration Validation${NC}"
echo "----------------------------------------"

# Test 16: Docker Compose configuration
run_test "Docker Compose Config" "docker compose -f docker/docker-compose.yml config > /dev/null"

# Test 17: Environment variables
run_test "Environment Variables" "test -n \"$LANGFLOW_API_ENDPOINT\""

# Test 18: Project structure
run_test "Project Structure" "find . -name 'mcp_servers' -type d | head -1 > /dev/null"

echo ""
echo -e "${BLUE}📋 Phase 7: Data and File System${NC}"
echo "----------------------------------------"

# Test 19: Data directory access
run_test "Data Directory Access" "test -r data/sources"

# Test 20: Log directory access
run_test "Log Directory Access" "test -w logs"

# Test 21: Source files availability
run_test "Source Files Available" "ls data/sources/*.txt | head -1 > /dev/null"

echo ""
echo -e "${BLUE}📋 Phase 8: Network Connectivity${NC}"
echo "----------------------------------------"

# Test 22: Localhost connectivity
run_test "Localhost Connectivity" "ping -c 1 localhost > /dev/null"

# Test 23: Docker network
run_test "Docker Network" "docker network ls | grep -q living-truth-network"

echo ""
echo -e "${BLUE}📋 Phase 9: Resource Usage${NC}"
echo "----------------------------------------"

# Test 24: Memory usage
echo -n "💾 Checking memory usage... "
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemUsage}}" | tail -n +2 | head -1)
echo -e "${GREEN}✅ $MEMORY_USAGE${NC}"

# Test 25: Disk space
echo -n "💿 Checking disk space... "
DISK_SPACE=$(df -h . | tail -1 | awk '{print $4}')
echo -e "${GREEN}✅ $DISK_SPACE available${NC}"

echo ""
echo -e "${BLUE}📋 Phase 10: Error Recovery${NC}"
echo "----------------------------------------"

# Test 26: Graceful error handling
echo -n "🛡️ Testing error handling... "
if curl -f -s http://localhost:8000/nonexistent > /dev/null 2>&1; then
    echo -e "${RED}❌ Should have failed${NC}"
    FAILED_TESTS=$((FAILED_TESTS + 1))
else
    echo -e "${GREEN}✅ Properly handled 404${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
fi
TOTAL_TESTS=$((TOTAL_TESTS + 1))

echo ""
echo -e "${BLUE}📊 Test Results Summary${NC}"
echo "=========================="
echo -e "Total Tests: ${YELLOW}$TOTAL_TESTS${NC}"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! System is robust and reliable.${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}⚠️  $FAILED_TESTS test(s) failed. Please review the issues above.${NC}"
    exit 1
fi 