#!/bin/bash

echo "🚀 Living Truth Engine - Quick Start"
echo "===================================="

# Check if we can run docker without sudo
if docker ps >/dev/null 2>&1; then
    echo "✅ Docker permissions OK"
    DOCKER_CMD="docker"
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "⚠️  Using sudo for Docker commands (log out and back in to avoid this)"
    DOCKER_CMD="sudo docker"
    DOCKER_COMPOSE_CMD="sudo docker-compose"
fi

# Check if services are already running
if $DOCKER_COMPOSE_CMD ps | grep -q "Up"; then
    echo "📊 Current service status:"
    $DOCKER_COMPOSE_CMD ps
    echo ""
    echo "Services are already running!"
    echo "🌐 Access points:"
    echo "   - Langflow: http://localhost:7860"
    echo "   - Dashboard: http://localhost:8050"
    echo "   - LM Studio: http://localhost:1234"
    exit 0
fi

# Ensure we're in the correct project directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo "📁 Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs config tests docs scripts models .Langflow

# Check if .env file exists and has required variables
if [ ! -f .env ]; then
    echo "❌ .env file not found. Creating template..."
    cat > .env << EOF
# Langflow Configuration
Langflow_API_ENDPOINT=http://localhost:7860
Langflow_API_KEY=your_Langflow_api_key
Langflow_CHATFLOW_ID=your_chatflow_id

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
    echo "✅ .env file exists"
fi

# Build and start services
echo "🔨 Building and starting services..."
$DOCKER_COMPOSE_CMD up -d --build

# Wait a moment for services to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo "📊 Service status:"
$DOCKER_COMPOSE_CMD ps

# Check if services are healthy
echo "🏥 Health check:"
$DOCKER_COMPOSE_CMD ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Services available at:"
echo "   - Langflow: http://localhost:7860"
echo "   - Dashboard: http://localhost:8050"
echo "   - LM Studio: http://localhost:1234"
echo "   - PostgreSQL: localhost:5432"
echo ""
echo "📝 Next steps:"
echo "   1. Update .env file with your actual API keys"
echo "   2. Import the living_truth_full_flow.json into Langflow"
echo "   3. Test the MCP server integration"
echo "   4. Access the dashboard at http://localhost:8050"
echo ""
echo "🛠️  Management commands:"
echo "   - View logs: $DOCKER_COMPOSE_CMD logs"
echo "   - Stop services: $DOCKER_COMPOSE_CMD down"
echo "   - Restart services: $DOCKER_COMPOSE_CMD restart" 