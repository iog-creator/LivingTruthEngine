---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['links.json', 'PHASE_9.md', 'manifest.json', 'PHASE_8.md', 'docs/project_master_log.md', 'verification.json']
---

# Living Truth Engine - Phase 9: Multi-Source Expansion & Advanced Evidence Linking

> 📚 **Project History**: See the full, append‑only log in  
> `docs/project_master_log.md`

## 🎯 **Phase 9 Objective**

Expand the system beyond a single YouTube channel to support **multiple simultaneous sources** (websites, PDFs, images, and other channels), add **cross-document linking and visualization**, and integrate more **AI-assisted verification workflows**.

## 🚀 **Current Status: Phase 9 Development Repository**

This repository contains the **Phase 9 development branch** of the Living Truth Engine, focused on:

### **✅ Phase 8.3 Foundation (Complete)**
- **Real AI Integration**: Desktop LM Studio on port 1234 for actual LLM generation
- **Advanced Visualization**: Interactive 3D network graphs with Plotly
- **Complete Analysis Pipeline**: Single 'Start Complete Analysis' button orchestrates entire workflow
- **Modern Single-File UI**: Clean, responsive interface with dark theme
- **System Integration**: Docker networking, MCP server with 20+ tools, health gates
- **Documentation & Rules**: Updated README.md, cursor rules, comprehensive documentation

### **✅ Phase 9.2.5: Rule System Rehabilitation (Complete)**
- **Consolidated Workflow**: Single `core_workflow.mdc` replaces conflicting workflow rules
- **MCP-First Rule Management**: Automated rule validation, archiving, and template application
- **Explicit Fallback Exceptions**: Clear guidance on allowed vs. forbidden fallbacks
- **Standardized Completion**: Automated phase completion summaries with health status
- **Archived Stale Rules**: Moved outdated and conflicting rules to `.cursor/rules/archive/`

### **✅ Phase 9.5.3: Timeline API + Graph Polish (Complete)**
- **Timeline API**: `/api/timeline/{run_id}` endpoint with <25ms response time
- **Graph UX Enhancements**: Node type filters, search, pinning, and selection polish
- **Graph Build Fix**: Resolved constraint violations with UPSERT support and transaction safety
- **Performance Optimization**: All APIs meeting timing requirements (<1s timeline, <2s graph)
- **Error Handling**: Enhanced with specific constraint violation error codes (409)

### **✅ Phase 9.5.5: Error Budgeting & Recovery Automation (Complete)**
- **Error Budget Framework**: SLO/SLI monitoring with rolling window calculations
- **Automated Recovery Workflows**: Self-healing mechanisms with configurable cooldown
- **Chaos Engineering**: Failure simulation and recovery time validation
- **CI/CD Integration**: Error budget validation and recovery script testing

### **✅ Phase 9.5.6: Chaos Engineering & Proactive Resilience (Complete)**
- **Enhanced Chaos Testing**: 6 chaos scenarios with blast radius control and safeguards
- **Predictive Monitoring**: Real-time anomaly detection with early-warning alerts
- **Proactive Recovery**: Adaptive response policies with service scaling and graceful degradation
- **Resilience Dashboard**: Infrastructure for resilience score calculation and historical analysis
- **MCP Tools**: `trigger_chaos_scenario()`, `get_resilience_score()`, `simulate_proactive_recovery()`

### **🎯 Phase 9.5.7: Resilience Dashboard UI (Next)** 🚀 READY TO START
- **Resilience Dashboard**: Interactive UI for chaos test results and resilience metrics
- **Real-time Monitoring**: Live updates of resilience scores and anomaly alerts
- **Historical Analysis**: Trend visualization and predictive analytics
- **CI/CD Integration**: Resilience score validation and dashboard testing

## 🔧 **Development Workflow**

### **Core Workflow (BUILD → VERIFY → ITERATE)**
All development follows the strict workflow defined in `.cursor/rules/core_workflow.mdc`:

1. **BUILD**: `docker compose -f docker/docker-compose.yml up -d --build`
2. **VERIFY**: Run health gates and smoke tests
3. **ITERATE**: Fix failures and re-run from BUILD

### **MCP-First Rule Management**
- **Rule Validation**: `validate_cursor_rules()` - Check all .mdc files for proper frontmatter
- **Rule Archiving**: `ruleset_archive_outdated()` - Move stale rules to archive/
- **Template Application**: `ruleset_apply_templates()` - Ensure core rules exist
- **Completion Summary**: `generate_phase_completion_summary()` - Auto-generate phase documentation

