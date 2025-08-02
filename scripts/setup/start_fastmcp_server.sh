#!/bin/bash

# Living Truth Engine FastMCP Server Startup Script
# This script starts the FastMCP server locally

set -e

echo "🚀 Starting Living Truth Engine FastMCP Server..."

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Check if we're in the right directory
if [ ! -f "living_truth_fastmcp_server.py" ]; then
    echo "❌ Error: living_truth_fastmcp_server.py not found in project directory"
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

# Start the FastMCP server
echo "🚀 Starting FastMCP server..."
echo "📝 Logs will be written to logs/living_truth_fastmcp.log"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python living_truth_fastmcp_server.py 