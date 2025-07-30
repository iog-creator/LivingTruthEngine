# Living Truth Engine - MCP Server Documentation

## Overview

The Flowise MCP Server provides integration between Cursor IDE and the Living Truth Engine's Flowise-based AI system for Biblical forensic analysis and survivor testimony corroboration.

## Available Tools

### 1. `query_flowise`
**Description**: Query the Flowise chatflow for Biblical forensic analysis, survivor testimony corroboration, anonymization, structured outputs (summary, study guide, timeline, audio), and visualizations

**Parameters**:
- `query` (string, required): Query string (e.g., 'Survivor testimony patterns' or YouTube URL)
- `anonymize` (boolean, default: false): Anonymize sensitive data (names hashed)
- `output_type` (string, default: "summary"): Output type: summary, study guide, timeline, audio

**Example Usage**:
```json
{
  "method": "tools.execute",
  "params": [
    "query_flowise",
    {
      "query": "Biblical abuse patterns",
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
**Description**: Request updates to the Flowise graph (e.g., 'Add node for web research')

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
- `FLOWISE_API_ENDPOINT`: Flowise API endpoint (default: http://localhost:3000)
- `FLOWISE_API_KEY`: Flowise API key
- `FLOWISE_CHATFLOW_ID`: Flowise chatflow ID

### Virtual Environment
- **Environment**: `living_venv`
- **Activation**: `source living_venv/bin/activate`
- **Python Path**: `${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/living_venv/bin/python`

## Integration with Cursor

### Global MCP Configuration
Located at `~/.cursor/mcp.json`:
```json
{
  "flowise-mcp-server": {
    "command": "${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/living_venv/bin/python",
    "args": ["${PROJECT_ROOT}/NotebookLM/LivingTruthEngine/flowise_mcp_server.py"],
    "env": {
      "FLOWISE_API_ENDPOINT": "http://localhost:3000",
      "FLOWISE_API_KEY": "your_flowise_api_key",
      "FLOWISE_CHATFLOW_ID": "your_chatflow_id",
      "PYTHONPATH": "${PROJECT_ROOT}/NotebookLM/LivingTruthEngine"
    }
  }
}
```

### Usage in Cursor
1. Restart Cursor to load the MCP server
2. Use the tools through Cursor's AI interface
3. Example: "Use query_flowise to analyze 'Biblical abuse patterns' with anonymize=true and output_type=study guide"

## Troubleshooting

### Common Issues
1. **Environment not activated**: Ensure `living_venv` is activated
2. **Missing environment variables**: Check `.env` file configuration
3. **Flowise not running**: Start Flowise with `flowise start`
4. **Permission errors**: Check file permissions and Python path

### Logs
- MCP server logs: `mcp_server.log`
- Flowise logs: Check Flowise UI at http://localhost:3000

## Development

### Adding New Tools
1. Add tool definition to `list_tools()` method
2. Implement tool execution in `execute_tool()` method
3. Add corresponding private method (e.g., `_new_tool()`)
4. Update documentation

### Testing
```bash
# Test tool listing
echo '{"method": "tools.list", "params": []}' | python flowise_mcp_server.py

# Test tool execution
echo '{"method": "tools.execute", "params": ["get_status"]}' | python flowise_mcp_server.py
```

## Security Considerations

- API keys are stored in environment variables
- Sensitive data can be anonymized using the `anonymize` parameter
- All operations are logged for audit purposes
- Database connections use environment-driven configuration

## Performance

- MCP server runs in the same process as Cursor
- Tool execution is synchronous
- Large queries may take time depending on Flowise graph complexity
- Dashboard visualizations are generated asynchronously 