### **Allowed Fallback Exceptions**
- YouTube captions/transcripts fallback when MCP fetch fails
- Reranker CPU execution when GPU is occupied (logged)
- Local dev data only when `ALLOW_FALLBACKS=true`
- In-memory search fallback if pgvector is unavailable (dev only)

## 🏗️ **Architecture**

### **Service Architecture**
```
┌─────────────────┐
│ Cursor AI       │
└─────────────────┘
        │ (15 meta-tools)
        ▼
┌─────────────────┐
│ MCP Hub Server  │
│ (Registry: 99+  │
│  tools)         │
└─────────────────┘
        │ (Proxy calls)
        ▼
┌─────────────────┬─────────────────┬─────────────────┐
│ Living Truth   │ Langflow MCP    │ Other Servers   │
│ FastMCP Server │ Server          │ (GitHub, DB,    │
│ (22 tools)     │ (12 tools)      │ HF, DevDocs,    │
│                │                 │ Rulego, Solver) │
└─────────────────┴─────────────────┴─────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│ Unified Dashboard│    │   PostgreSQL    │
│   (Port 8050)   │    │   (Port 5432)   │
│                 │    │                 │
│ • Guided UI     │    │ • Data Storage  │
│ • Multi-Source  │    │ • Langflow DB   │
│ • Evidence Graph│    │ • Analysis Data │
│ • Verification  │    │                 │
└─────────────────┘    └─────────────────┘
        │
        ▼
┌─────────────────┐
│   Langflow      │
│   (Port 7860)   │
│                 │
│ • Multi-Agent   │
│ • Python Native │
│ • Workflow UI   │
└─────────────────┘
```

## 📁 **Project Structure**

```
LivingTruthEngine-Phase9/
├── docker/                    # Docker configuration
│   ├── docker-compose.yml    # Service orchestration
│   └── .dockerignore         # Build exclusions
├── scripts/                   # Automation scripts
│   ├── setup/                # Setup and configuration
│   ├── testing/              # Test automation
│   └── deployment/           # Deployment scripts
├── src/                      # Source code
│   ├── mcp_servers/          # MCP server implementations
│   ├── analysis/             # Analysis modules
│   ├── ingestion_general/    # Multi-source ingestion
│   └── utils/                # Utility functions
├── data/                     # Data storage
│   ├── sources/              # Input data sources
│   ├── outputs/              # Analysis outputs
│   └── logs/                 # Application logs
├── config/                   # Configuration files
│   ├── tool_registry.json   # MCP Hub Server tool registry
│   └── source_registry.toml # Phase 9: Multi-source registry
├── tests/                    # Test suite
├── docs/                     # Documentation
└── .cursor/                  # Cursor IDE configuration
    ├── rules/                # Development rules
    └── mcp.json             # MCP Hub Server configuration
```

## 🔧 **Technology Stack**

### **Core Technologies**
- **Python 3.13**: Primary programming language
- **PostgreSQL 17**: Database system with langflow database
- **Neo4j 5.15.0**: Graph database for relationship analysis
- **Redis 7.2**: Caching and session management
- **Docker**: Containerization platform
- **Docker Compose v2**: Service orchestration

### **AI and ML**
- **LangChain**: AI framework for LLM integration
- **Hugging Face**: Model hosting and inference
- **OpenAI**: Language model API
- **SpaCy**: Natural language processing (Phase 9: NER models)

### **MCP Integration**
- **MCP Hub Server**: Consolidated tool gateway with 15 meta-tools
- **Tool Registry**: Central registry of 99 tools across 8 servers
- **FastMCP**: Framework for MCP server implementation
- **Dynamic Loading**: On-demand tool loading for efficiency
- **Piper TTS**: Text-to-speech synthesis
- **Dash/Plotly**: Interactive data visualizations

## 🚀 **Quick Start**

### **1. Environment Setup**
```bash
# Clone the repository
git clone <repository-url>
cd LivingTruthEngine-Phase9

# Activate virtual environment
source living_venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Start Services**
```bash
# Start all services
docker compose -f docker/docker-compose.yml up -d

