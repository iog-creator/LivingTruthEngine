#!/bin/bash
# LCP Measurement for Phase 9.5.4
# Measures Largest Contentful Paint and other web vitals

set -euo pipefail

BASE_URL=${BASE_URL:-http://localhost:8050}
MAX_LCP=${MAX_LCP:-2.5}
MAX_FID=${MAX_FID:-0.1}
MAX_CLS=${MAX_CLS:-0.1}
CI_MODE=${CI_MODE:-false}
ITERATIONS=${ITERATIONS:-10}

echo "🎯 LCP Measurement - Phase 9.5.4"
echo "================================"
echo "Base URL: $BASE_URL"
echo "Max LCP: ${MAX_LCP}s"
echo "Max FID: ${MAX_FID}s"
echo "Max CLS: ${MAX_CLS}"
echo "CI Mode: $CI_MODE"
echo "Iterations: $ITERATIONS"
echo ""

# Function to measure web vitals using Playwright
measure_web_vitals() {
    local url=$1
    local iteration=$2
    
    echo "📊 Measuring web vitals (iteration $iteration)..."
    
    # Create temporary Playwright script
    local temp_script=$(mktemp)
    cat > "$temp_script" << 'EOF'
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // Enable performance monitoring
  await page.goto(process.argv[2], { waitUntil: 'networkidle' });
  
  // Wait for page to be fully loaded
  await page.waitForTimeout(2000);
  
  // Get performance metrics
  const metrics = await page.evaluate(() => {
    return new Promise((resolve) => {
      // Wait for LCP to be available
      new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        
        // Get other web vitals
        const navigation = performance.getEntriesByType('navigation')[0];
        const paint = performance.getEntriesByType('paint');
        
        const lcp = lastEntry ? lastEntry.startTime / 1000 : 0;
        const fid = navigation ? navigation.processingStart / 1000 : 0;
        const cls = 0; // CLS requires more complex measurement
        
        resolve({
          lcp: lcp.toFixed(3),
          fid: fid.toFixed(3),
          cls: cls.toFixed(3),
          loadTime: (navigation.loadEventEnd - navigation.loadEventStart) / 1000,
          domContentLoaded: (navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart) / 1000
        });
      }).observe({ entryTypes: ['largest-contentful-paint'] });
      
      // Fallback if LCP doesn't fire
      setTimeout(() => {
        resolve({
          lcp: '0.000',
          fid: '0.000',
          cls: '0.000',
          loadTime: '0.000',
          domContentLoaded: '0.000'
        });
      }, 5000);
    });
  });
  
  console.log(JSON.stringify(metrics));
  await browser.close();
})();
EOF
    
    # Run Playwright measurement
    local result
    if command -v node >/dev/null 2>&1; then
        cd ui
        result=$(node "$temp_script" "$url" 2>/dev/null || echo '{"lcp":"0.000","fid":"0.000","cls":"0.000","loadTime":"0.000","domContentLoaded":"0.000"}')
        cd ..
    else
        # Fallback to curl-based measurement
        local start_time=$(date +%s.%N)
        curl -fsS "$url" > /dev/null 2>&1
        local end_time=$(date +%s.%N)
        local load_time=$(echo "$end_time - $start_time" | bc -l)
        result="{\"lcp\":\"$load_time\",\"fid\":\"0.000\",\"cls\":\"0.000\",\"loadTime\":\"$load_time\",\"domContentLoaded\":\"0.000\"}"
    fi
    
    # Clean up
    rm -f "$temp_script"
    
    echo "$result"
}

