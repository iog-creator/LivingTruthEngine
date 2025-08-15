#!/usr/bin/env python3
"""Test script to verify LM Studio plugin installation after upgrade."""

import os
import subprocess
import json
from pathlib import Path

def test_plugin_installation():
    """Test if the plugin is properly installed."""
    print("🔍 Testing LM Studio plugin installation after upgrade...")
    
    # Check plugin directory
    plugin_dir = Path("/home/mccoy/.lmstudio/extensions/plugins/lmstudio-mcp-tools")
    if not plugin_dir.exists():
        print("❌ Plugin directory not found")
        return False
    
    print(f"✅ Plugin directory found: {plugin_dir}")
    
    # Check required files
    required_files = ["manifest.json", "package.json", "dist/index.js"]
    for file in required_files:
        file_path = plugin_dir / file
        if not file_path.exists():
            print(f"❌ Required file missing: {file}")
            return False
        print(f"✅ Found: {file}")
    
    # Check manifest.json
    try:
        with open(plugin_dir / "manifest.json") as f:
            manifest = json.load(f)
        print(f"✅ Manifest: {manifest}")
    except Exception as e:
        print(f"❌ Failed to read manifest.json: {e}")
        return False
    
    return True

def test_http_bridge():
    """Test if the HTTP bridge is running."""
    print("\n🔍 Testing HTTP bridge...")
    
    try:
        import requests
        response = requests.post(
            "http://127.0.0.1:8756/tools/verify_ssot",
            headers={"Content-Type": "application/json"},
            json={},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ HTTP bridge is responding")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ HTTP bridge returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ HTTP bridge test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 LM Studio Plugin Post-Upgrade Test")
    print("=" * 50)
    
    plugin_ok = test_plugin_installation()
    bridge_ok = test_http_bridge()
    
    print("\n" + "=" * 50)
    if plugin_ok and bridge_ok:
        print("✅ All tests passed! Plugin should work in LM Studio.")
        print("\n📋 Next steps:")
        print("1. Restart LM Studio")
        print("2. Ask: 'Can you validate the cursor rules?'")
        print("3. Watch developer logs for inference")
    else:
        print("❌ Some tests failed. Check the output above.")
    
    return plugin_ok and bridge_ok

if __name__ == "__main__":
    main()
