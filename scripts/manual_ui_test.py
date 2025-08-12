#!/usr/bin/env python3
"""
Manual UI test that simulates actual browser interactions.
This tests the UI as a user would actually use it.
"""

import requests
import json
import time

API_BASE = "http://localhost:8050"
UI_URL = f"{API_BASE}/static/ui_status_chat.html"

def simulate_ui_workflow():
    """Simulate a complete UI workflow as a user would experience it."""
    print("🧪 Manual UI Workflow Test")
    print("=" * 40)
    
    # Step 1: Load the UI
    print("1. Loading UI...")
    try:
        response = requests.get(UI_URL, timeout=10)
        response.raise_for_status()
        print("   ✅ UI loaded successfully")
    except Exception as e:
        print(f"   ❌ Failed to load UI: {e}")
        return False
    
    # Step 2: Test health endpoint (what UI calls first)
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=10)
        response.raise_for_status()
        health_data = response.json()
        if health_data.get("status") == "ok":
            print("   ✅ Health endpoint working")
        else:
            print(f"   ❌ Health endpoint failed: {health_data}")
            return False
    except Exception as e:
        print(f"   ❌ Health endpoint error: {e}")
        return False
    
    # Step 3: Test runs endpoint (what UI calls next)
    print("3. Testing runs endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/runs", timeout=30)
        response.raise_for_status()
        runs_data = response.json()
        if runs_data.get("status") == "ok":
            runs = runs_data.get("data", [])
            print(f"   ✅ Runs endpoint working - found {len(runs)} runs")
            if runs:
                print(f"   📋 Latest run: {runs[0]['run_id']}")
            else:
                print("   ⚠️  No runs available")
        else:
            print(f"   ❌ Runs endpoint failed: {runs_data}")
            return False
    except Exception as e:
        print(f"   ❌ Runs endpoint error: {e}")
        return False
    
    # Step 4: Test tools endpoint
    print("4. Testing tools endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/tools", timeout=10)
        response.raise_for_status()
        tools_data = response.json()
        if tools_data.get("status") == "ok":
            categories = tools_data.get("data", {}).get("categories", {})
            print(f"   ✅ Tools endpoint working - found {len(categories)} categories")
        else:
            print(f"   ❌ Tools endpoint failed: {tools_data}")
            return False
    except Exception as e:
        print(f"   ❌ Tools endpoint error: {e}")
        return False
    
    # Step 5: Test analysis functionality (if runs available)
    if runs_data.get("data"):
        run_id = runs_data["data"][0]["run_id"]
        print(f"5. Testing analysis with run: {run_id}")
        
        # Test summary analysis
        print("   a. Testing summary analysis...")
        try:
            summary_data = {
                "tool_name": "analyze_veritas_summary",
                "params": {"run_id": run_id}
            }
            response = requests.post(f"{API_BASE}/api/execute", 
                                   json=summary_data, timeout=30)
            response.raise_for_status()
            summary_result = response.json()
            if summary_result.get("status") == "ok":
                print("      ✅ Summary analysis working")
            else:
                print(f"      ❌ Summary analysis failed: {summary_result}")
                return False
        except Exception as e:
            print(f"      ❌ Summary analysis error: {e}")
            return False
        
        # Test claims analysis
        print("   b. Testing claims analysis...")
        try:
            claims_data = {
                "tool_name": "analyze_veritas_claims",
                "params": {"run_id": run_id}
            }
            response = requests.post(f"{API_BASE}/api/execute", 
                                   json=claims_data, timeout=30)
            response.raise_for_status()
            claims_result = response.json()
            if claims_result.get("status") == "ok":
                print("      ✅ Claims analysis working")
            else:
                print(f"      ❌ Claims analysis failed: {claims_result}")
                return False
        except Exception as e:
            print(f"      ❌ Claims analysis error: {e}")
            return False
    
    print("\n🎉 Manual UI test completed successfully!")
    print(f"📱 The UI is ready to use at: {UI_URL}")
    print("\n📋 How to use the UI:")
    print("1. Open the URL in your browser")
    print("2. Click 'Proof-of-Life' to test everything")
    print("3. Select a run from the dropdown")
    print("4. Use 'Get Summary' or 'Get Claims' buttons")
    print("5. View results in the right panel")
    
    return True

if __name__ == "__main__":
    success = simulate_ui_workflow()
    if not success:
        print("\n❌ Manual UI test failed!")
        exit(1)



