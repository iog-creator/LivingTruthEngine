# Langflow MCP Tools Documentation

## Overview

The Langflow MCP Server provides programmatic access to Langflow workflows for AI-assisted development in the Living Truth Engine project. This server enables creating, updating, and querying Langflow workflows through the MCP (Model Context Protocol) interface.

## Available Tools

### 1. `query_langflow`

**Purpose**: Query Langflow workflows for survivor testimony analysis using multi-agent system.

**Parameters**:
- `query` (str): The query string or analysis request
- `anonymize` (bool, optional): Whether to anonymize the data (default: False)
- `output_type` (str, optional): Type of output - "summary", "study_guide", "timeline", "audio" (default: "summary")

**Returns**: Analysis results as formatted string

**Example**:
```python
result = mcp_langflow_mcp_server_query_langflow(
    query="Analyze this transcript for corroborating evidence",
    output_type="summary",
    anonymize=False
)
```

### 2. `create_langflow`

**Purpose**: Create or update a Langflow workflow programmatically via API.

**Parameters**:
- `flow_config` (Dict[str, Any]): Dictionary with workflow configuration
  - **Required**: `name` (str), `data` (dict with nodes and edges)
  - **Optional**: `description` (str), etc.
- `flow_id` (str, optional): ID of existing flow to update (uses PATCH if provided)

**Returns**: Dict with the created/updated flow details

**Example**:
```python
flow_config = {
    "name": "Survivor Testimony Analysis",
    "data": {
        "nodes": [
            {"id": "input", "type": "input", "data": {"label": "Transcript Input"}},
            {"id": "analysis", "type": "llm", "data": {"label": "Analysis Node"}}
        ],
        "edges": [
            {"source": "input", "target": "analysis"}
        ]
    },
    "description": "Workflow for analyzing survivor testimony"
}

result = mcp_langflow_mcp_server_create_langflow(flow_config)
```

### 3. `get_langflow_status`

**Purpose**: Get Langflow system status and connection information.

**Parameters**: None

**Returns**: JSON string with status information including:
- Langflow API endpoint status
- API key configuration status
- Project endpoint status
- Connection timestamps

**Example**:
```python
status = mcp_langflow_mcp_server_get_langflow_status()
```

### 4. `list_langflow_tools`

**Purpose**: List available tools in Langflow.

**Parameters**: None

**Returns**: JSON string with available Langflow tools

**Example**:
```python
tools = mcp_langflow_mcp_server_list_langflow_tools()
```

### 5. `get_current_time`

**Purpose**: Get the current time as a test tool.

**Parameters**: None

**Returns**: Current timestamp string

**Example**:
```python
time = mcp_langflow_mcp_server_get_current_time()
```

### 6. `test_tool`

**Purpose**: A simple test tool for Cursor detection.

**Parameters**:
- `message` (str): Test message

**Returns**: Test response string

**Example**:
```python
response = mcp_langflow_mcp_server_test_tool("Hello World")
```

## Configuration

### Environment Variables

The Langflow MCP Server requires the following environment variables:

```bash
LANGFLOW_API_ENDPOINT=http://localhost:7860
LANGFLOW_API_KEY=your_api_key_here
LANGFLOW_PROJECT_ID=399a0977-d08a-4d61-ba52-fd9811676762
```

### API Authentication

The server uses the `x-api-key` header for authentication with the Langflow API. Ensure your `LANGFLOW_API_KEY` is properly configured in your `.env` file.

## Error Handling

The Langflow MCP Server implements comprehensive error handling:

### `create_langflow` Error Types

1. **ValueError**: Invalid flow configuration
   - Missing required fields (`name`, `data`)
   - Invalid configuration type
   - Empty configuration

2. **ConnectionError**: API connectivity issues
   - Langflow API unavailable
   - Network connection failures

3. **HTTPException**: HTTP-related errors
   - Invalid API responses
   - Authentication failures
   - Server errors

### Error Response Format

All errors include detailed logging and appropriate exception types for proper error handling in client applications.

## Usage Examples

### Creating a New Workflow

```python
# Create a simple workflow for transcript analysis
flow_config = {
    "name": "Transcript Analysis Workflow",
    "data": {
        "nodes": [
            {
                "id": "input_node",
                "type": "input",
                "data": {"label": "Transcript Input"}
            },
            {
                "id": "analysis_node", 
                "type": "llm",
                "data": {"label": "AI Analysis"}
            },
            {
                "id": "output_node",
                "type": "output", 
                "data": {"label": "Analysis Results"}
            }
        ],
        "edges": [
            {"source": "input_node", "target": "analysis_node"},
            {"source": "analysis_node", "target": "output_node"}
        ]
    },
    "description": "Workflow for analyzing survivor testimony transcripts"
}

# Create the workflow
result = mcp_langflow_mcp_server_create_langflow(flow_config)
print(f"Created workflow with ID: {result['id']}")
```

### Updating an Existing Workflow

```python
# Update an existing workflow
flow_id = "existing-flow-id"
updated_config = {
    "name": "Updated Transcript Analysis",
    "data": {
        "nodes": [
            # Updated node configuration
        ],
        "edges": [
            # Updated edge configuration
        ]
    }
}

# Update the workflow
result = mcp_langflow_mcp_server_create_langflow(updated_config, flow_id)
print(f"Updated workflow: {result['name']}")
```

### Querying a Workflow

```python
# Query the workflow for analysis
query_result = mcp_langflow_mcp_server_query_langflow(
    query="Analyze this transcript for patterns of corroborating evidence",
    output_type="summary",
    anonymize=True
)
print(query_result)
```

## Testing

### Unit Tests

Run the unit tests for the Langflow MCP Server:

```bash
python -m pytest tests/test_langflow_mcp_server.py -v
```

### Integration Tests

Test the MCP server functionality:

```bash
# Test the create_langflow tool
echo '{"method": "tools.execute", "params": ["create_langflow", {"flow_config": {"name": "Test", "data": {"nodes": [], "edges": []}} }]}' | python src/mcp_servers/langflow_mcp_server.py
```

## Best Practices

1. **Always validate flow configurations** before creating workflows
2. **Use proper error handling** when calling MCP tools
3. **Check system status** before performing operations
4. **Test workflows** in development before production use
5. **Monitor API responses** for proper error handling
6. **Use descriptive workflow names** and descriptions
7. **Implement proper logging** for debugging and monitoring

## Troubleshooting

### Common Issues

1. **API Key Not Configured**
   - Ensure `LANGFLOW_API_KEY` is set in your `.env` file
   - Verify the API key has proper permissions

2. **Connection Errors**
   - Check if Langflow service is running on port 7860
   - Verify network connectivity
   - Check firewall settings

3. **Invalid Flow Configuration**
   - Ensure required fields (`name`, `data`) are present
   - Validate JSON structure of flow configuration
   - Check node and edge definitions

4. **HTTP Errors**
   - Check API endpoint URL
   - Verify authentication headers
   - Review server logs for detailed error information

### Debugging

Enable debug logging by setting the log level to DEBUG in the MCP server configuration. Check the logs in `data/outputs/logs/langflow_mcp.log` for detailed information about API calls and responses.

## Related Documentation

- [Living Truth Engine README](../README.md)
- [MCP Server Integration Guide](../.cursor/rules/mcp_server_integration.mdc)
- [Langflow API Documentation](https://docs.langflow.org/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp) 