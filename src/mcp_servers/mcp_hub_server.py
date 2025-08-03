#!/usr/bin/env python3
"""
MCP Hub Server - Consolidated Tool Gateway
==========================================

This server acts as a proxy/gateway that exposes only 15 meta-tools to Cursor
while dynamically accessing, building, or executing tools from the underlying
23+ tools across multiple servers. This avoids Cursor's 40-tool limit while
providing full access to all functionality.

Features:
- Tool registry management
- Dynamic tool execution
- Tool building and modification
- Batch operations
- Health monitoring
"""

import json
import importlib
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import traceback

# Add src to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from mcp.server.fastmcp import FastMCP
mcp = FastMCP()
tool = mcp.tool

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPHubServer:
    """MCP Hub Server for consolidated tool management."""
    
    def __init__(self):
        """Initialize the MCP Hub Server."""
        # Use absolute path to the project root
        project_root = Path(__file__).parent.parent.parent
        self.registry_path = project_root / "config" / "tool_registry.json"
        self.registry = self.load_registry()
        self.loaded_modules = {}
        logger.info(f"MCP Hub Server initialized with {self.registry.get('total_tools', 0)} tools")
    
    def load_registry(self) -> Dict[str, Any]:
        """Load the tool registry from JSON file with automatic backup."""
        backup_path = self.registry_path.with_suffix('.json.bak')
        
        try:
            if self.registry_path.exists():
                # Create backup before loading
                import shutil
                shutil.copy2(self.registry_path, backup_path)
                logger.debug(f"Created backup: {backup_path}")
                
                with open(self.registry_path, 'r') as f:
                    registry = json.load(f)
                
                # Validate registry structure
                self.validate_registry(registry)
                
                logger.info(f"Loaded tool registry with {registry.get('total_tools', 0)} tools")
                return registry
            else:
                logger.warning(f"Registry file not found: {self.registry_path}")
                return {"version": "1.0.0", "total_tools": 0, "servers": {}}
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
            
            # Try to load from backup
            if backup_path.exists():
                try:
                    logger.info(f"Attempting to load from backup: {backup_path}")
                    with open(backup_path, 'r') as f:
                        backup_registry = json.load(f)
                    logger.info("Successfully loaded registry from backup")
                    return backup_registry
                except Exception as backup_error:
                    logger.error(f"Failed to load backup registry: {backup_error}")
            
            return {"version": "1.0.0", "total_tools": 0, "servers": {}}

    def validate_registry(self, registry: Dict[str, Any]) -> bool:
        """
        Validate registry structure and content.
        
        Args:
            registry: Registry dictionary to validate
            
        Returns:
            True if valid, raises ValueError if invalid
        """
        validation_errors = []
        
        if not isinstance(registry, dict):
            validation_errors.append("Registry must be a dictionary")
        
        if 'servers' not in registry:
            validation_errors.append("Registry missing 'servers' key")
        
        if validation_errors:
            raise ValueError(f"Registry validation failed: {'; '.join(validation_errors)}")
        
        required_tool_fields = ['name', 'description', 'server', 'module', 'function']
        
        for server_name, server_data in registry['servers'].items():
            if not isinstance(server_data, dict):
                validation_errors.append(f"Server '{server_name}' data must be a dictionary")
                continue
            
            if 'tools' not in server_data:
                validation_errors.append(f"Server '{server_name}' missing 'tools' key")
                continue
            
            for tool in server_data['tools']:
                if not isinstance(tool, dict):
                    validation_errors.append(f"Tool in server '{server_name}' must be a dictionary")
                    continue
                
                # Check required fields
                for field in required_tool_fields:
                    if field not in tool:
                        validation_errors.append(f"Tool '{tool.get('name', 'unknown')}' missing required field: {field}")
                
                # Validate params_schema if present
                if 'params_schema' in tool:
                    if not isinstance(tool['params_schema'], dict):
                        validation_errors.append(f"Tool '{tool['name']}' params_schema must be a dictionary")
                    else:
                        for param_name, param_def in tool['params_schema'].items():
                            if not isinstance(param_def, dict):
                                validation_errors.append(f"Tool '{tool['name']}' parameter '{param_name}' definition must be a dictionary")
                            elif 'type' not in param_def:
                                validation_errors.append(f"Tool '{tool['name']}' parameter '{param_name}' missing 'type' field")
        
        if validation_errors:
            error_msg = f"Registry validation failed with {len(validation_errors)} errors: {'; '.join(validation_errors[:5])}"
            if len(validation_errors) > 5:
                error_msg += f" (and {len(validation_errors) - 5} more)"
            raise ValueError(error_msg)
        
        logger.info(f"Registry validation passed for {sum(len(server.get('tools', [])) for server in registry['servers'].values())} tools")
        return True
    
    def reload_registry(self) -> Dict[str, Any]:
        """Reload the tool registry from file."""
        self.registry = self.load_registry()
        return self.registry
    
    def get_tool_by_name(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get tool definition by name."""
        for server_name, server_data in self.registry.get("servers", {}).items():
            for tool_def in server_data.get("tools", []):
                if tool_def["name"] == tool_name:
                    return tool_def
        return None
    
    def load_module(self, module_name: str) -> Any:
        """Dynamically load a module."""
        if module_name not in self.loaded_modules:
            try:
                self.loaded_modules[module_name] = importlib.import_module(module_name)
                logger.debug(f"Loaded module: {module_name}")
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")
                return None
        return self.loaded_modules[module_name]
    
    def _execute_tool_internal(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Execute a tool by name with parameters."""
        import time
        
        tool_def = self.get_tool_by_name(tool_name)
        if not tool_def:
            raise ValueError(f"Tool '{tool_name}' not found in registry")

        start_time = time.time()
        
        try:
            module_name = tool_def["module"]
            function_name = tool_def["function"]

            # Load the module
            module = self.load_module(module_name)
            if not module:
                raise ImportError(f"Could not load module: {module_name}")

            # Get the function
            func = getattr(module, function_name, None)
            if not func:
                raise AttributeError(f"Function '{function_name}' not found in module '{module_name}'")

            # Execute the function
            logger.info(f"Executing tool: {tool_name} with params: {params}")
            result = func(**params)
            
            # Performance monitoring
            duration = time.time() - start_time
            logger.info(f"Executed {tool_name} in {duration:.2f}s")
            
            if duration > 1.0:
                logger.warning(f"Slow execution for {tool_name}: {duration:.2f}s")
            
            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Error executing tool '{tool_name}' after {duration:.2f}s: {e}")
            logger.error(traceback.format_exc())
            raise
    
    @tool()
    def list_tools(self, query: str = "", server: str = "") -> List[Dict[str, Any]]:
        """
        List available tools with optional filtering.
        
        Args:
            query: Filter tools by name or description
            server: Filter by server name
            
        Returns:
            List of tool definitions matching the criteria
        """
        tools = []
        query_lower = query.lower()
        server_lower = server.lower()
        
        for server_name, server_data in self.registry.get("servers", {}).items():
            if server and server_lower not in server_name.lower():
                continue
                
            for tool_def in server_data.get("tools", []):
                tool_name = tool_def["name"].lower()
                description = tool_def.get("description", "").lower()
                
                if not query or query_lower in tool_name or query_lower in description:
                    tools.append({
                        "name": tool_def["name"],
                        "description": tool_def.get("description", ""),
                        "server": server_name,
                        "module": tool_def.get("module", ""),
                        "params_schema": tool_def.get("params_schema", {})
                    })
        
        logger.info(f"Listed {len(tools)} tools (query: '{query}', server: '{server}')")
        return tools
    
    @tool()
    def get_tool_details(self, tool_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific tool.
        
        Args:
            tool_name: Name of the tool to get details for
            
        Returns:
            Detailed tool definition including schema and metadata
        """
        tool_def = self.get_tool_by_name(tool_name)
        if not tool_def:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        return {
            "name": tool_def["name"],
            "description": tool_def.get("description", ""),
            "server": tool_def["server"],
            "module": tool_def.get("module", ""),
            "function": tool_def.get("function", ""),
            "params_schema": tool_def.get("params_schema", {}),
            "registry_version": self.registry.get("version", "unknown")
        }
    
    @tool()
    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute any tool by name with parameters.
        
        Args:
            tool_name: Name of the tool to execute
            params: Parameters to pass to the tool
            
        Returns:
            Result from the tool execution
        """
        return self._execute_tool_internal(tool_name, params)
    
    @tool()
    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Search tools by semantic query.
        
        Args:
            query: Search query to match against tool names and descriptions
            
        Returns:
            List of matching tools with relevance information
        """
        results = []
        query_lower = query.lower()
        
        for server_name, server_data in self.registry.get("servers", {}).items():
            for tool_def in server_data.get("tools", []):
                tool_name = tool_def["name"].lower()
                description = tool_def.get("description", "").lower()
                
                # Simple relevance scoring
                relevance = 0
                if query_lower in tool_name:
                    relevance += 10
                if query_lower in description:
                    relevance += 5
                if query_lower in server_name.lower():
                    relevance += 2
                
                if relevance > 0:
                    results.append({
                        "name": tool_def["name"],
                        "description": tool_def.get("description", ""),
                        "server": server_name,
                        "relevance": relevance,
                        "module": tool_def.get("module", "")
                    })
        
        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)
        logger.info(f"Search found {len(results)} tools for query: '{query}'")
        return results
    
    @tool()
    def batch_execute_tools(self, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple tools in sequence.
        
        Args:
            tools: List of tool execution requests with 'name' and 'params'
            
        Returns:
            List of results from each tool execution
        """
        import time
        
        start_time = time.time()
        results = []
        
        for i, tool_request in enumerate(tools):
            try:
                tool_name = tool_request.get("name")
                params = tool_request.get("params", {})
                
                if not tool_name:
                    results.append({
                        "index": i,
                        "success": False,
                        "error": "Missing tool name"
                    })
                    continue
                
                result = self._execute_tool_internal(tool_name, params)
                results.append({
                    "index": i,
                    "tool_name": tool_name,
                    "success": True,
                    "result": result
                })
                
            except Exception as e:
                results.append({
                    "index": i,
                    "tool_name": tool_request.get("name", "unknown"),
                    "success": False,
                    "error": str(e)
                })
        
        total_duration = time.time() - start_time
        successful_count = len([r for r in results if r['success']])
        
        logger.info(f"Batch executed {len(tools)} tools in {total_duration:.2f}s, {successful_count} successful")
        
        if total_duration > 5.0:
            logger.warning(f"Slow batch execution: {total_duration:.2f}s for {len(tools)} tools")
        
        return results
    
    @tool()
    def get_status(self) -> Dict[str, Any]:
        """
        Get hub server status and health information.
        
        Returns:
            Status information including tool counts and health
        """
        total_tools = sum(
            len(server_data.get("tools", []))
            for server_data in self.registry.get("servers", {}).values()
        )
        
        return {
            "status": "healthy",
            "hub_version": "1.0.0",
            "registry_version": self.registry.get("version", "unknown"),
            "total_tools": total_tools,
            "total_servers": len(self.registry.get("servers", {})),
            "loaded_modules": len(self.loaded_modules),
            "timestamp": datetime.now().isoformat(),
            "registry_path": str(self.registry_path)
        }
    
    @tool()
    def reload_registry(self) -> str:
        """
        Reload the tool registry from file.
        
        Returns:
            Status message about the reload operation
        """
        try:
            old_count = sum(
                len(server_data.get("tools", []))
                for server_data in self.registry.get("servers", {}).values()
            )
            
            self.registry = self.load_registry()
            
            new_count = sum(
                len(server_data.get("tools", []))
                for server_data in self.registry.get("servers", {}).values()
            )
            
            return f"Registry reloaded successfully. Tools: {old_count} -> {new_count}"
            
        except Exception as e:
            return f"Error reloading registry: {e}"
    
    @tool()
    def execute_analysis_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute analysis-specific tools with enhanced error handling.
        
        Args:
            tool_name: Name of the analysis tool to execute
            params: Parameters for the tool
            
        Returns:
            Analysis result
        """
        # Validate that this is an analysis tool
        analysis_tools = [
            "query_langflow", "analyze_transcript", "generate_viz",
            "batch_analysis_operations"
        ]
        
        if tool_name not in analysis_tools:
            raise ValueError(f"'{tool_name}' is not an analysis tool. Available: {analysis_tools}")
        
        return self._execute_tool_internal(tool_name, params)
    
    @tool()
    def execute_system_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute system management tools with enhanced error handling.
        
        Args:
            tool_name: Name of the system tool to execute
            params: Parameters for the tool
            
        Returns:
            System operation result
        """
        # Validate that this is a system tool
        system_tools = [
            "get_status", "list_sources", "get_lm_studio_models",
            "batch_system_operations"
        ]
        
        if tool_name not in system_tools:
            raise ValueError(f"'{tool_name}' is not a system tool. Available: {system_tools}")
        
        return self._execute_tool_internal(tool_name, params)
    
    @tool()
    def execute_langflow_tool(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """
        Execute Langflow-specific tools with enhanced error handling.
        
        Args:
            tool_name: Name of the Langflow tool to execute
            params: Parameters for the tool
            
        Returns:
            Langflow operation result
        """
        # Validate that this is a Langflow tool
        langflow_tools = [
            "query_langflow", "create_langflow", "export_flow_to_file",
            "load_flow_from_file", "get_langflow_status"
        ]
        
        if tool_name not in langflow_tools:
            raise ValueError(f"'{tool_name}' is not a Langflow tool. Available: {langflow_tools}")
        
        return self._execute_tool_internal(tool_name, params)
    
    @tool()
    def get_tool_categories(self) -> Dict[str, List[str]]:
        """
        Get available tool categories and their tools.
        
        Returns:
            Dictionary mapping categories to tool lists
        """
        categories = {
            "analysis": ["query_langflow", "analyze_transcript", "generate_viz", "batch_analysis_operations"],
            "system": ["get_status", "list_sources", "get_lm_studio_models", "batch_system_operations"],
            "langflow": ["query_langflow", "create_langflow", "export_flow_to_file", "load_flow_from_file", "get_langflow_status"],
            "github": ["list_repositories", "create_issue"],
            "database": ["test_connection", "list_tables", "execute_query"],
            "models": ["search_models", "get_model_info", "generate_lm_studio_text"],
            "documentation": ["crawl_docs", "retrieve_docs"],
            "workflow": ["query_rulego_chain", "list_rulego_chains"],
            "solver": ["solve_constraint", "route_llm"]
        }
        
        return categories
    
    @tool()
    def execute_category_tools(self, category: str, tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute multiple tools from a specific category.
        
        Args:
            category: Category name (analysis, system, langflow, etc.)
            tools: List of tool execution requests
            
        Returns:
            Results from tool executions
        """
        categories = self.get_tool_categories()
        if category not in categories:
            raise ValueError(f"Unknown category '{category}'. Available: {list(categories.keys())}")
        
        valid_tools = categories[category]
        results = []
        
        for tool_request in tools:
            tool_name = tool_request.get("name")
            if tool_name not in valid_tools:
                results.append({
                    "tool_name": tool_name,
                    "success": False,
                    "error": f"Tool '{tool_name}' not in category '{category}'"
                })
                continue
            
            try:
                params = tool_request.get("params", {})
                result = self.execute_tool(tool_name, params)
                results.append({
                    "tool_name": tool_name,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "tool_name": tool_name,
                    "success": False,
                    "error": str(e)
                })
        
        return results

    @tool()
    def build_tool(self, tool_def: Dict[str, Any]) -> str:
        """
        Build and add a new tool to registry.
        
        Args:
            tool_def: Tool definition with required fields
            
        Returns:
            Success message
        """
        required = ['name', 'description', 'server', 'module', 'function', 'params_schema']
        if not all(k in tool_def for k in required):
            raise ValueError(f"Invalid tool definition. Required fields: {required}")
        
        # Validate params_schema
        for param_name, param_def in tool_def['params_schema'].items():
            if 'type' not in param_def:
                raise ValueError(f"Parameter '{param_name}' missing type definition")
        
        # Add to registry
        if 'servers' not in self.registry:
            self.registry['servers'] = {}
        
        server_name = tool_def['server']
        if server_name not in self.registry['servers']:
            self.registry['servers'][server_name] = {'tools': []}
        
        # Check if tool already exists
        existing_tools = [t['name'] for t in self.registry['servers'][server_name]['tools']]
        if tool_def['name'] in existing_tools:
            raise ValueError(f"Tool '{tool_def['name']}' already exists in server '{server_name}'")
        
        self.registry['servers'][server_name]['tools'].append(tool_def)
        
        # Update total count
        total_tools = sum(len(server['tools']) for server in self.registry['servers'].values())
        self.registry['total_tools'] = total_tools
        
        # Save to file
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
        
        logger.info(f"Built tool: {tool_def['name']} in server {server_name}")
        return f"✅ Tool '{tool_def['name']}' created successfully in server '{server_name}'"

    @tool()
    def update_tool(self, tool_name: str, updates: Dict[str, Any]) -> str:
        """
        Update an existing tool in registry.
        
        Args:
            tool_name: Name of the tool to update
            updates: Dictionary of fields to update
            
        Returns:
            Success message
        """
        tool_found = False
        for server_name, server_data in self.registry.get('servers', {}).items():
            for tool in server_data.get('tools', []):
                if tool['name'] == tool_name:
                    # Validate updates
                    if 'params_schema' in updates:
                        for param_name, param_def in updates['params_schema'].items():
                            if 'type' not in param_def:
                                raise ValueError(f"Parameter '{param_name}' missing type definition")
                    
                    tool.update(updates)
                    tool_found = True
                    break
            if tool_found:
                break
        
        if not tool_found:
            raise ValueError(f"Tool '{tool_name}' not found in registry")
        
        # Save to file
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
        
        logger.info(f"Updated tool: {tool_name}")
        return f"✅ Tool '{tool_name}' updated successfully"

    @tool()
    def delete_tool(self, tool_name: str) -> str:
        """
        Delete a tool from registry.
        
        Args:
            tool_name: Name of the tool to delete
            
        Returns:
            Success message
        """
        tool_found = False
        for server_name, server_data in self.registry.get('servers', {}).items():
            original_count = len(server_data.get('tools', []))
            server_data['tools'] = [t for t in server_data.get('tools', []) if t['name'] != tool_name]
            if len(server_data['tools']) < original_count:
                tool_found = True
                break
        
        if not tool_found:
            raise ValueError(f"Tool '{tool_name}' not found in registry")
        
        # Update total count
        total_tools = sum(len(server['tools']) for server in self.registry['servers'].values())
        self.registry['total_tools'] = total_tools
        
        # Save to file
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)
        
        logger.info(f"Deleted tool: {tool_name}")
        return f"✅ Tool '{tool_name}' deleted successfully"


def main():
    """Main entry point for the MCP Hub Server."""
    try:
        server = MCPHubServer()
        logger.info("Starting MCP Hub Server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("MCP Hub Server stopped by user")
    except Exception as e:
        logger.error(f"Error running MCP Hub Server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 