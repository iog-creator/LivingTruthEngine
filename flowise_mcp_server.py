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
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(), logging.FileHandler('mcp_server.log')])
logger = logging.getLogger(__name__)

class FlowiseMCPServer:
    def __init__(self):
        self.flowise_api_endpoint = os.getenv('FLOWISE_API_ENDPOINT', 'http://localhost:3000')
        self.flowise_api_key = os.getenv('FLOWISE_API_KEY')
        self.chatflow_id = os.getenv('FLOWISE_CHATFLOW_ID')
        
        if not self.flowise_api_key:
            logger.error("FLOWISE_API_KEY must be set in .env")
            sys.exit(1)
        
        logger.info(f"Flowise MCP Server initialized at {self.flowise_api_endpoint}")

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        try:
            method = request.get('method')
            params = request.get('params', {})
            request_id = request.get('id')
            
            if method == 'initialize':
                return self.initialize(params, request_id)
            elif method == 'tools/list':
                return self.list_tools(request_id)
            elif method == 'tools/call':
                return self.call_tool(params, request_id)
            else:
                return self.error_response(f"Unknown method: {method}", request_id)
        except Exception as e:
            logger.error(f"Request handling error: {e}")
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
        
        headers = {'Authorization': f'Bearer {self.flowise_api_key}', 'Content-Type': 'application/json'}
        payload = {
            "question": query,
            "overrideConfig": {
                "anonymize": anonymize,
                "output_type": output_type
            }
        }
        response = requests.post(f"{self.flowise_api_endpoint}/api/v1/prediction/{self.chatflow_id}", headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return {"result": result, "output": result.get('text', '')}
        else:
            logger.error(f"Flowise API error: {response.status_code} - {response.text}")
            return {"error": f"Flowise API error: {response.text}"}

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

    def _fix_flow(self, args: Dict[str, Any]) -> Dict[str, Any]:
        fix_request = args.get('fix_request', '')
        if not fix_request:
            return {"error": "Fix request parameter is required"}
        logger.info(f"Fix request: {fix_request}")
        # Placeholder for future API-based graph editing - for now, log and suggest manual UI update
        return {"result": f"Fix request logged: {fix_request}. Manual update required via Flowise UI at http://localhost:3000."}

def main():
    server = FlowiseMCPServer()
    
    # Send initialization notification
    init_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }
    print(json.dumps(init_notification))
    sys.stdout.flush()
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = server.handle_request(request)
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

if __name__ == "__main__":
    main() 