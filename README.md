# Living Truth Engine

A comprehensive AI-powered system for forensic analysis and survivor testimony processing, built with modern Docker practices and optimized for AI-assisted development.

## 🎯 **Project Overview**

The Living Truth Engine is an advanced AI system that combines multiple technologies to provide comprehensive analysis capabilities:

- **Cross-Referencing System**: Cross-referencing testimonials, people, places, events, concepts, and organizations
- **Biblical Forensic Analysis**: Advanced evidence analysis with confidence baselines and verification
- **Survivor Testimony Corroboration**: Advanced pattern recognition and evidence analysis
- **Multi-Source Evidence Analysis**: Connecting survivor stories with supporting evidence from various sources
- **AI-Powered Workflows**: Langflow-based orchestration with multi-agent systems
- **Modern Containerization**: Docker Compose v2 with best practices
- **MCP Integration**: Model Context Protocol for tool automation
- **Real-time Processing**: PostgreSQL database with vector storage
- **Unified Services**: All services running under `LivingTruthEngine` group
- **Migrated Functionality**: All living_truth_agent components successfully migrated and operational

## 🏗️ **Architecture**

### **Service Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Langflow      │    │   PostgreSQL    │    │   Living Truth  │
│   (Port 7860)   │    │   (Port 5432)   │    │   Engine        │
│                 │    │                 │    │   (Port 9123)   │
│ • AI Workflows  │    │ • Data Storage  │    │ • FastAPI       │
│ • Multi-Agent   │    │ • User Data     │    │ • Dashboard     │
│ • Node Editor   │    │ • Analysis Data │    │ • Integration   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                    ┌─────────────────┐    ┌─────────────────┐
                    │   Redis         │    │   Neo4j         │
                    │   (Port 6379)   │    │   (Port 7474)   │
                    │                 │    │                 │
                    │ • Caching       │    │ • Graph DB      │
                    │ • Sessions      │    │ • Relationships │
                    │ • Performance   │    │ • Network Maps  │
                    └─────────────────┘    └─────────────────┘
                    ┌─────────────────┐    ┌─────────────────┐
                    │   LM Studio     │    │   MCP Server    │
                    │   (Port 1234)   │    │   (Local)       │
                    │                 │    │                 │
                    │ • Local Models  │    │ • Tool Server   │
                    │ • AI Inference  │    │ • API Endpoints │
                    │ • Model Hosting │    │ • Integration   │
                    └─────────────────┘    └─────────────────┘
                    ┌─────────────────┐    ┌─────────────────┐
                    │   DevDocs       │    │   Rulego        │
                    │   (Port 9126)   │    │   (Port 9127)   │
                    │   (Optional)    │    │   (Optional)    │
                    │                 │    │                 │
                    │ • Doc Retrieval │    │ • Workflows     │
                    │ • Crawling      │    │ • Chains        │
                    │ • Search        │    │ • Orchestration │
                    └─────────────────┘    └─────────────────┘
                    ┌─────────────────┐
                    │   MCP Solver    │
                    │   (Port 9128)   │
                    │   (Optional)    │
                    │                 │
                    │ • Constraints   │
                    │ • LLM Routing   │
                    │ • Optimization  │
                    └─────────────────┘
