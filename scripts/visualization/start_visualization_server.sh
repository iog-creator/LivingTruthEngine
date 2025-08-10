#!/bin/bash

# MCP Visualization Server Startup Script
# This script starts the FastAPI server that serves the interactive visualization

set -e

# Get the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "🚀 Starting MCP Visualization Server..."
echo "Project root: $PROJECT_ROOT"

# Change to project root
cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "living_venv" ]; then
    echo "📦 Activating virtual environment..."
    source living_venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if required packages are installed
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null || {
    echo "❌ Required packages not found. Installing..."
    pip install fastapi uvicorn
}

# Check if MCP Hub Server is accessible
echo "🔍 Testing MCP Hub Server connection..."
python -c "
import sys
sys.path.insert(0, 'src')
from mcp_servers.mcp_hub_server import MCPHubServer
hub = MCPHubServer()
status = hub.get_status()
print(f'✅ MCP Hub Server status: {status}')
" || {
    echo "❌ MCP Hub Server not accessible. Please ensure it's running."
    exit 1
}

# Start the visualization server
echo "🌐 Starting FastAPI server on http://localhost:8081..."
echo "📊 Visualization will be available at: http://localhost:8081"
echo "🔧 API documentation will be available at: http://localhost:8081/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python scripts/visualization/mcp_visualization_api.py
