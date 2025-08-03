#!/bin/bash

# Living Truth Engine MCP Server v2 Startup Script
# This script starts the MCP server in either stdio or HTTP mode

set -e

echo "🚀 Living Truth Engine MCP Server v2"

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "living_truth_mcp_server_v2.py" ]; then
    echo "❌ Error: living_truth_mcp_server_v2.py not found in project directory"
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

# Parse command line arguments
MODE="stdio"
HOST="0.0.0.0"
PORT="8000"

while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--mode stdio|http] [--host HOST] [--port PORT]"
            echo ""
            echo "Modes:"
            echo "  stdio  - Run as stdio server for MCP clients (default)"
            echo "  http   - Run as HTTP server with API endpoints"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run in stdio mode"
            echo "  $0 --mode http        # Run in HTTP mode on port 8000"
            echo "  $0 --mode http --port 9000  # Run in HTTP mode on port 9000"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Start the server
if [ "$MODE" = "stdio" ]; then
    echo "🚀 Starting MCP server in stdio mode..."
    echo "📝 Logs will be written to logs/living_truth_mcp_v2.log"
    echo "🛑 Press Ctrl+C to stop the server"
    echo ""
    python living_truth_mcp_server_v2.py --mode stdio
elif [ "$MODE" = "http" ]; then
    echo "🚀 Starting MCP server in HTTP mode..."
    echo "🌐 Server will be available at http://$HOST:$PORT"
    echo "📝 Logs will be written to logs/living_truth_mcp_v2.log"
    echo "🛑 Press Ctrl+C to stop the server"
    echo ""
    echo "📋 Available endpoints:"
    echo "  GET  /              - Server info"
    echo "  GET  /health        - Health check"
    echo "  GET  /tools         - List available tools"
    echo "  GET  /status        - Get system status"
    echo "  GET  /sources       - List sources"
    echo "  POST /query         - Query Flowise"
    echo "  POST /analyze       - Analyze transcript"
    echo "  POST /visualize     - Generate visualization"
    echo "  POST /fix-flow      - Fix flow"
    echo ""
    python living_truth_mcp_server_v2.py --mode http --host "$HOST" --port "$PORT"
else
    echo "❌ Invalid mode: $MODE"
    echo "Valid modes: stdio, http"
    exit 1
fi 