```

### **Technology Stack**
- **Python 3.13**: Core analysis and processing
- **Langflow**: AI workflow orchestration platform
- **PostgreSQL 17**: Database system with vector storage
- **Redis**: Caching and session management
- **Neo4j**: Graph database for relationship mapping
- **LM Studio**: Local model inference and hosting
- **Docker Compose v2**: Modern container orchestration
- **LangChain**: AI framework integration
- **FastAPI**: Web framework for APIs
- **FastMCP**: Model Context Protocol server framework

## ✅ **Migrated Living Truth Agent Functionality**

### **Successfully Migrated Components (7/7 Operational)**

All core living_truth_agent functionality has been successfully migrated and is fully operational:

#### **1. Configuration System** ✅ **OPERATIONAL**
- **Biblical forensic settings** with confidence baselines (0.8)
- **Database configuration** (PostgreSQL, Neo4j, Redis)
- **Model configuration** (LM Studio, embeddings, reranking)
- **Security and privacy settings**

#### **2. HybridRetriever** ✅ **OPERATIONAL**
- **Vector search** with dynamic embedding selection
- **Keyword search** with BM25 ranking
- **Biblical evidence reranking** with confidence scoring
- **Survivor testimony scoring** with enhanced algorithms

#### **3. ResearchAnalysisSystem** ✅ **OPERATIONAL**
- **Entity extraction** with named entity recognition
- **Claims verification** with automated analysis
- **Relationship mapping** with network analysis
- **Risk assessment** algorithms

#### **4. ChannelArchiver** ✅ **OPERATIONAL**
- **YouTube transcript processing** with yt-dlp
- **Knowledge base generation** with RAG capabilities
- **Video metadata processing** (duration, upload date, view count)
- **Archive management** and status tracking

#### **5. AGI Integration** ✅ **OPERATIONAL**
- **Cross-validation** between systems
- **Confidence scoring** with weighted calculations
- **Integrated insights** generation
- **Recommendation systems** based on analysis

#### **6. Advanced Visualization** ✅ **OPERATIONAL**
- **3D network graphs** with interactive visualization
- **Timeline analysis** for temporal patterns
- **Claims dashboard** for verification interface
- **Entity distribution** charts

#### **7. MCP Tools** ✅ **OPERATIONAL**
- **All migrated functionality** accessible via MCP Hub Server
- **97 total tools** across 8 servers
- **15 meta-tools** for unified access
- **Performance monitoring** and error handling

### **Core Capabilities Ready**

The system is now ready for **cross-referencing testimonials, people, places, events, concepts, and organizations** - the primary goal of the living_truth_agent:

- **Biblical forensic analysis** with confidence baselines
- **Survivor testimony analysis** with evidence verification
- **Elite network mapping** with relationship analysis
- **Advanced search capabilities** with hybrid retrieval
- **Interactive visualizations** for complex data analysis

### **Testing Results**
- **✅ 7/7 tests passing** (100% success rate)
- **✅ All components operational** and functional
- **✅ Import paths fixed** and working
- **✅ MCP integration complete** and accessible

## 🚀 **Quick Start**

### **1. Prerequisites**
- **Docker**: Latest version with Compose v2
- **Python 3.13**: With virtual environment support
- **Node.js 22**: Latest LTS version
- **Git**: For version control
- **Ubuntu 22.04+**: For optimal compatibility

### **2. Ubuntu Cursor Fix (If Needed)**
If you experience "Cursor is not responding" issues on Ubuntu, run the AppArmor fix:
```bash
./scripts/setup/fix_cursor_apparmor.sh
```

**What it does:**
- Installs required dependencies (`libfuse2t64`)
- Moves Cursor AppImage to `~/Applications/`
- Creates AppArmor profile for unconfined execution
- Sets up desktop entry with `--no-sandbox` flag
- Cleans up old references automatically

**Verification:**
```bash
# Check AppArmor profile
sudo aa-status | grep cursor

# Test Cursor launch
~/Applications/cursor.AppImage --no-sandbox

# Monitor resources
htop
```

### **2. Environment Setup**
```bash
# Clone the repository
git clone <repository-url>
cd LivingTruthEngine

# Activate virtual environment
source living_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **3. Start Services**
```bash
# Start all services under LivingTruthEngine group
cd /home/mccoy/Projects/NotebookLM/LivingTruthEngine
docker compose -f docker/docker-compose.yml up -d

# Validate setup
./scripts/setup/validate_docker.sh
```

### **4. Access Services**
- **Langflow**: http://localhost:7860 (admin/admin)
- **MCP Server**: Running locally (not in Docker)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Neo4j**: http://localhost:7474
- **LM Studio**: http://localhost:1234 (with system model access)
 - **Dashboard**: http://localhost:8050 (health at /health, metadata at /meta including tabs)
 - **DevDocs**: http://localhost:9126 (internal health service used by MCP)
 - **Rulego**: http://localhost:9127 (internal health service used by MCP)
 - **MCP Solver**: http://localhost:9128 (internal health service used by MCP)

## 📁 **Project Structure**

