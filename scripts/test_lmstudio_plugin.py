#!/usr/bin/env python3
"""
Test LM Studio Plugin Integration
"""
import subprocess
import json
import time

def test_plugin_build():
    """Test that the plugin builds correctly"""
    print("🔨 Testing LM Studio plugin build...")
    try:
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd="lmstudio-mcp-tools",
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Plugin builds successfully")
            return True
        else:
            print(f"❌ Plugin build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Plugin build error: {e}")
        return False

def test_plugin_structure():
    """Test that the plugin has the correct structure"""
    print("📁 Testing plugin structure...")
    required_files = [
        "lmstudio-mcp-tools/manifest.json",
        "lmstudio-mcp-tools/package.json",
        "lmstudio-mcp-tools/dist/index.js",
        "lmstudio-mcp-tools/dist/toolsProvider.js"
    ]
    
    missing = []
    for file in required_files:
        try:
            with open(file, 'r') as f:
                pass  # File exists
        except FileNotFoundError:
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    else:
        print("✅ Plugin structure is correct")
        return True

def main():
    print("🧪 LM Studio Plugin Test")
    print("=" * 40)
    
    build_ok = test_plugin_build()
    structure_ok = test_plugin_structure()
    
    print("\n📊 Test Results:")
    print(f"Plugin Build: {'✅ PASS' if build_ok else '❌ FAIL'}")
    print(f"Plugin Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    
    if build_ok and structure_ok:
        print("\n🎉 Plugin is ready!")
        print("\n📋 Next steps:")
        print("1. Copy lmstudio-mcp-tools to LM Studio plugins directory")
        print("2. Restart LM Studio")
        print("3. Ask: 'Can you validate the cursor rules?'")
        print("4. Watch developer logs for inference!")
    else:
        print("\n🚨 Plugin needs fixes before use")

if __name__ == "__main__":
    main()
