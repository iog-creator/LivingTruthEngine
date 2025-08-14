#!/bin/bash
# Recovery Watchdog Script
# Phase 9.5.5 - Error Budgeting & Recovery Automation

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$PROJECT_ROOT/logs/recovery_watchdog.log"
HEALTH_ENDPOINT="http://localhost:8050/api/health/full"
ERROR_BUDGET_THRESHOLD=80.0
CHECK_INTERVAL=60  # seconds
MAX_RECOVERY_ATTEMPTS=3
COOLDOWN_PERIOD=300  # seconds

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

log_info "Recovery watchdog started"
log_info "Health endpoint: $HEALTH_ENDPOINT"
log_info "Error budget threshold: ${ERROR_BUDGET_THRESHOLD}%"
log_info "Check interval: ${CHECK_INTERVAL}s"
log_info "Max recovery attempts: $MAX_RECOVERY_ATTEMPTS"
log_info "Cooldown period: ${COOLDOWN_PERIOD}s"

# Recovery attempt tracking
declare -A recovery_attempts
declare -A last_recovery_time

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

# Function to check error budget status
check_error_budget() {
    local health_data="$1"
    local critical_services=0
    
    # Extract error budget information from health data
    if command -v jq >/dev/null 2>&1; then
        # Use jq to parse JSON
        critical_services=$(echo "$health_data" | jq -r '.data.error_budget_remaining.critical_services // 0')
    else
        # Fallback: simple grep for critical services
        if echo "$health_data" | grep -q '"health_status":"critical"'; then
            critical_services=1
        fi
    fi
    
    echo "$critical_services"
}

# Function to trigger recovery action
trigger_recovery() {
    local service_name="$1"
    local action_type="$2"
    local reason="$3"
    
    log_warning "Triggering recovery action: $action_type for $service_name"
    log_warning "Reason: $reason"
    
    # Check cooldown period
    local current_time=$(date +%s)
    local last_time="${last_recovery_time[$service_name]:-0}"
    local time_since_last=$((current_time - last_time))
    
    if [[ $time_since_last -lt $COOLDOWN_PERIOD ]]; then
        log_warning "Service $service_name is in cooldown period. Skipping recovery."
        return 1
    fi
    
    # Check max attempts
    local attempts="${recovery_attempts[$service_name]:-0}"
    if [[ $attempts -ge $MAX_RECOVERY_ATTEMPTS ]]; then
        log_error "Max recovery attempts reached for $service_name. Manual intervention required."
        return 1
    fi
    
    # Execute recovery action
    local success=false
    case "$action_type" in
        "container_restart")
            if docker compose -f "$PROJECT_ROOT/docker/docker-compose.yml" restart "$service_name" >/dev/null 2>&1; then
                success=true
            fi
            ;;
        "cache_purge")
            if docker exec lte-redis-1 redis-cli FLUSHALL >/dev/null 2>&1; then
                success=true
            fi
            ;;
        "db_reset")
            if docker compose -f "$PROJECT_ROOT/docker/docker-compose.yml" restart postgres >/dev/null 2>&1; then
                success=true
            fi
            ;;
        *)
            log_error "Unknown recovery action type: $action_type"
            return 1
            ;;
    esac
    
    # Update tracking
    if [[ "$success" == "true" ]]; then
        log_success "Recovery action $action_type for $service_name completed successfully"
        recovery_attempts[$service_name]=0  # Reset attempts on success
    else
        log_error "Recovery action $action_type for $service_name failed"
        recovery_attempts[$service_name]=$((attempts + 1))
    fi
    
    last_recovery_time[$service_name]=$current_time
    
    return 0
}

# Function to determine recovery action
determine_recovery_action() {
    local health_data="$1"
    local service_name="$2"
    
    # Check for specific service issues
    if echo "$health_data" | grep -q '"status":"error"'; then
        echo "container_restart"
        return 0
    fi
    
    # Check for database issues
    if echo "$health_data" | grep -q '"database.*error\|connection.*failed"'; then
        echo "db_reset"
        return 0
    fi
    
    # Check for cache issues
    if echo "$health_data" | grep -q '"cache.*error\|redis.*failed"'; then
        echo "cache_purge"
        return 0
    fi
    
    # Default to container restart
    echo "container_restart"
}

# Function to identify critical services
identify_critical_services() {
    local health_data="$1"
    local services=()
    
    # Extract service information from health data
    if command -v jq >/dev/null 2>&1; then
        # Use jq to extract critical services
        services=($(echo "$health_data" | jq -r '.data.error_budget_remaining.error_budgets | to_entries[] | select(.value | to_entries[] | .value.error_budget_consumed >= 80) | .key' 2>/dev/null || echo ""))
    else
        # Fallback: check for common service names
        if echo "$health_data" | grep -q '"api"'; then
            services+=("api")
        fi
        if echo "$health_data" | grep -q '"dashboard"'; then
            services+=("dashboard")
        fi
        if echo "$health_data" | grep -q '"database"'; then
            services+=("database")
        fi
    fi
    
    echo "${services[@]}"
}

# Main monitoring loop
main() {
    log_info "Starting recovery watchdog monitoring loop"
    
    while true; do
        log_info "Checking system health..."
        
        # Check health endpoint
        if ! health_data=$(check_health); then
            log_error "Failed to check health endpoint"
            sleep $CHECK_INTERVAL
            continue
        fi
        
        # Check error budget status
        critical_count=$(check_error_budget "$health_data")
        
        if [[ $critical_count -gt 0 ]]; then
            log_warning "Detected $critical_count critical service(s)"
            
            # Identify critical services
            critical_services=($(identify_critical_services "$health_data"))
            
            for service in "${critical_services[@]}"; do
                if [[ -n "$service" ]]; then
                    log_warning "Service $service is critical"
                    
                    # Determine recovery action
                    action_type=$(determine_recovery_action "$health_data" "$service")
                    
                    # Trigger recovery
                    if trigger_recovery "$service" "$action_type" "Error budget threshold exceeded"; then
                        log_info "Recovery action triggered for $service"
                    else
                        log_error "Failed to trigger recovery for $service"
                    fi
                fi
            done
        else
            log_info "All services healthy"
        fi
        
        # Wait before next check
        sleep $CHECK_INTERVAL
    done
}

# Signal handling
cleanup() {
    log_info "Recovery watchdog stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start monitoring
main "$@"