```
LivingTruthEngine/
├── .cursor/                          # Cursor IDE configuration
│   ├── rules/                        # Development rules and guidelines
│   │   ├── project_overview.mdc      # Project architecture and overview
│   │   ├── coding_standards.mdc      # AI-optimized coding standards
│   │   ├── development_workflow.mdc  # AI-assisted development process
│   │   ├── docker_best_practices.mdc # Docker configuration standards
│   │   ├── system_management.mdc     # Environment and automation
│   │   ├── mcp_server_integration.mdc# MCP server best practices
│   │   └── README.md                 # Rules documentation
│   ├── mcp.json                      # MCP server configuration
│   └── settings.json                 # Workspace settings
├── docker/                           # Docker configuration
│   ├── docker-compose.yml           # Service orchestration (v2)
│   └── .dockerignore                # Build exclusions
├── scripts/                          # Automation scripts
│   ├── setup/                       # Setup and configuration
│   │   ├── start_services.sh        # Start all services
│   │   ├── stop_services.sh         # Stop all services
│   │   ├── validate_docker.sh       # Docker validation
│   │   ├── update_system.sh         # System updates
│   │   └── check_system.sh          # System health checks
│   ├── analyze/                     # Analysis/archive scripts (moved here)
│   │   ├── analyze_imagination_podcast_*.py
│   │   └── archive_imagination_podcast*.py
│   ├── testing/                     # Test automation
│   └── deployment/                  # Deployment scripts
├── src/                             # Source code
│   ├── mcp_servers/                 # MCP server implementations
│   ├── analysis/                    # Analysis modules
│   └── utils/                       # Utility functions
├── data/                            # Data storage
│   ├── sources/                     # Input data sources
│   ├── outputs/                     # Analysis outputs
│   └── logs/                        # Application logs
├── config/                          # Configuration files
├── tests/                           # Test suite
├── docs/                            # Documentation
└── requirements.txt                 # Python dependencies
```



## 🔧 **Development Features**

### **MCP Server Tools (25 Total)**

#### **Living Truth FastMCP Server (24 tools)**
- **LM Studio Tools** (4): `get_lm_studio_models`, `generate_lm_studio_text`, `test_lm_studio_connection`, `get_lm_studio_status`
- **Core Tools** (6): `query_langflow`, `get_status`, `list_sources`, `analyze_transcript`, `generate_viz`, `generate_audio`
- **Batch Tools** (2): `batch_system_operations`, `batch_analysis_operations`
- **Utility Tools** (5): `get_project_info`, `get_current_time`, `test_tool`, `fix_flow`, `query_flowise`
- **Automation Tools** (5): `auto_detect_and_add_tools`, `auto_update_all_documentation`, `auto_update_cursor_rules`, `auto_validate_system_state`, `comprehensive_health_check`
- **Cursor Rule Tools** (2): `validate_cursor_rules`, `fix_cursor_rule_frontmatter` - Validate and fix cursor rule frontmatter

#### **Langflow MCP Server (6 tools)**
- `query_langflow` - Query Langflow workflows for survivor testimony analysis
- `create_langflow` - Create or update Langflow workflows programmatically
- `get_langflow_status` - Langflow system status and connection information
- `list_langflow_tools` - List available tools in Langflow
- `get_current_time` - Get current time as test tool
- `test_tool` - Simple test tool for Cursor detection

### **Additional MCP Servers (8 Total)**
- **DevDocs MCP Server**: Document retrieval and crawling (`crawl_docs`, `retrieve_docs`, `get_devdocs_status`, `get_devdocs_info`) — backed by an internal lightweight service exposing `/health` on port 9126
- **Rulego MCP Server**: Workflow orchestration (`query_rulego_chain`, `list_rulego_chains`, `create_rulego_chain`, `get_rulego_status`, `get_rulego_info`) — backed by an internal lightweight service exposing `/health` on port 9127
- **MCP Solver Server**: Constraint solving and LLM routing (`solve_constraint`, `route_llm`, `list_solver_capabilities`, `get_solver_status`, `get_solver_info`) — backed by an internal lightweight service exposing `/health` on port 9128
- **GitHub MCP Server**: Repository management and collaboration
- **PostgreSQL MCP Server**: Database operations and querying
- **Hugging Face MCP Server**: Model and dataset access

### **AI-Assisted Development**
- **Code generation** with context awareness
- **Automated testing** and validation
- **Intelligent refactoring** suggestions
- **Documentation generation**
- **Workflow optimization**

### **Cursor Rule Management**
- **Automated Validation**: Use `validate_cursor_rules()` to check all `.mdc` files for proper frontmatter
- **Automated Fixing**: Use `fix_cursor_rule_frontmatter(filename)` to fix specific cursor rule files
- **Proper Configuration**: 4 always-apply rules (project-wide), 13 file-specific rules with globs
- **Best Practices**: Follows Cursor documentation for rule types and `alwaysApply` settings

### **Docker Best Practices**
- **Docker Compose v2**: Modern syntax and features
- **BuildKit**: Fast, efficient builds
- **Security**: Non-root users, read-only volumes
- **Health Checks**: Comprehensive monitoring
- **Performance**: Slim images, layer optimization

