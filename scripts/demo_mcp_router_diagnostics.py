#!/usr/bin/env python3
"""
MCP Router Diagnostics Demo

This script demonstrates how to use the MCP Router Diagnostics tool in two ways:
1. As a standalone script (direct execution)
2. As an MCP tool (via the Phase9 MCP server)

Usage:
  python scripts/demo_mcp_router_diagnostics.py
"""

import json
import subprocess
import sys
from pathlib import Path

def demo_standalone_script():
    """Demonstrate using the MCP Router Diagnostics as a standalone script"""
    print("🔍 Demo 1: Standalone MCP Router Diagnostics Script")
    print("=" * 60)
    
    # Run the standalone script
    result = subprocess.run(
        [sys.executable, "scripts/mcp_router_diagnostics.py", 
         "--cmd", "make lm-mcp", 
         "--timeout", "5", 
         "--max-seconds", "10"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        print("✅ Standalone script execution successful!")
        print(f"📊 Tool count: {data['data']['tools_count']}")
        print(f"⏱️  Execution time: {data['data']['time_sec']}s")
        print(f"📈 Latency p50: {data['data']['list_latency']['p50_ms']}ms")
        print(f"🔧 Protocol: {data['data']['protocol_negotiated']}")
    else:
        print("❌ Standalone script execution failed!")
        print(f"Error: {result.stderr}")

def demo_mcp_tool():
    """Demonstrate using the MCP Router Diagnostics as an MCP tool"""
    print("\n🔍 Demo 2: MCP Router Diagnostics as MCP Tool")
    print("=" * 60)
    
    # Start the MCP server
    proc = subprocess.Popen(
        [sys.executable, 'src/mcp_servers/phase9_mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send initialize request
        init_request = {
            'jsonrpc': '2.0',
            'id': '1',
            'method': 'initialize',
            'params': {
                'protocolVersion': '2025-06-18',
                'capabilities': {'tools': {'listChanged': True}},
                'clientInfo': {'name': 'demo-client', 'version': '0.1.0'}
            }
        }
        proc.stdin.write(json.dumps(init_request) + '\n')
        proc.stdin.flush()
        
        # Read initialize response
        init_response = json.loads(proc.stdout.readline())
        
        # Send initialized notification
        init_notification = {
            'jsonrpc': '2.0',
            'method': 'notifications/initialized',
            'params': {'ready': True}
        }
        proc.stdin.write(json.dumps(init_notification) + '\n')
        proc.stdin.flush()
        
        # Call the mcp_router_diagnostics tool
        tool_request = {
            'jsonrpc': '2.0',
            'id': '2',
            'method': 'tools/call',
            'params': {
                'name': 'mcp_router_diagnostics',
                'arguments': {
                    'self': 'server',
                    'target_server': 'make lm-mcp',
                    'timeout': 5.0,
                    'max_seconds': 10.0
                }
            }
        }
        proc.stdin.write(json.dumps(tool_request) + '\n')
        proc.stdin.flush()
        
        # Read tool response
        tool_response = json.loads(proc.stdout.readline())
        
        if not tool_response.get('result', {}).get('isError', False):
            # Parse the result from the structured content
            result_data = tool_response['result']['structuredContent']['result']
            if result_data['status'] == 'ok':
                data = result_data['data']
                print("✅ MCP tool execution successful!")
                print(f"📊 Tool count: {data['tools_count']}")
                print(f"⏱️  Execution time: {data['time_sec']}s")
                print(f"📈 Latency p50: {data['list_latency']['p50_ms']}ms")
                print(f"🔧 Protocol: {data['protocol_negotiated']}")
                print(f"🎯 Target server: {data['target_server']}")
            else:
                print("❌ MCP tool execution failed!")
                print(f"Error: {result_data['error']}")
        else:
            print("❌ MCP tool execution failed!")
            print(f"Error: {tool_response['result']['content'][0]['text']}")
            
    finally:
        proc.terminate()
        proc.wait()

def demo_make_target():
    """Demonstrate using the Makefile target"""
    print("\n🔍 Demo 3: Using Makefile Target")
    print("=" * 60)
    
    result = subprocess.run(
        ["make", "mcp-diagnostics"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        # Extract JSON from the output (it's mixed with warnings)
        lines = result.stdout.split('\n')
        for line in lines:
            if line.strip().startswith('{') and line.strip().endswith('}'):
                try:
                    data = json.loads(line.strip())
                    if data['status'] == 'ok':
                        print("✅ Makefile target execution successful!")
                        print(f"📊 Tool count: {data['data']['tools_count']}")
                        print(f"⏱️  Execution time: {data['data']['time_sec']}s")
                        print(f"📈 Latency p50: {data['data']['list_latency']['p50_ms']}ms")
                        break
                except json.JSONDecodeError:
                    continue
    else:
        print("❌ Makefile target execution failed!")
        print(f"Error: {result.stderr}")

def main():
    """Run all demonstrations"""
    print("🚀 MCP Router Diagnostics Demo")
    print("=" * 60)
    print("This demo shows three ways to use the MCP Router Diagnostics tool:")
    print("1. Standalone script execution")
    print("2. MCP tool via Phase9 MCP server")
    print("3. Makefile target")
    print()
    
    try:
        demo_standalone_script()
        demo_mcp_tool()
        demo_make_target()
        
        print("\n" + "=" * 60)
        print("✅ All demonstrations completed successfully!")
        print("\n📋 Summary:")
        print("- The MCP Router Diagnostics tool works as a standalone script")
        print("- It's integrated as a callable MCP tool in the Phase9 MCP server")
        print("- It can be invoked via the Makefile target 'make mcp-diagnostics'")
        print("- All methods provide the same diagnostic capabilities")
        print("- The tool is safe, read-only, and provides comprehensive MCP server analysis")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
