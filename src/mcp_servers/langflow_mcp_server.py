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
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

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

if __name__ == "__main__":
    logger.info("Langflow MCP Server starting...")
    mcp.run() 