## 🔧 **Development Workflow**

### **1. Daily Development**
```bash
# Activate environment
source living_venv/bin/activate

# Start services
./scripts/setup/start_services.sh

# Check system status
./scripts/setup/check_system.sh
```

### **2. AI-Assisted Coding**
```bash
# Use Cursor AI for code generation
# Reference rules with @ruleName
# Leverage MCP tools for automation
```

## 🧭 Analysis and MCP-first Batching

- Analysis/archive scripts were moved to `scripts/analyze/` (see above). Prefer triggering analysis through the MCP Hub meta-tools rather than invoking scripts directly.
- Use batching to minimize calls and cost:
  - Analysis: `execute_category_tools('analysis', ...)` or `batch_execute_tools([...])`
  - GitHub (via hub): `execute_github_tool` or `execute_category_tools('github', ...)` with only these tools: `list_repositories`, `search_repositories`, `create_issue`, `get_github_status`

### **3. Testing and Validation**
```bash
# Run tests
python -m pytest tests/

# Validate Docker setup
./scripts/setup/validate_docker.sh

# Check MCP servers
python src/mcp_servers/test_mcp_server.py
```

### **4. System Maintenance**
```bash
# Update system components
./scripts/setup/update_system.sh

# Clean up resources
docker system prune
docker image prune -f
```

## 📊 **Development Guidelines**

### **Cursor Rules**
- **`@project_overview`**: Project architecture and overview
- **`@coding_standards`**: AI-optimized coding standards
- **`@development_workflow`**: AI-assisted development process
- **`@docker_best_practices`**: Docker configuration standards
- **`@system_management`**: Environment and automation
- **`@mcp_server_integration`**: MCP server best practices
- **`@error_handling_and_testing`**: Error handling and testing standards

## 🎯 **Current Working State**

### **✅ All Services Operational**
- **Langflow**: http://localhost:7860 (admin/admin) - AI workflow orchestration
- **LM Studio**: http://localhost:1234 - Local model hosting with system model access
- **PostgreSQL**: localhost:5432 - Database with langflow database
- **Neo4j**: http://localhost:7474 - Graph database for relationship analysis
- **Redis**: localhost:6379 - Caching and session management
- **Dash Dashboard**: http://localhost:8050 - Interactive visualizations

### **✅ Phase 8 Complete - Real Data Ingestion**
- **YouTube Channel Adapter**: Real discovery and processing from Imagination Station channel
- **Depth-Limited Expansion**: Configurable crawl depth for external link expansion
- **OCR/JS Toggles**: Optional OCR and JavaScript rendering capabilities
- **Verifiable Bundles**: Complete .veritasrun bundles with manifest, corpus, proofs, merkle, metrics
- **Dashboard Controls**: Full control over ingestion parameters via web interface
- **MCP Integration**: All Phase 8 features accessible via MCP tools
- **Flag Loading System**: Proper configuration management from veritas_flags.toml
- **Real Data Processing**: Successfully ingesting real YouTube data with transcripts

### **✅ MCP Server Status (8 Total)**
- **Living Truth FastMCP Server**: 22 tools available (includes LM Studio integration, audio generation)
- **Langflow MCP Server**: 6 tools available (includes create_langflow tool)
- **GitHub MCP Server**: Repository management
- **PostgreSQL MCP Server**: Database operations
- **Hugging Face MCP Server**: Model access
- **DevDocs MCP Server**: Document retrieval and crawling
- **Rulego MCP Server**: Workflow orchestration
- **MCP Solver Server**: Constraint solving and LLM routing

### **✅ Recent Achievements**
- **Proper Error Handling**: No fallback mechanisms, fail-fast approach
- **Phase 8 Implementation Complete**: Real YouTube data ingestion with all features operational
- **Flag Loading System Fixed**: Proper configuration management from veritas_flags.toml
- **Comprehensive Testing**: Phase 7 (3/3) and Phase 8 (3/3) tests passing with real data
- **Performance Targets**: All services responding under 2s
- **Programmatic Workflow Management**: create_langflow tool implemented
- **All MCP Servers**: Working with green dots in Cursor
- **Real Data Processing**: Successfully ingesting real YouTube data with transcripts
- **Bundle Creation**: Complete .veritasrun bundles with real data
- **Code Quality Improvements**: 92% warning reduction and modern Python practices
- **`@mcp_server_integration`**: MCP server best practices

