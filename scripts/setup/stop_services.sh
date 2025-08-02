#!/bin/bash

# Living Truth Engine - Service Stop Script
# This script stops all running services

set -e

echo "🛑 Stopping Living Truth Engine Services..."

# Navigate to the project root
cd "$(dirname "$0")/../.."

# Check for Docker Compose v2 (required)
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose v2 is not available."
    exit 1
fi

# Stop services
echo "🐳 Stopping Docker services..."
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml down

echo "✅ Services stopped successfully!"
echo ""
echo "📝 To start services again: ./scripts/setup/start_services.sh" 