#!/usr/bin/env python3
"""
MCP Visualization API Server

FastAPI server that serves the HTML visualization and provides REST API endpoints
for real MCP tool execution from the web interface.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from src.mcp_servers.mcp_hub_server import MCPHubServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ToolExecutionRequest(BaseModel):
    """Request model for tool execution."""
    tool_name: str
    params: Dict[str, Any] = {}


class MCPVisualizationAPIServer:
    """FastAPI server for MCP visualization integration."""
    
    def __init__(self):
        self.app = FastAPI(
            title="MCP Visualization API",
            description="API for interacting with MCP Hub Server tools from web visualization",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize MCP Hub Server
        self.hub_server = MCPHubServer()
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup API routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def serve_visualization():
            """Serve the main HTML visualization."""
            viz_path = project_root / "data" / "visualizations" / "phase8_pipeline_visualization.html"
            if viz_path.exists():
                with open(viz_path, 'r', encoding='utf-8') as f:
                    return HTMLResponse(content=f.read())
            else:
                return HTMLResponse(content="<h1>Visualization not found</h1>", status_code=404)
        
        @self.app.get("/api/tools")
        async def get_tools():
            """Get all available tools organized by category."""
            try:
                categories = self.hub_server.get_tool_categories()
                tools_info = {}
                
                for category, tool_names in categories.get('result', {}).items():
                    tools_info[category] = []
                    for tool_name in tool_names:
                        try:
                            tool_details = self.hub_server.get_tool_details(tool_name)
                            tools_info[category].append({
                                'name': tool_name,
                                'description': tool_details.get('result', {}).get('description', ''),
                                'params_schema': tool_details.get('result', {}).get('params_schema', {})
                            })
                        except Exception as e:
                            logger.warning(f"Could not get details for tool {tool_name}: {e}")
                            tools_info[category].append({
                                'name': tool_name,
                                'description': f'Tool: {tool_name}',
                                'params_schema': {}
                            })
                
                return {
                    'success': True,
                    'tools': tools_info,
                    'examples': self._get_tool_examples(tools_info)
                }
            except Exception as e:
                logger.error(f"Error getting tools: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/tools/{tool_name}")
        async def get_tool_info(tool_name: str):
            """Get detailed information about a specific tool."""
            try:
                tool_details = self.hub_server.get_tool_details(tool_name)
                return {
                    'success': True,
                    'tool_info': tool_details.get('result', {})
                }
            except Exception as e:
                logger.error(f"Error getting tool info for {tool_name}: {e}")
                raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
        
        @self.app.post("/api/execute")
        async def execute_tool(request: ToolExecutionRequest):
            """Execute a tool through the MCP Hub Server."""
            try:
                logger.info(f"Executing tool: {request.tool_name} with params: {request.params}")
                
                # Execute the tool
                result = self.hub_server.execute_tool(request.tool_name, request.params)
                
                logger.info(f"Tool {request.tool_name} executed successfully")
                return {
                    'success': True,
                    'result': result,
                    'tool_name': request.tool_name,
                    'timestamp': asyncio.get_event_loop().time()
                }
                
            except Exception as e:
                logger.error(f"Error executing tool {request.tool_name}: {e}")
                return {
                    'success': False,
                    'error': str(e),
                    'tool_name': request.tool_name,
                    'timestamp': asyncio.get_event_loop().time()
                }
        
        @self.app.get("/api/status")
        async def get_status():
            """Get MCP Hub Server status."""
            try:
                status = self.hub_server.get_status()
                return {
                    'success': True,
                    'status': status.get('result', status)
                }
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint."""
            return {
                'status': 'healthy',
                'service': 'mcp_visualization_api',
                'timestamp': asyncio.get_event_loop().time()
            }
    
    def _get_tool_examples(self, tools_info: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate example parameters for tools."""
        examples = {}
        
        for category, tools in tools_info.items():
            for tool in tools:
                tool_name = tool['name']
                params_schema = tool.get('params_schema', {})
                example_params = {}
                
                for param_name, param_info in params_schema.items():
                    param_type = param_info.get('type', 'string')
                    required = param_info.get('required', False)
                    
                    if param_type == 'string':
                        if 'query' in param_name.lower():
                            example_params[param_name] = "Sample query for analysis"
                        elif 'url' in param_name.lower():
                            example_params[param_name] = "https://www.youtube.com/@imaginationpodcastofficial"
                        elif 'name' in param_name.lower():
                            example_params[param_name] = "0xXsEyKguvU_transcript.txt"
                        elif 'topic' in param_name.lower():
                            example_params[param_name] = "survivor testimony analysis"
                        else:
                            example_params[param_name] = "sample_value"
                    elif param_type == 'int':
                        if 'max' in param_name.lower():
                            example_params[param_name] = 10
                        elif 'limit' in param_name.lower():
                            example_params[param_name] = 20
                        else:
                            example_params[param_name] = 5
                    elif param_type == 'boolean':
                        example_params[param_name] = False
                    elif param_type == 'list':
                        example_params[param_name] = []
                    elif param_type == 'dict':
                        example_params[param_name] = {}
                
                examples[tool_name] = {
                    'description': tool.get('description', ''),
                    'example': example_params
                }
        
        return examples


async def main():
    """Main function to run the FastAPI server."""
    try:
        # Initialize the API server
        logger.info("Initializing MCP Visualization API Server...")
        api_server = MCPVisualizationAPIServer()
        
        # Test the MCP Hub Server connection
        logger.info("Testing MCP Hub Server connection...")
        status = api_server.hub_server.get_status()
        logger.info(f"MCP Hub Server status: {status}")
        
        # Get available tools
        categories = api_server.hub_server.get_tool_categories()
        total_tools = sum(len(tools) for tools in categories.get('result', {}).values())
        logger.info(f"Available tools: {total_tools} total across {len(categories.get('result', {}))} categories")
        
        # Start the server
        logger.info("Starting FastAPI server...")
        config = uvicorn.Config(
            app=api_server.app,
            host="0.0.0.0",
            port=8081,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)
