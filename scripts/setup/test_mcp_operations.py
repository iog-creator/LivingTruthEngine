#!/usr/bin/env python3
"""
Test Langflow MCP Operations
===========================

This script demonstrates how to use Langflow MCP tools.
Run this in Cursor after restarting to load the MCP configuration.
"""

def test_langflow_mcp():
    """Test Langflow MCP operations."""
    
    print("🚀 Testing Langflow MCP Operations")
    print("=" * 40)
    
    # Test 1: List flows
    try:
        print("\n1. Listing flows...")
        flows = mcp_lf-cursor_list_flows()
        print(f"✅ Found {len(flows)} flows")
        for flow in flows:
            print(f"  - {flow.get('name', 'Unknown')} (ID: {flow.get('id', 'Unknown')})")
    except Exception as e:
        print(f"❌ List flows failed: {e}")
    
    # Test 2: Get flow status
    try:
        print("\n2. Getting flow status...")
        status = mcp_lf-cursor_get_flow_status()
        print(f"✅ Flow status: {status}")
    except Exception as e:
        print(f"❌ Get status failed: {e}")
    
    # Test 3: Create flow (if needed)
    try:
        print("\n3. Creating flow...")
        with open('flows/living_truth_engine_flow.json', 'r') as f:
            flow_data = json.load(f)
        
        result = mcp_lf-cursor_create_flow(flow_data)
        print(f"✅ Flow created: {result}")
    except Exception as e:
        print(f"❌ Create flow failed: {e}")
    
    print("\n🎯 MCP testing completed!")

if __name__ == "__main__":
    test_langflow_mcp()
