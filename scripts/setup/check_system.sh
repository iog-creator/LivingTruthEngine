#!/bin/bash

# Living Truth Engine - System Status Check
# Checks all components and their versions

set -e

echo "🔍 Living Truth Engine - System Status Check"
echo "============================================"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get version safely
get_version() {
    local cmd=$1
    local version_cmd=$2
    
    if command_exists "$cmd"; then
        eval "$version_cmd" 2>/dev/null || echo "Error getting version"
    else
        echo "Not installed"
    fi
}

# Function to check if version is latest
check_latest() {
    local current=$1
    local latest=$2
    local component=$3
    
    if [ "$current" = "$latest" ]; then
        echo "✅ $component: $current (Latest)"
    else
        echo "⚠️  $component: $current (Latest: $latest)"
    fi
}

echo "📋 System Components Status:"
echo "----------------------------"

# Docker Engine
DOCKER_ENGINE=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "Not running")
DOCKER_CLIENT=$(docker version --format '{{.Client.Version}}' 2>/dev/null || echo "Not installed")
echo "🐳 Docker Engine: $DOCKER_ENGINE"
echo "🐳 Docker Client: $DOCKER_CLIENT"

# Docker Compose
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_V2=$(docker compose version --short 2>/dev/null || echo "Error")
    echo "🐳 Docker Compose v2: $DOCKER_COMPOSE_V2"
elif command_exists docker-compose; then
    DOCKER_COMPOSE_V1=$(docker-compose --version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "Error")
    echo "⚠️  Docker Compose v1: $DOCKER_COMPOSE_V1 (Consider upgrading to v2)"
else
    echo "❌ Docker Compose: Not installed"
fi

# BuildKit
if docker buildx version &> /dev/null; then
    BUILDKIT_VERSION=$(docker buildx version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+' || echo "Error")
    echo "🔧 BuildKit: $BUILDKIT_VERSION"
else
    echo "❌ BuildKit: Not installed"
fi

# Python
PYTHON_VERSION=$(python --version 2>/dev/null | sed 's/Python //' || echo "Not installed")
echo "🐍 Python: $PYTHON_VERSION"

# Node.js
NODE_VERSION=$(node --version 2>/dev/null | sed 's/v//' || echo "Not installed")
echo "📦 Node.js: $NODE_VERSION"

# npm
NPM_VERSION=$(npm --version 2>/dev/null || echo "Not installed")
echo "📦 npm: $NPM_VERSION"

echo ""
echo "🔍 Docker System Status:"
echo "----------------------"

# Check Docker daemon
if docker info &> /dev/null; then
    echo "✅ Docker daemon: Running"
    
    # Check Docker resources
    echo "📊 Docker Resources:"
    docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}\t{{.Reclaimable}}"
    
    # Check running containers
    echo ""
    echo "🐳 Running Containers:"
    if docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -q .; then
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        echo "No containers running"
    fi
    
    # Check Docker networks
    echo ""
    echo "🌐 Docker Networks:"
    docker network ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"
    
else
    echo "❌ Docker daemon: Not running"
    echo "💡 Start with: sudo systemctl start docker"
fi

echo ""
echo "🔍 Project Status:"
echo "-----------------"

# Check if we're in the right directory
if [ -f "docker/docker-compose.yml" ]; then
    echo "✅ Project structure: Valid"
else
    echo "❌ Project structure: Invalid (missing docker-compose.yml)"
    exit 1
fi

# Check .env file
if [ -f ".env" ]; then
    echo "✅ Environment file: Present"
    echo "📋 Environment variables:"
    grep -E '^[A-Z_]+=' .env | cut -d'=' -f1 | sort
else
    echo "⚠️  Environment file: Missing (.env)"
fi

# Check data directories
echo ""
echo "📁 Data Directories:"
for dir in data/sources data/outputs/logs data/outputs/visualizations; do
    if [ -d "$dir" ]; then
        echo "✅ $dir: Exists"
    else
        echo "⚠️  $dir: Missing"
    fi
done

# Check virtual environment
echo ""
echo "🐍 Python Environment:"
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment: Active ($VIRTUAL_ENV)"
else
    echo "⚠️  Virtual environment: Not active"
    echo "💡 Activate with: source living_venv/bin/activate"
fi

# Check Python packages
if command_exists pip; then
    echo "📦 Python packages:"
    pip list --format=columns | grep -E "(fastapi|uvicorn|python-dotenv|requests)" || echo "Core packages not found"
fi

echo ""
echo "🚀 Service Status:"
echo "-----------------"

# Check if services are running
if command_exists docker; then
    if docker ps | grep -q "living-truth"; then
        echo "✅ Living Truth services: Running"
        docker ps --filter "name=living-truth" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        echo "⚠️  Living Truth services: Not running"
        echo "💡 Start with: ./scripts/setup/start_services.sh"
    fi
fi

echo ""
echo "📝 Recommendations:"
echo "------------------"

# Check for updates
if command_exists docker-compose && ! docker compose version &> /dev/null; then
    echo "💡 Upgrade Docker Compose to v2: ./scripts/setup/update_system.sh"
fi

if ! docker buildx version &> /dev/null; then
    echo "💡 Install BuildKit: ./scripts/setup/update_system.sh"
fi

if [ ! -f ".env" ]; then
    echo "💡 Create .env file with required environment variables"
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "💡 Activate virtual environment: source living_venv/bin/activate"
fi

echo ""
echo "✅ System check complete!" 