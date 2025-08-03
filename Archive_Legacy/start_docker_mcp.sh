#!/bin/bash

# Living Truth Engine Docker MCP Server Startup Script
# This script starts the FastMCP server in Docker

set -e

echo "🐳 Starting Living Truth Engine MCP Server in Docker..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found in current directory"
    echo "Please run this script from the LivingTruthEngine directory"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create a .env file with your configuration"
    echo "Required variables:"
    echo "  - FLOWISE_API_KEY"
    echo "  - FLOWISE_CHATFLOW_ID"
    echo "  - LANGCHAIN_API_KEY"
    echo "  - SERP_API_KEY"
fi

# Build and start the services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo "✅ Services started!"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "📝 View logs:"
echo "  docker-compose logs -f living-truth-mcp"
echo ""
echo "🛑 Stop services:"
echo "  docker-compose down"
echo ""
echo "🌐 MCP Server should be available on port 8000"
echo "🔗 Flowise should be available on port 3000" 