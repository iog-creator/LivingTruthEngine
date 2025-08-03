#!/usr/bin/env python3
"""
Langflow MCP Server
Provides MCP tools for Langflow integration using the same pattern as working servers
"""

import os
import sys
import json
import logging
import requests
import time
import uuid
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from fastapi import HTTPException

# Load environment variables from project root
import pathlib
project_root = pathlib.Path(__file__).parent.parent.parent
load_dotenv(project_root / '.env')

# Ensure logs directory exists in project root
logs_dir = project_root / 'data' / 'outputs' / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(logs_dir / 'langflow_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP()

class LangflowMCP:
    def __init__(self):
        self.langflow_api_endpoint = os.getenv('LANGFLOW_API_ENDPOINT', 'http://localhost:7860')
        self.langflow_api_key = os.getenv('LANGFLOW_API_KEY')
        self.project_id = os.getenv('LANGFLOW_PROJECT_ID', '399a0977-d08a-4d61-ba52-fd9811676762')
        
        logger.info(f"Langflow MCP Server initialized")
        logger.info(f"Langflow endpoint: {self.langflow_api_endpoint}")
        logger.info(f"Project ID: {self.project_id}")

    def query_langflow(self, query: str, anonymize: bool = False, output_type: str = "summary") -> str:
        """Query the Langflow workflow for survivor testimony analysis."""
        try:
            if not self.langflow_api_key:
                return "❌ LANGFLOW_API_KEY not configured"
            
            # Prepare headers with API key
            headers = {
                "Authorization": f"Bearer {self.langflow_api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare the query payload
            payload = {
                "question": query,
                "overrideConfig": {
                    "sessionId": f"mcp_query_{int(time.time())}",
                    "returnSourceDocuments": True
                }
            }
            
            if anonymize:
                payload["overrideConfig"]["anonymize"] = True
            
            if output_type != "summary":
                payload["overrideConfig"]["outputType"] = output_type
            
            # Make the request to Langflow
            url = f"{self.langflow_api_endpoint}/api/v1/mcp/project/{self.project_id}/"
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return f"✅ Langflow query successful:\n\n{result.get('text', 'No response text')}"
            else:
                return f"❌ Langflow query failed: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"Langflow query error: {e}")
            return f"❌ Langflow query error: {str(e)}"

    def get_langflow_status(self) -> str:
        """Get Langflow system status and available tools."""
        try:
            headers = {}
            if self.langflow_api_key:
                headers["Authorization"] = f"Bearer {self.langflow_api_key}"
            
            # Check main MCP endpoint
            main_url = f"{self.langflow_api_endpoint}/api/v1/mcp/sse"
            main_response = requests.get(main_url, headers=headers, timeout=10)
            
            # Check project-specific endpoint
            project_url = f"{self.langflow_api_endpoint}/api/v1/mcp/project/{self.project_id}/sse"
            project_response = requests.get(project_url, headers=headers, timeout=10)
            
            status_info = {
                "langflow_api_endpoint": self.langflow_api_endpoint,
                "langflow_api_key": "✅ Configured" if self.langflow_api_key else "❌ Not configured",
                "project_id": self.project_id,
                "main_endpoint_status": "✅ Connected" if main_response.status_code == 200 else f"❌ Failed ({main_response.status_code})",
                "project_endpoint_status": "✅ Connected" if project_response.status_code == 200 else f"❌ Failed ({project_response.status_code})",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return json.dumps(status_info, indent=2)
            
        except Exception as e:
            logger.error(f"Status check error: {e}")
            return f"❌ Status check error: {str(e)}"

    def list_langflow_tools(self) -> str:
        """List available tools in Langflow."""
        try:
            headers = {}
            if self.langflow_api_key:
                headers["Authorization"] = f"Bearer {self.langflow_api_key}"
            
            # Get tools from project
            url = f"{self.langflow_api_endpoint}/api/v1/mcp/project/{self.project_id}/tools"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                tools = response.json()
                return f"✅ Available Langflow tools:\n\n{json.dumps(tools, indent=2)}"
            else:
                return f"❌ Failed to get tools: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"List tools error: {e}")
            return f"❌ List tools error: {str(e)}"

    def get_current_time(self) -> str:
        """Get current time as test tool."""
        return f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}"

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
            logger.error("Invalid flow configuration: %s", flow_config)
            raise ValueError("Flow configuration must be a non-empty dictionary")

        required_fields = ["name", "data"]  # Verified: 'name' and 'data' (nodes/edges) required
        if not all(key in flow_config for key in required_fields):
            logger.error("Missing required fields in flow_config: %s", required_fields)
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
                url += "/"  # Add trailing slash for POST requests
                method = "POST"  # Verified create method

            logger.debug("Sending %s request to %s with config: %s", method, url, flow_config)
            response = requests.request(method, url, json=flow_config, headers=headers, timeout=10)
            response.raise_for_status()

            result = response.json()
            logger.info("Workflow %s: %s", "updated" if flow_id else "created", result.get("id", "unknown"))
            return result  # Returns full flow object, e.g., {"id": "...", "name": "...", "data": {...}}

        except requests.exceptions.ConnectionError as e:
            logger.error("Failed to connect to Langflow API: %s", e)
            raise ConnectionError("Langflow API unavailable")
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error from Langflow API: %s - Response: %s", e, response.text if 'response' in locals() else "N/A")
            raise HTTPException(status_code=response.status_code, detail=response.text if 'response' in locals() else str(e))
        except Exception as e:
            logger.error("Unexpected error creating/updating workflow: %s", e)
            raise ConnectionError(f"Error processing workflow: {e}")

    def export_flow_to_file(self, flow_id: str, file_path: str = "data/flows/exported_flow.json") -> str:
        """Export flow to JSON file for editing."""
        try:
            headers = {
                "x-api-key": self.langflow_api_key,
                "Content-Type": "application/json",
                "accept": "application/json"
            }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            response = requests.get(f"{self.langflow_api_endpoint}/api/v1/flows/{flow_id}", headers=headers, timeout=10)
            response.raise_for_status()
            flow_json = response.json()
            
            with open(file_path, 'w') as f:
                json.dump(flow_json, f, indent=4)
            
            logger.info(f"Exported flow {flow_id} to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Export flow error: {e}")
            raise ConnectionError(f"Failed to export flow: {e}")

    def load_flow_from_file(self, file_path: str) -> Dict[str, Any]:
        """Load flow JSON from file for configuration."""
        try:
            with open(file_path, 'r') as f:
                flow_json = json.load(f)
            logger.info(f"Loaded flow from {file_path}")
            return flow_json
        except Exception as e:
            logger.error(f"Load flow error: {e}")
            raise ValueError(f"Failed to load flow from {file_path}: {e}")

    def configure_node_in_flow(self, flow_json: Dict[str, Any], node_id: str, config_params: Dict[str, Any]) -> Dict[str, Any]:
        """Configure node in loaded flow JSON."""
        try:
            for node in flow_json['data']['nodes']:
                if node['id'] == node_id:
                    for key, value in config_params.items():
                        if key in node['data']['node']['template']:
                            param = node['data']['node']['template'][key]
                            if param.get('required', False) and not value:
                                raise ValueError(f"Required param {key} cannot be empty")
                            param['value'] = value
                    logger.info(f"Configured node {node_id} with params: {config_params}")
                    break
            else:
                raise ValueError(f"Node {node_id} not found in flow")
            
            return flow_json
        except Exception as e:
            logger.error(f"Configure node error: {e}")
            raise ValueError(f"Failed to configure node: {e}")

    def add_node_to_flow(self, flow_json: Dict[str, Any], template_type: str, config_params: Dict[str, Any], position: Dict[str, float]) -> Dict[str, Any]:
        """Add new node to flow JSON using schema template."""
        try:
            # Get template from hard-coded examples or load from file
            template = self.get_component_template(template_type)
            if not template:
                raise ValueError(f"Template type {template_type} not found")
            
            node = template.copy()
            node['id'] = str(uuid.uuid4())
            node['position'] = position
            
            # Configure the node with provided parameters
            for key, value in config_params.items():
                if key in node['data']['node']['template']:
                    node['data']['node']['template'][key]['value'] = value
            
            flow_json['data']['nodes'].append(node)
            logger.info(f"Added {template_type} node to flow")
            return flow_json
            
        except Exception as e:
            logger.error(f"Add node error: {e}")
            raise ValueError(f"Failed to add node: {e}")

    def get_component_template(self, template_type: str) -> Optional[Dict[str, Any]]:
        """Get component template by type."""
        # Hard-coded templates based on Langflow node types
        templates = {
            "TextNode": {
                "id": "placeholder",
                "type": "TextNode",
                "position": {"x": 0, "y": 0},
                "data": {
                    "node": {
                        "template": {
                            "text": {
                                "type": "str",
                                "value": "",
                                "required": True,
                                "show": True,
                                "multiline": True
                            }
                        },
                        "description": "Text input/output node",
                        "base_classes": ["TextNode"],
                        "display_name": "Text",
                        "documentation": "Simple text input/output"
                    }
                }
            },
            "ChatInput": {
                "id": "placeholder",
                "type": "ChatInput",
                "position": {"x": 0, "y": 0},
                "data": {
                    "node": {
                        "template": {
                            "message": {
                                "type": "str",
                                "value": "",
                                "required": True,
                                "show": True,
                                "multiline": True
                            }
                        },
                        "description": "Chat input node",
                        "base_classes": ["ChatInput"],
                        "display_name": "Chat Input",
                        "documentation": "Chat input component"
                    }
                }
            },
            "ChatOutput": {
                "id": "placeholder",
                "type": "ChatOutput",
                "position": {"x": 0, "y": 0},
                "data": {
                    "node": {
                        "template": {
                            "message": {
                                "type": "str",
                                "value": "",
                                "required": True,
                                "show": True,
                                "multiline": True
                            }
                        },
                        "description": "Chat output node",
                        "base_classes": ["ChatOutput"],
                        "display_name": "Chat Output",
                        "documentation": "Chat output component"
                    }
                }
            }
        }
        
        return templates.get(template_type)

    def import_flow_from_json(self, flow_json: Dict[str, Any], flow_id: Optional[str] = None) -> Dict[str, Any]:
        """Import JSON to Langflow via API (create/update)."""
        return self.create_langflow(flow_json, flow_id)

    def save_flow_to_file(self, flow_json: Dict[str, Any], file_path: str = "data/flows/updated_flow.json") -> str:
        """Save modified flow to file for track/verification."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(flow_json, f, indent=4)
            
            logger.info(f"Saved flow to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Save flow error: {e}")
            raise ValueError(f"Failed to save flow to {file_path}: {e}")

# Create Langflow instance
langflow = LangflowMCP()

# Define MCP tools
@mcp.tool()
def query_langflow(query: str, anonymize: bool = False, output_type: str = "summary") -> str:
    """Query the Langflow workflow for survivor testimony analysis using multi-agent system."""
    return langflow.query_langflow(query, anonymize, output_type)

@mcp.tool()
def get_langflow_status() -> str:
    """Get Langflow system status and connection information."""
    return langflow.get_langflow_status()

@mcp.tool()
def list_langflow_tools() -> str:
    """List available tools in Langflow."""
    return langflow.list_langflow_tools()

@mcp.tool()
def get_current_time() -> str:
    """Get the current time as a test tool."""
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time: {current_time}"

@mcp.tool()
def test_tool(message: str) -> str:
    """A simple test tool for Cursor detection."""
    return f"Langflow MCP test tool response: {message}"

@mcp.tool()
def create_langflow(flow_config: Dict[str, Any], flow_id: Optional[str] = None) -> Dict[str, Any]:
    """Create or update a Langflow workflow (MCP tool)."""
    return langflow.create_langflow(flow_config, flow_id)

@mcp.tool()
def export_flow_to_file(flow_id: str, file_path: str = "data/flows/exported_flow.json") -> str:
    """Export flow to JSON file for editing."""
    return langflow.export_flow_to_file(flow_id, file_path)

@mcp.tool()
def load_flow_from_file(file_path: str) -> Dict[str, Any]:
    """Load flow JSON from file for configuration."""
    return langflow.load_flow_from_file(file_path)

@mcp.tool()
def configure_node_in_flow(flow_json: Dict[str, Any], node_id: str, config_params: Dict[str, Any]) -> Dict[str, Any]:
    """Configure node in loaded flow JSON."""
    return langflow.configure_node_in_flow(flow_json, node_id, config_params)

@mcp.tool()
def add_node_to_flow(flow_json: Dict[str, Any], template_type: str, config_params: Dict[str, Any], position: Dict[str, float]) -> Dict[str, Any]:
    """Add new node to flow JSON using schema template."""
    return langflow.add_node_to_flow(flow_json, template_type, config_params, position)

@mcp.tool()
def import_flow_from_json(flow_json: Dict[str, Any], flow_id: Optional[str] = None) -> Dict[str, Any]:
    """Import JSON to Langflow via API (create/update)."""
    return langflow.import_flow_from_json(flow_json, flow_id)

@mcp.tool()
def save_flow_to_file(flow_json: Dict[str, Any], file_path: str = "data/flows/updated_flow.json") -> str:
    """Save modified flow to file for track/verification."""
    return langflow.save_flow_to_file(flow_json, file_path)

if __name__ == "__main__":
    logger.info("Langflow MCP Server starting...")
    mcp.run() 