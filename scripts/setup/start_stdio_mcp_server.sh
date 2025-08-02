#!/bin/bash

# Living Truth Engine MCP Server - Stdio Mode Startup Script
# This script starts the MCP server in stdio mode (like working servers)

set -e

echo "🚀 Living Truth Engine MCP Server - Stdio Mode"

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "living_truth_mcp_server_stdio.py" ]; then
    echo "❌ Error: living_truth_mcp_server_stdio.py not found in project directory"
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

# Start the MCP server in stdio mode
echo "🚀 Starting MCP server in stdio mode..."
echo "📝 Logs will be written to logs/living_truth_mcp_stdio.log"
echo "🛑 Press Ctrl+C to stop the server"
echo ""
echo "📋 This server follows the exact same pattern as working MCP servers:"
echo "   - sequential-thinking-mcp-server"
echo "   - brave-search-mcp-server"
echo "   - github-mcp-server"
echo ""
echo "🔧 To test the server, use JSON-RPC requests like:"
echo "   echo '{\"jsonrpc\": \"2.0\", \"id\": 1, \"method\": \"initialize\", \"params\": {}}' | python living_truth_mcp_server_stdio.py"
echo ""

python living_truth_mcp_server_stdio.py 