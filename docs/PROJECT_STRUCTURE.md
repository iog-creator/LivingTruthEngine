# Project Structure

## Description
This document provides a comprehensive overview of the Living Truth Engine project structure, including all directories, files, and their purposes.

## 🎯 **Root Directory Structure**

```
LivingTruthEngine/
├── .cursor/                    # Cursor IDE configuration
│   ├── rules/                 # Cursor rules (.mdc files)
│   └── mcp.json              # MCP server configuration
├── .git/                      # Git version control
├── .vscode/                   # VS Code configuration
│   └── settings.json         # VS Code settings
├── Archive_Legacy/            # Legacy and archived files
├── config/                    # Configuration files
│   ├── tool_registry.json    # MCP Hub Server tool registry
│   ├── tool_registry.json.bak # Backup of tool registry
│   ├── living_truth_config.json # Living Truth Engine configuration
│   ├── living_truth_full_flow.json # Langflow workflow configuration
│   ├── rulego.conf           # Rulego configuration
│   ├── package.json          # Node.js dependencies
│   └── package-lock.json     # Node.js lock file
├── data/                      # Data storage
│   ├── flows/                # Langflow workflow files
│   ├── models/               # Model files and configurations
│   ├── outputs/              # Analysis outputs
│   │   ├── audio/           # Generated audio files
│   │   ├── logs/            # Application logs
│   │   └── visualizations/  # Generated visualizations
│   ├── processed/           # Processed data files
│   ├── solutions/           # Analysis solutions
│   └── sources/             # Input data sources
│       ├── analysis/        # Analysis results
│       ├── backups/         # Data backups
│       ├── devdocs/         # Documentation files
│       ├── keyframes/       # Video keyframes
│       ├── organized/       # Organized data
│       └── videos/          # Video files
├── docker/                   # Docker configuration
│   ├── docker-compose.yml   # Main Docker Compose file
│   ├── docker-compose.langflow.yml # Langflow-specific compose
│   ├── Dockerfile           # Main Dockerfile
│   └── Dockerfile.dash      # Dash dashboard Dockerfile
├── docs/                     # Documentation
│   ├── DEPLOYMENT_GUIDE.md  # Deployment instructions
│   ├── LANGFLOW_MCP_TOOLS.md # Langflow MCP tools documentation
│   ├── LANGFLOW_NODE_INDEX.md # Langflow node documentation
│   ├── LM_STUDIO_MODEL_ACCESS.md # LM Studio model access
│   ├── MCP_SERVERS_OVERVIEW.md # MCP servers documentation
│   ├── PROJECT_SETUP.md     # Project setup guide
│   ├── PROJECT_STRUCTURE.md # This file
│   ├── README.md            # Documentation README
│   ├── SYSTEM_ARCHITECTURE.md # System architecture
│   └── TESTING_OVERVIEW.md  # Testing documentation
├── logs/                     # Application logs
├── scripts/                  # Automation scripts
│   ├── deployment/          # Deployment scripts
│   ├── maintenance/         # Maintenance scripts
│   ├── setup/               # Setup and configuration scripts
│   │   ├── activate_env.sh  # Environment activation
│   │   ├── check_system.sh  # System health check
│   │   ├── clear_cursor_cache.sh # Cursor cache cleanup
│   │   ├── fix_cursor_apparmor.sh # Cursor AppArmor fix
│   │   ├── import_langflow_workflow.py # Langflow workflow import
│   │   ├── quick_start.sh   # Quick start script
│   │   ├── regenerate_tool_registry.py # Tool registry regeneration
│   │   ├── restart_cursor_for_mcp.sh # Cursor MCP restart
│   │   ├── robustness_test.sh # Robustness testing
│   │   ├── setup_docker.sh  # Docker setup
│   │   ├── setup_langflow_workflow.sh # Langflow workflow setup
│   │   ├── start_cursor.sh  # Cursor startup
│   │   ├── start_langflow.sh # Langflow startup
│   │   ├── start_services.sh # Service startup
│   │   ├── stop_langflow.sh # Langflow shutdown
│   │   ├── stop_services.sh # Service shutdown
│   │   ├── update_system.sh # System updates
│   │   └── validate_docker.sh # Docker validation
│   └── testing/             # Testing scripts
│       ├── functional_tests.py # Comprehensive functional tests
│       ├── simple_performance_test.sh # Simple performance tests
│       └── trace_performance.sh # Performance tracing
├── src/                      # Source code
│   ├── analysis/            # Analysis modules
│   │   └── dash_app.py      # Dash dashboard application
│   └── mcp_servers/         # MCP server implementations
│       ├── dashboard.py     # Dashboard MCP server
│       ├── devdocs_mcp_server.py # DevDocs MCP server
│       ├── github_mcp_server.py # GitHub MCP server
│       ├── huggingface_mcp_server.py # Hugging Face MCP server
│       ├── langflow_mcp_server.py # Langflow MCP server
│       ├── living_truth_fastmcp_server.py # Living Truth FastMCP server
│       ├── mcp_hub_server.py # MCP Hub Server (main gateway)
│       ├── mcp_solver_server.py # MCP Solver server
│       ├── postgresql_mcp_server.py # PostgreSQL MCP server
│       ├── rulego_mcp_server.py # Rulego MCP server
│       ├── test_mcp_detection.py # MCP server testing
│       └── test_mcp_server.py # MCP server unit tests
├── tests/                    # Test files
│   ├── test_langflow_flow.py # Langflow flow testing
│   ├── test_langflow_mcp_server.py # Langflow MCP server tests
│   └── test_simple_flow.py  # Simple flow testing
├── .dockerignore            # Docker ignore file
├── .gitignore               # Git ignore file
├── CURRENT_STATUS.md        # Current system status
├── env.template             # Environment template
├── env_config.txt           # Environment configuration reference
├── README.md                # Main project README
└── requirements.txt         # Python dependencies
```

