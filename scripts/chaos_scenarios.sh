#!/bin/bash
# Enhanced Chaos Scenarios Script
# Phase 9.5.6 - Chaos Engineering & Proactive Resilience
set -euo pipefail

# Configuration
BASE_URL=${BASE_URL:-http://localhost:8050}
PROJECT_ROOT=${PROJECT_ROOT:-$(pwd)}
SCENARIO_TYPE=${1:-"service_kill"}
BLAST_RADIUS=${BLAST_RADIUS:-"small"}
DURATION_SECONDS=${DURATION_SECONDS:-30}
SAFEGUARDS_ENABLED=${SAFEGUARDS_ENABLED:-true}
SCHEDULED_MODE=${SCHEDULED_MODE:-false}
CRON_EXPRESSION=${CRON_EXPRESSION:-""}

# Logging
LOG_FILE="/tmp/chaos_scenarios.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$LOG_FILE" >&2)

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Safety checks
check_safeguards() {
    if [[ "$SAFEGUARDS_ENABLED" == "true" ]]; then
        log "Safeguards enabled - checking system health before chaos test"
        
        # Check if we're in production
        if [[ "$NODE_ENV" == "production" ]]; then
            log "ERROR: Chaos testing not allowed in production environment"
            exit 1
        fi
        
        # Check system health
        health_response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/health/full" || echo "000")
        if [[ "$health_response" != "200" ]]; then
            log "ERROR: System health check failed (HTTP $health_response)"
            exit 1
        fi
        
        # Check available resources
        available_memory=$(free -m | awk 'NR==2{printf "%.0f", $7*100/$2}')
        if [[ "$available_memory" -lt 20 ]]; then
            log "ERROR: Insufficient memory available ($available_memory%)"
            exit 1
        fi
        
        log "Safeguards passed - proceeding with chaos test"
    fi
}

# Health monitoring
monitor_health() {
    local start_time=$1
    local duration=$2
    local check_interval=5
    
    log "Monitoring system health during chaos test..."
    
    while [[ $(($(date +%s) - start_time)) -lt duration ]]; do
        health_response=$(curl -s "$BASE_URL/api/health/full" 2>/dev/null || echo '{"status":"error"}')
        health_status=$(echo "$health_response" | jq -r '.status // "unknown"')
        
        if [[ "$health_status" != "ok" ]]; then
            log "WARNING: System health degraded during chaos test: $health_status"
        fi
        
        sleep $check_interval
    done
}

# Recovery verification
verify_recovery() {
    local max_wait_time=120
    local check_interval=5
    local elapsed=0
    
    log "Verifying system recovery..."
    
    while [[ $elapsed -lt $max_wait_time ]]; do
        health_response=$(curl -s "$BASE_URL/api/health/full" 2>/dev/null || echo '{"status":"error"}')
        health_status=$(echo "$health_response" | jq -r '.status // "unknown"')
        
        if [[ "$health_status" == "ok" ]]; then
            log "System recovered successfully"
            return 0
        fi
        
        sleep $check_interval
        elapsed=$((elapsed + check_interval))
    done
    
    log "ERROR: System did not recover within $max_wait_time seconds"
    return 1
}

# Chaos scenario implementations
run_service_kill_scenario() {
    local service_name=${2:-"dashboard"}
    local kill_method=${3:-"docker_kill"}
    
    log "Running service kill scenario: $service_name ($kill_method)"
    
    # Get container ID
    container_id=$(docker ps --filter "name=$service_name" --format "{{.ID}}" | head -1)
    if [[ -z "$container_id" ]]; then
        log "ERROR: Service $service_name not found"
        return 1
    fi
    
    # Kill the service
    if [[ "$kill_method" == "docker_kill" ]]; then
        docker kill "$container_id"
        log "Killed container $container_id"
    elif [[ "$kill_method" == "docker_stop" ]]; then
        docker stop "$container_id"
        log "Stopped container $container_id"
    fi
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Restart the service
    docker start "$container_id"
    log "Restarted container $container_id"
}

run_network_latency_scenario() {
    local latency_ms=${2:-100}
    local packet_loss_percent=${3:-5}
    
    log "Running network latency scenario: ${latency_ms}ms latency, ${packet_loss_percent}% packet loss"
    
    # Check if tc (traffic control) is available
    if ! command -v tc &> /dev/null; then
        log "ERROR: tc command not available for network latency simulation"
        return 1
    fi
    
    # Get default interface
    interface=$(ip route | grep default | awk '{print $5}' | head -1)
    if [[ -z "$interface" ]]; then
        log "ERROR: Could not determine default network interface"
        return 1
    fi
    
    # Add latency and packet loss
    tc qdisc add dev "$interface" root netem delay "${latency_ms}ms" loss "${packet_loss_percent}%"
    log "Applied network conditions to $interface"
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Remove network conditions
    tc qdisc del dev "$interface" root
    log "Removed network conditions from $interface"
}

