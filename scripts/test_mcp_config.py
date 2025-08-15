#!/usr/bin/env python3
"""
Test MCP Configuration
"""
import json
import subprocess
import time
import os

def test_mcp_config():
    """Test that the MCP configuration is correct"""
    print("🔍 Testing MCP configuration...")
    
    config_path = os.path.expanduser("~/.lmstudio/mcp.json")
    
    if not os.path.exists(config_path):
        print(f"❌ MCP config not found at {config_path}")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        if "mcpServers" not in config:
            print("❌ No mcpServers section found")
            return False
        
        if "living-truth-engine" not in config["mcpServers"]:
            print("❌ living-truth-engine server not configured")
            return False
        
        server_config = config["mcpServers"]["living-truth-engine"]
        required_fields = ["command", "args", "cwd"]
        
        missing = []
        for field in required_fields:
            if field not in server_config:
                missing.append(field)
        
        if missing:
            print(f"❌ Missing fields: {missing}")
            return False
        
        print("✅ MCP configuration is correct")
        print(f"   Command: {server_config['command']}")
        print(f"   Args: {server_config['args']}")
        print(f"   CWD: {server_config['cwd']}")
        return True
        
    except Exception as e:
        print(f"❌ Error reading MCP config: {e}")
        return False

def test_mcp_server_connection():
    """Test that the MCP server can be reached"""
    print("🔍 Testing MCP server connection...")
    
    try:
        # Test if the MCP server process is running
        result = subprocess.run(
            ["pgrep", "-f", "phase9_mcp_server.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ MCP server process is running")
            return True
        else:
            print("❌ MCP server process is not running")
            return False
            
    except Exception as e:
        print(f"❌ Error checking MCP server: {e}")
        return False

def main():
    print("🧪 MCP Configuration Test")
    print("=" * 40)
    
    config_ok = test_mcp_config()
    server_ok = test_mcp_server_connection()
    
    print("\n📊 Test Results:")
    print(f"MCP Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"MCP Server: {'✅ PASS' if server_ok else '❌ FAIL'}")
    
    if config_ok and server_ok:
        print("\n🎉 MCP is ready!")
        print("\n📋 Next steps:")
        print("1. Restart LM Studio")
        print("2. Ask: 'Can you validate the cursor rules?'")
        print("3. Watch developer logs for inference!")
        print("\n💡 The MCP server should now be available in LM Studio")
    else:
        print("\n🚨 Some components need attention")
        if not server_ok:
            print("   - Start MCP server: make lm-mcp")

if __name__ == "__main__":
    main()
