#!/usr/bin/env python3
"""
Use Langflow MCP Server
======================

Demonstrate how to use the Langflow MCP server that's configured in Cursor.
This script shows the proper way to interact with Langflow via MCP.
"""

import json
import sys
from pathlib import Path

def demonstrate_langflow_mcp_usage():
    """Demonstrate how to use Langflow MCP server."""
    
    print("🚀 Langflow MCP Server Usage Guide")
    print("=" * 50)
    
    print("\n📋 Configuration in .cursor/mcp.json:")
    print("""
{
  "mcpServers": {
    "lf-cursor": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "http://localhost:7860/api/v1/mcp/project/3bd92a44-057b-4378-a674-80910d570986/sse"
      ],
      "description": "Langflow MCP Server - Direct connection to Langflow instance"
    }
  }
}
""")
    
    print("\n🎯 Available MCP Tools in Cursor:")
    print("""
Once the MCP server is configured and Cursor is restarted, you can use:

1. mcp_lf-cursor_* - Direct Langflow MCP tools
2. mcp_mcp_hub_server_execute_langflow_tool - Via MCP Hub Server

Example usage in Cursor:
- mcp_lf-cursor_list_flows() - List all flows
- mcp_lf-cursor_create_flow() - Create a new flow
- mcp_lf-cursor_run_flow() - Execute a flow
- mcp_lf-cursor_get_flow_status() - Get flow status
""")
    
    print("\n🔧 Testing MCP Server Connection:")
    print("""
1. Restart Cursor to load the new MCP configuration
2. Check Cursor Settings > MCP for green dots
3. Test with: mcp_lf-cursor_list_flows()
4. If successful, you'll see available Langflow tools
""")
    
    print("\n📁 Current Flow Status:")
    flow_file = Path("flows/living_truth_engine_flow.json")
    if flow_file.exists():
        with open(flow_file, 'r') as f:
            flow_data = json.load(f)
        print(f"✅ Flow file exists: {flow_data.get('name', 'Unknown')}")
        print(f"📋 Nodes: {len(flow_data.get('data', {}).get('nodes', []))}")
        print(f"🔗 Edges: {len(flow_data.get('data', {}).get('edges', []))}")
    else:
        print("❌ Flow file not found")
    
    print("\n🎯 Next Steps:")
    print("1. Restart Cursor to load MCP configuration")
    print("2. Test MCP connection: mcp_lf-cursor_list_flows()")
    print("3. Import flow: mcp_lf-cursor_create_flow()")
    print("4. Run flow: mcp_lf-cursor_run_flow()")
    print("5. Monitor: mcp_lf-cursor_get_flow_status()")

def create_mcp_test_script():
    """Create a test script for MCP operations."""
    
    test_script = """#!/usr/bin/env python3
\"\"\"
Test Langflow MCP Operations
===========================

This script demonstrates how to use Langflow MCP tools.
Run this in Cursor after restarting to load the MCP configuration.
\"\"\"

def test_langflow_mcp():
    \"\"\"Test Langflow MCP operations.\"\"\"
    
    print("🚀 Testing Langflow MCP Operations")
    print("=" * 40)
    
    # Test 1: List flows
    try:
        print("\\n1. Listing flows...")
        flows = mcp_lf-cursor_list_flows()
        print(f"✅ Found {len(flows)} flows")
        for flow in flows:
            print(f"  - {flow.get('name', 'Unknown')} (ID: {flow.get('id', 'Unknown')})")
    except Exception as e:
        print(f"❌ List flows failed: {e}")
    
    # Test 2: Get flow status
    try:
        print("\\n2. Getting flow status...")
        status = mcp_lf-cursor_get_flow_status()
        print(f"✅ Flow status: {status}")
    except Exception as e:
        print(f"❌ Get status failed: {e}")
    
    # Test 3: Create flow (if needed)
    try:
        print("\\n3. Creating flow...")
        with open('flows/living_truth_engine_flow.json', 'r') as f:
            flow_data = json.load(f)
        
        result = mcp_lf-cursor_create_flow(flow_data)
        print(f"✅ Flow created: {result}")
    except Exception as e:
        print(f"❌ Create flow failed: {e}")
    
    print("\\n🎯 MCP testing completed!")

if __name__ == "__main__":
    test_langflow_mcp()
"""
    
    with open("scripts/setup/test_mcp_operations.py", "w") as f:
        f.write(test_script)
    
    print("✅ Created test script: scripts/setup/test_mcp_operations.py")

def main():
    """Main function."""
    
    demonstrate_langflow_mcp_usage()
    create_mcp_test_script()
    
    print("\n🎯 Summary:")
    print("The Langflow MCP server is now configured in .cursor/mcp.json")
    print("Restart Cursor to load the configuration and test the MCP tools")
    print("Use mcp_lf-cursor_* commands to interact with Langflow directly")

if __name__ == "__main__":
    main() 