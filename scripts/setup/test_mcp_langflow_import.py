#!/usr/bin/env python3
"""
Test MCP Hub Server Langflow Import
===================================

Test importing the Langflow flow using MCP Hub Server tools.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.append('src')

from mcp_servers.mcp_hub_server import MCPHubServer

def test_mcp_langflow_import():
    """Test importing Langflow flow using MCP Hub Server."""
    
    print("🧪 Testing MCP Hub Server Langflow Import")
    print("=" * 50)
    
    # Initialize MCP Hub Server
    server = MCPHubServer()
    print("✅ MCP Hub Server initialized")
    
    # Load flow JSON
    flow_file = Path("flows/living_truth_engine_flow.json")
    if not flow_file.exists():
        print(f"❌ Flow file not found: {flow_file}")
        return False
    
    with open(flow_file, 'r') as f:
        flow_config = json.load(f)
    print("✅ Flow JSON loaded")
    
    # Test MCP Langflow tools
    try:
        # Test get_langflow_status
        print("\n1. Testing get_langflow_status...")
        result = server.execute_langflow_tool("get_langflow_status", {})
        print(f"✅ Langflow status: {result}")
        
        # Test create_langflow
        print("\n2. Testing create_langflow...")
        result = server.execute_langflow_tool("create_langflow", {
            "flow_config": flow_config
        })
        print(f"✅ Flow creation result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Langflow import failed: {e}")
        return False

if __name__ == "__main__":
    if test_mcp_langflow_import():
        print("\n🎉 MCP Langflow import test completed successfully!")
    else:
        print("\n❌ MCP Langflow import test failed!")
        sys.exit(1) 