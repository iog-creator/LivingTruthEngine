@project_overview.mdc
@development_workflow.mdc
@docker_best_practices.mdc
@system_management.mdc
@mcp_server_integration.mdc
@coding_standards.mdc
@mcp_server_guide_troubshooting.mdc
@how_to_make_a_cursor_rule.mdc

Implement the refined `create_langflow` tool in `src/mcp_servers/langflow_mcp_server.py` to enable programmatic creation and updating of Langflow workflows via the verified API. This addresses the gap in flow-building capabilities for the langflow_mcp_server, making it more robust for AI-assisted development in the Living Truth Engine project.

Key requirements based on verified Langflow API specs:
- Use POST to `/api/v1/flows/` for creating new flows.
- Use PATCH to `/api/v1/flows/{flow_id}` for updating existing flows.
- Authentication via `x-api-key` header from `LANGFLOW_API_KEY` in `.env`.
- Required fields in flow_config: "name" (string) and "data" (dict with nodes and edges).
- Optional fields: "description", etc.
- Return the full JSON response from the API (e.g., {"id": "...", "name": "...", "data": {...}}).
- Handle errors: ValueError for invalid config, ConnectionError for API unavailability, HTTPException for HTTP errors (include response.text in detail).
- Use structured logging with logger.getLogger(__name__).
- Add type hints, comprehensive docstring with Args/Returns/Raises.
- Decorate as @tool() for MCP integration.
- Ensure tool name uses underscores and is under 60 characters.

Exact code to implement in the LangflowMCPServer class:

```python
import logging
import requests
from typing import Dict, Any, Optional
from fastapi import HTTPException
from mcp import tool  # FastMCP import per project standards

logger = logging.getLogger(__name__)

# ... (existing class code)

def create_langflow(self, flow_config: Dict[str, Any], flow_id: Optional[str] = None) -> Dict[str, Any]:
    """Create or update a Langflow workflow via API.

    Args:
        flow_config: Dictionary with workflow configuration (required: 'name', 'data'; optional: 'description', etc.).
        flow_id: Optional ID of existing flow to update (uses PATCH if provided).

    Returns:
        Dict with the created/updated flow details.

    Raises:
        ValueError: If flow_config is invalid or missing required fields.
        ConnectionError: If Langflow API is unavailable.
        HTTPException: For HTTP-related errors with appropriate status codes.
    """
    if not flow_config or not isinstance(flow_config, dict):
        self.logger.error("Invalid flow configuration: %s", flow_config)
        raise ValueError("Flow configuration must be a non-empty dictionary")

    required_fields = ["name", "data"]  # Verified: 'name' and 'data' (nodes/edges) required
    if not all(key in flow_config for key in required_fields):
        self.logger.error("Missing required fields in flow_config: %s", required_fields)
        raise ValueError(f"Flow configuration must include: {required_fields}")

    try:
        headers = {
            "x-api-key": self.langflow_api_key,
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        url = f"{self.langflow_api_endpoint}/api/v1/flows"
        if flow_id:
            url += f"/{flow_id}"
            method = "PATCH"  # Verified update method
        else:
            method = "POST"  # Verified create method

        self.logger.debug("Sending %s request to %s with config: %s", method, url, flow_config)
        response = requests.request(method, url, json=flow_config, headers=headers, timeout=10)
        response.raise_for_status()

        result = response.json()
        self.logger.info("Workflow %s: %s", "updated" if flow_id else "created", result.get("id", "unknown"))
        return result  # Returns full flow object, e.g., {"id": "...", "name": "...", "data": {...}}

    except requests.exceptions.ConnectionError as e:
        self.logger.error("Failed to connect to Langflow API: %s", e)
        raise ConnectionError("Langflow API unavailable")
    except requests.exceptions.HTTPError as e:
        self.logger.error("HTTP error from Langflow API: %s - Response: %s", e, response.text if 'response' in locals() else "N/A")
        raise HTTPException(status_code=response.status_code, detail=response.text if 'response' in locals() else str(e))
    except Exception as e:
        self.logger.error("Unexpected error creating/updating workflow: %s", e)
        raise ConnectionError(f"Error processing workflow: {e}")

@tool()
def create_langflow(self, flow_config: Dict[str, Any], flow_id: Optional[str] = None) -> Dict[str, Any]:
    """Create or update a Langflow workflow (MCP tool)."""
    return self.create_langflow(flow_config, flow_id)
```

After implementation:
- Update `.cursor/mcp.json` if needed to ensure the server uses the correct env vars.
- Add to `requirements.txt` if missing: requests, fastapi.
- Create unit tests in `tests/test_langflow_mcp_server.py` for valid/invalid configs and update case.
- Run integration test: echo '{"method": "tools.execute", "params": ["create_langflow", {"flow_config": {"name": "Test", "data": {"nodes": [], "edges": []}} }]}' | python src/mcp_servers/langflow_mcp_server.py
- Update README.md MCP tools section and docs/LANGFLOW_MCP_TOOLS.md with the new tool details.
- Validate with mcp_living_truth_fastmcp_server_get_status() and ensure green dot in Cursor.
- Follow all referenced rules for coding standards, MCP integration, and Docker best practices. If issues, check logs in data/logs/ and restart Langflow service.