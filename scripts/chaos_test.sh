#!/bin/bash
# Chaos Testing Script
# Phase 9.5.5 - Error Budgeting & Recovery Automation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/logs/chaos_test.log"
HEALTH_ENDPOINT="http://localhost:8050/api/health/full"
RESULTS_FILE="$PROJECT_ROOT/logs/chaos_test_results.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1" | tee -a "$LOG_FILE"
}

# Initialize log file
mkdir -p "$(dirname "$LOG_FILE")"
touch "$LOG_FILE"

# Test results array
declare -a test_results

# Function to check health endpoint
check_health() {
    local response
    local status_code
    
    response=$(curl -s -w "%{http_code}" "$HEALTH_ENDPOINT" || echo "000")
    status_code="${response: -3}"
    response_body="${response%???}"
    
    if [[ "$status_code" == "200" ]]; then
        echo "$response_body"
    else
        log_error "Health endpoint returned status code: $status_code"
        return 1
    fi
}

# Function to wait for service recovery
wait_for_recovery() {
    local max_wait=60  # seconds
    local wait_interval=5  # seconds
    local elapsed=0
    
    log_info "Waiting for service recovery..."
    
    while [[ $elapsed -lt $max_wait ]]; do
        if health_data=$(check_health 2>/dev/null); then
            log_success "Service recovered"
            return 0
        fi
        
        sleep $wait_interval
        elapsed=$((elapsed + wait_interval))
        log_info "Still waiting for recovery... ($elapsed/$max_wait seconds)"
    done
    
    log_error "Service did not recover within $max_wait seconds"
    return 1
}

