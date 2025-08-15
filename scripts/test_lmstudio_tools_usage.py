#!/usr/bin/env python3
"""
Test that simulates LM Studio calling the tools bridge
"""
import requests
import json
import time
import subprocess
import threading

def start_bridge():
    """Start the tools bridge in background"""
    print("🚀 Starting LM Studio tools bridge...")
    process = subprocess.Popen(
        ["python", "scripts/bridge/lmstudio_tools_bridge.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(3)  # Wait for startup
    return process

def test_tools_calls():
    """Simulate LM Studio calling the tools"""
    print("🔧 Testing tools bridge endpoints...")
    
    # Test 1: verify_ssot
    print("\n1️⃣ Testing verify_ssot...")
    start_time = time.time()
    response = requests.post(
        "http://127.0.0.1:8756/tools/verify_ssot",
        json={},
        timeout=60
    )
    end_time = time.time()
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ verify_ssot: {end_time - start_time:.2f}s")
        print(f"   Status: {result.get('status')}")
        print(f"   Output preview: {result.get('output', '')[:100]}...")
    else:
        print(f"❌ verify_ssot failed: {response.status_code}")
    
    # Test 2: read_ssot_report
    print("\n2️⃣ Testing read_ssot_report...")
    response = requests.post(
        "http://127.0.0.1:8756/tools/read_ssot_report",
        json={},
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ read_ssot_report: {result.get('status')}")
        print(f"   Data keys: {list(result.get('data', {}).keys())}")
    else:
        print(f"❌ read_ssot_report failed: {response.status_code}")
    
    # Test 3: draft_patches
    print("\n3️⃣ Testing draft_patches...")
    response = requests.post(
        "http://127.0.0.1:8756/tools/draft_patches",
        json={},
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ draft_patches: {result.get('status')}")
        suggestions = result.get('suggestions', [])
        print(f"   Suggestions: {len(suggestions)}")
        for suggestion in suggestions:
            print(f"   - {suggestion.get('file')}: {suggestion.get('rationale')}")
    else:
        print(f"❌ draft_patches failed: {response.status_code}")

def main():
    print("🧪 LM Studio Tools Usage Test")
    print("=" * 40)
    
    # Start bridge
    bridge_process = start_bridge()
    
    try:
        # Test tools
        test_tools_calls()
        
        print("\n🎯 Next Steps:")
        print("1. In LM Studio, go to Settings → Tools")
        print("2. Add these tool definitions:")
        print("""
{
  "name": "verify_ssot",
  "description": "Run comprehensive SSOT validation check",
  "url": "http://127.0.0.1:8756/tools/verify_ssot",
  "method": "POST",
  "headers": {"Content-Type": "application/json"},
  "body": "{}"
}
        """)
        print("3. Ask LM Studio: 'Can you verify the SSOT status of the project?'")
        print("4. Watch LM Studio call the tools and show inference!")
        
    finally:
        # Cleanup
        bridge_process.terminate()
        print("\n🧹 Bridge stopped")

if __name__ == "__main__":
    main()
