---
phase: 9.5.7
status: active
last_reviewed: 2025-08-14
related_files: ['docs/PROJECT_STRUCTURE.md', 'docs/MCP_SERVERS_OVERVIEW.md', 'docs/project_master_log.md']
---

# Living Truth Engine — Phase 9.5.7

**Current focus:** Resilience Dashboard UI  
**Last repo health run:** 2025-08-14  
**Status:** ✅ All MCP tools validated, 33 MDC files properly formatted

## 🎯 **Project Overview**

The Living Truth Engine is a comprehensive AI-powered analysis system for survivor testimony and evidence verification. It combines advanced language models, vector search, and automated workflows to provide deep insights into complex narratives.

## 🚀 **Quick Start**

```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d --build

# Access the application
# Dashboard: http://localhost:8050
# Langflow: http://localhost:7860
# LM Studio: http://localhost:1234

# Run health checks
bash scripts/resilience_dashboard_test.sh
```

## 🔧 **Active MCP Tools (9 servers, 63+ tools)**

### **Core Analysis Servers**
- **Living Truth FastMCP Server** (`living_truth_fastmcp_server.py`) - 22 tools
  - LM Studio integration, transcript analysis, visualization
- **Phase9 MCP Server** (`phase9_mcp_server.py`) - 15+ tools
  - Cursor rules management, validation, system health

### **Integration Servers**
- **MCP Hub Server** (`mcp_hub_server.py`) - 15 meta-tools
  - Single gateway to all 63 tools
- **Langflow MCP Server** (`langflow_mcp_server.py`) - 12 tools
  - Workflow management, JSON import/export
- **PostgreSQL MCP Server** (`postgresql_mcp_server.py`) - 6 tools
  - Database operations and management

### **Utility Servers**
- **Hugging Face MCP Server** (`huggingface_mcp_server.py`) - 5 tools
- **DevDocs MCP Server** (`devdocs_mcp_server.py`) - 4 tools
- **Rulego MCP Server** (`rulego_mcp_server.py`) - 5 tools
- **MCP Solver Server** (`mcp_solver_server.py`) - 5 tools
- **GitHub MCP Server** (`github_mcp_server.py`) - 4 tools

## 🐳 **Active Docker Services (13 services)**

### **Core Services**
- **living-truth-engine** - Main application
- **dashboard** - Web dashboard (port 8050)
- **langflow** - Workflow management (port 7860)
- **lm-studio** - Local language models (port 1234)

### **Data Services**
- **postgres** - Primary database
- **neo4j** - Graph database
- **redis** - Caching and sessions

### **Analysis Services**
- **veritas_api** - Analysis API
- **veritas_worker** - Background processing
- **veritas_console** - Console interface

### **Support Services**
- **devdocs** - Documentation server
- **rulego** - Workflow orchestration
- **mcp-solver** - Constraint solving

## 📋 **Recent Improvements (Phases 8.3-8.5)**

### **MCP Tools and Rules**
- ✅ **Enhanced validation logic** - Correctly detects duplicate frontmatter vs content
- ✅ **Smart content extraction** - Properly extracts main content after any frontmatter
- ✅ **Consistent validation** - Both Phase9 and FastMCP servers use identical logic
- ✅ **AlwaysApply policy** - Only `00-global.mdc` auto-applies, others use agent selection
- ✅ **User Rules policy** - Guidelines for global Cursor settings

### **Tool Rituals (Mandatory for ALL Changes)**
```bash
# 1. MCP Sync and Logging Check
python scripts/mcp_sync.py && python scripts/logging_schema_check.py

# 2. Phase9 MCP Server Validation
python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.validate_cursor_rules(); print('MCP Validation:', result)"

# 3. FastMCP Server Validation
python -c "from src.mcp_servers.living_truth_fastmcp_server import validate_cursor_rules; result = validate_cursor_rules(); print('FastMCP Validation:', result)"
```

## 📚 **Documentation**

### **Core Documentation**
- [Project Structure](docs/PROJECT_STRUCTURE.md) - Complete file organization
- [MCP Servers Overview](docs/MCP_SERVERS_OVERVIEW.md) - All MCP tools and servers
- [Project Master Log](docs/project_master_log.md) - Complete project history
- [System Architecture](docs/SYSTEM_ARCHITECTURE.md) - Technical architecture
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Setup and deployment

### **Service Documentation**
- [Services Manifest](docs/SERVICES_MANIFEST.md) - All service configurations
- [Testing Overview](docs/TESTING_OVERVIEW.md) - Testing strategies and tools
- [Langflow Integration](docs/LANGFLOW_MCP_INTEGRATION.md) - Workflow management

## 🧪 **Testing and Validation**

### **Health Checks**
```bash
# Comprehensive health check
bash scripts/resilience_dashboard_test.sh

# UI testing
npx playwright test --reporter=list

# API testing
pytest -q tests/api tests/models tests/prompts
```

### **Validation Results**
- ✅ **All 33 MDC files** have proper frontmatter format
- ✅ **Both MCP servers** validate correctly
- ✅ **MCP sync and logging** working properly
- ✅ **AlwaysApply policy** enforced across all rules

## 🎯 **Current Phase: 9.5.7 - Resilience Dashboard UI**

**Focus:** Building comprehensive resilience monitoring dashboard with:
- Real-time system health monitoring
- Chaos testing integration
- Predictive failure detection
- Automated recovery systems

## 🔗 **Quick Links**

- **Dashboard**: http://localhost:8050
- **Langflow**: http://localhost:7860
- **LM Studio**: http://localhost:1234
- **Documentation**: [docs/](docs/)
- **MCP Tools**: [src/mcp_servers/](src/mcp_servers/)

---

**Last Updated**: August 14, 2025  
**Phase**: 9.5.7 - Resilience Dashboard UI  
**Status**: ✅ Active Development
