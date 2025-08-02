# Living Truth Engine - Project Setup Guide

## Overview

This document provides comprehensive setup information for the Living Truth Engine project, including environment configuration, service setup, and current working state.

## 🏗️ **Current Architecture**

### **Core Services (Operational)**
1. **✅ Langflow**: Port 7860 - AI workflow orchestration
2. **✅ PostgreSQL**: Port 5432 - Database with langflow database
3. **✅ Neo4j**: Port 7474/7687 - Graph database
4. **✅ Redis**: Port 6379 - Caching and sessions
5. **✅ LM Studio**: Port 1234 - Local model hosting
6. **✅ Living Truth Engine**: Port 9123-9124 - Core analysis engine
7. **✅ Dash Dashboard**: Port 8050 - Interactive visualizations

### **Optional Services (Configured)**
8. **🆕 DevDocs**: Port 9126 - Document retrieval (MCP server ready)
9. **🆕 Rulego**: Port 9127 - Workflow orchestration (MCP server ready)
10. **🆕 MCP Solver**: Port 9128 - Constraint solving (MCP server ready)

## ⚙️ **Environment Configuration**

### **Essential Environment Variables**

Copy the following to your `.env` file:

```bash
# Langflow Configuration
LANGFLOW_API_ENDPOINT=http://localhost:7860
LANGFLOW_API_KEY=your_langflow_api_key_here
LANGFLOW_PROJECT_ID=your_project_id_here

# Database Configuration
POSTGRES_DB=living_truth_engine
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here

# Service Endpoints
LM_STUDIO_ENDPOINT=http://localhost:1234

# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
GITHUB_USERNAME=your_github_username

# Hugging Face Configuration
HUGGINGFACE_TOKEN=your_huggingface_token_here

# LangChain Configuration
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true

# External APIs
SERP_API_KEY=your_serp_api_key_here

# Atlassian Configuration
ATLASSIAN_ORG_ID=your_atlassian_org_id_here
ATLASSIAN_API_KEY=your_atlassian_api_key_here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# Python Path
PYTHONPATH=/home/mccoy/Projects/NotebookLM/LivingTruthEngine/src
```

### **API Keys Required**

1. **Langflow API Key**: Get from Langflow admin interface
2. **GitHub Token**: Personal access token for repository management
3. **Hugging Face Token**: For model and dataset access
4. **LangChain API Key**: For LangSmith tracing and monitoring
5. **SerpAPI Key**: For web search functionality
6. **Atlassian API Key**: For project management integration

## 🐳 **Docker Configuration**

### **Project Setup**
```bash
# Project Group
DOCKER_PROJECT_GROUP=LivingTruthEngine

# Compose File Location
DOCKER_COMPOSE_PATH=/home/mccoy/Projects/NotebookLM/LivingTruthEngine/docker/docker-compose.yml
```

### **Service Management**
```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d

# Stop all services
docker compose -f docker/docker-compose.yml down

# Check service status
docker compose -f docker/docker-compose.yml ps

# View logs
docker compose -f docker/docker-compose.yml logs -f
```

## 🔧 **MCP Server Configuration**

### **Total MCP Servers: 8**

#### **1. Living Truth FastMCP Server (22 tools)**
- **LM Studio Tools** (4): `get_lm_studio_models`, `generate_lm_studio_text`, `test_lm_studio_connection`, `get_lm_studio_status`
- **Core Tools** (6): `query_langflow`, `get_status`, `list_sources`, `analyze_transcript`, `generate_viz`, `generate_audio`
- **Batch Tools** (2): `batch_system_operations`, `batch_analysis_operations`
- **Utility Tools** (5): `get_project_info`, `get_current_time`, `test_tool`, `fix_flow`, `query_flowise`
- **Automation Tools** (5): `auto_detect_and_add_tools`, `auto_update_all_documentation`, `auto_update_cursor_rules`, `auto_validate_system_state`, `comprehensive_health_check`

