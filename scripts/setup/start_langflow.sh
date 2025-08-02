#!/bin/bash

# Living Truth Engine - Start Langflow Only
# This script starts Langflow and its dependencies independently

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}Living Truth Engine - Start Langflow Only${NC}"
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
docker compose -f docker/docker-compose.langflow.yml down 2>/dev/null || true

# Start Langflow services
print_status "Starting Langflow services..."
docker compose -f docker/docker-compose.langflow.yml up -d

# Wait for services to be healthy
print_status "Waiting for services to be ready..."

# Wait for PostgreSQL
print_status "Waiting for PostgreSQL..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.langflow.yml ps postgres | grep -q "healthy"; then
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

# Wait for LM Studio
print_status "Waiting for LM Studio..."
timeout=120
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.langflow.yml ps lm-studio | grep -q "healthy"; then
        print_status "LM Studio is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_warning "LM Studio may still be starting up (this can take a while)"
fi

# Wait for Langflow
print_status "Waiting for Langflow..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.langflow.yml ps langflow | grep -q "healthy"; then
        print_status "Langflow is ready!"
        break
    fi
    sleep 2
    timeout=$((timeout - 2))
done

if [ $timeout -le 0 ]; then
    print_error "Langflow failed to start within 60 seconds"
    print_status "Checking Langflow logs..."
    docker compose -f docker/docker-compose.langflow.yml logs langflow --tail=20
    exit 1
fi

# Wait for MCP Server
print_status "Waiting for MCP Server..."
timeout=60
while [ $timeout -gt 0 ]; do
    if docker compose -f docker/docker-compose.langflow.yml ps living-truth-mcp | grep -q "Up"; then
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
echo -e "${BLUE}Langflow Services Status:${NC}"
echo "============================="
docker compose -f docker/docker-compose.langflow.yml ps

echo ""
echo -e "${BLUE}Service Information:${NC}"
echo "========================"
echo -e "${GREEN}Langflow:${NC} http://localhost:3100"
echo -e "${GREEN}LM Studio:${NC} http://localhost:1235"
echo -e "${GREEN}MCP Server:${NC} http://localhost:8000"
echo -e "${GREEN}PostgreSQL:${NC} localhost:5433"
echo ""

echo -e "${BLUE}Next Steps:${NC}"
echo "============"
echo "1. Open Langflow at http://localhost:3100"
echo "2. Login with admin/admin"
echo "3. Import the Forensic Analysis workflow"
echo "4. Configure environment variables in .env file:"
echo "   - LANGFLOW_API_KEY"
echo "   - BRAVE_API_KEY"
echo "5. Test the MCP server at http://localhost:8000"
echo ""

print_status "Langflow services started successfully!" 