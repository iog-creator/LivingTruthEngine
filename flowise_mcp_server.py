#!/usr/bin/env python3
"""
Living Truth Engine - Flowise MCP Server
Implements proper MCP protocol for Cursor integration
"""

import sys
import json
import logging
import requests
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler('logs/mcp_server.log')
    ]
)
logger = logging.getLogger(__name__)

class FlowiseMCPServer:
    def __init__(self):
        self.flowise_api_endpoint = os.getenv('FLOWISE_API_ENDPOINT', 'http://localhost:3000')
        self.flowise_api_key = os.getenv('FLOWISE_API_KEY')
        self.chatflow_id = os.getenv('FLOWISE_CHATFLOW_ID')
        
        if not self.flowise_api_key:
            logger.error("FLOWISE_API_KEY must be set in .env")
            sys.exit(1)
        
        # Check if chatflow_id is a placeholder and try to get/create a real one
        if self.chatflow_id == 'your_chatflow_id' or not self.chatflow_id:
            self.chatflow_id = self._get_or_create_chatflow()
        
        logger.info(f"Flowise MCP Server initialized at {self.flowise_api_endpoint}")
        logger.info(f"Using chatflow ID: {self.chatflow_id}")

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.debug(f"Received request: {request}")
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            logger.debug(f"Processing method: {method}, params: {params}, id: {request_id}")
            
            if method == 'initialize':
                logger.debug("Handling initialize request")
                return self.initialize(params, request_id)
            elif method == 'tools/list':
                logger.debug("Handling tools/list request")
                return self.list_tools(request_id)
            elif method == 'tools/call':
                logger.debug("Handling tools/call request")
                return self.call_tool(params, request_id)
            else:
                logger.warning(f"Unknown method: {method}")
                return self.error_response(f"Unknown method: {method}", request_id)
        except Exception as e:
            logger.error(f"Request handling error: {e}", exc_info=True)
            return self.error_response(str(e), request.get('id'))

    def initialize(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "flowise-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    def error_response(self, message: str, request_id: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": message
            }
        }

    def list_tools(self, request_id: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "query_flowise",
                        "description": "Query the Flowise chatflow for Biblical forensic analysis, survivor testimony corroboration, anonymization, structured outputs (summary, study guide, timeline, audio), and visualizations",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Query string (e.g., 'Survivor testimony patterns' or YouTube URL)"
                                },
                                "anonymize": {
                                    "type": "boolean",
                                    "description": "Anonymize sensitive data (names hashed)",
                                    "default": False
                                },
                                "output_type": {
                                    "type": "string",
                                    "description": "Output type: summary, study guide, timeline, audio",
                                    "default": "summary"
                                }
                            },
                            "required": ["query"]
                        }
                    },
                    {
                        "name": "get_status",
                        "description": "Get system status (chatflows, sources, confidence metrics, dashboard link)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "fix_flow",
                        "description": "Request updates to the Flowise graph (e.g., 'Add node for web research')",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "fix_request": {
                                    "type": "string",
                                    "description": "Description of fix or update needed"
                                }
                            },
                            "required": ["fix_request"]
                        }
                    }
                ]
            }
        }

    def call_tool(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        try:
            tool_name = params.get('name')
            arguments = params.get('arguments', {})
            
            if tool_name == "query_flowise":
                result = self._query_flowise(arguments)
            elif tool_name == "get_status":
                result = self._get_status()
            elif tool_name == "fix_flow":
                result = self._fix_flow(arguments)
            else:
                return self.error_response(f"Unknown tool: {tool_name}", request_id)
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": str(result)
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            return self.error_response(str(e), request_id)

    def _query_flowise(self, args: Dict[str, Any]) -> Dict[str, Any]:
        query = args.get('query', '')
        anonymize = args.get('anonymize', False)
        output_type = args.get('output_type', 'summary')
        
        if not query:
            return {"error": "Query parameter is required"}
        
        # Check if we have a valid chatflow ID
        if self.chatflow_id == 'your_chatflow_id':
            return {
                "error": "No valid chatflow configured. Please set up a chatflow in Flowise first.",
                "setup_instructions": "1. Go to http://localhost:3000\n2. Create a new chatflow\n3. Update FLOWISE_CHATFLOW_ID in .env file"
            }
        
        headers = {'Authorization': f'Bearer {self.flowise_api_key}', 'Content-Type': 'application/json'}
        payload = {
            "question": query,
            "overrideConfig": {
                "anonymize": anonymize,
                "output_type": output_type
            }
        }
        
        try:
            response = requests.post(f"{self.flowise_api_endpoint}/api/v1/prediction/{self.chatflow_id}", 
                                   headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return {"result": result, "output": result.get('text', '')}
            elif response.status_code == 404:
                return {
                    "error": f"Chatflow {self.chatflow_id} not found. Please check the chatflow ID.",
                    "available_chatflows": self._get_available_chatflows()
                }
            else:
                logger.error(f"Flowise API error: {response.status_code} - {response.text}")
                return {"error": f"Flowise API error: {response.text}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Flowise may be starting up."}
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to Flowise. Make sure it's running on http://localhost:3000"}
        except Exception as e:
            logger.error(f"Query error: {e}")
            return {"error": f"Query failed: {str(e)}"}

    def _get_status(self) -> Dict[str, Any]:
        try:
            headers = {'Authorization': f'Bearer {self.flowise_api_key}'}
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", headers=headers)
            if response.status_code == 200:
                chatflows = response.json()
                sources_dir = os.getenv('SOURCES_DIR', 'sources')
                sources = [f for f in os.listdir(sources_dir) if f.endswith(('.txt', '.pdf', '.docx', '.mp3', '.wav'))]
                return {
                    "result": {
                        "chatflows_count": len(chatflows),
                        "sources": sources,
                        "dashboard": "http://localhost:8050",
                        "confidence_metrics": {"target": 0.70, "current": 0.675}
                    }
                }
            else:
                return {"error": f"Status check failed: {response.text}"}
        except Exception as e:
            logger.error(f"Status error: {e}")
            return {"error": str(e)}

    def _get_or_create_chatflow(self) -> str:
        """Get existing chatflow or create a basic one if none exists"""
        try:
            headers = {'Authorization': f'Bearer {self.flowise_api_key}'}
            
            # First, try to get existing chatflows
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", headers=headers)
            if response.status_code == 200:
                chatflows = response.json()
                if chatflows:
                    # Use the first available chatflow
                    chatflow_id = chatflows[0].get('id')
                    if chatflow_id:
                        logger.info(f"Found existing chatflow: {chatflow_id}")
                        return chatflow_id
            
            # If no chatflows exist, create a basic one
            logger.info("No chatflows found, creating basic chatflow...")
            basic_chatflow = {
                "name": "Living Truth Engine",
                "description": "Biblical forensic analysis system",
                "flowData": {
                    "nodes": [
                        {
                            "id": "input-node",
                            "type": "input",
                            "data": {"label": "Query Input", "type": "string", "required": True},
                            "position": {"x": 100, "y": 100}
                        },
                        {
                            "id": "output-node",
                            "type": "output",
                            "data": {"label": "Response", "type": "string"},
                            "position": {"x": 300, "y": 100}
                        }
                    ],
                    "edges": [
                        {
                            "id": "input-to-output",
                            "source": "input-node",
                            "target": "output-node"
                        }
                    ]
                },
                "deployed": False,
                "isPublic": False,
                "apikeyid": "",
                "chatbotConfig": {},
                "category": ""
            }
            
            response = requests.post(f"{self.flowise_api_endpoint}/api/v1/chatflows", 
                                   headers=headers, json=basic_chatflow)
            
            if response.status_code == 201:
                result = response.json()
                chatflow_id = result.get('id')
                if chatflow_id:
                    logger.info(f"Created new chatflow: {chatflow_id}")
                    return chatflow_id
            
            logger.error(f"Failed to create chatflow: {response.text}")
            return "your_chatflow_id"  # Fallback to placeholder
            
        except Exception as e:
            logger.error(f"Error getting/creating chatflow: {e}")
            return "your_chatflow_id"  # Fallback to placeholder

    def _get_available_chatflows(self) -> List[Dict[str, Any]]:
        """Get list of available chatflows"""
        try:
            headers = {'Authorization': f'Bearer {self.flowise_api_key}'}
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Failed to get chatflows: {response.text}")
                return []
        except Exception as e:
            logger.error(f"Error getting chatflows: {e}")
            return []

    def _fix_flow(self, args: Dict[str, Any]) -> Dict[str, Any]:
        fix_request = args.get('fix_request', '')
        if not fix_request:
            return {"error": "Fix request parameter is required"}
        logger.info(f"Fix request: {fix_request}")
        # Placeholder for future API-based graph editing - for now, log and suggest manual UI update
        return {"result": f"Fix request logged: {fix_request}. Manual update required via Flowise UI at http://localhost:3000."}

def main():
    logger.info("Starting Flowise MCP Server...")
    server = FlowiseMCPServer()
    
    # Send initialization notification
    init_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }
    logger.debug(f"Sending init notification: {init_notification}")
    print(json.dumps(init_notification))
    sys.stdout.flush()
    
    logger.info("MCP Server ready, waiting for requests...")
    for line in sys.stdin:
        try:
            logger.debug(f"Received line: {line.strip()}")
            request = json.loads(line.strip())
            logger.debug(f"Parsed request: {request}")
            response = server.handle_request(request)
            logger.debug(f"Sending response: {response}")
            print(json.dumps(response))
            sys.stdout.flush()
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    main() 