## 📁 **Key Directory Purposes**

### **Configuration (config/)**
- **tool_registry.json**: Central registry for all MCP tools (63 tools across 8 servers)
- **tool_registry.json.bak**: Automatic backup of tool registry
- **living_truth_config.json**: Living Truth Engine configuration
- **living_truth_full_flow.json**: Langflow workflow configuration
- **rulego.conf**: Rulego workflow orchestration configuration
- **package.json**: Node.js dependencies for web components

### **Data Storage (data/)**
- **flows/**: Langflow workflow files and exports
- **models/**: AI model files and configurations
- **outputs/**: Generated analysis outputs
  - **audio/**: Text-to-speech generated audio files
  - **logs/**: Application and analysis logs
  - **visualizations/**: Generated network graphs and visualizations
- **processed/**: Processed and cleaned data files
- **solutions/**: Analysis solutions and results
- **sources/**: Input data sources
  - **analysis/**: Analysis results and reports
  - **backups/**: Data backups and snapshots
  - **devdocs/**: Documentation files and references
  - **keyframes/**: Video keyframe extractions
  - **organized/**: Organized and structured data
  - **videos/**: Video files and transcripts

### **Documentation (docs/)**
- **DEPLOYMENT_GUIDE.md**: Complete deployment instructions
- **LANGFLOW_MCP_TOOLS.md**: Langflow MCP tools documentation
- **LANGFLOW_NODE_INDEX.md**: Langflow node reference
- **LM_STUDIO_MODEL_ACCESS.md**: LM Studio model access guide
- **MCP_SERVERS_OVERVIEW.md**: Complete MCP server documentation
- **PROJECT_SETUP.md**: Project setup and configuration
- **PROJECT_STRUCTURE.md**: This project structure guide
- **README.md**: Documentation overview
- **SYSTEM_ARCHITECTURE.md**: System architecture documentation
- **TESTING_OVERVIEW.md**: Testing procedures and metrics

### **Source Code (src/)**
- **analysis/**: Analysis and visualization modules
  - **dash_app.py**: Interactive Dash dashboard application
- **mcp_servers/**: All MCP server implementations
  - **mcp_hub_server.py**: Main MCP Hub Server (15 meta-tools)
  - **living_truth_fastmcp_server.py**: Core analysis engine (22 tools)
  - **langflow_mcp_server.py**: Langflow integration (12 tools)
  - **postgresql_mcp_server.py**: Database operations (6 tools)
  - **huggingface_mcp_server.py**: Model access (5 tools)
  - **devdocs_mcp_server.py**: Documentation retrieval (4 tools)
  - **rulego_mcp_server.py**: Workflow orchestration (5 tools)
  - **mcp_solver_server.py**: Constraint solving (5 tools)
  - **github_mcp_server.py**: Repository management (4 tools)

### **Scripts (scripts/)**
- **setup/**: Setup and configuration scripts
  - **activate_env.sh**: Virtual environment activation
  - **check_system.sh**: System health monitoring
  - **regenerate_tool_registry.py**: Tool registry management
  - **start_services.sh**: Service startup automation
  - **validate_docker.sh**: Docker configuration validation
- **testing/**: Testing and validation scripts
  - **functional_tests.py**: Comprehensive functional testing
  - **trace_performance.sh**: Performance monitoring
  - **simple_performance_test.sh**: Quick performance validation

### **Tests (tests/)**
- **test_langflow_flow.py**: Langflow workflow testing
- **test_langflow_mcp_server.py**: Langflow MCP server unit tests
- **test_simple_flow.py**: Simple workflow testing

## 🔧 **Configuration Files**

### **Environment Configuration**
- **env.template**: Template for environment variables
- **env_config.txt**: Reference for all environment variables and their purposes
- **.env**: Local environment configuration (not in git)

### **Docker Configuration**
- **docker/docker-compose.yml**: Main service orchestration
- **docker/docker-compose.langflow.yml**: Langflow-specific services
- **docker/Dockerfile**: Main application container
- **docker/Dockerfile.dash**: Dashboard container

### **IDE Configuration**
- **.cursor/**: Cursor IDE configuration
  - **rules/**: Cursor rules for AI assistance
  - **mcp.json**: MCP server configuration
- **.vscode/**: VS Code configuration
  - **settings.json**: VS Code settings and extensions

## 📊 **Data Flow**

### **Input Processing**
```
Raw Data (data/sources/) → Processing → Structured Data (data/processed/)
```

### **Analysis Pipeline**
```
Structured Data → Analysis Engine → Results (data/outputs/)
```

### **Visualization**
```
Results → Visualization Engine → Dash Dashboard (data/outputs/visualizations/)
```

### **Workflow Management**
```
Langflow Workflows (data/flows/) → MCP Tools → Analysis Results
```

## 🎯 **Key Files**

### **Core Configuration**
- **config/tool_registry.json**: Central registry for all 63 MCP tools
- **src/mcp_servers/mcp_hub_server.py**: Main MCP Hub Server implementation
- **docker/docker-compose.yml**: Service orchestration configuration
- **scripts/testing/functional_tests.py**: Comprehensive testing suite

### **Documentation**
- **README.md**: Main project overview
- **CURRENT_STATUS.md**: Current system status and metrics
- **docs/SYSTEM_ARCHITECTURE.md**: Complete system architecture
- **docs/DEPLOYMENT_GUIDE.md**: Deployment and setup instructions

### **Environment Management**
- **env_config.txt**: Complete environment variable reference
- **env.template**: Environment setup template
- **requirements.txt**: Python dependencies
- **scripts/setup/activate_env.sh**: Environment activation

## 🚀 **Development Workflow**

### **1. Environment Setup**
```bash
# Activate environment
source scripts/setup/activate_env.sh

# Start services
./scripts/setup/start_services.sh

# Validate setup
./scripts/setup/validate_docker.sh
```

### **2. Development**
```bash
# Run tests
python3 scripts/testing/functional_tests.py

# Check system health
./scripts/setup/check_system.sh

# Monitor performance
./scripts/testing/trace_performance.sh
```

### **3. Deployment**
```bash
# Deploy services
docker compose -f docker/docker-compose.yml up -d

# Start MCP Hub Server
python3 src/mcp_servers/mcp_hub_server.py &
```

## 📈 **Success Metrics**

### **Organization Metrics**
- ✅ **100% file organization**: All files in appropriate directories
- ✅ **100% documentation coverage**: All components documented
- ✅ **100% configuration management**: All configs properly organized
- ✅ **100% test organization**: All tests in proper location

### **Structure Quality**
- ✅ **Clear separation**: Configuration, data, code, and documentation separated
- ✅ **Logical grouping**: Related files grouped in appropriate directories
- ✅ **Scalable structure**: Structure supports future growth
- ✅ **Maintainable organization**: Easy to navigate and maintain

---

**This project structure provides a clean, organized, and scalable foundation for the Living Truth Engine, with clear separation of concerns and comprehensive documentation.** 