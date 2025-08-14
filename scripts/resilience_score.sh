#!/bin/bash
# Resilience Score Calculation Script
# Phase 9.5.6 - Chaos Engineering & Proactive Resilience
set -euo pipefail

# Configuration
BASE_URL=${BASE_URL:-http://localhost:8050}
DB_CONNECTION_STRING=${DB_CONNECTION_STRING:-"postgresql://postgres:postgres@localhost:5432/living_truth_engine"}
WINDOW_HOURS=${WINDOW_HOURS:-24}
CI_MODE=${CI_MODE:-false}
MIN_RESILIENCE_SCORE=${MIN_RESILIENCE_SCORE:-80.0}

# Logging
LOG_FILE="/tmp/resilience_score.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Database functions
execute_sql() {
    local query="$1"
    psql "$DB_CONNECTION_STRING" -t -c "$query" 2>/dev/null || echo "0"
}

get_resilience_score() {
    local window_hours="$1"
    
    log "Calculating resilience score for last $window_hours hours..."
    
    # Execute the resilience score calculation function
    local result=$(execute_sql "SELECT * FROM lte.calculate_resilience_score($window_hours);")
    
    if [[ -z "$result" ]] || [[ "$result" == "0" ]]; then
        log "ERROR: Failed to calculate resilience score"
        return 1
    fi
    
    echo "$result"
}

get_chaos_test_stats() {
    local window_hours="$1"
    
    log "Getting chaos test statistics..."
    
    local query="
        SELECT 
            COUNT(*) as total_tests,
            COUNT(*) FILTER (WHERE recovery_success = TRUE) as successful_recoveries,
            AVG(test_duration_ms) FILTER (WHERE recovery_success = TRUE) as avg_recovery_time,
            COUNT(*) FILTER (WHERE slo_violation = TRUE) as slo_violations
        FROM lte.chaos_scenario_results
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * $window_hours;
    "
    
    execute_sql "$query"
}

get_recovery_action_stats() {
    local window_hours="$1"
    
    log "Getting recovery action statistics..."
    
    local query="
        SELECT 
            COUNT(*) as total_actions,
            COUNT(*) FILTER (WHERE success = TRUE) as successful_actions,
            AVG(duration_ms) FILTER (WHERE success = TRUE) as avg_action_duration,
            COUNT(*) FILTER (WHERE impact_mitigated = TRUE) as mitigated_impacts
        FROM lte.proactive_recovery_actions
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * $window_hours;
    "
    
    execute_sql "$query"
}

get_prediction_stats() {
    local window_hours="$1"
    
    log "Getting prediction statistics..."
    
    local query="
        SELECT 
            COUNT(*) as total_predictions,
            AVG(accuracy) FILTER (WHERE accuracy IS NOT NULL) as avg_accuracy,
            COUNT(*) FILTER (WHERE accuracy > 0.8) as accurate_predictions
        FROM lte.predictions
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * $window_hours;
    "
    
    execute_sql "$query"
}

get_anomaly_stats() {
    local window_hours="$1"
    
    log "Getting anomaly statistics..."
    
    local query="
        SELECT 
            COUNT(*) as total_anomalies,
            COUNT(*) FILTER (WHERE severity = 'critical') as critical_anomalies,
            COUNT(*) FILTER (WHERE severity = 'high') as high_anomalies,
            COUNT(*) FILTER (WHERE alert_sent = TRUE) as alerts_sent
        FROM lte.anomaly_detections
        WHERE timestamp >= NOW() - INTERVAL '1 hour' * $window_hours;
    "
    
    execute_sql "$query"
}

# Score calculation functions
calculate_chaos_score() {
    local total_tests="$1"
    local successful_recoveries="$2"
    
    if [[ "$total_tests" -eq 0 ]]; then
        echo "100.0"
    else
        local score=$(echo "scale=2; $successful_recoveries * 100 / $total_tests" | bc -l)
        echo "$score"
    fi
}

calculate_recovery_score() {
    local total_actions="$1"
    local successful_actions="$2"
    
    if [[ "$total_actions" -eq 0 ]]; then
        echo "100.0"
    else
        local score=$(echo "scale=2; $successful_actions * 100 / $total_actions" | bc -l)
        echo "$score"
    fi
}

calculate_prediction_score() {
    local avg_accuracy="$1"
    
    if [[ -z "$avg_accuracy" ]] || [[ "$avg_accuracy" == "NULL" ]]; then
        echo "100.0"
    else
        local score=$(echo "scale=2; $avg_accuracy * 100" | bc -l)
        echo "$score"
    fi
}

calculate_anomaly_score() {
    local total_anomalies="$1"
    local critical_anomalies="$2"
    local high_anomalies="$3"
    
    if [[ "$total_anomalies" -eq 0 ]]; then
        echo "100.0"
    else
        # Penalize based on anomaly count and severity
        local critical_penalty=$(echo "scale=2; $critical_anomalies * 10" | bc -l)
        local high_penalty=$(echo "scale=2; $high_anomalies * 5" | bc -l)
        local total_penalty=$(echo "scale=2; $critical_penalty + $high_penalty" | bc -l)
        local score=$(echo "scale=2; 100 - $total_penalty" | bc -l)
        
        # Ensure score doesn't go below 0
        if [[ $(echo "$score < 0" | bc -l) -eq 1 ]]; then
            echo "0.0"
        else
            echo "$score"
        fi
    fi
}

# Main resilience score calculation
calculate_overall_resilience_score() {
    local window_hours="$1"
    
    log "Calculating overall resilience score for last $window_hours hours..."
    
    # Get component scores from database
    local resilience_data=$(get_resilience_score "$window_hours")
    
    if [[ -z "$resilience_data" ]]; then
        log "ERROR: No resilience data available"
        return 1
    fi
    
    # Parse the result (assuming it's a single row with multiple columns)
    local overall_score=$(echo "$resilience_data" | awk '{print $1}')
    local chaos_score=$(echo "$resilience_data" | awk '{print $2}')
    local recovery_score=$(echo "$resilience_data" | awk '{print $3}')
    local prediction_score=$(echo "$resilience_data" | awk '{print $4}')
    local anomaly_score=$(echo "$resilience_data" | awk '{print $5}')
    
    # Get detailed statistics
    local chaos_stats=$(get_chaos_test_stats "$window_hours")
    local recovery_stats=$(get_recovery_action_stats "$window_hours")
    local prediction_stats=$(get_prediction_stats "$window_hours")
    local anomaly_stats=$(get_anomaly_stats "$window_hours")
    
    # Create detailed report
    local report=$(cat << EOF
{
    "resilience_score": {
        "overall": $overall_score,
        "components": {
            "chaos_test": $chaos_score,
            "recovery": $recovery_score,
            "prediction": $prediction_score,
            "anomaly": $anomaly_score
        },
        "weights": {
            "chaos_test": 0.3,
            "recovery": 0.3,
            "prediction": 0.2,
            "anomaly": 0.2
        }
    },
    "statistics": {
        "chaos_tests": {
            "total": $(echo "$chaos_stats" | awk '{print $1}'),
            "successful_recoveries": $(echo "$chaos_stats" | awk '{print $2}'),
            "avg_recovery_time_ms": $(echo "$chaos_stats" | awk '{print $3}'),
            "slo_violations": $(echo "$chaos_stats" | awk '{print $4}')
        },
        "recovery_actions": {
            "total": $(echo "$recovery_stats" | awk '{print $1}'),
            "successful": $(echo "$recovery_stats" | awk '{print $2}'),
            "avg_duration_ms": $(echo "$recovery_stats" | awk '{print $3}'),
            "mitigated_impacts": $(echo "$recovery_stats" | awk '{print $4}')
        },
        "predictions": {
            "total": $(echo "$prediction_stats" | awk '{print $1}'),
            "avg_accuracy": $(echo "$prediction_stats" | awk '{print $2}'),
            "accurate_predictions": $(echo "$prediction_stats" | awk '{print $3}')
        },
        "anomalies": {
            "total": $(echo "$anomaly_stats" | awk '{print $1}'),
            "critical": $(echo "$anomaly_stats" | awk '{print $2}'),
            "high": $(echo "$anomaly_stats" | awk '{print $3}'),
            "alerts_sent": $(echo "$anomaly_stats" | awk '{print $4}')
        }
    },
    "calculation_window_hours": $window_hours,
    "timestamp": "$(date -Iseconds)"
}
EOF
)
    
    echo "$report"
}

# CI mode validation
validate_ci_resilience() {
    local resilience_score="$1"
    
    log "Validating resilience score for CI: $resilience_score"
    
    if [[ $(echo "$resilience_score >= $MIN_RESILIENCE_SCORE" | bc -l) -eq 1 ]]; then
        log "SUCCESS: Resilience score $resilience_score meets minimum threshold $MIN_RESILIENCE_SCORE"
        return 0
    else
        log "ERROR: Resilience score $resilience_score below minimum threshold $MIN_RESILIENCE_SCORE"
        return 1
    fi
}

# Health check integration
update_health_endpoint() {
    local resilience_score="$1"
    local report="$2"
    
    log "Updating health endpoint with resilience score..."
    
    # This would typically update a health endpoint or configuration
    # For now, we'll just log the score
    log "Resilience score for health endpoint: $resilience_score"
    
    # Store the report in a file for health endpoint to read
    echo "$report" > /tmp/resilience_score_report.json
}

# MCP integration
report_to_mcp() {
    local resilience_score="$1"
    local report="$2"
    
    log "Reporting resilience score to MCP server..."
    
    # Report to MCP server if available
    if command -v python3 &> /dev/null; then
        python3 -c "
import requests
import json
import sys

try:
    result = {
        'resilience_score': $resilience_score,
        'report': json.loads('''$report'''),
        'timestamp': '$(date -Iseconds)'
    }
    
    # Send to MCP server (if available)
    response = requests.post('http://localhost:8050/api/resilience/report', 
                           json=result, timeout=5)
    print(f'MCP resilience report sent: {response.status_code}')
except Exception as e:
    print(f'MCP resilience report failed: {e}')
"
    fi
}

# Main execution
main() {
    local window_hours="${1:-$WINDOW_HOURS}"
    
    log "Starting resilience score calculation..."
    
    # Check if bc is available for calculations
    if ! command -v bc &> /dev/null; then
        log "ERROR: bc command not available for calculations"
        exit 1
    fi
    
    # Calculate resilience score
    local report=$(calculate_overall_resilience_score "$window_hours")
    
    if [[ -z "$report" ]]; then
        log "ERROR: Failed to calculate resilience score"
        exit 1
    fi
    
    # Extract overall score
    local resilience_score=$(echo "$report" | jq -r '.resilience_score.overall')
    
    # Display results
    log "Resilience Score Results:"
    log "  Overall Score: $resilience_score"
    log "  Chaos Test Score: $(echo "$report" | jq -r '.resilience_score.components.chaos_test')"
    log "  Recovery Score: $(echo "$report" | jq -r '.resilience_score.components.recovery')"
    log "  Prediction Score: $(echo "$report" | jq -r '.resilience_score.components.prediction')"
    log "  Anomaly Score: $(echo "$report" | jq -r '.resilience_score.components.anomaly')"
    
    # Display statistics
    log "Statistics:"
    log "  Chaos Tests: $(echo "$report" | jq -r '.statistics.chaos_tests.total') total, $(echo "$report" | jq -r '.statistics.chaos_tests.successful_recoveries') successful"
    log "  Recovery Actions: $(echo "$report" | jq -r '.statistics.recovery_actions.total') total, $(echo "$report" | jq -r '.statistics.recovery_actions.successful') successful"
    log "  Predictions: $(echo "$report" | jq -r '.statistics.predictions.total') total, $(echo "$report" | jq -r '.statistics.predictions.avg_accuracy') avg accuracy"
    log "  Anomalies: $(echo "$report" | jq -r '.statistics.anomalies.total') total, $(echo "$report" | jq -r '.statistics.anomalies.critical') critical"
    
    # CI mode validation
    if [[ "$CI_MODE" == "true" ]]; then
        if ! validate_ci_resilience "$resilience_score"; then
            log "CI validation failed - resilience score below threshold"
            exit 1
        fi
    fi
    
    # Update health endpoint
    update_health_endpoint "$resilience_score" "$report"
    
    # Report to MCP
    report_to_mcp "$resilience_score" "$report"
    
    # Output JSON report
    echo "$report"
    
    log "Resilience score calculation completed successfully"
}

# Help and usage
show_help() {
    cat << EOF
Resilience Score Calculation Script - Phase 9.5.6

Usage: $0 [WINDOW_HOURS] [OPTIONS]

ARGUMENTS:
  WINDOW_HOURS                    - Time window in hours for score calculation (default: 24)

OPTIONS:
  --ci                           - Enable CI mode with threshold validation
  --min-score SCORE              - Minimum resilience score for CI (default: 80.0)
  --help                         - Show this help

ENVIRONMENT VARIABLES:
  BASE_URL                       - Base URL for health checks
  DB_CONNECTION_STRING           - PostgreSQL connection string
  WINDOW_HOURS                   - Default time window in hours
  CI_MODE                        - Enable CI mode
  MIN_RESILIENCE_SCORE           - Minimum score for CI validation

EXAMPLES:
  $0 24                          # Calculate score for last 24 hours
  $0 168 --ci                    # Calculate score for last week with CI validation
  $0 --min-score 85.0 --ci       # Use custom minimum score

EOF
}

# Parse command line arguments
if [[ $# -gt 0 ]] && [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --ci)
            CI_MODE="true"
            shift
            ;;
        --min-score)
            MIN_RESILIENCE_SCORE="$2"
            shift 2
            ;;
        *)
            break
            ;;
    esac
done

# Run main function
main "$@"
