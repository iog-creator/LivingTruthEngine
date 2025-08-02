#!/bin/bash

# Living Truth Engine - System Update Script
# Updates all Docker components and applications to latest versions

set -e

echo "🚀 Living Truth Engine - System Update Script"
echo "=============================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get latest version from GitHub releases
get_latest_version() {
    local repo=$1
    curl -s "https://api.github.com/repos/$repo/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/'
}

echo "📋 Current System Status:"
echo "------------------------"

# Check current versions
echo "🐳 Docker Engine: $(docker version --format '{{.Server.Version}}')"
echo "🐳 Docker Client: $(docker version --format '{{.Client.Version}}')"

if command_exists docker-compose; then
    echo "🐳 Docker Compose: $(docker-compose --version)"
fi

if command_exists docker; then
    if docker compose version &> /dev/null; then
        echo "🐳 Docker Compose v2: $(docker compose version)"
    fi
fi

echo "🐍 Python: $(python --version)"
echo "📦 Node.js: $(node --version)"
echo "🔧 BuildKit: $(docker buildx version 2>/dev/null || echo 'Not installed')"

echo ""
echo "🔄 Starting System Updates..."
echo "============================"

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update

# Update Docker to latest version
echo "🐳 Updating Docker..."
if command_exists docker; then
    # Remove old Docker Compose v1
    if command_exists docker-compose; then
        echo "🗑️  Removing Docker Compose v1..."
        sudo apt-get remove -y docker-compose
    fi
    
    # Install Docker Compose v2 plugin
    echo "📦 Installing Docker Compose v2..."
    sudo apt-get install -y docker-compose-plugin
    
    # Install BuildKit if not present
    if ! command_exists docker-buildx; then
        echo "📦 Installing Docker BuildKit..."
        sudo apt-get install -y docker-buildx-plugin
    fi
    
    # Install Docker Compose v2 standalone (alternative)
    if ! docker compose version &> /dev/null; then
        echo "📦 Installing Docker Compose v2 standalone..."
        DOCKER_COMPOSE_VERSION=$(get_latest_version "docker/compose")
        sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
fi

# Update Node.js to latest LTS
echo "📦 Updating Node.js..."
if command_exists node; then
    CURRENT_NODE_VERSION=$(node --version | sed 's/v//')
    LATEST_NODE_VERSION=$(curl -s https://nodejs.org/dist/index.json | grep -o '"version":"[^"]*"' | head -1 | sed 's/"version":"//' | sed 's/"//')
    
    if [ "$CURRENT_NODE_VERSION" != "$LATEST_NODE_VERSION" ]; then
        echo "🔄 Updating Node.js from v$CURRENT_NODE_VERSION to v$LATEST_NODE_VERSION..."
        
        # Install NodeSource repository
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt-get install -y nodejs
        
        # Install npm globally
        sudo npm install -g npm@latest
    else
        echo "✅ Node.js is already at latest version"
    fi
fi

# Update Python packages
echo "🐍 Updating Python packages..."
if command_exists pip; then
    pip install --upgrade pip setuptools wheel
fi

# Update global npm packages
echo "📦 Updating global npm packages..."
if command_exists npm; then
    npm update -g
fi

# Clean up
echo "🧹 Cleaning up..."
sudo apt-get autoremove -y
sudo apt-get autoclean

echo ""
echo "✅ System Update Complete!"
echo "========================="

echo "📋 Updated System Status:"
echo "------------------------"

# Show updated versions
echo "🐳 Docker Engine: $(docker version --format '{{.Server.Version}}')"
echo "🐳 Docker Client: $(docker version --format '{{.Client.Version}}')"

if docker compose version &> /dev/null; then
    echo "🐳 Docker Compose v2: $(docker compose version)"
fi

echo "🐍 Python: $(python --version)"
echo "📦 Node.js: $(node --version)"
echo "🔧 BuildKit: $(docker buildx version)"

echo ""
echo "🎉 All components updated to latest versions!"
echo ""
echo "📝 Next steps:"
echo "   - Restart Docker: sudo systemctl restart docker"
echo "   - Test Docker Compose: docker compose version"
echo "   - Test BuildKit: docker buildx version"
echo "   - Start services: ./scripts/setup/start_services.sh" 