# Living Truth Engine - MCP Server Documentation

## Overview

The Langflow MCP Server provides integration between Cursor IDE and the Living Truth Engine's Langflow-based AI system for survivor testimony analysis and evidence corroboration.

## Available Tools

### 1. `query_Langflow`
**Description**: Query the Langflow chatflow for survivor testimony analysis, evidence corroboration, anonymization, structured outputs (summary, study guide, timeline, audio), and visualizations

**Parameters**:
- `query` (string, required): Query string (e.g., 'Survivor testimony patterns' or YouTube URL)
- `anonymize` (boolean, default: false): Anonymize sensitive data (names hashed)
- `output_type` (string, default: "summary"): Output type: summary, study guide, timeline, audio

**Example Usage**:
```json
{
  "method": "tools.execute",
  "params": [
    "query_Langflow",
    {
      "query": "survivor testimony patterns",
      "anonymize": true,
      "output_type": "study_guide"
    }
  ]
}
```

### 2. `get_status`
**Description**: Get system status (chatflows, sources, confidence metrics, dashboard link)

**Parameters**: None

**Example Usage**:
```json
{
  "method": "tools.execute",
  "params": ["get_status"]
}
```

### 3. `fix_flow`
**Description**: Request updates to the Langflow graph (e.g., 'Add node for web research')

**Parameters**:
- `fix_request` (string, required): Description of fix or update needed

**Example Usage**:
```json
{
  "method": "tools.execute",
  "params": [
    "fix_flow",
    {
      "fix_request": "Add node for web research capabilities"
    }
  ]
}
```

## Configuration

### Environment Variables
The MCP server requires these environment variables (set in `.env`):
- `Langflow_API_ENDPOINT`: Langflow API endpoint (default: http://localhost:7860)
- `Langflow_API_KEY`: Langflow API key
- `Langflow_CHATFLOW_ID`: Langflow chatflow ID

### Virtual Environment
- **Environment**: `living_venv`
- **Activation**: `source living_venv/bin/activate`
- **Python Path**: `${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/living_venv/bin/python`

## Integration with Cursor

### Global MCP Configuration
Located at `~/.cursor/mcp.json`:
```json
{
  "Langflow-mcp-server": {
    "command": "${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/living_venv/bin/python",
    "args": ["${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/Langflow_mcp_server.py"],
    "env": {
      "Langflow_API_ENDPOINT": "http://localhost:7860",
      "Langflow_API_KEY": "your_Langflow_api_key",
      "Langflow_CHATFLOW_ID": "your_chatflow_id",
      "PYTHONPATH": "${PROJECT_ROOT}/NotebookLM/LivingTruthEngine"
    }
  }
}
```

### Usage in Cursor
1. Restart Cursor to load the MCP server
2. Use the tools through Cursor's AI interface
3. Example: "Use query_Langflow to analyze 'survivor testimony patterns' with anonymize=true and output_type=study guide"

## Troubleshooting

### Common Issues
1. **Environment not activated**: Ensure `living_venv` is activated
2. **Missing environment variables**: Check `.env` file configuration
3. **Langflow not running**: Start Langflow with `Langflow start`
4. **Permission errors**: Check file permissions and Python path

### Logs
- MCP server logs: `mcp_server.log`
- Langflow logs: Check Langflow UI at http://localhost:7860

## Development

### Adding New Tools
1. Add tool definition to `list_tools()` method
2. Implement tool execution in `execute_tool()` method
3. Add corresponding private method (e.g., `_new_tool()`)
4. Update documentation

### Testing
```bash
# Test tool listing
echo '{"method": "tools.list", "params": []}' | python Langflow_mcp_server.py

# Test tool execution
echo '{"method": "tools.execute", "params": ["get_status"]}' | python Langflow_mcp_server.py
```

## Security Considerations

- API keys are stored in environment variables
- Sensitive data can be anonymized using the `anonymize` parameter
- All operations are logged for audit purposes
- Database connections use environment-driven configuration

## Performance

- MCP server runs in the same process as Cursor
- Tool execution is synchronous
- Large queries may take time depending on Langflow graph complexity
- Dashboard visualizations are generated asynchronously 