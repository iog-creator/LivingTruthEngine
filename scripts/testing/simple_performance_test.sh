#!/bin/bash

# Living Truth Engine - Simple Performance Testing Script
# Tests service response times using direct HTTP calls

set -e

echo "🏃 Living Truth Engine Simple Performance Testing"
echo "================================================"

# Test Langflow health
echo "📊 Testing Langflow Health"
echo "-------------------------"
start_time=$(date +%s.%N)
if curl -f http://localhost:7860/health > /dev/null 2>&1; then
    echo "✅ Langflow healthy"
else
    echo "❌ Langflow not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

# Test LM Studio health
echo "📊 Testing LM Studio Health"
echo "---------------------------"
start_time=$(date +%s.%N)
if curl -f http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "✅ LM Studio healthy"
else
    echo "❌ LM Studio not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

# Test PostgreSQL health
echo "📊 Testing PostgreSQL Health"
echo "----------------------------"
start_time=$(date +%s.%N)
if pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "✅ PostgreSQL healthy"
else
    echo "❌ PostgreSQL not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

# Test Redis health
echo "📊 Testing Redis Health"
echo "----------------------"
start_time=$(date +%s.%N)
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis healthy"
else
    echo "❌ Redis not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

# Test Neo4j health
echo "📊 Testing Neo4j Health"
echo "----------------------"
start_time=$(date +%s.%N)
if curl -f http://localhost:7474 > /dev/null 2>&1; then
    echo "✅ Neo4j healthy"
else
    echo "❌ Neo4j not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

# Test Living Truth Engine health
echo "📊 Testing Living Truth Engine Health"
echo "------------------------------------"
start_time=$(date +%s.%N)
if curl -f http://localhost:9123/health > /dev/null 2>&1; then
    echo "✅ Living Truth Engine healthy"
else
    echo "❌ Living Truth Engine not responding"
fi
end_time=$(date +%s.%N)
duration=$(echo "$end_time - $start_time" | bc)
echo "⏱️  Response time: ${duration}s"
echo ""

echo "📋 Performance Summary"
echo "====================="
echo "✅ Simple performance testing completed"
echo "📊 All services should respond in <2s"
echo "🎯 Target: <2s for API calls, <5s for complex operations"
echo ""
echo "💡 Optimization Tips:"
echo "  - Check LM Studio configuration (THREADS, GPU_LAYERS)"
echo "  - Monitor system resources (CPU, memory)"
echo "  - Review Docker container performance"
echo "  - Consider caching for repeated operations" 