#!/usr/bin/env python3
"""
Test LM Studio Plugin Installation
"""
import subprocess
import json
import time
import os

def test_plugin_installation():
    """Test that the plugin is properly installed"""
    print("🔍 Testing LM Studio plugin installation...")
    
    plugin_path = "/home/mccoy/.lmstudio/extensions/plugins/lmstudio-mcp-tools"
    
    # Check if plugin directory exists
    if not os.path.exists(plugin_path):
        print(f"❌ Plugin not found at {plugin_path}")
        return False
    
    # Check required files
    required_files = [
        "manifest.json",
        "package.json", 
        "dist/index.js",
        "dist/toolsProvider.js"
    ]
    
    missing = []
    for file in required_files:
        full_path = os.path.join(plugin_path, file)
        if not os.path.exists(full_path):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    
    print("✅ Plugin is properly installed")
    return True

def test_mcp_server():
    """Test that the MCP server is running"""
    print("🔍 Testing MCP server...")
    
    try:
        # Test if MCP server is responding
        result = subprocess.run(
            ["pgrep", "-f", "phase9_mcp_server.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ MCP server is running")
            return True
        else:
            print("❌ MCP server is not running")
            return False
    except Exception as e:
        print(f"❌ Error checking MCP server: {e}")
        return False

def main():
    print("🧪 LM Studio Plugin Installation Test")
    print("=" * 50)
    
    plugin_ok = test_plugin_installation()
    mcp_ok = test_mcp_server()
    
    print("\n📊 Test Results:")
    print(f"Plugin Installation: {'✅ PASS' if plugin_ok else '❌ FAIL'}")
    print(f"MCP Server: {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    
    if plugin_ok and mcp_ok:
        print("\n🎉 Everything is ready!")
        print("\n📋 Next steps:")
        print("1. Restart LM Studio")
        print("2. Ask: 'Can you validate the cursor rules?'")
        print("3. Watch developer logs for inference!")
        print("\n💡 The plugin should now be available in LM Studio")
    else:
        print("\n🚨 Some components need attention")
        if not mcp_ok:
            print("   - Start MCP server: make lm-mcp")

if __name__ == "__main__":
    main()
