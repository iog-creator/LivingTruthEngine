#!/usr/bin/env python3
"""
MCP Visualization Server

This server provides a bridge between the HTML visualization interface
and the MCP Hub Server, allowing real tool execution from the web interface.
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

from src.mcp_servers.mcp_hub_server import MCPHubServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPVisualizationServer:
    """Server that bridges HTML visualization with MCP Hub Server."""
    
    def __init__(self, hub_server: MCPHubServer):
        self.hub_server = hub_server
        self.available_tools = self._get_available_tools()
    
    def _get_available_tools(self) -> Dict[str, Any]:
        """Get available tools from the MCP Hub Server."""
        try:
            # Get tool categories
            categories_result = self.hub_server.get_tool_categories()
            categories = categories_result.get('result', {})
            
            # Get detailed tool information
            tools_info = {}
            for category, tool_names in categories.items():
                for tool_name in tool_names:
                    try:
                        tool_details = self.hub_server.get_tool_details(tool_name)
                        tools_info[tool_name] = {
                            'category': category,
                            'details': tool_details.get('result', {}),
                            'description': tool_details.get('result', {}).get('description', ''),
                            'params_schema': tool_details.get('result', {}).get('params_schema', {})
                        }
                    except Exception as e:
                        logger.warning(f"Could not get details for tool {tool_name}: {e}")
                        tools_info[tool_name] = {
                            'category': category,
                            'details': {},
                            'description': f'Tool: {tool_name}',
                            'params_schema': {}
                        }
            
            return tools_info
        except Exception as e:
            logger.error(f"Error getting available tools: {e}")
            return {}
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool through the MCP Hub Server."""
        try:
            logger.info(f"Executing tool: {tool_name} with params: {params}")
            
            # Execute the tool
            result = await self.hub_server.execute_tool(tool_name, params)
            
            logger.info(f"Tool {tool_name} executed successfully")
            return {
                'success': True,
                'result': result.get('result', result),
                'tool_name': tool_name,
                'timestamp': asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                'success': False,
                'error': str(e),
                'tool_name': tool_name,
                'timestamp': asyncio.get_event_loop().time()
            }
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool."""
        return self.available_tools.get(tool_name)
    
    def get_all_tools(self) -> Dict[str, Any]:
        """Get all available tools organized by category."""
        categories = {}
        for tool_name, tool_info in self.available_tools.items():
            category = tool_info.get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append({
                'name': tool_name,
                'description': tool_info.get('description', ''),
                'params_schema': tool_info.get('params_schema', {})
            })
        return categories
    
    def get_tool_examples(self) -> Dict[str, Any]:
        """Get example parameters for tools."""
        examples = {}
        for tool_name, tool_info in self.available_tools.items():
            params_schema = tool_info.get('params_schema', {})
            example_params = {}
            
            for param_name, param_info in params_schema.items():
                param_type = param_info.get('type', 'string')
                if param_type == 'string':
                    if 'query' in param_name.lower():
                        example_params[param_name] = "Sample query for analysis"
                    elif 'url' in param_name.lower():
                        example_params[param_name] = "https://example.com"
                    elif 'name' in param_name.lower():
                        example_params[param_name] = "sample_name"
                    else:
                        example_params[param_name] = "sample_value"
                elif param_type == 'int':
                    example_params[param_name] = 10
                elif param_type == 'boolean':
                    example_params[param_name] = False
                elif param_type == 'list':
                    example_params[param_name] = []
                elif param_type == 'dict':
                    example_params[param_name] = {}
            
            examples[tool_name] = {
                'description': tool_info.get('description', ''),
                'example': example_params
            }
        
        return examples


class MCPVisualizationAPI:
    """FastAPI server for MCP visualization integration."""
    
    def __init__(self, visualization_server: MCPVisualizationServer):
        self.visualization_server = visualization_server
    
    async def execute_tool_endpoint(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """API endpoint to execute a tool."""
        return await self.visualization_server.execute_tool(tool_name, params)
    
    def get_tools_endpoint(self) -> Dict[str, Any]:
        """API endpoint to get all available tools."""
        return {
            'success': True,
            'tools': self.visualization_server.get_all_tools(),
            'examples': self.visualization_server.get_tool_examples()
        }
    
    def get_tool_info_endpoint(self, tool_name: str) -> Dict[str, Any]:
        """API endpoint to get information about a specific tool."""
        tool_info = self.visualization_server.get_tool_info(tool_name)
        if tool_info:
            return {
                'success': True,
                'tool_info': tool_info
            }
        else:
            return {
                'success': False,
                'error': f'Tool {tool_name} not found'
            }


async def main():
    """Main function to run the MCP visualization server."""
    try:
        # Initialize the MCP Hub Server
        logger.info("Initializing MCP Hub Server...")
        hub_server = MCPHubServer()
        
        # Initialize the visualization server
        logger.info("Initializing MCP Visualization Server...")
        viz_server = MCPVisualizationServer(hub_server)
        
        # Initialize the API
        api = MCPVisualizationAPI(viz_server)
        
        # Test the connection
        logger.info("Testing MCP Hub Server connection...")
        status = hub_server.get_status()
        logger.info(f"MCP Hub Server status: {status}")
        
        # Get available tools
        tools = viz_server.get_all_tools()
        logger.info(f"Available tools: {len(tools)} categories")
        for category, tool_list in tools.items():
            logger.info(f"  {category}: {len(tool_list)} tools")
        
        # Test a simple tool execution
        logger.info("Testing tool execution...")
        test_result = await viz_server.execute_tool('get_status', {})
        logger.info(f"Test execution result: {test_result}")
        
        logger.info("MCP Visualization Server initialized successfully!")
        logger.info("You can now use the HTML visualization to interact with MCP tools.")
        
        # Keep the server running
        while True:
            await asyncio.sleep(1)
            
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
