#!/bin/bash

echo "🚀 Living Truth Engine Docker Setup Script"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -aG docker $USER
    echo "✅ Docker installed. Please log out and back in for group changes to take effect."
    echo "   Then run this script again."
    exit 1
else
    echo "✅ Docker is already installed"
    docker --version
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Installing..."
    sudo apt-get install -y docker-compose
else
    echo "✅ Docker Compose is already installed"
    docker-compose --version
fi

# Check if user is in docker group
if ! groups $USER | grep -q docker; then
    echo "⚠️  User is not in docker group. Adding user to docker group..."
    sudo usermod -aG docker $USER
    echo "✅ User added to docker group. Please log out and back in."
    exit 1
else
    echo "✅ User is in docker group"
fi

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs config tests docs scripts models .flowise

# Check if .env file exists and has required variables
if [ ! -f .env ]; then
    echo "❌ .env file not found. Creating from template..."
    cat > .env << EOF
# Flowise Configuration
FLOWISE_API_ENDPOINT=http://localhost:3000
FLOWISE_API_KEY=your_flowise_api_key
FLOWISE_CHATFLOW_ID=your_chatflow_id

# LangChain Configuration
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# SerpAPI Configuration
SERP_API_KEY=your_serpapi_key

# Database Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=living_truth_engine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=pass

# LM Studio Configuration
LM_STUDIO_URL=http://localhost:1234/v1
LM_STUDIO_BASE_URL=http://localhost:1234

# Dashboard Configuration
DASHBOARD_PORT=8050
DASHBOARD_HOST=0.0.0.0

# MCP Server Configuration
MCP_SERVER_PORT=3001
MCP_SERVER_HOST=0.0.0.0

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/living_truth_engine.log

# Model Configuration
DEFAULT_MODEL=qwen3-8b
VISION_MODEL=qwen2.5-vl-7b
EMBEDDING_MODEL=qwen3-0.6b

# TTS Configuration
TTS_MODEL_PATH=en_US-lessac-medium.onnx
TTS_CONFIG_PATH=en_US-lessac-medium.json
EOF
    echo "✅ .env file created. Please update with your actual API keys."
else
    echo "✅ .env file already exists"
fi

# Build and start services
echo "🔨 Building and starting Docker services..."
docker-compose up -d --build

# Check service status
echo "📊 Checking service status..."
docker-compose ps

echo "✅ Docker setup complete!"
echo ""
echo "🌐 Services available at:"
echo "   - Flowise: http://localhost:3000"
echo "   - Dashboard: http://localhost:8050"
echo "   - LM Studio: http://localhost:1234"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "📝 Next steps:"
echo "   1. Update .env file with your actual API keys"
echo "   2. Import the living_truth_full_flow.json into Flowise"
echo "   3. Test the MCP server integration"
echo "   4. Access the dashboard at http://localhost:8050" 