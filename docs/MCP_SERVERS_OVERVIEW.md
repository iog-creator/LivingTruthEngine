# MCP Servers Overview

## Description
This document provides a comprehensive overview of all MCP (Model Context Protocol) servers in the Living Truth Engine system, including their tools, purposes, and integration patterns.

## 🎯 **MCP Server Architecture**

### **MCP Hub Server (Primary Gateway)**
- **File**: `src/mcp_servers/mcp_hub_server.py`
- **Purpose**: Single consolidated server providing access to all 63 tools via 15 meta-tools
- **Tools**: 15 meta-tools for tool discovery, execution, and management
- **Status**: ✅ Active and operational

### **Underlying MCP Servers (8 servers, 63 tools total)**

#### **1. Living Truth FastMCP Server**
- **File**: `src/mcp_servers/living_truth_fastmcp_server.py`
- **Tools**: 22 tools
- **Purpose**: Core analysis engine for survivor testimony analysis
- **Categories**:
  - **LM Studio Tools**: Model access and text generation
  - **Core Tools**: Transcript analysis and visualization
  - **Batch Tools**: Bulk operations and system management
  - **Utility Tools**: Project information and testing
  - **Automation Tools**: Documentation and system validation

#### **2. Langflow MCP Server**
- **File**: `src/mcp_servers/langflow_mcp_server.py`
- **Tools**: 12 tools
- **Purpose**: Langflow workflow management and JSON import/export
- **Features**:
  - Workflow creation and management
  - JSON import/export for accurate schema handling
  - Node configuration and flow execution
  - Template-based workflow building

#### **3. PostgreSQL MCP Server**
- **File**: `src/mcp_servers/postgresql_mcp_server.py`
- **Tools**: 6 tools
- **Purpose**: Database operations and management
- **Features**:
  - Database connectivity and health checks
  - Query execution and result processing
  - Schema management and data validation

#### **4. Hugging Face MCP Server**
- **File**: `src/mcp_servers/huggingface_mcp_server.py`
- **Tools**: 5 tools
- **Purpose**: Model access and inference
- **Features**:
  - Model listing and information
  - Text generation and inference
  - Model metadata and configuration

#### **5. DevDocs MCP Server**
- **File**: `src/mcp_servers/devdocs_mcp_server.py`
- **Tools**: 4 tools
- **Purpose**: Documentation retrieval and search
- **Features**:
  - Documentation crawling and indexing
  - Content retrieval and search
  - Documentation status and health

#### **6. Rulego MCP Server**
- **File**: `src/mcp_servers/rulego_mcp_server.py`
- **Tools**: 5 tools
- **Purpose**: Workflow orchestration and rule management
- **Features**:
  - Chain creation and management
  - Rule execution and validation
  - Workflow orchestration

#### **7. MCP Solver Server**
- **File**: `src/mcp_servers/mcp_solver_server.py`
- **Tools**: 5 tools
- **Purpose**: Constraint solving and optimization
- **Features**:
  - Constraint definition and solving
  - Optimization algorithms
  - Problem modeling and solution generation

#### **8. GitHub MCP Server**
- **File**: `src/mcp_servers/github_mcp_server.py`
- **Tools**: 4 tools
- **Purpose**: Repository management and version control
- **Features**:
  - Repository operations
  - Issue and pull request management
  - Code analysis and metrics

## 📋 **Tool Categories and Functions**

### **Analysis Tools (Living Truth FastMCP Server)**
- `analyze_transcript()` - Analyze survivor testimony for patterns
- `generate_viz()` - Create visualizations and network graphs
- `generate_audio()` - Text-to-speech synthesis
- `query_langflow()` - Query Langflow workflows
- `list_sources()` - List available data sources

### **System Management Tools**
- `get_status()` - System health and status
- `get_project_info()` - Project information and configuration
- `comprehensive_health_check()` - Full system validation
- `auto_validate_system_state()` - Automated system validation

### **Workflow Management Tools (Langflow MCP Server)**
- `create_langflow()` - Create new workflows
- `export_flow_to_file()` - Export workflows to JSON
- `import_flow_from_json()` - Import workflows from JSON
- `configure_node_in_flow()` - Configure workflow nodes
- `add_node_to_flow()` - Add nodes to workflows

### **Database Tools (PostgreSQL MCP Server)**
- `execute_query()` - Execute SQL queries
- `get_table_info()` - Get table schema information
- `backup_database()` - Create database backups
- `restore_database()` - Restore from backups

### **Model Access Tools (Hugging Face MCP Server)**
- `list_models()` - List available models
- `generate_text()` - Generate text using models
- `get_model_info()` - Get model metadata
- `test_model_connection()` - Test model connectivity

## 🔧 **Integration Patterns**

### **MCP Hub Server Integration**
```python
# Access any tool through the hub server
from mcp_servers.mcp_hub_server import MCPHubServer

hub = MCPHubServer()
result = hub.execute_tool("analyze_transcript", {"transcript_name": "test"})
```

### **Direct Server Access**
```python
# Access specific servers directly
from mcp_servers.living_truth_fastmcp_server import LivingTruthEngine

engine = LivingTruthEngine()
result = engine.analyze_transcript("test_transcript")
```

### **Batch Operations**
```python
# Execute multiple tools in sequence
tools = [
    {"name": "get_status", "params": {}},
    {"name": "analyze_transcript", "params": {"transcript_name": "test"}}
]
results = hub.batch_execute_tools(tools)
```

## 📊 **Performance and Monitoring**

### **Performance Targets**
- **Individual tool execution**: <1 second
- **Batch operations**: <5 seconds
- **Registry loading**: <0.1 seconds
- **Error recovery**: <1 second

### **Monitoring Features**
- **Automatic timing** for all tool executions
- **Performance warnings** for slow operations
- **Error tracking** with detailed logging
- **Health checks** for all servers

### **Backup and Recovery**
- **Automatic registry backup** on load
- **Recovery from backup** on corruption
- **Enhanced validation** with error reporting
- **Graceful degradation** on failures

## 🚨 **Troubleshooting**

### **Common Issues**
1. **Tool not found**: Check registry with `list_tools()`
2. **Import errors**: Verify module paths and PYTHONPATH
3. **Performance issues**: Monitor execution times and optimize
4. **Registry corruption**: Use automatic backup recovery

### **Recovery Procedures**
1. **Restart MCP Hub Server**: Reload registry and tools
2. **Validate registry**: Check tool definitions and schemas
3. **Check server health**: Verify all underlying servers
4. **Monitor performance**: Track execution times and warnings

## 📚 **Related Documentation**
- **@mcp_hub_server.mdc** - Detailed hub server documentation
- **@mcp_server_integration.mdc** - Integration patterns and best practices
- **@current_working_state.mdc** - Current system status
- **LANGFLOW_MCP_TOOLS.md** - Langflow-specific tools and workflows

## 🎯 **Success Metrics**
- ✅ **100% tool access** - All 63 tools accessible via hub
- ✅ **100% performance** - All tools meet timing targets
- ✅ **100% reliability** - Backup and recovery systems active
- ✅ **100% monitoring** - Comprehensive performance tracking
- ✅ **100% documentation** - Complete tool and server documentation

---

**This MCP server architecture provides scalable, reliable, and performant access to all system tools while maintaining optimal Cursor integration.** 