#!/bin/bash

# Living Truth Engine - Performance Testing Script
# Measures response times for various operations

set -e

echo "🏃 Living Truth Engine Performance Testing"
echo "=========================================="

# Activate virtual environment
if [ -f "living_venv/bin/activate" ]; then
    source living_venv/bin/activate
    echo "✅ Virtual environment activated"
elif [ -f "../living_venv/bin/activate" ]; then
    source ../living_venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Test queries
queries=(
    "Test query 1 - Basic analysis"
    "Test query 2 - Pattern recognition"
    "Test query 3 - Evidence correlation"
)

echo ""
echo "📊 Testing Langflow Query Performance"
echo "------------------------------------"

for query in "${queries[@]}"; do
    echo "Testing: $query"
    
    # Measure response time
    start_time=$(date +%s.%N)
    
    # Use Python to test the query
    python3 -c "
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'src'))

try:
    from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    result = engine.query_langflow('$query', output_type='summary')
    
    if '✅' in result or 'successful' in result.lower():
        print('✅ Success')
    else:
        print('❌ Failed')
        
except Exception as e:
    print(f'❌ Error: {e}')
"
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    echo "⏱️  Response time: ${duration}s"
    
    # Check if response time exceeds 5 seconds
    if (( $(echo "$duration > 5" | bc -l) )); then
        echo "⚠️  WARNING: Response time exceeds 5 seconds"
    fi
    
    echo ""
done

echo "📊 Testing MCP Tool Performance"
echo "-------------------------------"

# Test MCP tools
mcp_tests=(
    "get_status"
    "list_sources"
    "generate_viz"
)

for test in "${mcp_tests[@]}"; do
    echo "Testing MCP tool: $test"
    
    start_time=$(date +%s.%N)
    
    python3 -c "
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'src'))

try:
    from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    if '$test' == 'get_status':
        result = engine.get_status()
    elif '$test' == 'list_sources':
        result = engine.list_sources()
    elif '$test' == 'generate_viz':
        result = engine.generate_visualization('network')
    else:
        result = 'Unknown test'
    
    if '✅' in result or '📁' in result:
        print('✅ Success')
    else:
        print('❌ Failed')
        
except Exception as e:
    print(f'❌ Error: {e}')
"
    
    end_time=$(date +%s.%N)
    duration=$(echo "$end_time - $start_time" | bc)
    
    echo "⏱️  Response time: ${duration}s"
    
    if (( $(echo "$duration > 2" | bc -l) )); then
        echo "⚠️  WARNING: Response time exceeds 2 seconds"
    fi
    
    echo ""
done

echo "📊 Testing LM Studio Performance"
echo "--------------------------------"

# Test LM Studio connection
echo "Testing LM Studio connection:"
start_time=$(date +%s.%N)

python3 -c "
import time
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'src'))

try:
    from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    result = engine.get_lm_studio_status()
    
    if '✅' in result:
        print('✅ LM Studio healthy')
    else:
        print('❌ LM Studio issues')
        
except Exception as e:
    print(f'❌ Error: {e}')
"

end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)

echo "⏱️  Response time: ${duration}s"

if (( $(echo "$duration > 1" | bc -l) )); then
    echo "⚠️  WARNING: LM Studio response time exceeds 1 second"
fi

echo ""
echo "📋 Performance Summary"
echo "====================="
echo "✅ Performance testing completed"
echo "📊 Check response times above for any warnings"
echo "🎯 Target: <2s for API calls, <5s for complex operations"
echo ""
echo "💡 Optimization Tips:"
echo "  - Check LM Studio configuration (THREADS, GPU_LAYERS)"
echo "  - Monitor system resources (CPU, memory)"
echo "  - Review Docker container performance"
echo "  - Consider caching for repeated operations" 