run_db_exhaustion_scenario() {
    local max_connections=${2:-5}
    local connection_timeout_ms=${3:-5000}
    
    log "Running DB connection exhaustion scenario: max $max_connections connections"
    
    # Create connection exhaustion script
    cat > /tmp/db_exhaustion.py << 'EOF'
import psycopg2
import time
import threading
import sys

def exhaust_connections(max_conns, timeout_ms):
    connections = []
    try:
        for i in range(max_conns):
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="living_truth_engine",
                user="postgres",
                password="postgres"
            )
            connections.append(conn)
            print(f"Connection {i+1} established")
        
        print(f"Exhausted {len(connections)} connections")
        time.sleep(timeout_ms / 1000)
        
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        for conn in connections:
            try:
                conn.close()
            except:
                pass

if __name__ == "__main__":
    max_conns = int(sys.argv[1])
    timeout_ms = int(sys.argv[2])
    exhaust_connections(max_conns, timeout_ms)
EOF
    
    # Run connection exhaustion
    python3 /tmp/db_exhaustion.py "$max_connections" "$connection_timeout_ms" &
    exhaustion_pid=$!
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Clean up
    kill $exhaustion_pid 2>/dev/null || true
    rm -f /tmp/db_exhaustion.py
    log "DB connection exhaustion test completed"
}

run_cpu_pressure_scenario() {
    local cpu_cores=${2:-2}
    local load_percentage=${3:-80}
    
    log "Running CPU pressure scenario: $cpu_cores cores at ${load_percentage}% load"
    
    # Check if stress command is available
    if ! command -v stress &> /dev/null; then
        log "ERROR: stress command not available for CPU pressure simulation"
        return 1
    fi
    
    # Calculate stress duration
    stress_duration=$((DURATION_SECONDS + 10))
    
    # Run CPU stress
    stress --cpu "$cpu_cores" --timeout "$stress_duration" &
    stress_pid=$!
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Clean up
    kill $stress_pid 2>/dev/null || true
    log "CPU pressure test completed"
}

run_memory_pressure_scenario() {
    local memory_gb=${2:-1}
    local pressure_duration_seconds=${3:-30}
    
    log "Running memory pressure scenario: ${memory_gb}GB for ${pressure_duration_seconds}s"
    
    # Check if stress command is available
    if ! command -v stress &> /dev/null; then
        log "ERROR: stress command not available for memory pressure simulation"
        return 1
    fi
    
    # Calculate stress duration
    stress_duration=$((DURATION_SECONDS + 10))
    
    # Run memory stress
    stress --vm 1 --vm-bytes "${memory_gb}G" --timeout "$stress_duration" &
    stress_pid=$!
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Clean up
    kill $stress_pid 2>/dev/null || true
    log "Memory pressure test completed"
}

run_queue_failure_scenario() {
    local delay_seconds=${2:-10}
    local queue_size_limit=${3:-100}
    
    log "Running queue failure scenario: ${delay_seconds}s delay, size limit $queue_size_limit"
    
    # Simulate queue delay by sleeping
    log "Simulating queue delay..."
    sleep "$delay_seconds"
    
    # Simulate queue overflow
    log "Simulating queue overflow..."
    for i in $(seq 1 $queue_size_limit); do
        # Send requests to create queue pressure
        curl -s "$BASE_URL/api/health" > /dev/null &
    done
    
    # Wait for duration
    sleep "$DURATION_SECONDS"
    
    # Clean up background processes
    wait
    log "Queue failure test completed"
}

# Main chaos scenario runner
run_chaos_scenario() {
    local scenario_type=$1
    local start_time=$(date +%s)
    
    log "Starting chaos scenario: $scenario_type (blast radius: $BLAST_RADIUS, duration: ${DURATION_SECONDS}s)"
    
    # Run safety checks
    check_safeguards
    
    # Start health monitoring in background
    monitor_health "$start_time" "$DURATION_SECONDS" &
    monitor_pid=$!
    
    # Run the specific scenario
    case "$scenario_type" in
        "service_kill")
            run_service_kill_scenario "$@"
            ;;
        "network_latency")
            run_network_latency_scenario "$@"
            ;;
        "db_exhaustion")
            run_db_exhaustion_scenario "$@"
            ;;
        "cpu_pressure")
            run_cpu_pressure_scenario "$@"
            ;;
        "memory_pressure")
            run_memory_pressure_scenario "$@"
            ;;
        "queue_failure")
            run_queue_failure_scenario "$@"
            ;;
        *)
            log "ERROR: Unknown scenario type: $scenario_type"
            exit 1
            ;;
    esac
    
    # Wait for monitoring to complete
    wait $monitor_pid 2>/dev/null || true
    
    # Verify recovery
    if verify_recovery; then
        log "Chaos scenario completed successfully"
        return 0
    else
        log "Chaos scenario failed - system did not recover"
        return 1
    fi
}