### **MCP Server Usage**
```python
# Example: Query Langflow workflow
result = mcp_living_truth_fastmcp_server_query_langflow(
    query="Analyze survivor testimony for corroborating evidence",
    anonymize=True,
    output_type="summary"
)

# Example: System status check
status = mcp_living_truth_fastmcp_server_get_status()
```

### **Docker Commands**
```bash
# Start services with BuildKit
DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml up -d

# Validate configuration
docker compose -f docker/docker-compose.yml config

# Monitor services
docker compose -f docker/docker-compose.yml logs -f
```

## 🎯 **Best Practices**

### **Development Standards**
1. **Use virtual environment** for all Python operations
2. **Reference cursor rules** with @ commands
3. **Leverage MCP tools** for automation
4. **Follow Docker best practices** for containerization
5. **Maintain comprehensive documentation**

### **Code Quality**
- **Type hints** for better AI understanding
- **Comprehensive docstrings** for context
- **Consistent naming conventions**
- **Modular architecture** for maintainability
- **Error handling** with proper logging

### **Docker Best Practices**
- **Use Docker Compose v2** syntax
- **Enable BuildKit** for faster builds
- **Implement security** with non-root users
- **Configure health checks** for monitoring
- **Use slim base images** for efficiency

## 📈 **Performance Metrics**

### **System Performance**
- **Service Uptime**: 99%+ availability
- **API Response Time**: < 2 seconds
- **Build Time**: < 5 minutes with BuildKit
- **Resource Usage**: < 80% CPU/memory utilization

### **Development Metrics**
- **Code Quality**: 100% type coverage, >90% test coverage
- **Docker Efficiency**: Slim images, optimized layers
- **MCP Integration**: < 1 second tool response time
- **Development Velocity**: 3x improvement with AI assistance

## 🔐 **Security**

### **Docker Security**
- **Non-root users** in all containers
- **Read-only volumes** for sensitive data
- **Network isolation** with custom networks
- **Health checks** for service monitoring

### **Data Security**
- **Environment variables** for sensitive data
- **API key management** through MCP
- **Secure data processing** with anonymization
- **Backup and recovery** procedures

## 🤝 **Contributing**

### **Development Standards**
1. **Follow cursor rules** for consistent development
2. **Use established patterns** from project structure
3. **Leverage MCP tools** for automation
4. **Maintain documentation** with AI assistance

### **Quality Assurance**
- **Run validation scripts** before committing
- **Follow Docker best practices** for containerization
- **Reference appropriate cursor rules**
- **Test with MCP integration**
- **Validate system health** regularly

## 📞 **Support**

### **Documentation**
- **Cursor Rules**: Check `.cursor/rules/` for development guidelines
- **Docker Setup**: See `docker/` directory for configuration
- **Scripts**: Check `scripts/` directory for automation tools

### **Troubleshooting**
- **Docker Issues**: Run `./scripts/setup/validate_docker.sh`
- **System Problems**: Run `./scripts/setup/check_system.sh`
- **MCP Server Issues**: Check MCP server integration rules
- **Development Questions**: Reference cursor rules with @ commands

---

**Living Truth Engine** - Advanced AI-powered system for survivor testimony corroboration and evidence analysis, built with modern Docker practices and comprehensive development guidelines.

## 📋 **Quick Reference**

### **Essential Commands**
```bash
# Start development environment
source living_venv/bin/activate
./scripts/setup/start_services.sh

# Validate system
./scripts/setup/validate_docker.sh
./scripts/setup/check_system.sh

# Update system
./scripts/setup/update_system.sh

# Clean up resources
docker system prune
docker image prune -f
```

### **Service URLs**
- **Langflow**: http://localhost:7860
- **PostgreSQL**: localhost:5432
- **Neo4j**: http://localhost:7474
- **Redis**: localhost:6379
- **LM Studio**: http://localhost:1234
- **Living Truth Engine**: http://localhost:9123-9124
- **MCP Server**: Running locally (not in Docker) for stability
- **DevDocs**: http://localhost:9126 — internal health service used by MCP
- **Rulego**: http://localhost:9127 — internal health service used by MCP
- **MCP Solver**: http://localhost:9128 — internal health service used by MCP

### **Key Files**
- **Docker Compose**: `docker/docker-compose.yml`
- **Cursor Rules**: `.cursor/rules/`
- **MCP Config**: `.cursor/mcp.json`
- **Environment**: `.env` 