#!/bin/bash

# Living Truth Engine - Start Flowise Only
# This script starts Flowise and its dependencies independently

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}Living Truth Engine - Start Flowise Only${NC}"
echo "=============================================="

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Stop any existing services to avoid conflicts
print_status "Stopping any existing services..."
docker compose -f docker/docker-compose.flowise.yml down 2>/dev/null || true

# Start Flowise services
print_status "Starting Flowise services..."
docker compose -f docker/docker-compose.flowise.yml up -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.flowise.yml ps postgres | grep -q "healthy"; then
        print_status "PostgreSQL is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_error "PostgreSQL failed to start within 60 seconds"
    exit 1
fi

# Wait for Flowise
print_status "Waiting for Flowise..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.flowise.yml ps flowise | grep -q "healthy"; then
        print_status "Flowise is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_error "Flowise failed to start within 60 seconds"
    exit 1
fi

# Wait for MCP Server
print_status "Waiting for MCP Server..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.flowise.yml ps living-truth-mcp | grep -q "Up"; then
        print_status "MCP Server is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_warning "MCP Server may still be starting up"
fi

echo ""
echo -e "${BLUE}Flowise Services Status:${NC}"
echo "=========================="
docker compose -f docker/docker-compose.flowise.yml ps

echo ""
echo -e "${BLUE}Service Information:${NC}"
echo "========================"
echo -e "${GREEN}Flowise:${NC} http://localhost:3000"
echo -e "${GREEN}MCP Server:${NC} http://localhost:8000"
echo -e "${GREEN}PostgreSQL:${NC} localhost:5434"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo "============"
echo "1. Open Flowise at http://localhost:3000"
echo "2. Import your chatflows and workflows"
echo "3. Configure environment variables in .env file:"
echo "   - FLOWISE_API_KEY"
echo "   - FLOWISE_CHATFLOW_ID"
echo "   - SERP_API_KEY"
echo "4. Test the MCP server at http://localhost:8000"
echo ""

print_status "Flowise services started successfully!" 