#!/usr/bin/env python3
"""
Test script to verify MCP server detection and functionality
Simulates how Cursor would interact with the MCP server
"""

import json
import os
import subprocess
import sys


def test_mcp_server():
    """Test the MCP server functionality"""

    # Path to the MCP server
    server_path = (
        "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/basic_mcp_server.py"
    )
    python_path = (
        "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/living_venv/bin/python3"
    )

    print("🔍 Testing MCP Server Detection...")
    print(f"Server Path: {server_path}")
    print(f"Python Path: {python_path}")

    # Check if files exist
    if not os.path.exists(server_path):
        print("❌ MCP server file not found!")
        return False

    if not os.path.exists(python_path):
        print("❌ Python executable not found!")
        return False

    print("✅ Files exist")

    # Test 1: Initialize
    print("\n📡 Test 1: Initialize")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"},
        },
    }

    try:
        result = subprocess.run(
            [python_path, server_path],
            input=json.dumps(init_request) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ Initialize successful")
            print(f"Response: {result.stdout}")
        else:
            print("❌ Initialize failed")
            print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Initialize timeout")
        return False

    # Test 2: List Tools
    print("\n🛠️ Test 2: List Tools")
    list_request = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

    try:
        result = subprocess.run(
            [python_path, server_path],
            input=json.dumps(list_request) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ List tools successful")
            response = result.stdout.strip()
            print(f"Response: {response}")

            # Parse response to check for tools
            try:
                response_data = json.loads(response.split("\n")[-1])
                if "result" in response_data and "tools" in response_data["result"]:
                    tools = response_data["result"]["tools"]
                    print(f"✅ Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool['name']}: {tool['description']}")
                else:
                    print("❌ No tools found in response")
                    return False
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return False
        else:
            print("❌ List tools failed")
            print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ List tools timeout")
        return False

    # Test 3: Call Tool
    print("\n⚡ Test 3: Call Tool")
    call_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "get_current_time", "arguments": {}},
    }

    try:
        result = subprocess.run(
            [python_path, server_path],
            input=json.dumps(call_request) + "\n",
            text=True,
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✅ Call tool successful")
            response = result.stdout.strip()
            print(f"Response: {response}")

            # Parse response to check for result
            try:
                response_data = json.loads(response.split("\n")[-1])
                if "result" in response_data and "content" in response_data["result"]:
                    content = response_data["result"]["content"]
                    print(f"✅ Tool executed successfully")
                    print(f"Content: {content}")
                else:
                    print("❌ No result content found")
                    return False
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
                return False
        else:
            print("❌ Call tool failed")
            print(f"Error: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Call tool timeout")
        return False

    print("\n🎉 All tests passed! MCP server is working correctly.")
    return True


def check_cursor_mcp_config():
    """Check the Cursor MCP configuration"""
    print("\n🔧 Checking Cursor MCP Configuration...")

    mcp_config_path = "/home/mccoy/.cursor/mcp.json"

    if not os.path.exists(mcp_config_path):
        print("❌ MCP config file not found!")
        return False

    try:
        with open(mcp_config_path, "r") as f:
            config = json.load(f)

        print("✅ MCP config file exists and is valid JSON")

        if "mcpServers" in config:
            servers = config["mcpServers"]
            print(f"✅ Found {len(servers)} MCP servers:")

            for server_name, server_config in servers.items():
                print(f"  - {server_name}")
                if "command" in server_config:
                    print(f"    Command: {server_config['command']}")
                if "args" in server_config:
                    print(f"    Args: {server_config['args']}")

            # Check if our server is first (to avoid 5-server limit)
            server_names = list(servers.keys())
            if "basic_mcp_server" in server_names:
                position = server_names.index("basic_mcp_server")
                print(f"✅ basic_mcp_server is at position {position + 1}")
                if position == 0:
                    print("✅ Server is in first position (good for avoiding limits)")
                else:
                    print("⚠️ Server is not in first position (may hit 5-server limit)")
            else:
                print("❌ basic_mcp_server not found in config")
                return False
        else:
            print("❌ No mcpServers section found")
            return False

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in MCP config: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")
        return False

    return True


def main():
    """Main test function"""
    print("🚀 MCP Server Detection Test")
    print("=" * 50)

    # Test 1: Check configuration
    config_ok = check_cursor_mcp_config()

    # Test 2: Test server functionality
    server_ok = test_mcp_server()

    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"Server Functionality: {'✅ PASS' if server_ok else '❌ FAIL'}")

    if config_ok and server_ok:
        print("\n🎉 All tests passed! Your MCP server should be detected by Cursor.")
        print("\n📋 Next Steps:")
        print("1. Restart Cursor completely")
        print("2. Check Settings → MCP Servers")
        print("3. Look for 'basic_mcp_server' with a green dot")
        print("4. Try asking: 'Use get_current_time to get the current time'")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
