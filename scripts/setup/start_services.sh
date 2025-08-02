#!/bin/bash

# Living Truth Engine - Service Startup Script
# This script starts all required services using Docker Compose

set -e

echo "🚀 Starting Living Truth Engine Services..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check for Docker Compose v2 (required)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
    echo "✅ Using Docker Compose v2"
else
    echo "❌ Docker Compose v2 is not available. Please install it first."
    echo "💡 Run: ./scripts/setup/update_system.sh to install"
    exit 1
fi

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Load environment variables
if [ -f "../.env" ]; then
    echo "📋 Loading environment variables from .env"
    # Load environment variables, excluding comments and empty lines
    set -a
    source <(cat ../.env | grep -v '^#' | grep -v '^$')
    set +a
else
    echo "⚠️  No .env file found. Using default values."
fi

# Validate compose file first
echo "🔍 Validating Docker Compose configuration..."
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml config

# Start services with BuildKit
echo "🐳 Starting Docker services with BuildKit..."
DOCKER_BUILDKIT=1 $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml up -d --build

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service status
echo "📊 Service Status:"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml ps

# Show logs
echo "📋 Recent logs:"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml logs --tail=20

echo ""
echo "✅ Services started successfully!"
echo ""
echo "🌐 Service URLs:"
echo "   - Flowise Dashboard: http://localhost:3000"
echo "   - PostgreSQL Database: localhost:5432"
echo "   - MCP Server: localhost:8000"
echo ""
echo "📝 To view logs: $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml logs -f"
echo "🛑 To stop services: $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml down" 