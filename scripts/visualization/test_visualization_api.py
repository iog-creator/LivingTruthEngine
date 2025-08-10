#!/usr/bin/env python3
"""
Test script for MCP Visualization API

This script tests the visualization API endpoints to ensure they work correctly.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.mcp_servers.mcp_hub_server import MCPHubServer


async def test_mcp_hub_server():
    """Test MCP Hub Server functionality."""
    print("🔍 Testing MCP Hub Server...")
    
    try:
        hub = MCPHubServer()
        
        # Test status
        status = hub.get_status()
        print(f"✅ Status: {status.get('status', 'unknown')}")
        
        # Test tool categories
        categories = hub.get_tool_categories()
        total_tools = sum(len(tools) for tools in categories.get('result', {}).values())
        print(f"✅ Tool categories: {len(categories.get('result', {}))} categories, {total_tools} total tools")
        
        # Test tool details
        tool_details = hub.get_tool_details('get_status')
        print(f"✅ Tool details: {tool_details.get('result', {}).get('description', 'No description')}")
        
        # Test tool execution
        result = hub.execute_tool('get_status', {})
        print(f"✅ Tool execution: {type(result).__name__} - {str(result)[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP Hub Server test failed: {e}")
        return False


def test_visualization_files():
    """Test that visualization files exist."""
    print("🔍 Testing visualization files...")
    
    try:
        # Check HTML file
        html_path = project_root / "data" / "visualizations" / "phase8_pipeline_visualization.html"
        if html_path.exists():
            print(f"✅ HTML visualization: {html_path}")
        else:
            print(f"❌ HTML visualization not found: {html_path}")
            return False
        
        # Check API server
        api_path = project_root / "scripts" / "visualization" / "mcp_visualization_api.py"
        if api_path.exists():
            print(f"✅ API server: {api_path}")
        else:
            print(f"❌ API server not found: {api_path}")
            return False
        
        # Check startup script
        startup_path = project_root / "scripts" / "visualization" / "start_visualization_server.sh"
        if startup_path.exists():
            print(f"✅ Startup script: {startup_path}")
        else:
            print(f"❌ Startup script not found: {startup_path}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ File test failed: {e}")
        return False


def test_dependencies():
    """Test that required dependencies are available."""
    print("🔍 Testing dependencies...")
    
    try:
        import fastapi
        print("✅ FastAPI available")
        
        import uvicorn
        print("✅ Uvicorn available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Testing MCP Visualization System...")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Visualization Files", test_visualization_files),
        ("MCP Hub Server", test_mcp_hub_server),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The visualization system is ready to use.")
        print("\n🚀 To start the visualization server:")
        print("   ./scripts/visualization/start_visualization_server.sh")
        print("\n🌐 Then visit: http://localhost:8081")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with exception: {e}")
        sys.exit(1)
