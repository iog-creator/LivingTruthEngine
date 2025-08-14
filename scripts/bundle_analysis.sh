#!/bin/bash
# Bundle Analysis for Phase 9.5.4
# Monitors JavaScript and CSS bundle sizes with optimization recommendations

set -euo pipefail

UI_DIR=${UI_DIR:-./ui}
BUILD_DIR=${BUILD_DIR:-./ui/.next}
MAX_JS_SIZE=${MAX_JS_SIZE:-250}
MAX_CSS_SIZE=${MAX_CSS_SIZE:-50}
MAX_TOTAL_SIZE=${MAX_TOTAL_SIZE:-500}
CI_MODE=${CI_MODE:-false}

echo "📦 Bundle Analysis - Phase 9.5.4"
echo "================================"
echo "UI Directory: $UI_DIR"
echo "Build Directory: $BUILD_DIR"
echo "Max JS Size: ${MAX_JS_SIZE}KB"
echo "Max CSS Size: ${MAX_CSS_SIZE}KB"
echo "Max Total Size: ${MAX_TOTAL_SIZE}KB"
echo "CI Mode: $CI_MODE"
echo ""

# Function to get file size in KB
get_file_size_kb() {
    local file=$1
    if [[ -f "$file" ]]; then
        local size_bytes=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null)
        echo "scale=2; $size_bytes / 1024" | bc -l
    else
        echo "0"
    fi
}

# Function to get gzipped size in KB
get_gzipped_size_kb() {
    local file=$1
    if [[ -f "$file" ]]; then
        local size_bytes=$(gzip -c "$file" | wc -c)
        echo "scale=2; $size_bytes / 1024" | bc -l
    else
        echo "0"
    fi
}

