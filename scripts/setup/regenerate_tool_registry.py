#!/usr/bin/env python3
"""
Regenerate the complete tool registry with all 63 tools.
This script reads the actual MCP server files and creates a complete registry.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any

def extract_tools_from_file(file_path: Path) -> List[Dict[str, Any]]:
    """Extract tool definitions from an MCP server file."""
    tools = []
    
    if not file_path.exists():
        return tools
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find all @mcp.tool() decorated functions
    tool_pattern = r'@mcp\.tool\(\)\s*\ndef\s+(\w+)\s*\([^)]*\)\s*->\s*[^:]*:\s*"""(.*?)"""'
    matches = re.findall(tool_pattern, content, re.DOTALL)
    
    for func_name, docstring in matches:
        # Extract server name from file path
        server_name = file_path.stem
        
        # Create tool definition
        tool = {
            "name": func_name,
            "description": docstring.strip().replace('\n', ' ').replace('  ', ' '),
            "server": server_name,
            "module": f"src.mcp_servers.{server_name}",
            "function": func_name,
            "params_schema": {
                "param": {
                    "type": "string",
                    "required": True
                }
            }
        }
        tools.append(tool)
    
    return tools

def regenerate_tool_registry():
    """Regenerate the complete tool registry."""
    project_root = Path(__file__).parent.parent.parent
    registry_path = project_root / "config" / "tool_registry.json"
    
    # Define server files and their expected tool counts
    server_files = {
        "living_truth_fastmcp_server": 22,
        "langflow_mcp_server": 12,
        "postgresql_mcp_server": 6,
        "huggingface_mcp_server": 5,
        "devdocs_mcp_server": 4,
        "rulego_mcp_server": 5,
        "mcp_solver_server": 5,
        "github_mcp_server": 4
    }
    
    registry = {
        "version": "1.0.0",
        "last_updated": "2025-08-03",
        "total_tools": 63,
        "servers": {}
    }
    
    total_tools = 0
    
    for server_name, expected_count in server_files.items():
        file_path = project_root / "src" / "mcp_servers" / f"{server_name}.py"
        tools = extract_tools_from_file(file_path)
        
        if len(tools) != expected_count:
            print(f"⚠️  Warning: {server_name} has {len(tools)} tools, expected {expected_count}")
        
        registry["servers"][server_name] = {
            "description": f"{server_name.replace('_', ' ').title()} MCP Server",
            "tools": tools
        }
        
        total_tools += len(tools)
        print(f"✅ {server_name}: {len(tools)} tools")
    
    registry["total_tools"] = total_tools
    
    # Save the registry
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
    
    print(f"\n🎉 Tool registry regenerated!")
    print(f"📊 Total tools: {total_tools}")
    print(f"📁 Saved to: {registry_path}")
    
    return registry

if __name__ == "__main__":
    regenerate_tool_registry() 