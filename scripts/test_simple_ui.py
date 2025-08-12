#!/usr/bin/env python3
"""
Simple test for the new simplified UI.
"""

import requests
import json

API_BASE = "http://localhost:8050"
UI_URL = f"{API_BASE}/static/ui_status_chat.html"

def test_simple_ui():
    """Test the simplified UI."""
    print("🧪 Testing Simplified UI")
    print("=" * 30)
    
    # Test 1: UI loads
    print("1. Testing UI load...")
    try:
        response = requests.get(UI_URL, timeout=10)
        response.raise_for_status()
        if "Simple UI" in response.text:
            print("   ✅ UI loads correctly")
        else:
            print("   ❌ UI content not as expected")
            return False
    except Exception as e:
        print(f"   ❌ UI load failed: {e}")
        return False
    
    # Test 2: Health endpoint
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {data}")
            return False
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
        return False
    
    # Test 3: Runs endpoint
    print("3. Testing runs endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/runs", timeout=30)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "ok":
            runs = data.get("data", [])
            print(f"   ✅ Runs endpoint working - {len(runs)} runs found")
        else:
            print(f"   ❌ Runs endpoint failed: {data}")
            return False
    except Exception as e:
        print(f"   ❌ Runs endpoint error: {e}")
        return False
    
    # Test 4: Analysis endpoints (if runs available)
    if data.get("data"):
        run_id = data["data"][0]["run_id"]
        print(f"4. Testing analysis with run: {run_id}")
        
        # Test summary
        try:
            summary_data = {
                "tool_name": "analyze_veritas_summary",
                "params": {"run_id": run_id}
            }
            response = requests.post(f"{API_BASE}/api/execute", 
                                   json=summary_data, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("status") == "ok":
                print("   ✅ Summary analysis working")
            else:
                print(f"   ❌ Summary analysis failed: {result}")
                return False
        except Exception as e:
            print(f"   ❌ Summary analysis error: {e}")
            return False
        
        # Test claims
        try:
            claims_data = {
                "tool_name": "analyze_veritas_claims",
                "params": {"run_id": run_id}
            }
            response = requests.post(f"{API_BASE}/api/execute", 
                                   json=claims_data, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("status") == "ok":
                print("   ✅ Claims analysis working")
            else:
                print(f"   ❌ Claims analysis failed: {result}")
                return False
        except Exception as e:
            print(f"   ❌ Claims analysis error: {e}")
            return False
    
    print("\n🎉 Simplified UI test completed successfully!")
    print(f"📱 Access the UI at: {UI_URL}")
    print("\n📋 How to use:")
    print("1. Open the URL in your browser")
    print("2. Click 'Test Connection' to verify API")
    print("3. Select a run from the dropdown")
    print("4. Click 'Get Summary' or 'Get Claims'")
    print("5. View results in the output panel")
    
    return True

if __name__ == "__main__":
    success = test_simple_ui()
    if not success:
        print("\n❌ Simplified UI test failed!")
        exit(1)