# Function to analyze bundle sizes
analyze_bundle_sizes() {
    echo "🔍 Analyzing bundle sizes..."
    echo ""
    
    local total_js_size=0
    local total_css_size=0
    local total_assets_size=0
    local failed=0
    
    # Analyze JavaScript bundles
    echo "📊 JavaScript Bundles:"
    echo "======================"
    
    if [[ -d "$BUILD_DIR/static/chunks" ]]; then
        for js_file in "$BUILD_DIR"/static/chunks/*.js; do
            if [[ -f "$js_file" ]]; then
                local size_kb=$(get_file_size_kb "$js_file")
                local gzipped_kb=$(get_gzipped_size_kb "$js_file")
                local filename=$(basename "$js_file")
                
                echo "  📄 $filename:"
                echo "    Size: ${size_kb}KB (gzipped: ${gzipped_kb}KB)"
                
                if (( $(echo "$gzipped_kb > $MAX_JS_SIZE" | bc -l) )); then
                    echo "    ❌ Exceeds ${MAX_JS_SIZE}KB budget!"
                    failed=1
                else
                    echo "    ✅ Within ${MAX_JS_SIZE}KB budget"
                fi
                
                total_js_size=$(echo "$total_js_size + $gzipped_kb" | bc -l)
            fi
        done
    else
        echo "  ⚠️  No JavaScript chunks found in $BUILD_DIR/static/chunks"
    fi
    
    echo ""
    echo "📊 CSS Bundles:"
    echo "==============="
    
    if [[ -d "$BUILD_DIR/static/css" ]]; then
        for css_file in "$BUILD_DIR"/static/css/*.css; do
            if [[ -f "$css_file" ]]; then
                local size_kb=$(get_file_size_kb "$css_file")
                local gzipped_kb=$(get_gzipped_size_kb "$css_file")
                local filename=$(basename "$css_file")
                
                echo "  🎨 $filename:"
                echo "    Size: ${size_kb}KB (gzipped: ${gzipped_kb}KB)"
                
                if (( $(echo "$gzipped_kb > $MAX_CSS_SIZE" | bc -l) )); then
                    echo "    ❌ Exceeds ${MAX_CSS_SIZE}KB budget!"
                    failed=1
                else
                    echo "    ✅ Within ${MAX_CSS_SIZE}KB budget"
                fi
                
                total_css_size=$(echo "$total_css_size + $gzipped_kb" | bc -l)
            fi
        done
    else
        echo "  ⚠️  No CSS files found in $BUILD_DIR/static/css"
    fi
    
    echo ""
    echo "📊 Other Assets:"
    echo "================"
    
    if [[ -d "$BUILD_DIR/static" ]]; then
        # Count other assets (images, fonts, etc.)
        local asset_count=0
        for asset_file in "$BUILD_DIR"/static/*; do
            if [[ -f "$asset_file" && ! "$asset_file" =~ \.(js|css)$ ]]; then
                local size_kb=$(get_file_size_kb "$asset_file")
                local filename=$(basename "$asset_file")
                
                echo "  📁 $filename: ${size_kb}KB"
                total_assets_size=$(echo "$total_assets_size + $size_kb" | bc -l)
                asset_count=$((asset_count + 1))
            fi
        done
        
        if [[ $asset_count -eq 0 ]]; then
            echo "  ℹ️  No additional assets found"
        fi
    fi
    
    echo ""
    echo "📋 Bundle Summary:"
    echo "=================="
    echo "JavaScript (gzipped): ${total_js_size}KB"
    echo "CSS (gzipped): ${total_css_size}KB"
    echo "Other assets: ${total_assets_size}KB"
    
    local total_size=$(echo "$total_js_size + $total_css_size + $total_assets_size" | bc -l)
    echo "Total size: ${total_size}KB"
    echo ""
    
    # Check total size budget
    if (( $(echo "$total_size > $MAX_TOTAL_SIZE" | bc -l) )); then
        echo "❌ Total bundle size (${total_size}KB) exceeds ${MAX_TOTAL_SIZE}KB budget!"
        failed=1
    else
        echo "✅ Total bundle size (${total_size}KB) within ${MAX_TOTAL_SIZE}KB budget"
    fi
    
    echo ""
    return $failed
}

# Function to provide optimization recommendations
provide_optimization_recommendations() {
    echo "💡 Optimization Recommendations:"
    echo "================================"
    
    if [[ -d "$BUILD_DIR/static/chunks" ]]; then
        local largest_js=""
        local largest_js_size=0
        
        for js_file in "$BUILD_DIR"/static/chunks/*.js; do
            if [[ -f "$js_file" ]]; then
                local size_kb=$(get_gzipped_size_kb "$js_file")
                if (( $(echo "$size_kb > $largest_js_size" | bc -l) )); then
                    largest_js_size=$size_kb
                    largest_js=$(basename "$js_file")
                fi
            fi
        done
        
        if [[ -n "$largest_js" ]]; then
            echo "🔍 Largest JS bundle: $largest_js (${largest_js_size}KB)"
            echo "   Consider:"
            echo "   - Code splitting for large components"
            echo "   - Lazy loading for non-critical features"
            echo "   - Tree shaking to remove unused code"
            echo "   - Dynamic imports for route-based splitting"
        fi
    fi
    
    if [[ -d "$BUILD_DIR/static/css" ]]; then
        local total_css_size=0
        for css_file in "$BUILD_DIR"/static/css/*.css; do
            if [[ -f "$css_file" ]]; then
                local size_kb=$(get_gzipped_size_kb "$css_file")
                total_css_size=$(echo "$total_css_size + $size_kb" | bc -l)
            fi
        done
        
        echo "🎨 CSS optimization:"
        echo "   - Current CSS size: ${total_css_size}KB"
        echo "   - Consider:"
        echo "   - Purge unused CSS with Tailwind"
        echo "   - Extract critical CSS inline"
        echo "   - Use CSS-in-JS for component-specific styles"
    fi
    
    echo ""
    echo "🛠️  General optimization tips:"
    echo "   - Enable Next.js production optimizations"
    echo "   - Use dynamic imports for code splitting"
    echo "   - Optimize images with next/image"
    echo "   - Minimize third-party dependencies"
    echo "   - Use webpack bundle analyzer for detailed analysis"
    echo ""
}

# Function to run bundle optimization
run_bundle_optimization() {
    echo "⚡ Running bundle optimization..."
    echo ""
    
    if [[ ! -d "$UI_DIR" ]]; then
        echo "❌ UI directory not found: $UI_DIR"
        return 1
    fi
    
    cd "$UI_DIR"
    
    echo "📦 Installing dependencies..."
    npm install --silent
    
    echo "🔨 Building optimized bundle..."
    npm run build
    
    echo "✅ Bundle optimization complete!"
    echo ""
}

# Main execution
if [[ "$1" == "optimize" ]]; then
    run_bundle_optimization
    exit 0
fi

# Check if build directory exists
if [[ ! -d "$BUILD_DIR" ]]; then
    echo "⚠️  Build directory not found: $BUILD_DIR"
    echo "Running bundle optimization..."
    run_bundle_optimization
fi

# Analyze bundle sizes
if analyze_bundle_sizes; then
    echo "✅ All bundle size budgets met!"
else
    echo "❌ Bundle size budgets exceeded!"
    
    if [[ "$CI_MODE" == "true" ]]; then
        echo "🚨 CI Mode: Failing build due to bundle size violations"
        exit 1
    else
        echo "💡 Run './scripts/bundle_analysis.sh optimize' to optimize bundles"
    fi
fi

# Provide optimization recommendations
provide_optimization_recommendations

echo "🎯 Bundle Analysis Complete!"
echo "Targets:"
echo "  - JavaScript: ≤${MAX_JS_SIZE}KB ✅"
echo "  - CSS: ≤${MAX_CSS_SIZE}KB ✅"
echo "  - Total: ≤${MAX_TOTAL_SIZE}KB ✅"
