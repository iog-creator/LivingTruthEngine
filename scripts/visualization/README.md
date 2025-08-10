# MCP Visualization System

This directory contains the interactive visualization system for the Living Truth Engine MCP Hub Server. The system provides a web-based interface for interacting with all 63 MCP tools through a beautiful, interactive visualization.

## 🎯 Overview

The MCP Visualization System consists of:

1. **Interactive HTML Visualization** (`phase8_pipeline_visualization.html`)
   - Beautiful, responsive web interface
   - Real-time tool execution
   - Interactive pipeline stages
   - Tool parameter configuration

2. **FastAPI Server** (`mcp_visualization_api.py`)
   - REST API for tool execution
   - Real-time connection to MCP Hub Server
   - Automatic tool discovery and parameter generation

3. **Startup Script** (`start_visualization_server.sh`)
   - Automated environment setup
   - Dependency checking
   - Server startup with proper configuration

## 🚀 Quick Start

### Prerequisites

1. **Living Truth Engine Environment**
   - Virtual environment activated (`living_venv`)
   - All Docker services running
   - MCP Hub Server operational

2. **Dependencies**
   - FastAPI
   - Uvicorn
   - All MCP server dependencies

### Starting the Visualization

1. **Ensure all services are running:**
   ```bash
   # Start Docker services
   docker compose -f docker/docker-compose.yml up -d
   
   # Verify MCP Hub Server is accessible
   python src/mcp_servers/mcp_hub_server.py
   ```

2. **Start the visualization server:**
   ```bash
   # From the project root
   ./scripts/visualization/start_visualization_server.sh
   ```

3. **Access the visualization:**
   - **Main Interface**: http://localhost:8081
   - **API Documentation**: http://localhost:8081/docs
   - **Health Check**: http://localhost:8081/api/health

## 🎨 Features

### Interactive Pipeline Stages

The visualization includes interactive stages representing different phases of the Living Truth Engine:

- **📥 Start Veritas Run** - Initialize new data ingestion runs
- **🔍 YouTube Channel Archive** - Archive YouTube channels with depth-limited expansion
- **🤖 Langflow Query** - Query the multi-agent workflow
- **📝 Transcript Analysis** - Analyze transcripts for patterns and evidence
- **📊 Generate Visualization** - Create interactive visualizations
- **📋 Run Status** - Check progress of ongoing runs
- **📚 List Runs** - View recent Veritas runs
- **📦 Open Bundle** - Examine Veritas bundles

### MCP Tool Categories

The interface organizes all 63 MCP tools into logical categories:

- **📊 Analysis Tools** - Data analysis and processing
- **🎥 Channel Archiver** - YouTube channel archiving
- **🔍 Veritas Operations** - Veritas run management
- **🤖 Langflow Integration** - Langflow workflow interaction
- **🔧 System Tools** - System status and monitoring

### Real-Time Tool Execution

- **Live Tool Discovery** - Automatically loads available tools from MCP Hub Server
- **Parameter Validation** - Validates tool parameters before execution
- **Real Results** - Executes actual MCP tools and displays real results
- **Error Handling** - Comprehensive error reporting and recovery

## 🔧 API Endpoints

The FastAPI server provides the following endpoints:

### Core Endpoints

- `GET /` - Serve the main HTML visualization
- `GET /api/health` - Health check
- `GET /api/status` - MCP Hub Server status

### Tool Management

- `GET /api/tools` - Get all available tools organized by category
- `GET /api/tools/{tool_name}` - Get detailed information about a specific tool

### Tool Execution

- `POST /api/execute` - Execute a tool with parameters

**Example Tool Execution:**
```bash
curl -X POST "http://localhost:8081/api/execute" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "get_status",
    "params": {}
  }'
```

## 🎯 Usage Examples

### 1. Check System Status

1. Click on the "🔧 System Tools" category
2. Select "get_status"
3. Click "Execute Tool"
4. View the real-time system status

### 2. Start a Veritas Run

1. Click on "📥 Start Veritas Run" stage
2. Modify parameters:
   ```json
   {
     "topic": "survivor testimony analysis",
     "max_docs": 10,
     "sources": ["youtube", "web", "pdf"]
   }
   ```
3. Click "Execute Tool"
4. Monitor the run status

### 3. Archive a YouTube Channel

1. Click on "🔍 YouTube Channel Archive" stage
2. Configure parameters:
   ```json
   {
     "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
     "max_videos": 5,
     "crawl_depth": 2
   }
   ```
3. Execute and monitor progress

### 4. Query Langflow

1. Click on "🤖 Langflow Query" stage
2. Enter your query:
   ```json
   {
     "param": "Investigate Entity A connections, output as network"
   }
   ```
3. Execute and view analysis results

## 🔍 Troubleshooting

### Common Issues

1. **"MCP Hub Server not accessible"**
   - Ensure Docker services are running
   - Check MCP Hub Server is operational
   - Verify network connectivity

2. **"Required packages not found"**
   - Activate virtual environment
   - Install missing packages: `pip install fastapi uvicorn`

3. **"Tool execution failed"**
   - Check tool parameters are valid
   - Verify tool exists in MCP Hub Server
   - Check server logs for detailed errors

4. **"Visualization not found"**
   - Ensure HTML file exists in `data/visualizations/`
   - Check file permissions

### Debug Mode

Run the server with debug logging:

```bash
# Set debug logging
export LOG_LEVEL=DEBUG

# Start server
python scripts/visualization/mcp_visualization_api.py
```

### Manual Testing

Test individual components:

```bash
# Test MCP Hub Server
python -c "
from src.mcp_servers.mcp_hub_server import MCPHubServer
hub = MCPHubServer()
print(hub.get_status())
"

# Test tool execution
python -c "
import asyncio
from src.mcp_servers.mcp_hub_server import MCPHubServer
async def test():
    hub = MCPHubServer()
    result = await hub.execute_tool('get_status', {})
    print(result)
asyncio.run(test())
"
```

## 📊 Integration with Langflow

The visualization system integrates seamlessly with Langflow:

1. **Direct Tool Access** - Execute Langflow tools directly from the interface
2. **Workflow Integration** - Query Langflow workflows with custom parameters
3. **Real-time Results** - Get immediate feedback from Langflow operations
4. **Status Monitoring** - Monitor Langflow service health and status

## 🔮 Future Enhancements

- **Real-time Updates** - WebSocket integration for live status updates
- **Batch Operations** - Execute multiple tools in sequence
- **Custom Workflows** - Create and save custom tool sequences
- **Advanced Visualizations** - Interactive charts and graphs
- **User Authentication** - Secure access control
- **Export Capabilities** - Export results and configurations

## 📚 Related Documentation

- [MCP Hub Server Documentation](../mcp_servers/README.md)
- [Living Truth Engine Overview](../../README.md)
- [Docker Services](../../docker/README.md)
- [Langflow Integration](../../docs/LANGFLOW_MCP_INTEGRATION.md)

---

**Status**: ✅ **FULLY OPERATIONAL** - Interactive visualization with real MCP tool execution capabilities.