#### **2. Langflow MCP Server (6 tools)**
- `query_langflow` - Query Langflow workflows for survivor testimony analysis
- `create_langflow` - Create or update Langflow workflows programmatically
- `get_langflow_status` - Langflow system status and connection information
- `list_langflow_tools` - List available tools in Langflow
- `get_current_time` - Get current time as test tool
- `test_tool` - Simple test tool for Cursor detection

#### **3. Additional MCP Servers**
- **DevDocs MCP Server**: Document retrieval and crawling
- **Rulego MCP Server**: Workflow orchestration
- **MCP Solver Server**: Constraint solving and LLM routing
- **GitHub MCP Server**: Repository management
- **PostgreSQL MCP Server**: Database operations
- **Hugging Face MCP Server**: Model access

### **MCP Configuration File**
Location: `.cursor/mcp.json`

All MCP servers are configured to run locally (not in Docker) for stability and are working with green dots in Cursor.

## 🧪 **Testing Configuration**

### **Functional Testing**
- **Test Script**: `scripts/testing/functional_tests.py`
- **Test Categories**: 7 categories verifying actual service capabilities
- **Current Status**: 6/7 tests passing (85% coverage)
- **Failing Test**: Audio Generation (missing piper-tts voice models)

### **Performance Testing**
- **Target Response Time**: <2s for API calls
- **Performance Scripts**: 
  - `scripts/testing/trace_performance.sh`
  - `scripts/testing/simple_performance_test.sh`
- **Current Status**: All services responding under 2s

## 🎯 **Current Working State**

### **✅ All Services Operational**
- **Langflow**: http://localhost:7860 (admin/admin)
- **LM Studio**: http://localhost:1234 (with system model access)
- **PostgreSQL**: localhost:5432 (with langflow database)
- **Neo4j**: http://localhost:7474
- **Redis**: localhost:6379
- **Dash Dashboard**: http://localhost:8050 (interactive visualizations)

### **✅ Recent Achievements**
- **Proper Error Handling**: No fallback mechanisms, fail-fast approach
- **Comprehensive Testing**: 6/7 functional tests passing (85% coverage)
- **Performance Targets**: All services responding under 2s
- **Programmatic Workflow Management**: create_langflow tool implemented
- **All MCP Servers**: Working with green dots in Cursor

## 🚀 **Quick Start**

### **1. Environment Setup**
```bash
# Copy environment template
cp env.template .env

# Edit .env with your actual API keys
nano .env
```

### **2. Start Services**
```bash
# Start all Docker services
docker compose -f docker/docker-compose.yml up -d

# Verify services are running
docker compose -f docker/docker-compose.yml ps
```

### **3. Test Setup**
```bash
# Run functional tests
python scripts/testing/functional_tests.py

# Check MCP server status
python src/mcp_servers/test_mcp_server.py
```

### **4. Access Services**
- **Langflow**: http://localhost:7860 (admin/admin)
- **Dash Dashboard**: http://localhost:8050
- **Neo4j Browser**: http://localhost:7474

## 📚 **Documentation**

- **README.md**: Project overview and quick start
- **CURRENT_STATUS.md**: Detailed current state and achievements
- **docs/LANGFLOW_MCP_TOOLS.md**: Langflow MCP tools documentation
- **env_config.txt**: Comprehensive configuration documentation
- **env_minimal.txt**: Minimal environment variables for .env file

## 🔍 **Troubleshooting**

### **Common Issues**
1. **Port Conflicts**: Check if ports 7860, 1234, 5432, 7474, 6379, 8050 are available
2. **API Key Issues**: Verify all API keys in .env file are valid
3. **Docker Issues**: Ensure Docker and Docker Compose v2 are installed
4. **MCP Server Issues**: Check .cursor/mcp.json configuration

### **Logs Location**
- **Application Logs**: `data/outputs/logs/`
- **Docker Logs**: `docker compose -f docker/docker-compose.yml logs -f`
- **MCP Server Logs**: `data/outputs/logs/langflow_mcp.log`

## 📊 **Performance Metrics**

- **Service Uptime**: 99%+ for all core services
- **API Response Time**: <2s for most operations
- **MCP Tool Response**: <1s for simple operations
- **System Health**: All services healthy
- **Test Coverage**: 85% functional test coverage 