# Verify services are running
curl http://localhost:8050/api/health
```

### **3. Access the Modern UI**
- **Dashboard**: http://localhost:8050/static/ui_status_chat.html
- **Langflow**: http://localhost:7860
- **API Health**: http://localhost:8050/api/health/full

## 📋 **Phase 9 Implementation Plan**

### **1. Multi-Source Runner Backend**
- [ ] Update `VeritasRunner` to accept multiple source configs
- [ ] Implement source adapters (`youtube_adapter`, `web_fetcher`, `pdf_extractor`)
- [ ] Merge docs into unified corpus with per-source tags

### **2. Source Registry**
- [ ] Create `config/source_registry.toml` with reusable source presets
- [ ] Implement source list management from Dashboard

### **3. Entity & Claim Linking**
- [ ] Enhance canonicalization to extract named entities (NER model)
- [ ] Implement claims extraction (subject-predicate-object triples)
- [ ] Create `links.json` in bundle with cross-document edges

### **4. Evidence Graph**
- [ ] Implement `/api/graph/{run_id}` endpoint
- [ ] Create interactive 2D/3D evidence graph view
- [ ] Add filtering by entity type, date, confidence

### **5. AI-Assisted Verification**
- [ ] Implement `verify_claims_in_run(run_id)` MCP tool
- [ ] Add corroboration/contradiction detection
- [ ] Create `verification.json` in bundles

### **6. Dashboard Changes**
- [ ] Update "New Run" form for multiple source selection
- [ ] Add per-source parameter controls
- [ ] Implement Evidence Graph tab in Analyze section
- [ ] Add claim verification panel

### **7. Enhanced Manifest Schema**
- [ ] Update `manifest.json` schema with `sources` array
- [ ] Add `links` reference to links.json
- [ ] Add `verification` reference to verification.json

## 🧪 **Testing**

### **Run Tests**
```bash
# Functional tests
pytest tests/test_no_fallbacks.py tests/test_health_gates.py -v

# Phase 9 specific tests
pytest tests/test_multi_source.py tests/test_evidence_graph.py -v
```

### **Verification Scripts**
```bash
# Bring-up and smoke tests
bash scripts/bring_up.sh && bash scripts/smoke_youtube.sh

# Multi-source verification
bash scripts/smoke_multi_source.sh
```

## 📚 **Documentation**

- **PHASE_9_PLAN.md**: Detailed implementation plan
- **PHASE_8_3_NEW_UI_COMPLETION.md**: Phase 8.3 completion summary
- **CONSOLIDATED_COMPLETION_SUMMARY.md**: Overall project status
- **.cursor/rules/**: Development rules and guidelines

## 🔍 **API Endpoints**

### **Health & Status**
- `GET /api/health` - Basic health check
- `GET /api/health/full` - Comprehensive health check
- `GET /api/tools` - Available MCP tools

### **Runs Management**
- `GET /api/runs` - List all runs
- `GET /api/runs/{id}` - Get run details
- `GET /api/runs/{id}/corpus` - Get run corpus
- `POST /api/runs/youtube/start` - Start YouTube analysis

### **Analysis & Execution**
- `POST /api/execute` - Execute MCP tools
- `POST /api/ai/chat` - AI chat interface
- `GET /api/visualizations/{run_id}` - Get visualizations

### **Phase 9 Endpoints (In Development)**
- `GET /api/graph/{run_id}` - Evidence graph data
- `POST /api/runs/multi-source/start` - Start multi-source analysis
- `GET /api/verification/{run_id}` - Claim verification results

## 🛠️ **Development Guidelines**

### **Code Standards**
- **Type Hints**: Required for all Python functions
- **Docstrings**: Comprehensive documentation
- **Naming**: Consistent snake_case for Python, camelCase for JavaScript
- **Error Handling**: Explicit error handling with logging
- **Testing**: 90%+ code coverage required

### **Phase 9 Specific Guidelines**
- **Multi-source First**: All new features must support multiple sources
- **Evidence Linking**: Prioritize cross-document relationship discovery
- **AI Verification**: Integrate AI-assisted claim verification
- **Graph Visualization**: Focus on interactive evidence graphs

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Service Startup**: Port conflicts, missing dependencies
2. **Database Issues**: Connection problems, data corruption
3. **MCP Server**: Configuration errors, tool availability
4. **Performance**: Resource constraints, slow queries
5. **Security**: Permission issues, authentication problems

### **Recovery Procedures**
- **Service Restart**: Automated restart procedures
- **Data Recovery**: Backup and restore procedures
- **Configuration Reset**: Reset to known good state
- **Environment Reset**: Complete environment rebuild

## 📊 **Quality Metrics**

### **Code Quality**
- **Type Coverage**: 100% type hints
- **Documentation**: 100% docstring coverage
- **Test Coverage**: >90% code coverage
- **Linting**: Zero linting errors
- **Security**: No security vulnerabilities

### **System Performance**
- **Uptime**: 99%+ service availability
- **Response Time**: <2s for API calls
- **Resource Usage**: <80% CPU/memory utilization
- **Build Time**: <5 minutes for full build
- **Deployment**: <2 minutes for deployment

---

**This repository represents the Phase 9 development branch of the Living Truth Engine, focused on multi-source expansion and advanced evidence linking capabilities.** 