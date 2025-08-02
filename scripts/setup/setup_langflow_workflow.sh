#!/bin/bash
# Living Truth Engine - Langflow Workflow Setup Script
# Sets up and imports the Biblical Forensic Analysis workflow

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}Living Truth Engine - Forensic Analysis Workflow Setup${NC}"
echo "============================================================="

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

# Function to check if service is healthy
check_service_health() {
    local service_name=$1
    local health_url=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Checking $service_name health..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$health_url" > /dev/null 2>&1; then
            print_status "$service_name is healthy!"
            return 0
        else
            print_warning "$service_name not ready yet (attempt $attempt/$max_attempts)"
            sleep 10
            ((attempt++))
        fi
    done
    
    print_error "$service_name failed to become healthy after $max_attempts attempts"
    return 1
}

# Function to wait for service to be ready
wait_for_service() {
    local service_name=$1
    local port=$2
    local max_attempts=30
    local attempt=1
    
    print_status "Waiting for $service_name to be ready on port $port..."
    
    while [ $attempt -le $max_attempts ]; do
        if nc -z localhost $port 2>/dev/null; then
            print_status "$service_name is ready on port $port!"
            return 0
        else
            print_warning "$service_name not ready yet on port $port (attempt $attempt/$max_attempts)"
            sleep 10
            ((attempt++))
        fi
    done
    
    print_error "$service_name failed to be ready on port $port after $max_attempts attempts"
    return 1
}

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Navigate to project root
cd "$PROJECT_ROOT"
print_status "Working directory: $(pwd)"

# Stop existing services if running
print_status "Stopping existing services..."
docker compose -f docker/docker-compose.yml down --remove-orphans

# Start all services
print_status "Starting all services..."
docker compose -f docker/docker-compose.yml up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."

# Wait for PostgreSQL
if ! wait_for_service "PostgreSQL" 5432; then
    print_error "PostgreSQL failed to start"
    exit 1
fi

# Wait for LM Studio
if ! wait_for_service "LM Studio" 1234; then
    print_error "LM Studio failed to start"
    exit 1
fi

# Wait for Langflow
if ! wait_for_service "Langflow" 7860; then
    print_error "Langflow failed to start"
    exit 1
fi

# Wait for Flowise
if ! wait_for_service "Flowise" 3000; then
    print_error "Flowise failed to start"
    exit 1
fi

# Wait for MCP Server
if ! wait_for_service "MCP Server" 8000; then
    print_error "MCP Server failed to start"
    exit 1
fi

# Check service health
print_status "Checking service health..."

# Check Langflow health
if ! check_service_health "Langflow" "http://localhost:7860/health"; then
    print_error "Langflow health check failed"
    exit 1
fi

# Check LM Studio health
if ! check_service_health "LM Studio" "http://localhost:1234/v1/models"; then
    print_error "LM Studio health check failed"
    exit 1
fi

# Check Flowise health
if ! check_service_health "Flowise" "http://localhost:3000/"; then
    print_error "Flowise health check failed"
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source living_venv/bin/activate

# Install required packages if needed
print_status "Checking Python dependencies..."
pip install requests python-dotenv

# Import Langflow workflow
print_status "Importing Forensic Analysis workflow..."
python scripts/setup/import_langflow_workflow.py

if [ $? -eq 0 ]; then
    print_status "✅ Workflow import completed successfully!"
else
    print_error "❌ Workflow import failed"
    exit 1
fi

# Display service information
echo ""
echo -e "${BLUE}Service Information:${NC}"
echo "======================"
echo -e "${GREEN}Langflow:${NC} http://localhost:7860 (admin/admin)"
echo -e "${GREEN}Flowise:${NC} http://localhost:3000"
echo -e "${GREEN}LM Studio:${NC} http://localhost:1234"
echo -e "${GREEN}MCP Server:${NC} http://localhost:8000"
echo -e "${GREEN}PostgreSQL:${NC} localhost:5432"
echo ""

# Display workflow information
echo -e "${BLUE}Workflow Information:${NC}"
echo "========================"
echo -e "${GREEN}Name:${NC} Living Truth Engine Forensic Analysis"
echo -e "${GREEN}Type:${NC} Multi-Agent System for Elite Network Analysis"
echo -e "${GREEN}Models:${NC} Qwen3-8B (LLM), Qwen3-0.6B (Embeddings)"
echo -e "${GREEN}Database:${NC} PostgreSQL with PGVector for entity relationships"
echo -e "${GREEN}Tools:${NC} Brave Search, Web Scraper, MCP Tools, pgVectorSearch"
echo ""

# Display next steps
echo -e "${BLUE}Next Steps:${NC}"
echo "==========="
echo "1. Open Langflow at http://localhost:7860"
echo "2. Login with admin/admin"
echo "3. Find the 'Living Truth Engine Forensic Analysis' workflow"
echo "4. Configure environment variables in .env file:"
echo "   - BRAVE_API_KEY"
echo "   - MCP_API_KEY"
echo "5. Test the workflow with a sample query"
echo ""

print_status "Setup completed successfully! 🎉" 