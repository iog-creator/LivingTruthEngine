#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$PROJECT_ROOT"

echo "🚀 Starting Living Truth Engine - Unified Dashboard"
echo "📍 Project root: $PROJECT_ROOT"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source living_venv/bin/activate

# Check dependencies
echo "🔍 Checking dependencies..."
python -c "import fastapi, uvicorn, jinja2" 2>/dev/null || {
    echo "📥 Installing missing dependencies..."
    pip install fastapi uvicorn jinja2
}

# Check MCP Hub Server accessibility
echo "🔗 Checking MCP Hub Server..."
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

# Check port availability
PORT=8082
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port $PORT is already in use. Please stop the service using that port."
    exit 1
fi

echo "🌐 Starting Unified Dashboard on http://localhost:$PORT..."
echo "📚 API Documentation: http://localhost:$PORT/docs"
echo "❤️  Health Check: http://localhost:$PORT/api/health"

# Start the dashboard
python src/dashboard/unified_dashboard.py

