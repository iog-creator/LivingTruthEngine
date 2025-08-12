#!/bin/bash

# Living Truth Engine - New UI Workflow Verification Script
# Tests the complete workflow systematically

set -e

echo "🚀 Living Truth Engine - New UI Workflow Verification"
echo "=================================================="

API_BASE="http://localhost:8050"
UI_URL="$API_BASE/static/ui_status_chat.html"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

test_endpoint() {
    local endpoint=$1
    local method=${2:-GET}
    local data=${3:-}
    
    if [ "$method" = "POST" ] && [ -n "$data" ]; then
        response=$(curl -s -X POST "$API_BASE$endpoint" \
            -H "Content-Type: application/json" \
            -d "$data" 2>/dev/null || echo '{"status":"fail","error":"curl failed"}')
    else
        response=$(curl -s "$API_BASE$endpoint" 2>/dev/null || echo '{"status":"fail","error":"curl failed"}')
    fi
    
    echo "$response"
}

# Test 1: Health Check
log_info "Testing health endpoint..."
health_response=$(test_endpoint "/api/health")
if echo "$health_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
    log_success "Health endpoint working"
else
    log_error "Health endpoint failed: $health_response"
    exit 1
fi

# Test 2: Tools Check
log_info "Testing tools endpoint..."
tools_response=$(test_endpoint "/api/tools")
if echo "$tools_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
    categories=$(echo "$tools_response" | jq -r '.data.categories | keys | length')
    log_success "Tools endpoint working - found $categories categories"
else
    log_error "Tools endpoint failed: $tools_response"
    exit 1
fi

# Test 3: Runs Check
log_info "Testing runs endpoint..."
runs_response=$(test_endpoint "/api/runs")
if echo "$runs_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
    run_count=$(echo "$runs_response" | jq -r '.data | length')
    log_success "Runs endpoint working - found $run_count runs"
    
    if [ "$run_count" -gt 0 ]; then
        latest_run=$(echo "$runs_response" | jq -r '.data[0].run_id')
        log_info "Latest run: $latest_run"
    else
        log_warning "No runs found - will create one for testing"
    fi
else
    log_error "Runs endpoint failed: $runs_response"
    exit 1
fi

# Test 4: Create a new run if needed
if [ "$run_count" -eq 0 ] || [ -z "$latest_run" ]; then
    log_info "Creating a new YouTube analysis run..."
    run_data='{"channel_url":"https://www.youtube.com/@imaginationpodcastofficial","limit":1,"max_depth":1}'
    run_response=$(test_endpoint "/api/runs/youtube/start" "POST" "$run_data")
    
    if echo "$run_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
        latest_run=$(echo "$run_response" | jq -r '.data.run_id')
        log_success "Created new run: $latest_run"
    else
        log_error "Failed to create run: $run_response"
        exit 1
    fi
fi

# Test 5: Analysis Summary
log_info "Testing analysis summary..."
summary_data="{\"tool_name\":\"analyze_veritas_summary\",\"params\":{\"run_id\":\"$latest_run\"}}"
summary_response=$(test_endpoint "/api/execute" "POST" "$summary_data")

if echo "$summary_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
    log_success "Analysis summary working"
else
    log_error "Analysis summary failed: $summary_response"
    exit 1
fi

# Test 6: Analysis Claims
log_info "Testing analysis claims..."
claims_data="{\"tool_name\":\"analyze_veritas_claims\",\"params\":{\"run_id\":\"$latest_run\"}}"
claims_response=$(test_endpoint "/api/execute" "POST" "$claims_data")

if echo "$claims_response" | jq -e '.status == "ok"' >/dev/null 2>&1; then
    log_success "Analysis claims working"
else
    log_error "Analysis claims failed: $claims_response"
    exit 1
fi

# Test 7: UI Accessibility
log_info "Testing UI accessibility..."
ui_response=$(curl -s "$UI_URL" 2>/dev/null || echo "FAILED")

if echo "$ui_response" | grep -q "html" >/dev/null 2>&1; then
    log_success "UI accessible"
else
    log_error "UI not accessible"
    exit 1
fi

# Test 8: Complete Workflow Test
log_info "Testing complete workflow..."
echo "Running Python test script..."
if python scripts/test_new_ui.py >/dev/null 2>&1; then
    log_success "Complete workflow test passed"
else
    log_error "Complete workflow test failed"
    exit 1
fi

echo ""
echo "🎉 All verification tests passed!"
echo "=================================================="
echo "📱 New UI is ready to use at: $UI_URL"
echo ""
echo "🔧 How to use:"
echo "1. Open the UI in your browser"
echo "2. Click 'Proof-of-Life' to test the complete workflow"
echo "3. Select a run from the dropdown"
echo "4. Use 'Get Summary' or 'Get Claims' to analyze content"
echo ""
echo "✨ Features:"
echo "- Status stack showing LLM, Embedding, and progress"
echo "- Real-time analysis with visual feedback"
echo "- Clean, modern interface with dark theme"
echo "- Works with existing MCP tools and API endpoints"
echo ""
echo "🚀 The new dashboard is working perfectly!"




