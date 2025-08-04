# Langflow MCP Server Integration

## Overview

This document describes the integration of Langflow with the Model Context Protocol (MCP) system, providing direct access to Langflow operations through Cursor's MCP interface.

## Architecture

### **MCP Server Configuration**

The Langflow MCP server is configured in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "lf-cursor": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "http://localhost:7860/api/v1/mcp/project/3bd92a44-057b-4378-a674-80910d570986/sse"
      ],
      "description": "Langflow MCP Server - Direct connection to Langflow instance"
    }
  }
}
```

### **Connection Flow**

1. **Cursor MCP Client** → **uvx mcp-proxy** → **Langflow MCP Server** → **Langflow Instance**
2. **Direct API Access** via `mcp_lf-cursor_*` tools
3. **Hub Server Integration** via `mcp_mcp_hub_server_execute_langflow_tool`

## Available MCP Tools

### **Direct Langflow MCP Tools**

Once Cursor is restarted with the MCP configuration, the following tools become available:

| Tool | Description | Usage |
|------|-------------|-------|
| `mcp_lf-cursor_list_flows()` | List all flows in Langflow | `mcp_lf-cursor_list_flows()` |
| `mcp_lf-cursor_create_flow()` | Create a new flow | `mcp_lf-cursor_create_flow(flow_config)` |
| `mcp_lf-cursor_run_flow()` | Execute a flow | `mcp_lf-cursor_run_flow(flow_id, inputs)` |
| `mcp_lf-cursor_get_flow_status()` | Get flow execution status | `mcp_lf-cursor_get_flow_status(flow_id)` |
| `mcp_lf-cursor_get_flow()` | Get flow details | `mcp_lf-cursor_get_flow(flow_id)` |
| `mcp_lf-cursor_update_flow()` | Update flow configuration | `mcp_lf-cursor_update_flow(flow_id, updates)` |
| `mcp_lf-cursor_delete_flow()` | Delete a flow | `mcp_lf-cursor_delete_flow(flow_id)` |

### **MCP Hub Server Integration**

The MCP Hub Server also provides Langflow tools:

| Tool | Description | Usage |
|------|-------------|-------|
| `mcp_mcp_hub_server_execute_langflow_tool()` | Execute Langflow tools via hub | `mcp_mcp_hub_server_execute_langflow_tool("create_langflow", {"flow_config": data})` |

## Usage Examples

### **1. List All Flows**

```python
# Direct MCP tool
flows = mcp_lf-cursor_list_flows()
print(f"Found {len(flows)} flows")

# Via Hub Server
result = mcp_mcp_hub_server_execute_langflow_tool("list_flows", {})
```

### **2. Create a New Flow**

```python
# Load flow configuration
with open('flows/living_truth_engine_flow.json', 'r') as f:
    flow_config = json.load(f)

# Create flow via direct MCP
result = mcp_lf-cursor_create_flow(flow_config)
flow_id = result.get('id')
print(f"Flow created with ID: {flow_id}")

# Create flow via hub server
result = mcp_mcp_hub_server_execute_langflow_tool("create_langflow", {
    "flow_config": flow_config
})
```

### **3. Run a Flow**

```python
# Run flow with inputs
inputs = {
    "query": "Investigate Entity A connections",
    "anonymize": False,
    "output_type": "network"
}

result = mcp_lf-cursor_run_flow("90d0cc9d-d590-4734-813e-5664c95f907a", inputs)
print(f"Flow execution result: {result}")
```

### **4. Monitor Flow Status**

```python
# Get flow status
status = mcp_lf-cursor_get_flow_status("90d0cc9d-d590-4734-813e-5664c95f907a")
print(f"Flow status: {status}")
```

## Setup and Configuration

### **1. Prerequisites**

- Langflow running on `http://localhost:7860`
- Cursor IDE with MCP support
- `uvx` package installed for MCP proxy

### **2. Configuration Steps**

1. **Update `.cursor/mcp.json`** with Langflow MCP server configuration
2. **Restart Cursor** to load the new MCP configuration
3. **Verify Connection** by checking Cursor Settings > MCP for green dots
4. **Test Tools** with `mcp_lf-cursor_list_flows()`

### **3. Verification**

```bash
# Check Langflow health
curl -s http://localhost:7860/health | jq .

# Test MCP endpoint (if available)
curl -s http://localhost:7860/api/v1/mcp/project/3bd92a44-057b-4378-a674-80910d570986/sse
```

## Integration with Living Truth Engine

### **Flow Management**

The Living Truth Engine uses the Langflow MCP server for:

1. **Flow Creation**: Import generated flows into Langflow
2. **Flow Execution**: Run investigative research workflows
3. **Flow Monitoring**: Track execution status and results
4. **Flow Updates**: Modify flow configurations as needed

### **Workflow Integration**

```python
# Complete workflow example
def run_investigative_research(query: str):
    """Run investigative research using Living Truth Engine flow."""
    
    # 1. Get or create flow
    flows = mcp_lf-cursor_list_flows()
    flow_id = None
    
    for flow in flows:
        if "Living Truth Engine Flow" in flow.get('name', ''):
            flow_id = flow.get('id')
            break
    
    if not flow_id:
        # Create new flow
        with open('flows/living_truth_engine_flow.json', 'r') as f:
            flow_config = json.load(f)
        result = mcp_lf-cursor_create_flow(flow_config)
        flow_id = result.get('id')
    
    # 2. Run flow
    inputs = {
        "query": query,
        "anonymize": False,
        "output_type": "network"
    }
    
    result = mcp_lf-cursor_run_flow(flow_id, inputs)
    
    # 3. Monitor status
    status = mcp_lf-cursor_get_flow_status(flow_id)
    
    return {
        "flow_id": flow_id,
        "result": result,
        "status": status
    }
```

## Troubleshooting

### **Common Issues**

1. **MCP Server Not Connecting**
   - Check Langflow is running on port 7860
   - Verify MCP endpoint is accessible
   - Restart Cursor after configuration changes

2. **Tools Not Available**
   - Check Cursor Settings > MCP for green dots
   - Verify `.cursor/mcp.json` configuration
   - Test with `mcp_lf-cursor_list_flows()`

3. **Flow Operations Failing**
   - Check flow ID is correct
   - Verify flow configuration is valid
   - Check Langflow logs for errors

### **Debugging Commands**

```bash
# Check Langflow status
curl -s http://localhost:7860/health | jq .

# List flows via API
curl -s http://localhost:7860/api/v1/flows/ | jq .

# Test MCP connection
python3 scripts/setup/test_langflow_mcp.py
```

## Advantages

### **1. Direct Integration**
- Native MCP support in Cursor
- Real-time flow operations
- Seamless development experience

### **2. Automation**
- Programmatic flow management
- Automated testing and deployment
- Integration with CI/CD pipelines

### **3. Monitoring**
- Real-time flow status monitoring
- Execution result tracking
- Error handling and recovery

### **4. Flexibility**
- Multiple access methods (direct MCP, hub server)
- Custom workflow integration
- Extensible tool set

## Future Enhancements

### **1. Enhanced Tool Set**
- Flow template management
- Component library integration
- Advanced monitoring tools

### **2. Workflow Automation**
- Automated flow deployment
- Scheduled execution
- Result processing pipelines

### **3. Integration Improvements**
- Better error handling
- Performance optimization
- Enhanced security

## Conclusion

The Langflow MCP server integration provides a powerful, direct connection to Langflow operations through Cursor's MCP interface. This enables seamless development, testing, and deployment of Living Truth Engine workflows while maintaining the flexibility to use both direct MCP tools and the MCP Hub Server for different use cases. 