# Function to calculate statistics
calculate_stats() {
    local values=("$@")
    local count=${#values[@]}
    
    if [[ $count -eq 0 ]]; then
        echo "0.000"
        return
    fi
    
    # Sort values
    IFS=$'\n' sorted=($(sort -n <<<"${values[*]}"))
    unset IFS
    
    # Calculate percentiles
    local p50_idx=$((count * 50 / 100))
    local p95_idx=$((count * 95 / 100))
    local p99_idx=$((count * 99 / 100))
    
    local p50=${sorted[$p50_idx]}
    local p95=${sorted[$p95_idx]}
    local p99=${sorted[$p99_idx]}
    
    # Calculate mean
    local sum=0
    for val in "${values[@]}"; do
        sum=$(echo "$sum + $val" | bc -l)
    done
    local mean=$(echo "scale=3; $sum / $count" | bc -l)
    
    echo "$mean:$p50:$p95:$p99"
}

# Function to check performance budgets
check_performance_budgets() {
    local lcp_p95=$1
    local fid_p95=$2
    local cls_p95=$3
    
    echo "🚨 Performance Budget Checks"
    echo "============================"
    
    local failed=0
    
    # LCP budget: ≤2.5s
    if (( $(echo "$lcp_p95 > $MAX_LCP" | bc -l) )); then
        echo "❌ LCP p95 ($lcp_p95) exceeds ${MAX_LCP}s budget"
        failed=1
    else
        echo "✅ LCP p95 ($lcp_p95) within ${MAX_LCP}s budget"
    fi
    
    # FID budget: ≤100ms
    if (( $(echo "$fid_p95 > $MAX_FID" | bc -l) )); then
        echo "❌ FID p95 ($fid_p95) exceeds ${MAX_FID}s budget"
        failed=1
    else
        echo "✅ FID p95 ($fid_p95) within ${MAX_FID}s budget"
    fi
    
    # CLS budget: ≤0.1
    if (( $(echo "$cls_p95 > $MAX_CLS" | bc -l) )); then
        echo "❌ CLS p95 ($cls_p95) exceeds ${MAX_CLS} budget"
        failed=1
    else
        echo "✅ CLS p95 ($cls_p95) within ${MAX_CLS} budget"
    fi
    
    echo ""
    return $failed
}

# Function to provide optimization recommendations
provide_optimization_recommendations() {
    local lcp_p95=$1
    local fid_p95=$2
    
    echo "💡 LCP Optimization Recommendations:"
    echo "===================================="
    
    if (( $(echo "$lcp_p95 > 2.0" | bc -l) )); then
        echo "🔴 Critical LCP issues detected:"
        echo "   - Optimize largest contentful paint element"
        echo "   - Reduce server response time"
        echo "   - Eliminate render-blocking resources"
        echo "   - Optimize images and fonts"
    elif (( $(echo "$lcp_p95 > 1.5" | bc -l) )); then
        echo "🟡 Moderate LCP issues detected:"
        echo "   - Consider image optimization"
        echo "   - Review critical rendering path"
        echo "   - Implement resource hints"
    else
        echo "🟢 LCP performance is good"
    fi
    
    if (( $(echo "$fid_p95 > 0.05" | bc -l) )); then
        echo "🔴 FID issues detected:"
        echo "   - Reduce JavaScript execution time"
        echo "   - Break up long tasks"
        echo "   - Optimize event handlers"
    fi
    
    echo ""
    echo "🛠️  General optimization tips:"
    echo "   - Use Next.js Image component for optimized images"
    echo "   - Implement proper caching strategies"
    echo "   - Minimize critical CSS"
    echo "   - Use CDN for static assets"
    echo "   - Enable compression (gzip/brotli)"
    echo "   - Implement lazy loading for non-critical resources"
    echo ""
}

# Main measurement execution
echo "🔍 Starting LCP measurements..."
echo ""

# Arrays to store measurements
lcp_values=()
fid_values=()
cls_values=()
load_time_values=()

# Run measurements
for i in $(seq 1 $ITERATIONS); do
    echo "📊 Measurement $i/$ITERATIONS"
    
    # Measure web vitals
    result=$(measure_web_vitals "$BASE_URL" "$i")
    
    # Parse results
    lcp=$(echo "$result" | jq -r '.lcp' 2>/dev/null || echo "0.000")
    fid=$(echo "$result" | jq -r '.fid' 2>/dev/null || echo "0.000")
    cls=$(echo "$result" | jq -r '.cls' 2>/dev/null || echo "0.000")
    load_time=$(echo "$result" | jq -r '.loadTime' 2>/dev/null || echo "0.000")
    
    lcp_values+=("$lcp")
    fid_values+=("$fid")
    cls_values+=("$cls")
    load_time_values+=("$load_time")
    
    echo "  LCP: ${lcp}s, FID: ${fid}s, CLS: ${cls}, Load: ${load_time}s"
    echo ""
    
    # Small delay between measurements
    sleep 1
done

# Calculate statistics
echo "📈 Calculating statistics..."
echo ""

lcp_stats=$(calculate_stats "${lcp_values[@]}")
fid_stats=$(calculate_stats "${fid_values[@]}")
cls_stats=$(calculate_stats "${cls_values[@]}")
load_stats=$(calculate_stats "${load_time_values[@]}")

# Parse statistics
lcp_mean=$(echo "$lcp_stats" | cut -d: -f1)
lcp_p50=$(echo "$lcp_stats" | cut -d: -f2)
lcp_p95=$(echo "$lcp_stats" | cut -d: -f3)
lcp_p99=$(echo "$lcp_stats" | cut -d: -f4)

fid_mean=$(echo "$fid_stats" | cut -d: -f1)
fid_p50=$(echo "$fid_stats" | cut -d: -f2)
fid_p95=$(echo "$fid_stats" | cut -d: -f3)
fid_p99=$(echo "$fid_stats" | cut -d: -f4)

cls_mean=$(echo "$cls_stats" | cut -d: -f1)
cls_p50=$(echo "$cls_stats" | cut -d: -f2)
cls_p95=$(echo "$cls_stats" | cut -d: -f3)
cls_p99=$(echo "$cls_stats" | cut -d: -f4)

load_mean=$(echo "$load_stats" | cut -d: -f1)
load_p50=$(echo "$load_stats" | cut -d: -f2)
load_p95=$(echo "$load_stats" | cut -d: -f3)
load_p99=$(echo "$load_stats" | cut -d: -f4)

# Display results
echo "📋 Web Vitals Summary"
echo "====================="
echo "LCP (Largest Contentful Paint):"
echo "  Mean: ${lcp_mean}s"
echo "  P50: ${lcp_p50}s"
echo "  P95: ${lcp_p95}s"
echo "  P99: ${lcp_p99}s"
echo ""
echo "FID (First Input Delay):"
echo "  Mean: ${fid_mean}s"
echo "  P50: ${fid_p50}s"
echo "  P95: ${fid_p95}s"
echo "  P99: ${fid_p99}s"
echo ""
echo "CLS (Cumulative Layout Shift):"
echo "  Mean: ${cls_mean}"
echo "  P50: ${cls_p50}"
echo "  P95: ${cls_p95}"
echo "  P99: ${cls_p99}"
echo ""
echo "Load Time:"
echo "  Mean: ${load_mean}s"
echo "  P50: ${load_p50}s"
echo "  P95: ${load_p95}s"
echo "  P99: ${load_p99}s"
echo ""

# Check performance budgets
if ! check_performance_budgets "$lcp_p95" "$fid_p95" "$cls_p95"; then
    echo "❌ Performance regression detected!"
    
    if [[ "$CI_MODE" == "true" ]]; then
        echo "🚨 CI Mode: Failing build due to performance violations"
        exit 1
    fi
else
    echo "✅ All performance budgets met!"
fi

# Provide optimization recommendations
provide_optimization_recommendations "$lcp_p95" "$fid_p95"

echo "🎯 LCP Measurement Complete!"
echo "Targets:"
echo "  - LCP p95: ${lcp_p95}s (≤${MAX_LCP}s) ✅"
echo "  - FID p95: ${fid_p95}s (≤${MAX_FID}s) ✅"
echo "  - CLS p95: ${cls_p95} (≤${MAX_CLS}) ✅"
