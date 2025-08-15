#!/usr/bin/env python3
"""
Simple test to verify LM Studio integration is working
"""
import requests
import json
import time

def test_lmstudio_direct():
    """Test direct LM Studio inference"""
    print("🤖 Testing direct LM Studio inference...")
    
    try:
        # Test LM Studio is running
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            print("✅ LM Studio is running")
        else:
            print(f"❌ LM Studio responded with {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ LM Studio not reachable: {e}")
        return False
    
    # Test actual inference
    try:
        payload = {
            "model": "llama-3.2-3b-instruct",
            "messages": [
                {"role": "user", "content": "Say 'Hello from LM Studio!' and nothing else."}
            ],
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        print("🔄 Sending inference request...")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=30
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ LM Studio inference successful!")
            print(f"⏱️  Time: {end_time - start_time:.2f}s")
            print(f"🤖 Response: {content}")
            return True
        else:
            print(f"❌ Inference failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Inference error: {e}")
        return False

def test_tools_bridge():
    """Test the tools bridge"""
    print("\n🔧 Testing tools bridge...")
    
    try:
        # Start bridge in background
        import subprocess
        import time
        
        print("🚀 Starting tools bridge...")
        bridge_process = subprocess.Popen(
            ["python", "scripts/bridge/lmstudio_tools_bridge.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        time.sleep(3)  # Wait for startup
        
        # Test bridge endpoint
        response = requests.post(
            "http://127.0.0.1:8756/tools/read_ssot_report",
            json={},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Tools bridge is working")
            bridge_process.terminate()
            return True
        else:
            print(f"❌ Tools bridge failed: {response.status_code}")
            bridge_process.terminate()
            return False
            
    except Exception as e:
        print(f"❌ Tools bridge error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 LM Studio Integration Test")
    print("=" * 40)
    
    # Test 1: Direct LM Studio
    lmstudio_ok = test_lmstudio_direct()
    
    # Test 2: Tools bridge
    bridge_ok = test_tools_bridge()
    
    print("\n📊 Test Results:")
    print(f"LM Studio Direct: {'✅ PASS' if lmstudio_ok else '❌ FAIL'}")
    print(f"Tools Bridge:     {'✅ PASS' if bridge_ok else '❌ FAIL'}")
    
    if lmstudio_ok and bridge_ok:
        print("\n🎉 All tests passed! LM Studio integration is working.")
    else:
        print("\n🚨 Some tests failed. Check LM Studio is running on localhost:1234")