# Function to run container kill test
run_container_kill_test() {
    local test_name="container_kill"
    local start_time=$(date +%s)
    local test_success=false
    local recovery_success=false
    local target_container=""
    
    log_info "Starting container kill chaos test"
    
    # Get list of running containers
    local containers=($(docker ps --format "{{.Names}}" | grep -v "postgres\|redis" || true))
    
    if [[ ${#containers[@]} -eq 0 ]]; then
        log_warning "No suitable containers found for kill test"
        return 1
    fi
    
    # Select random container
    target_container="${containers[$((RANDOM % ${#containers[@]}))]}"
    log_info "Target container: $target_container"
    
    # Kill the container
    if docker kill "$target_container" >/dev/null 2>&1; then
        test_success=true
        log_info "Successfully killed container: $target_container"
    else
        log_error "Failed to kill container: $target_container"
        return 1
    fi
    
    # Wait for recovery
    if wait_for_recovery; then
        recovery_success=true
    fi
    
    local end_time=$(date +%s)
    local test_duration=$((end_time - start_time))
    
    # Record test result
    local result=$(cat <<EOF
{
    "test_name": "$test_name",
    "target_container": "$target_container",
    "test_success": $test_success,
    "recovery_success": $recovery_success,
    "test_duration_seconds": $test_duration,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    test_results+=("$result")
    log_info "Container kill test completed"
}

# Function to run CPU stress test
run_cpu_stress_test() {
    local test_name="cpu_stress"
    local duration=30  # seconds
    local start_time=$(date +%s)
    local test_success=false
    local recovery_success=false
    
    log_info "Starting CPU stress chaos test (duration: ${duration}s)"
    
    # Check if stress command is available
    if ! command -v stress >/dev/null 2>&1; then
        log_warning "stress command not available, skipping CPU stress test"
        return 1
    fi
    
    # Start CPU stress
    local stress_pid
    if stress --cpu 4 --timeout "$duration" >/dev/null 2>&1 & then
        stress_pid=$!
        test_success=true
        log_info "CPU stress started (PID: $stress_pid)"
    else
        log_error "Failed to start CPU stress"
        return 1
    fi
    
    # Wait for stress to complete
    wait $stress_pid 2>/dev/null || true
    
    # Check system recovery
    if health_data=$(check_health 2>/dev/null); then
        recovery_success=true
        log_success "System recovered from CPU stress"
    else
        log_warning "System may not have fully recovered from CPU stress"
    fi
    
    local end_time=$(date +%s)
    local test_duration=$((end_time - start_time))
    
    # Record test result
    local result=$(cat <<EOF
{
    "test_name": "$test_name",
    "duration_seconds": $duration,
    "test_success": $test_success,
    "recovery_success": $recovery_success,
    "test_duration_seconds": $test_duration,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    test_results+=("$result")
    log_info "CPU stress test completed"
}

# Function to run database outage test
run_db_outage_test() {
    local test_name="db_outage"
    local outage_duration=10  # seconds
    local start_time=$(date +%s)
    local test_success=false
    local recovery_success=false
    
    log_info "Starting database outage chaos test (outage duration: ${outage_duration}s)"
    
    # Stop postgres container
    if docker compose -f "$PROJECT_ROOT/docker/docker-compose.yml" stop postgres >/dev/null 2>&1; then
        test_success=true
        log_info "Successfully stopped postgres container"
    else
        log_error "Failed to stop postgres container"
        return 1
    fi
    
    # Wait for outage duration
    log_info "Database outage in progress..."
    sleep $outage_duration
    
    # Start postgres container
    if docker compose -f "$PROJECT_ROOT/docker/docker-compose.yml" start postgres >/dev/null 2>&1; then
        log_info "Successfully started postgres container"
    else
        log_error "Failed to start postgres container"
        return 1
    fi
    
    # Wait for recovery
    if wait_for_recovery; then
        recovery_success=true
    fi
    
    local end_time=$(date +%s)
    local test_duration=$((end_time - start_time))
    
    # Record test result
    local result=$(cat <<EOF
{
    "test_name": "$test_name",
    "outage_duration_seconds": $outage_duration,
    "test_success": $test_success,
    "recovery_success": $recovery_success,
    "test_duration_seconds": $test_duration,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    test_results+=("$result")
    log_info "Database outage test completed"
}

# Function to run memory stress test
run_memory_stress_test() {
    local test_name="memory_stress"
    local duration=20  # seconds
    local start_time=$(date +%s)
    local test_success=false
    local recovery_success=false
    
    log_info "Starting memory stress chaos test (duration: ${duration}s)"
    
    # Check if stress command is available
    if ! command -v stress >/dev/null 2>&1; then
        log_warning "stress command not available, skipping memory stress test"
        return 1
    fi
    
    # Start memory stress (allocate 1GB for 20 seconds)
    local stress_pid
    if stress --vm 1 --vm-bytes 1G --timeout "$duration" >/dev/null 2>&1 & then
        stress_pid=$!
        test_success=true
        log_info "Memory stress started (PID: $stress_pid)"
    else
        log_error "Failed to start memory stress"
        return 1
    fi
    
    # Wait for stress to complete
    wait $stress_pid 2>/dev/null || true
    
    # Check system recovery
    if health_data=$(check_health 2>/dev/null); then
        recovery_success=true
        log_success "System recovered from memory stress"
    else
        log_warning "System may not have fully recovered from memory stress"
    fi
    
    local end_time=$(date +%s)
    local test_duration=$((end_time - start_time))
    
    # Record test result
    local result=$(cat <<EOF
{
    "test_name": "$test_name",
    "duration_seconds": $duration,
    "test_success": $test_success,
    "recovery_success": $recovery_success,
    "test_duration_seconds": $test_duration,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    test_results+=("$result")
    log_info "Memory stress test completed"
}

# Function to run network latency test
run_network_latency_test() {
    local test_name="network_latency"
    local duration=15  # seconds
    local start_time=$(date +%s)
    local test_success=false
    local recovery_success=false
    
    log_info "Starting network latency chaos test (duration: ${duration}s)"
    
    # Check if tc command is available
    if ! command -v tc >/dev/null 2>&1; then
        log_warning "tc command not available, skipping network latency test"
        return 1
    fi
    
    # Add network latency (100ms)
    if sudo tc qdisc add dev lo root netem delay 100ms >/dev/null 2>&1; then
        test_success=true
        log_info "Added network latency (100ms)"
    else
        log_error "Failed to add network latency"
        return 1
    fi
    
    # Wait for duration
    sleep $duration
    
    # Remove network latency
    if sudo tc qdisc del dev lo root >/dev/null 2>&1; then
        log_info "Removed network latency"
    else
        log_warning "Failed to remove network latency"
    fi
    
    # Check system recovery
    if health_data=$(check_health 2>/dev/null); then
        recovery_success=true
        log_success "System recovered from network latency"
    else
        log_warning "System may not have fully recovered from network latency"
    fi
    
    local end_time=$(date +%s)
    local test_duration=$((end_time - start_time))
    
    # Record test result
    local result=$(cat <<EOF
{
    "test_name": "$test_name",
    "duration_seconds": $duration,
    "test_success": $test_success,
    "recovery_success": $recovery_success,
    "test_duration_seconds": $test_duration,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    test_results+=("$result")
    log_info "Network latency test completed"
}

# Function to save test results
save_test_results() {
    local results_json="["
    local first=true
    
    for result in "${test_results[@]}"; do
        if [[ "$first" == "true" ]]; then
            first=false
        else
            results_json+=","
        fi
        results_json+="$result"
    done
    
    results_json+="]"
    
    # Save to file
    mkdir -p "$(dirname "$RESULTS_FILE")"
    echo "$results_json" > "$RESULTS_FILE"
    
    log_info "Test results saved to: $RESULTS_FILE"
}

# Function to print test summary
print_test_summary() {
    local total_tests=${#test_results[@]}
    local successful_tests=0
    local recovered_tests=0
    
    log_info "=== Chaos Test Summary ==="
    log_info "Total tests run: $total_tests"
    
    for result in "${test_results[@]}"; do
        if echo "$result" | grep -q '"test_success": true'; then
            ((successful_tests++))
        fi
        if echo "$result" | grep -q '"recovery_success": true'; then
            ((recovered_tests++))
        fi
    done
    
    log_info "Successful tests: $successful_tests/$total_tests"
    log_info "Recovered tests: $recovered_tests/$total_tests"
    
    if [[ $successful_tests -eq $total_tests ]] && [[ $recovered_tests -eq $total_tests ]]; then
        log_success "All chaos tests passed!"
    else
        log_warning "Some chaos tests failed or did not recover"
    fi
}

# Main function
main() {
    local test_types=("$@")
    
    if [[ ${#test_types[@]} -eq 0 ]]; then
        # Run all tests if none specified
        test_types=("container_kill" "cpu_stress" "db_outage" "memory_stress" "network_latency")
    fi
    
    log_info "Starting chaos testing suite"
    log_info "Tests to run: ${test_types[*]}"
    
    # Check initial health
    if ! initial_health=$(check_health); then
        log_error "System is not healthy before starting chaos tests"
        exit 1
    fi
    
    log_success "System is healthy, starting chaos tests"
    
    # Run specified tests
    for test_type in "${test_types[@]}"; do
        case "$test_type" in
            "container_kill")
                run_container_kill_test
                ;;
            "cpu_stress")
                run_cpu_stress_test
                ;;
            "db_outage")
                run_db_outage_test
                ;;
            "memory_stress")
                run_memory_stress_test
                ;;
            "network_latency")
                run_network_latency_test
                ;;
            *)
                log_warning "Unknown test type: $test_type"
                ;;
        esac
        
        # Brief pause between tests
        sleep 5
    done
    
    # Save results and print summary
    save_test_results
    print_test_summary
    
    log_info "Chaos testing suite completed"
}

# Show usage
show_usage() {
    echo "Usage: $0 [test_type...]"
    echo ""
    echo "Available test types:"
    echo "  container_kill    - Kill a random container"
    echo "  cpu_stress        - Stress CPU with high load"
    echo "  db_outage         - Simulate database outage"
    echo "  memory_stress     - Stress memory allocation"
    echo "  network_latency   - Add network latency"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 container_kill     # Run only container kill test"
    echo "  $0 cpu_stress db_outage  # Run specific tests"
}

# Parse command line arguments
if [[ $# -gt 0 ]] && [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_usage
    exit 0
fi

# Run main function
main "$@"