# Scheduled chaos testing
setup_scheduled_chaos() {
    if [[ "$SCHEDULED_MODE" == "true" ]]; then
        log "Setting up scheduled chaos testing with cron: $CRON_EXPRESSION"
        
        # Create cron job
        (crontab -l 2>/dev/null; echo "$CRON_EXPRESSION $0 $SCENARIO_TYPE") | crontab -
        
        log "Scheduled chaos testing configured"
    fi
}

# MCP integration
report_to_mcp() {
    local scenario_type=$1
    local success=$2
    local duration_ms=$3
    
    # Report to MCP server if available
    if command -v python3 &> /dev/null; then
        python3 -c "
import requests
import json
import sys

try:
    result = {
        'scenario_type': '$scenario_type',
        'blast_radius': '$BLAST_RADIUS',
        'duration_seconds': $DURATION_SECONDS,
        'success': $success,
        'duration_ms': $duration_ms,
        'timestamp': '$(date -Iseconds)'
    }
    
    # Send to MCP server (if available)
    response = requests.post('http://localhost:8050/api/chaos/report', 
                           json=result, timeout=5)
    print(f'MCP report sent: {response.status_code}')
except Exception as e:
    print(f'MCP report failed: {e}')
"
    fi
}

# Main execution
main() {
    local start_time=$(date +%s)
    local success=false
    
    # Setup scheduled chaos if requested
    if [[ "$SCHEDULED_MODE" == "true" ]]; then
        setup_scheduled_chaos
        exit 0
    fi
    
    # Run chaos scenario
    if run_chaos_scenario "$@"; then
        success=true
    fi
    
    # Calculate duration
    local end_time=$(date +%s)
    local duration_ms=$(((end_time - start_time) * 1000))
    
    # Report results
    log "Chaos scenario results:"
    log "  Type: $SCENARIO_TYPE"
    log "  Blast radius: $BLAST_RADIUS"
    log "  Duration: ${DURATION_SECONDS}s"
    log "  Success: $success"
    log "  Total time: ${duration_ms}ms"
    
    # Report to MCP
    report_to_mcp "$SCENARIO_TYPE" "$success" "$duration_ms"
    
    # Exit with appropriate code
    if [[ "$success" == "true" ]]; then
        exit 0
    else
        exit 1
    fi
}

# Help and usage
show_help() {
    cat << EOF
Enhanced Chaos Scenarios Script - Phase 9.5.6

Usage: $0 [SCENARIO_TYPE] [OPTIONS]

SCENARIO_TYPES:
  service_kill [SERVICE] [METHOD]     - Kill/stop a service container
  network_latency [MS] [LOSS%]        - Add network latency and packet loss
  db_exhaustion [CONNS] [TIMEOUT_MS]  - Exhaust database connections
  cpu_pressure [CORES] [LOAD%]        - Generate CPU load
  memory_pressure [GB] [DURATION_S]   - Generate memory pressure
  queue_failure [DELAY_S] [SIZE]      - Simulate queue delays and overflow

OPTIONS:
  --blast-radius RADIUS               - Set blast radius (small/medium/large)
  --duration SECONDS                  - Set test duration in seconds
  --safeguards ENABLED                - Enable/disable safety checks
  --scheduled                         - Setup scheduled chaos testing
  --cron EXPRESSION                   - Cron expression for scheduling
  --help                              - Show this help

ENVIRONMENT VARIABLES:
  BASE_URL                            - Base URL for health checks
  PROJECT_ROOT                        - Project root directory
  NODE_ENV                            - Environment (production blocks chaos)

EXAMPLES:
  $0 service_kill dashboard docker_kill
  $0 network_latency 200 10
  $0 cpu_pressure 4 90 --duration 60
  $0 --scheduled --cron "0 2 * * *" service_kill

EOF
}

# Parse command line arguments
if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
fi

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        --blast-radius)
            BLAST_RADIUS="$2"
            shift 2
            ;;
        --duration)
            DURATION_SECONDS="$2"
            shift 2
            ;;
        --safeguards)
            SAFEGUARDS_ENABLED="$2"
            shift 2
            ;;
        --scheduled)
            SCHEDULED_MODE="true"
            shift
            ;;
        --cron)
            CRON_EXPRESSION="$2"
            shift 2
            ;;
        *)
            break
            ;;
    esac
done

# Run main function
main "$@"
