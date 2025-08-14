#!/bin/bash
# Enhanced Performance Harness for Phase 9.5.4
# Measures p95 latencies for API endpoints with baseline management

set -euo pipefail

BASE=${BASE:-http://localhost:8050}
RUN_ID=${1:-"20250813_210021_youtube-analysis--https---www-youtube-co"}
BASELINE_FILE=${BASELINE_FILE:-./perf_baseline.json}
CI_MODE=${CI_MODE:-false}
ITERATIONS=${ITERATIONS:-100}
WARMUP_RUNS=${WARMUP_RUNS:-10}

echo "🧪 Enhanced Performance Harness - Phase 9.5.4"
echo "=============================================="
echo "Base URL: $BASE"
echo "Run ID: $RUN_ID"
echo "Baseline: $BASELINE_FILE"
echo "CI Mode: $CI_MODE"
echo "Iterations: $ITERATIONS"
echo ""

# Function to measure p95 latency with detailed statistics
measure_p95() {
    local endpoint=$1
    local name=$2
    local warmup_runs=${3:-$WARMUP_RUNS}
    local measure_runs=${4:-$ITERATIONS}
    
    echo "📊 Measuring $name ($endpoint)"
    
    # Warm up
    echo "  Warming up ($warmup_runs runs)..."
    for i in $(seq 1 $warmup_runs); do
        curl -fsS "$BASE$endpoint" > /dev/null 2>&1
    done
    
    # Measure
    echo "  Measuring ($measure_runs runs)..."
    times=()
    for i in $(seq 1 $measure_runs); do
        t=$( (TIMEFORMAT=%R; time curl -fsS "$BASE$endpoint" > /dev/null 2>&1) 2>&1 )
        times+=("$t")
    done
    
    # Calculate statistics
    p50=$(printf "%s\n" "${times[@]}" | sort -n | awk 'NR==int(0.50*NR_current){print; exit}')
    p95=$(printf "%s\n" "${times[@]}" | sort -n | awk 'NR==int(0.95*NR_current){print; exit}')
    p99=$(printf "%s\n" "${times[@]}" | sort -n | awk 'NR==int(0.99*NR_current){print; exit}')
    mean=$(printf "%s\n" "${times[@]}" | awk '{sum+=$1} END {print sum/NR}')
    min=$(printf "%s\n" "${times[@]}" | sort -n | head -1)
    max=$(printf "%s\n" "${times[@]}" | sort -n | tail -1)
    
    echo "  📈 $name Statistics:"
    echo "    Mean: ${mean}s"
    echo "    P50: ${p50}s"
    echo "    P95: ${p95}s"
    echo "    P99: ${p99}s"
    echo "    Min: ${min}s"
    echo "    Max: ${max}s"
    echo ""
    
    # Return p95 value for CI gates
    echo "${name}_p95_s=$p95"
    echo "${name}_mean_s=$mean"
    echo "${name}_p99_s=$p99"
}

# Function to check performance budgets
check_performance_budgets() {
    local timeline_p95=$1
    local graph_p95=$2
    local build_duration=$3
    
    echo "🚨 Performance Budget Checks"
    echo "============================"
    
    local failed=0
    
    # Timeline API budget: ≤1.0s
    if (( $(echo "$timeline_p95 > 1.0" | bc -l) )); then
        echo "❌ Timeline API p95 ($timeline_p95) exceeds 1.0s budget"
        failed=1
    else
        echo "✅ Timeline API p95 ($timeline_p95) within 1.0s budget"
    fi
    
    # Graph API budget: ≤1.5s
    if (( $(echo "$graph_p95 > 1.5" | bc -l) )); then
        echo "❌ Graph API p95 ($graph_p95) exceeds 1.5s budget"
        failed=1
    else
        echo "✅ Graph API p95 ($graph_p95) within 1.5s budget"
    fi
    
    # Graph Build budget: ≤5.0s
    if (( $(echo "$build_duration > 5.0" | bc -l) )); then
        echo "❌ Graph Build duration ($build_duration) exceeds 5.0s budget"
        failed=1
    else
        echo "✅ Graph Build duration ($build_duration) within 5.0s budget"
    fi
    
    echo ""
    return $failed
}

# Function to manage performance baseline
manage_baseline() {
    local action=$1
    local timeline_p95=$2
    local graph_p95=$3
    local build_duration=$4
    
    case $action in
        "load")
            if [[ -f "$BASELINE_FILE" ]]; then
                echo "📋 Loading performance baseline from $BASELINE_FILE"
                baseline=$(cat "$BASELINE_FILE")
                echo "Baseline loaded: $baseline"
            else
                echo "⚠️  No baseline file found: $BASELINE_FILE"
                baseline=""
            fi
            ;;
        "save")
            echo "💾 Saving performance baseline to $BASELINE_FILE"
            baseline_data=$(cat <<EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "timeline_api_p95": $timeline_p95,
  "graph_api_p95": $graph_p95,
  "graph_build_duration": $build_duration,
  "run_id": "$RUN_ID"
}
EOF
)
            echo "$baseline_data" > "$BASELINE_FILE"
            echo "Baseline saved: $baseline_data"
            ;;
        "compare")
            if [[ -f "$BASELINE_FILE" ]]; then
                echo "📊 Comparing with baseline..."
                baseline_timeline=$(jq -r '.timeline_api_p95' "$BASELINE_FILE")
                baseline_graph=$(jq -r '.graph_api_p95' "$BASELINE_FILE")
                baseline_build=$(jq -r '.graph_build_duration' "$BASELINE_FILE")
                
                timeline_diff=$(echo "$timeline_p95 - $baseline_timeline" | bc -l)
                graph_diff=$(echo "$graph_p95 - $baseline_graph" | bc -l)
                build_diff=$(echo "$build_duration - $baseline_build" | bc -l)
                
                echo "Timeline API: $timeline_p95 (baseline: $baseline_timeline, diff: ${timeline_diff}s)"
                echo "Graph API: $graph_p95 (baseline: $baseline_graph, diff: ${graph_diff}s)"
                echo "Graph Build: $build_duration (baseline: $baseline_build, diff: ${build_diff}s)"
            fi
            ;;
    esac
}

