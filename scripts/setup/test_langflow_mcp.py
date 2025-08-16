#!/usr/bin/env python3
"""
Test Langflow MCP Server Connection
==================================

Test the direct connection to Langflow via MCP server
to verify available tools and functionality.
"""

import json
from pathlib import Path

import requests


def test_langflow_mcp_connection():
    """Test the Langflow MCP server connection."""

    print("🚀 Testing Langflow MCP Server Connection")
    print("=" * 50)

    # Langflow MCP endpoint
    mcp_endpoint = "http://localhost:7860/api/v1/mcp/project/3bd92a44-057b-4378-a674-80910d570986/sse"

    try:
        # Test basic connection
        print(f"🔍 Testing connection to: {mcp_endpoint}")
        response = requests.get(mcp_endpoint, timeout=10)

        if response.status_code == 200:
            print("✅ Langflow MCP server is accessible")
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

    # Test Langflow API endpoints
    print("\n🔍 Testing Langflow API endpoints...")

    # Health check
    try:
        health_response = requests.get("http://localhost:7860/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Langflow health: {health_data}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # List flows
    try:
        flows_response = requests.get("http://localhost:7860/api/v1/flows/")
        if flows_response.status_code == 200:
            flows_data = flows_response.json()
            print(f"✅ Found {len(flows_data)} flows")
            for flow in flows_data:
                print(
                    f"  - {flow.get('name', 'Unknown')} (ID: {flow.get('id', 'Unknown')})"
                )
        else:
            print(f"❌ Flows list failed: {flows_response.status_code}")
    except Exception as e:
        print(f"❌ Flows list error: {e}")

    # Test MCP tools via API
    print("\n🔍 Testing MCP tools via API...")

    # Get available tools
    try:
        tools_response = requests.get("http://localhost:7860/api/v1/tools/")
        if tools_response.status_code == 200:
            tools_data = tools_response.json()
            print(f"✅ Found {len(tools_data)} tools")
            for tool in tools_data[:5]:  # Show first 5
                print(
                    f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}"
                )
        else:
            print(f"❌ Tools list failed: {tools_response.status_code}")
    except Exception as e:
        print(f"❌ Tools list error: {e}")

    print("\n🎯 Langflow MCP server test completed!")
    return True


def test_flow_operations():
    """Test flow operations via Langflow API."""

    print("\n🔧 Testing Flow Operations")
    print("=" * 30)

    # Load the generated flow
    flow_file = Path("flows/living_truth_engine_flow.json")
    if not flow_file.exists():
        print("❌ Flow file not found")
        return False

    with open(flow_file, "r") as f:
        flow_data = json.load(f)

    print(f"✅ Loaded flow: {flow_data.get('name', 'Unknown')}")

    # Test flow creation via API
    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": "admin",  # Default admin key
        }

        create_response = requests.post(
            "http://localhost:7860/api/v1/flows/", json=flow_data, headers=headers
        )

        if create_response.status_code in [200, 201]:
            result = create_response.json()
            flow_id = result.get("id")
            flow_name = result.get("name", "Unknown")
            print(f"✅ Flow created successfully!")
            print(f"  - ID: {flow_id}")
            print(f"  - Name: {flow_name}")
            print(f"  - URL: http://localhost:7860/flows/{flow_id}")
            return True
        else:
            print(f"❌ Flow creation failed: {create_response.status_code}")
            print(f"  Response: {create_response.text}")
            return False

    except Exception as e:
        print(f"❌ Flow creation error: {e}")
        return False


def main():
    """Main test function."""

    print("🚀 Langflow MCP Server Integration Test")
    print("=" * 50)

    # Test basic connection
    if not test_langflow_mcp_connection():
        print("❌ Basic connection test failed")
        return

    # Test flow operations
    if test_flow_operations():
        print("\n✅ All tests passed!")
        print("🎯 Langflow MCP server is ready for use")
    else:
        print("\n❌ Some tests failed")
        print("🔧 Check Langflow configuration and API endpoints")


if __name__ == "__main__":
    main()
