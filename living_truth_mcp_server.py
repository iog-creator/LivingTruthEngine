#!/usr/bin/env python3
"""
Living Truth Engine - MCP Server
Implements proper JSON-RPC MCP protocol for Cursor integration
Based on working RippleAGI MCP server template
"""

import sys
import json
import logging
import requests
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Load environment variables from .env file
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(), 
        logging.FileHandler('logs/living_truth_mcp_server.log')
    ]
)
logger = logging.getLogger(__name__)

class LivingTruthMCPServer:
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
        
        logger.info(f"Living Truth MCP Server initialized at {self.flowise_api_endpoint}")
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
        logger.debug("Handling initialize request")
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "living-truth-mcp-server",
                    "version": "1.0.0"
                }
            }
        }

    def list_tools(self, request_id: str) -> Dict[str, Any]:
        logger.debug("Handling tools/list request")
        tools = [
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
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools
            }
        }

    def call_tool(self, params: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        logger.debug(f"Handling tools/call request with params: {params}")
        tool_name = params.get('name')
        arguments = params.get('arguments', {})
        
        try:
            if tool_name == 'query_flowise':
                result = self._query_flowise(arguments)
            elif tool_name == 'get_status':
                result = self._get_status(arguments)
            elif tool_name == 'fix_flow':
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
                            "text": result
                        }
                    ]
                }
            }
        except Exception as e:
            logger.error(f"Tool execution error: {e}", exc_info=True)
            return self.error_response(str(e), request_id)

    def _query_flowise(self, arguments: Dict[str, Any]) -> str:
        query = arguments.get('query', '')
        anonymize = arguments.get('anonymize', False)
        output_type = arguments.get('output_type', 'summary')
        
        logger.info(f"Querying Flowise: {query}, anonymize: {anonymize}, output_type: {output_type}")
        
        # Check if Flowise is running
        try:
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", 
                                  headers={"Authorization": f"Bearer {self.flowise_api_key}"},
                                  timeout=10)
            if response.status_code != 200:
                return f"Error: Flowise API returned status {response.status_code}. Please ensure Flowise is running."
        except Exception as e:
            return f"Error connecting to Flowise: {e}. Please ensure Flowise is running on {self.flowise_api_endpoint}"
        
        # Query the chatflow
        try:
            payload = {
                "question": query,
                "overrideConfig": {
                    "sessionId": f"mcp_{os.getpid()}",
                    "anonymize": anonymize,
                    "outputType": output_type
                }
            }
            
            response = requests.post(
                f"{self.flowise_api_endpoint}/api/v1/prediction/{self.chatflow_id}",
                headers={
                    "Authorization": f"Bearer {self.flowise_api_key}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return f"✅ Flowise Query Result:\n\n{result.get('text', 'No text response')}"
            else:
                return f"Error: Flowise returned status {response.status_code}: {response.text}"
                
        except Exception as e:
            logger.error(f"Flowise query error: {e}", exc_info=True)
            return f"Error querying Flowise: {e}"

    def _get_status(self, arguments: Dict[str, Any]) -> str:
        logger.info("Getting system status")
        
        status_parts = []
        
        # Check Flowise status
        try:
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", 
                                  headers={"Authorization": f"Bearer {self.flowise_api_key}"},
                                  timeout=10)
            if response.status_code == 200:
                chatflows = response.json()
                status_parts.append(f"✅ Flowise: Running with {len(chatflows)} chatflows")
                status_parts.append(f"   Current chatflow ID: {self.chatflow_id}")
            else:
                status_parts.append(f"❌ Flowise: Error {response.status_code}")
        except Exception as e:
            status_parts.append(f"❌ Flowise: Not accessible ({e})")
        
        # Check PostgreSQL
        try:
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv('POSTGRES_HOST', 'localhost'),
                port=os.getenv('POSTGRES_PORT', '5432'),
                database=os.getenv('POSTGRES_DB', 'living_truth_engine'),
                user=os.getenv('POSTGRES_USER', 'postgres'),
                password=os.getenv('POSTGRES_PASSWORD', 'pass')
            )
            conn.close()
            status_parts.append("✅ PostgreSQL: Connected")
        except Exception as e:
            status_parts.append(f"❌ PostgreSQL: Not accessible ({e})")
        
        # Check LM Studio
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=5)
            if response.status_code == 200:
                status_parts.append("✅ LM Studio: Running")
            else:
                status_parts.append(f"❌ LM Studio: Error {response.status_code}")
        except Exception as e:
            status_parts.append(f"❌ LM Studio: Not accessible ({e})")
        
        # Check Dashboard
        try:
            response = requests.get("http://localhost:8050", timeout=5)
            if response.status_code == 200:
                status_parts.append("✅ Dashboard: Running at http://localhost:8050")
            else:
                status_parts.append(f"❌ Dashboard: Error {response.status_code}")
        except Exception as e:
            status_parts.append(f"❌ Dashboard: Not accessible ({e})")
        
        return "\n".join(status_parts)

    def _fix_flow(self, arguments: Dict[str, Any]) -> str:
        fix_request = arguments.get('fix_request', '')
        logger.info(f"Fix flow request: {fix_request}")
        
        # This would typically interact with Flowise API to modify the chatflow
        # For now, return a placeholder response
        return f"✅ Fix request received: {fix_request}\n\nThis functionality will be implemented to modify the Flowise chatflow based on your request."

    def _get_or_create_chatflow(self) -> str:
        """Get existing chatflow or create a new one if needed."""
        try:
            # Try to get existing chatflows
            response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", 
                                  headers={"Authorization": f"Bearer {self.flowise_api_key}"},
                                  timeout=10)
            
            if response.status_code == 200:
                chatflows = response.json()
                if chatflows:
                    # Use the first available chatflow
                    chatflow_id = chatflows[0]['id']
                    logger.info(f"Using existing chatflow: {chatflow_id}")
                    return chatflow_id
            
            # Create a basic chatflow if none exist
            logger.info("No chatflows found, creating basic chatflow")
            basic_chatflow = {
                "name": "Living Truth Engine Basic",
                "description": "Basic chatflow for Living Truth Engine",
                "nodes": [
                    {
                        "id": "start",
                        "type": "start",
                        "position": {"x": 100, "y": 100},
                        "data": {"label": "Start"}
                    },
                    {
                        "id": "llm",
                        "type": "llmChain",
                        "position": {"x": 300, "y": 100},
                        "data": {
                            "label": "LLM Chain",
                            "model": "qwen3-8b",
                            "temperature": 0.7
                        }
                    },
                    {
                        "id": "end",
                        "type": "end",
                        "position": {"x": 500, "y": 100},
                        "data": {"label": "End"}
                    }
                ],
                "edges": [
                    {"source": "start", "target": "llm"},
                    {"source": "llm", "target": "end"}
                ]
            }
            
            response = requests.post(
                f"{self.flowise_api_endpoint}/api/v1/chatflows",
                headers={
                    "Authorization": f"Bearer {self.flowise_api_key}",
                    "Content-Type": "application/json"
                },
                json=basic_chatflow,
                timeout=30
            )
            
            if response.status_code == 201:
                chatflow_id = response.json()['id']
                logger.info(f"Created new chatflow: {chatflow_id}")
                return chatflow_id
            else:
                logger.error(f"Failed to create chatflow: {response.status_code} - {response.text}")
                return "your_chatflow_id"  # Fallback
                
        except Exception as e:
            logger.error(f"Error getting/creating chatflow: {e}")
            return "your_chatflow_id"  # Fallback

    def error_response(self, message: str, request_id: str) -> Dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": message
            }
        }

def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Living Truth MCP Server...")
    
    server = LivingTruthMCPServer()
    
    # Send initialization notification
    init_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    }
    print(json.dumps(init_notification))
    
    logger.info("MCP Server ready, waiting for requests...")
    
    # Main loop - read from stdin, write to stdout
    for line in sys.stdin:
        try:
            line = line.strip()
            if not line:
                continue
                
            logger.debug(f"Received line: {line}")
            request = json.loads(line)
            logger.debug(f"Parsed request: {request}")
            
            response = server.handle_request(request)
            logger.debug(f"Sending response: {response}")
            print(json.dumps(response))
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {e}"
                }
            }
            print(json.dumps(error_response))
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {e}"
                }
            }
            print(json.dumps(error_response))

if __name__ == "__main__":
    main() 