# Main performance measurement
echo "🔍 Starting performance measurements..."
echo ""

# Measure Timeline API
timeline_stats=$(measure_p95 "/api/timeline/$RUN_ID" "timeline_api")
timeline_p95=$(echo "$timeline_stats" | grep "timeline_api_p95_s" | cut -d'=' -f2)

# Measure Graph API
graph_stats=$(measure_p95 "/api/graph/$RUN_ID" "graph_api")
graph_p95=$(echo "$graph_stats" | grep "graph_api_p95_s" | cut -d'=' -f2)

# Measure Graph Build (single run for performance)
echo "📊 Measuring graph build performance"
echo "  Building graph..."
start_time=$(date +%s.%N)
curl -fsS -X POST "$BASE/api/graph/$RUN_ID/build?rebuild=1" > /dev/null 2>&1
end_time=$(date +%s.%N)
build_duration=$(echo "$end_time - $start_time" | bc -l)
echo "  ✅ Graph build duration: ${build_duration}s"
echo ""

# Performance summary
echo "📋 Performance Summary"
echo "====================="
echo "Timeline API p95: ${timeline_p95}s"
echo "Graph API p95: ${graph_p95}s"
echo "Graph Build: ${build_duration}s"
echo ""

# Baseline management
if [[ "$CI_MODE" == "true" ]]; then
    manage_baseline "compare" "$timeline_p95" "$graph_p95" "$build_duration"
else
    manage_baseline "save" "$timeline_p95" "$graph_p95" "$build_duration"
fi

# Performance budget checks
if ! check_performance_budgets "$timeline_p95" "$graph_p95" "$build_duration"; then
    echo "❌ Performance regression detected!"
    exit 1
fi

echo "✅ All performance gates passed!"
echo ""
echo "🎯 Performance Targets Met:"
echo "  - Timeline API p95: ${timeline_p95}s (≤1.0s) ✅"
echo "  - Graph API p95: ${graph_p95}s (≤1.5s) ✅"
echo "  - Graph Build: ${build_duration}s (≤5.0s) ✅"
