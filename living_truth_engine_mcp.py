#!/usr/bin/env python3
"""
Living Truth Engine MCP Server
Simple, working MCP server following the same pattern as other working servers
"""

import sys
import json
import logging
import requests
import os
import time
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/living_truth_mcp.log')
    ]
)
logger = logging.getLogger(__name__)

class LivingTruthEngineMCP:
    def __init__(self):
        self.flowise_api_endpoint = os.getenv('FLOWISE_API_ENDPOINT', 'http://localhost:3000')
        self.flowise_api_key = os.getenv('FLOWISE_API_KEY')
        self.chatflow_id = os.getenv('FLOWISE_CHATFLOW_ID')
        
        logger.info(f"Living Truth Engine MCP initialized")
        logger.info(f"Flowise endpoint: {self.flowise_api_endpoint}")
        logger.info(f"Chatflow ID: {self.chatflow_id}")

    def query_flowise(self, query: str, anonymize: bool = False, output_type: str = "summary") -> str:
        """Query the Flowise chatflow."""
        try:
            if not self.flowise_api_key:
                return "❌ FLOWISE_API_KEY not configured"
            
            if not self.chatflow_id or self.chatflow_id == 'your_chatflow_id':
                return "❌ FLOWISE_CHATFLOW_ID not configured"
            
            # Prepare the query
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
            
            # Make the request
            headers = {
                "Authorization": f"Bearer {self.flowise_api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.flowise_api_endpoint}/api/v1/prediction/{self.chatflow_id}"
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return f"✅ Query successful:\n\n{result.get('text', 'No response text')}"
            else:
                return f"❌ Query failed: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"Query error: {e}")
            return f"❌ Query error: {str(e)}"

    def get_status(self) -> str:
        """Get system status."""
        try:
            status = {
                "flowise_api_endpoint": self.flowise_api_endpoint,
                "flowise_api_key": "✅ Configured" if self.flowise_api_key else "❌ Not configured",
                "chatflow_id": self.chatflow_id if self.chatflow_id and self.chatflow_id != 'your_chatflow_id' else "❌ Not configured",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Test Flowise connection
            if self.flowise_api_key and self.chatflow_id and self.chatflow_id != 'your_chatflow_id':
                try:
                    headers = {"Authorization": f"Bearer {self.flowise_api_key}"}
                    response = requests.get(f"{self.flowise_api_endpoint}/api/v1/chatflows", headers=headers, timeout=5)
                    if response.status_code == 200:
                        status["flowise_connection"] = "✅ Connected"
                    else:
                        status["flowise_connection"] = f"❌ Error: {response.status_code}"
                except Exception as e:
                    status["flowise_connection"] = f"❌ Connection failed: {str(e)}"
            else:
                status["flowise_connection"] = "❌ Not configured"
            
            return json.dumps(status, indent=2)
            
        except Exception as e:
            logger.error(f"Status error: {e}")
            return f"❌ Status error: {str(e)}"

    def fix_flow(self, fix_request: str) -> str:
        """Request flow updates."""
        try:
            return f"✅ Flow fix request received: {fix_request}\n\nThis would typically update the Flowise graph. For now, this is a placeholder function."
        except Exception as e:
            logger.error(f"Fix flow error: {e}")
            return f"❌ Fix flow error: {str(e)}"

def main():
    """Main MCP server loop."""
    logger.info("Living Truth Engine MCP Server starting...")
    
    # Create server instance
    server = LivingTruthEngineMCP()
    
    # Simple JSON-RPC stdio server
    while True:
        try:
            # Read JSON-RPC request from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            request = json.loads(line.strip())
            method = request.get("method")
            request_id = request.get("id")
            
            logger.debug(f"Received request: {method}")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": True
                        },
                        "serverInfo": {
                            "name": "living-truth-engine-mcp",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "tools/list":
                tools = [
                    {
                        "name": "living_truth_query_flowise",
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
                        "name": "living_truth_get_status",
                        "description": "Get Living Truth Engine system status (chatflows, sources, confidence metrics, dashboard link)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    },
                    {
                        "name": "living_truth_fix_flow",
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
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"tools": tools}
                }
            elif method == "tools/call":
                name = request.get("params", {}).get("name")
                arguments = request.get("params", {}).get("arguments", {})
                
                logger.debug(f"Calling tool: {name} with args: {arguments}")
                
                if name == "living_truth_query_flowise":
                    query = arguments.get("query", "")
                    anonymize = arguments.get("anonymize", False)
                    output_type = arguments.get("output_type", "summary")
                    result = server.query_flowise(query, anonymize, output_type)
                elif name == "living_truth_get_status":
                    result = server.get_status()
                elif name == "living_truth_fix_flow":
                    fix_request = arguments.get("fix_request", "")
                    result = server.fix_flow(fix_request)
                else:
                    result = f"❌ Unknown tool: {name}"
                
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {"content": [{"type": "text", "text": result}]}
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            # Write response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            continue
        except Exception as e:
            logger.error(f"Server error: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": request_id if 'request_id' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            }
            print(json.dumps(error_response))
            sys.stdout.flush()

if __name__ == "__main__":
    main() 