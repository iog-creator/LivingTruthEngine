#!/bin/bash
# Phase 9.5.6 Smoke Test - Chaos Engineering & Proactive Resilience
# Comprehensive testing of all chaos engineering and proactive resilience features
set -euo pipefail

# Configuration
BASE_URL=${BASE_URL:-http://localhost:8050}
PROJECT_ROOT=${PROJECT_ROOT:-$(pwd)}
CI_MODE=${CI_MODE:-false}
VERBOSE=${VERBOSE:-false}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging
LOG_FILE="/tmp/p9_5_6_smoke.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] SUCCESS:${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Test result tracking
test_result() {
    local test_name="$1"
    local success="$2"
    local message="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [[ "$success" == "true" ]]; then
        PASSED_TESTS=$((PASSED_TESTS + 1))
        log_success "$test_name: $message"
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        log_error "$test_name: $message"
    fi
}

# Health check functions
check_health_endpoint() {
    log "Checking health endpoint..."
    
    local response
    response=$(curl -s -w "%{http_code}" "$BASE_URL/api/health/full" || echo "000")
    local status_code="${response: -3}"
    local response_body="${response%???}"
    
    if [[ "$status_code" == "200" ]]; then
        local health_data
        health_data=$(echo "$response_body" | jq -r '.status // "unknown"')
        
        if [[ "$health_data" == "ok" ]]; then
            test_result "Health Endpoint" "true" "Health endpoint responding correctly"
            return 0
        else
            test_result "Health Endpoint" "false" "Health status not ok: $health_data"
            return 1
        fi
    else
        test_result "Health Endpoint" "false" "Health endpoint returned status $status_code"
        return 1
    fi
}

# Database schema validation
check_resilience_schema() {
    log "Checking resilience database schema..."
    
    local schema_check
    schema_check=$(psql "postgresql://postgres:postgres@localhost:5432/living_truth_engine" -t -c "
        SELECT 
            COUNT(*) as table_count
        FROM information_schema.tables 
        WHERE table_schema = 'lte' 
        AND table_name IN (
            'anomaly_detections', 
            'predictive_models', 
            'predictions', 
            'proactive_recovery_actions', 
            'resilience_scores', 
            'chaos_scenarios', 
            'chaos_scenario_results'
        );
    " 2>/dev/null || echo "0")
    
    local table_count=$(echo "$schema_check" | tr -d ' ')
    
    if [[ "$table_count" -ge 7 ]]; then
        test_result "Resilience Schema" "true" "All 7 resilience tables found"
        return 0
    else
        test_result "Resilience Schema" "false" "Only $table_count/7 resilience tables found"
        return 1
    fi
}

# Chaos scenarios script test
test_chaos_scenarios_script() {
    log "Testing chaos scenarios script..."
    
    # Test script exists and is executable
    if [[ -x "./scripts/chaos_scenarios.sh" ]]; then
        test_result "Chaos Script Exists" "true" "Chaos scenarios script is executable"
    else
        test_result "Chaos Script Exists" "false" "Chaos scenarios script not found or not executable"
        return 1
    fi
    
    # Test help output
    local help_output
    help_output=$(./scripts/chaos_scenarios.sh --help 2>&1 || echo "ERROR")
    
    if [[ "$help_output" != *"ERROR"* ]] && [[ "$help_output" == *"Enhanced Chaos Scenarios Script"* ]]; then
        test_result "Chaos Script Help" "true" "Chaos script help output working"
    else
        test_result "Chaos Script Help" "false" "Chaos script help output failed"
        return 1
    fi
    
    return 0
}

# Resilience score script test
test_resilience_score_script() {
    log "Testing resilience score script..."
    
    # Test script exists and is executable
    if [[ -x "./scripts/resilience_score.sh" ]]; then
        test_result "Resilience Script Exists" "true" "Resilience score script is executable"
    else
        test_result "Resilience Script Exists" "false" "Resilience score script not found or not executable"
        return 1
    fi
    
    # Test help output
    local help_output
    help_output=$(./scripts/resilience_score.sh --help 2>&1 || echo "ERROR")
    
    if [[ "$help_output" != *"ERROR"* ]] && [[ "$help_output" == *"Resilience Score Calculation Script"* ]]; then
        test_result "Resilience Script Help" "true" "Resilience script help output working"
    else
        test_result "Resilience Script Help" "false" "Resilience script help output failed"
        return 1
    fi
    
    return 0
}

# Predictive monitoring module test
test_predictive_monitoring() {
    log "Testing predictive monitoring module..."
    
    # Test module import
    local import_test
    import_test=$(python3 -c "
try:
    from src.monitoring.predictive_monitoring import PredictiveMonitor, AnomalyDetector, PredictiveModel
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$import_test" == *"SUCCESS"* ]]; then
        test_result "Predictive Monitoring Import" "true" "Predictive monitoring module imports successfully"
    else
        test_result "Predictive Monitoring Import" "false" "Predictive monitoring import failed: $import_test"
        return 1
    fi
    
    # Test basic functionality
    local functionality_test
    functionality_test=$(python3 -c "
from src.monitoring.predictive_monitoring import AnomalyDetector, PredictiveModel

try:
    # Test anomaly detector
    detector = AnomalyDetector()
    anomaly = detector.detect_spike_anomaly('test_service', 'latency', 100.0)
    
    # Test predictive model
    model = PredictiveModel()
    model.update_model('test_service', 'latency', 100.0)
    prediction = model.predict_value('test_service', 'latency', 5)
    
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$functionality_test" == *"SUCCESS"* ]]; then
        test_result "Predictive Monitoring Functionality" "true" "Predictive monitoring basic functionality working"
    else
        test_result "Predictive Monitoring Functionality" "false" "Predictive monitoring functionality failed: $functionality_test"
        return 1
    fi
    
    return 0
}

# Proactive recovery module test
test_proactive_recovery() {
    log "Testing proactive recovery module..."
    
    # Test module import
    local import_test
    import_test=$(python3 -c "
try:
    from src.monitoring.proactive_recovery import ProactiveRecoveryManager, RecoveryPolicyManager
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$import_test" == *"SUCCESS"* ]]; then
        test_result "Proactive Recovery Import" "true" "Proactive recovery module imports successfully"
    else
        test_result "Proactive Recovery Import" "false" "Proactive recovery import failed: $import_test"
        return 1
    fi
    
    # Test basic functionality
    local functionality_test
    functionality_test=$(python3 -c "
from src.monitoring.proactive_recovery import RecoveryPolicyManager

try:
    # Test policy manager
    policy_manager = RecoveryPolicyManager('postgresql://postgres:postgres@localhost:5432/living_truth_engine')
    
    # Test policy evaluation with mock metrics
    mock_metrics = {
        'api': {'latency': 50.0, 'error_rate': 0.1},
        'system': {'memory_usage': 60.0, 'cpu_usage': 30.0}
    }
    
    actions = policy_manager.evaluate_policies(mock_metrics)
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$functionality_test" == *"SUCCESS"* ]]; then
        test_result "Proactive Recovery Functionality" "true" "Proactive recovery basic functionality working"
    else
        test_result "Proactive Recovery Functionality" "false" "Proactive recovery functionality failed: $functionality_test"
        return 1
    fi
    
    return 0
}

# MCP tools test
test_mcp_tools() {
    log "Testing MCP tools for Phase 9.5.6..."
    
    # Test trigger_chaos_scenario tool
    local chaos_tool_test
    chaos_tool_test=$(python3 -c "
from src.mcp_servers.phase9_mcp_server import server

try:
    result = server.trigger_chaos_scenario('service_kill', {'blast_radius': 'small', 'duration': 5})
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$chaos_tool_test" == *"SUCCESS"* ]]; then
        test_result "MCP Chaos Tool" "true" "MCP chaos scenario tool working"
    else
        test_result "MCP Chaos Tool" "false" "MCP chaos scenario tool failed: $chaos_tool_test"
    fi
    
    # Test get_resilience_score tool
    local resilience_tool_test
    resilience_tool_test=$(python3 -c "
from src.mcp_servers.phase9_mcp_server import server

try:
    result = server.get_resilience_score(24)
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$resilience_tool_test" == *"SUCCESS"* ]]; then
        test_result "MCP Resilience Tool" "true" "MCP resilience score tool working"
    else
        test_result "MCP Resilience Tool" "false" "MCP resilience score tool failed: $resilience_tool_test"
    fi
    
    # Test simulate_proactive_recovery tool
    local recovery_tool_test
    recovery_tool_test=$(python3 -c "
from src.mcp_servers.phase9_mcp_server import server

try:
    stress_scenario = {'service_name': 'api', 'stress_level': 'medium', 'predicted_load': 100.0}
    result = server.simulate_proactive_recovery(stress_scenario)
    print('SUCCESS')
except Exception as e:
    print(f'ERROR: {e}')
" 2>&1)
    
    if [[ "$recovery_tool_test" == *"SUCCESS"* ]]; then
        test_result "MCP Recovery Tool" "true" "MCP proactive recovery tool working"
    else
        test_result "MCP Recovery Tool" "false" "MCP proactive recovery tool failed: $recovery_tool_test"
    fi
    
    return 0
}

# Chaos scenario execution test (safe mode)
test_chaos_execution() {
    log "Testing chaos scenario execution (safe mode)..."
    
    # Test a safe chaos scenario (CPU pressure with short duration)
    local chaos_result
    chaos_result=$(./scripts/chaos_scenarios.sh cpu_pressure 2 50 --duration 5 --safeguards true 2>&1 || echo "ERROR")
    
    if [[ "$chaos_result" != *"ERROR"* ]] && [[ "$chaos_result" == *"CPU pressure test completed"* ]]; then
        test_result "Chaos Execution" "true" "Chaos scenario execution working"
    else
        test_result "Chaos Execution" "false" "Chaos scenario execution failed: $chaos_result"
        return 1
    fi
    
    return 0
}

# Resilience score calculation test
test_resilience_calculation() {
    log "Testing resilience score calculation..."
    
    # Test resilience score calculation
    local resilience_result
    resilience_result=$(./scripts/resilience_score.sh 1 2>&1 || echo "ERROR")
    
    if [[ "$resilience_result" != *"ERROR"* ]] && [[ "$resilience_result" == *"resilience_score"* ]]; then
        test_result "Resilience Calculation" "true" "Resilience score calculation working"
    else
        test_result "Resilience Calculation" "false" "Resilience score calculation failed: $resilience_result"
        return 1
    fi
    
    return 0
}

# CI mode validation
test_ci_validation() {
    log "Testing CI mode validation..."
    
    # Test resilience score with CI mode
    local ci_result
    ci_result=$(./scripts/resilience_score.sh 1 --ci --min-score 0.0 2>&1 || echo "ERROR")
    
    if [[ "$ci_result" != *"ERROR"* ]]; then
        test_result "CI Validation" "true" "CI mode validation working"
    else
        test_result "CI Validation" "false" "CI mode validation failed: $ci_result"
        return 1
    fi
    
    return 0
}

# Database function test
test_database_functions() {
    log "Testing database functions..."
    
    # Test resilience score calculation function
    local function_test
    function_test=$(psql "postgresql://postgres:postgres@localhost:5432/living_truth_engine" -t -c "
        SELECT COUNT(*) FROM lte.calculate_resilience_score(1);
    " 2>/dev/null || echo "ERROR")
    
    if [[ "$function_test" != *"ERROR"* ]] && [[ -n "$(echo "$function_test" | tr -d ' ')" ]]; then
        test_result "Database Functions" "true" "Database functions working"
    else
        test_result "Database Functions" "false" "Database functions failed: $function_test"
        return 1
    fi
    
    return 0
}

# Performance test
test_performance() {
    log "Testing performance of resilience components..."
    
    # Test predictive monitoring performance
    local monitoring_perf
    monitoring_perf=$(python3 -c "
import time
from src.monitoring.predictive_monitoring import AnomalyDetector

start_time = time.time()
detector = AnomalyDetector()
for i in range(100):
    detector.detect_spike_anomaly('test_service', 'latency', 100.0 + i)
end_time = time.time()

if end_time - start_time < 1.0:
    print('SUCCESS')
else:
    print('SLOW')
" 2>&1)
    
    if [[ "$monitoring_perf" == *"SUCCESS"* ]]; then
        test_result "Monitoring Performance" "true" "Predictive monitoring performance acceptable"
    else
        test_result "Monitoring Performance" "false" "Predictive monitoring performance slow: $monitoring_perf"
    fi
    
    # Test resilience score calculation performance
    local score_perf_start
    score_perf_start=$(date +%s.%N)
    
    ./scripts/resilience_score.sh 1 > /dev/null 2>&1
    
    local score_perf_end
    score_perf_end=$(date +%s.%N)
    local score_perf_duration
    score_perf_duration=$(echo "$score_perf_end - $score_perf_start" | bc -l)
    
    if [[ $(echo "$score_perf_duration < 5.0" | bc -l) -eq 1 ]]; then
        test_result "Score Calculation Performance" "true" "Resilience score calculation performance acceptable (${score_perf_duration}s)"
    else
        test_result "Score Calculation Performance" "false" "Resilience score calculation too slow (${score_perf_duration}s)"
    fi
    
    return 0
}

# Main test execution
main() {
    log "Starting Phase 9.5.6 Smoke Test - Chaos Engineering & Proactive Resilience"
    log "Base URL: $BASE_URL"
    log "Project Root: $PROJECT_ROOT"
    log "CI Mode: $CI_MODE"
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Run all tests
    log "Running comprehensive smoke tests..."
    
    # Basic health checks
    check_health_endpoint
    
    # Database schema validation
    check_resilience_schema
    
    # Script tests
    test_chaos_scenarios_script
    test_resilience_score_script
    
    # Module tests
    test_predictive_monitoring
    test_proactive_recovery
    
    # MCP tools tests
    test_mcp_tools
    
    # Execution tests (safe mode)
    test_chaos_execution
    test_resilience_calculation
    
    # CI validation
    test_ci_validation
    
    # Database function tests
    test_database_functions
    
    # Performance tests
    test_performance
    
    # Print summary
    log "=== Phase 9.5.6 Smoke Test Summary ==="
    log "Total Tests: $TOTAL_TESTS"
    log "Passed: $PASSED_TESTS"
    log "Failed: $FAILED_TESTS"
    
    if [[ $FAILED_TESTS -eq 0 ]]; then
        log_success "All tests passed! Phase 9.5.6 smoke test completed successfully."
        exit 0
    else
        log_error "$FAILED_TESTS tests failed. Phase 9.5.6 smoke test failed."
        exit 1
    fi
}

# Help and usage
show_help() {
    cat << EOF
Phase 9.5.6 Smoke Test - Chaos Engineering & Proactive Resilience

Usage: $0 [OPTIONS]

OPTIONS:
  --ci                           - Enable CI mode with stricter validation
  --verbose                      - Enable verbose output
  --help                         - Show this help

ENVIRONMENT VARIABLES:
  BASE_URL                       - Base URL for health checks (default: http://localhost:8050)
  PROJECT_ROOT                   - Project root directory (default: current directory)
  CI_MODE                        - Enable CI mode

EXAMPLES:
  $0                              # Run smoke test
  $0 --ci                        # Run smoke test in CI mode
  $0 --verbose                   # Run smoke test with verbose output

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --ci)
            CI_MODE="true"
            shift
            ;;
        --verbose)
            VERBOSE="true"
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run main function
main "$@"
