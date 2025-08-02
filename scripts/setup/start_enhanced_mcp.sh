#!/bin/bash

# Living Truth Engine Enhanced MCP Server Startup Script
# This script starts the enhanced MCP server with grouped functions

set -e

echo "🚀 Starting Living Truth Engine Enhanced MCP Server..."

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "src/mcp_servers/living_truth_enhanced_mcp.py" ]; then
    echo "❌ Error: living_truth_enhanced_mcp.py not found in project directory"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "living_venv" ]; then
    echo "📦 Activating virtual environment..."
    source living_venv/bin/activate
else
    echo "⚠️  Warning: living_venv not found, using system Python"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create a .env file with your configuration"
fi

# Create necessary directories
mkdir -p logs sources visualizations

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# Start the Enhanced MCP server
echo "🚀 Starting Enhanced MCP server..."
echo "📝 Logs will be written to logs/living_truth_enhanced_mcp.log"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "🔧 Available tool groups:"
echo "   - Docker Management: docker_start_services, docker_stop_services, docker_get_status, docker_view_logs"
echo "   - System Management: system_validate_setup, system_check_health, system_update_components"
echo "   - Development: dev_run_tests, dev_check_code_quality, dev_install_dependencies"
echo "   - Flowise Integration: flowise_query_chatflow, flowise_list_chatflows"
echo "   - Utilities: get_project_info, list_available_tools"
echo ""

python src/mcp_servers/living_truth_enhanced_mcp.py 