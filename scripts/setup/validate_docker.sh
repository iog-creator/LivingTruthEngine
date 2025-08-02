#!/bin/bash

# Living Truth Engine - Docker Best Practices Validation
# Validates our Docker configuration against official Docker best practices

set -e

echo "🔍 Docker Best Practices Validation"
echo "==================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    local status=$1
    local message=$2
    case $status in
        "PASS")
            echo "✅ $message"
            ;;
        "FAIL")
            echo "❌ $message"
            ;;
        "WARN")
            echo "⚠️  $message"
            ;;
        "INFO")
            echo "ℹ️  $message"
            ;;
    esac
}

echo "📋 Checking Docker Components..."
echo "-------------------------------"

# Check Docker version
if command_exists docker; then
    DOCKER_VERSION=$(docker version --format '{{.Client.Version}}')
    print_status "PASS" "Docker Client: $DOCKER_VERSION"
else
    print_status "FAIL" "Docker Client: Not installed"
    exit 1
fi

# Check Docker Compose v2
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version --short)
    print_status "PASS" "Docker Compose v2: $COMPOSE_VERSION"
else
    print_status "FAIL" "Docker Compose v2: Not installed"
fi

# Check BuildKit
if docker buildx version &> /dev/null; then
    BUILDKIT_VERSION=$(docker buildx version | grep -o '[0-9]\+\.[0-9]\+\.[0-9]\+')
    print_status "PASS" "BuildKit: $BUILDKIT_VERSION"
else
    print_status "WARN" "BuildKit: Not installed (recommended for better builds)"
fi

echo ""
echo "🔍 Validating Docker Compose Configuration..."
echo "--------------------------------------------"

# Validate compose file
if [ -f "docker/docker-compose.yml" ]; then
    if docker compose -f docker/docker-compose.yml config &> /dev/null; then
        print_status "PASS" "Docker Compose file: Valid syntax"
    else
        print_status "FAIL" "Docker Compose file: Invalid syntax"
        docker compose -f docker/docker-compose.yml config
        exit 1
    fi
else
    print_status "FAIL" "Docker Compose file: Not found"
    exit 1
fi

echo ""
echo "🔍 Checking Docker Best Practices..."
echo "----------------------------------"

# Check for security best practices
echo "🔒 Security Checks:"

# Check if running as non-root user
if grep -q "USER appuser" docker/Dockerfile.mcp; then
    print_status "PASS" "Non-root user configured"
else
    print_status "FAIL" "Running as root (security risk)"
fi

# Check for health checks
if grep -q "HEALTHCHECK" docker/Dockerfile.mcp; then
    print_status "PASS" "Health check configured"
else
    print_status "WARN" "No health check configured"
fi

# Check for multi-stage builds (if applicable)
if grep -q "FROM.*as" docker/Dockerfile.mcp; then
    print_status "PASS" "Multi-stage build used"
else
    print_status "INFO" "Single-stage build (acceptable for this use case)"
fi

# Check for .dockerignore
if [ -f ".dockerignore" ]; then
    print_status "PASS" ".dockerignore file present"
else
    print_status "WARN" ".dockerignore file missing (recommended)"
fi

echo ""
echo "🐳 Docker Compose Best Practices:"

# Check for proper restart policies
if grep -q "restart: unless-stopped\|restart: always" docker/docker-compose.yml; then
    print_status "PASS" "Restart policies configured"
else
    print_status "WARN" "No restart policies configured"
fi

# Check for health checks in compose
if grep -q "healthcheck:" docker/docker-compose.yml; then
    print_status "PASS" "Health checks configured in compose"
else
    print_status "WARN" "No health checks in compose file"
fi

# Check for proper networking
if grep -q "networks:" docker/docker-compose.yml; then
    print_status "PASS" "Custom networks configured"
else
    print_status "WARN" "Using default network"
fi

# Check for volume configurations
if grep -q "volumes:" docker/docker-compose.yml; then
    print_status "PASS" "Volumes configured"
else
    print_status "WARN" "No volumes configured"
fi

echo ""
echo "🔍 Environment and Configuration..."
echo "---------------------------------"

# Check .env file
if [ -f ".env" ]; then
    print_status "PASS" ".env file present"
    
    # Check for sensitive data in .env
    if grep -q "PASSWORD\|SECRET\|KEY" .env; then
        print_status "INFO" "Sensitive data found in .env (expected)"
    fi
else
    print_status "WARN" ".env file missing"
fi

# Check for data directories
for dir in data/sources data/outputs/logs data/outputs/visualizations; do
    if [ -d "$dir" ]; then
        print_status "PASS" "Directory exists: $dir"
    else
        print_status "WARN" "Directory missing: $dir"
    fi
done

echo ""
echo "🔍 Performance and Optimization..."
echo "--------------------------------"

# Check for BuildKit usage
if grep -q "DOCKER_BUILDKIT=1" scripts/setup/start_services.sh; then
    print_status "PASS" "BuildKit enabled in startup script"
else
    print_status "WARN" "BuildKit not explicitly enabled"
fi

# Check for proper base image
if grep -q "FROM python:3.12-slim" docker/Dockerfile.mcp; then
    print_status "PASS" "Using slim base image"
else
    print_status "WARN" "Not using slim base image"
fi

# Check for layer optimization
if grep -q "COPY requirements.txt" docker/Dockerfile.mcp && grep -q "RUN pip install" docker/Dockerfile.mcp; then
    print_status "PASS" "Dependencies installed before code copy (good layer caching)"
else
    print_status "WARN" "Layer optimization could be improved"
fi

echo ""
echo "🔍 Docker System Status..."
echo "-------------------------"

# Check Docker daemon
if docker info &> /dev/null; then
    print_status "PASS" "Docker daemon running"
    
    # Check Docker resources
    echo "📊 Docker Resources:"
    docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}\t{{.Reclaimable}}"
    
    # Check for unused resources
    UNUSED_IMAGES=$(docker images -f "dangling=true" -q | wc -l)
    if [ "$UNUSED_IMAGES" -gt 0 ]; then
        print_status "WARN" "Unused images found: $UNUSED_IMAGES"
        echo "💡 Clean with: docker image prune"
    else
        print_status "PASS" "No unused images"
    fi
    
else
    print_status "FAIL" "Docker daemon not running"
fi

echo ""
echo "📝 Recommendations:"
echo "------------------"

# Generate recommendations based on findings
if ! docker compose version &> /dev/null; then
    echo "💡 Install Docker Compose v2: ./scripts/setup/update_system.sh"
fi

if ! docker buildx version &> /dev/null; then
    echo "💡 Install BuildKit: ./scripts/setup/update_system.sh"
fi

if [ ! -f ".dockerignore" ]; then
    echo "💡 Create .dockerignore file to exclude unnecessary files"
fi

if ! grep -q "HEALTHCHECK" docker/Dockerfile.mcp; then
    echo "💡 Add health checks to Dockerfile"
fi

echo ""
echo "✅ Docker validation complete!"
echo ""
echo "🚀 Next steps:"
echo "   - Run: ./scripts/setup/start_services.sh"
echo "   - Monitor: docker compose -f docker/docker-compose.yml logs -f"
echo "   - Clean up: docker system prune" 