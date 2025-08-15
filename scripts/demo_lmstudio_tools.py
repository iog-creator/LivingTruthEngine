#!/usr/bin/env python3
"""
Demo: Show LM Studio calling the tools bridge
"""
import requests
import json
import time
import subprocess
import threading

def start_bridge():
    """Start the tools bridge"""
    print("🚀 Starting LM Studio tools bridge...")
    process = subprocess.Popen(
        ["python", "scripts/bridge/lmstudio_tools_bridge.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)
    return process

def simulate_lmstudio_tool_call():
    """Simulate what happens when LM Studio calls a tool"""
    print("🤖 Simulating LM Studio calling verify_ssot tool...")
    
    # This is what LM Studio would do when you ask "Can you verify the SSOT status?"
    response = requests.post(
        "http://127.0.0.1:8756/tools/verify_ssot",
        json={},
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Tool response: {result}")
        return result
    else:
        print(f"❌ Tool call failed: {response.status_code}")
        return None

def main():
    print("🎬 LM Studio Tools Demo")
    print("=" * 40)
    
    # Start bridge
    bridge_process = start_bridge()
    
    try:
        print("\n📋 What you should see in LM Studio:")
        print("1. You ask: 'Can you verify the SSOT status of the project?'")
        print("2. LM Studio decides to call the verify_ssot tool")
        print("3. LM Studio makes this HTTP request:")
        print("   POST http://127.0.0.1:8756/tools/verify_ssot")
        print("4. You see inference happening in LM Studio logs")
        print("5. LM Studio gets the tool response and continues")
        
        print("\n🔧 Testing the tool call now...")
        result = simulate_lmstudio_tool_call()
        
        if result:
            print(f"\n📊 Tool Response Summary:")
            print(f"   Status: {result.get('status')}")
            print(f"   Output: {result.get('output')}")
            
            print(f"\n🎯 To see this in action:")
            print(f"1. Keep this bridge running: make lm-tools")
            print(f"2. In LM Studio, add the tool definition from LM_STUDIO_SETUP_GUIDE.md")
            print(f"3. Ask: 'Can you verify the SSOT status of the project?'")
            print(f"4. Watch the inference logs show the tool call!")
        
    finally:
        bridge_process.terminate()
        print("\n🧹 Demo complete")

if __name__ == "__main__":
    main()
