#!/usr/bin/env python3
"""
Test script for the new Living Truth Engine UI workflow.
Tests each component systematically before moving to the next.
"""

import requests
import json
import sys
from typing import Dict, Any

API_BASE = "http://localhost:8050"

def test_endpoint(endpoint: str, method: str = "GET", data: Dict = None) -> Dict[str, Any]:
    """Test an API endpoint and return the response."""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e), "status": "fail"}

def test_health():
    """Test health endpoint."""
    print("🔍 Testing health endpoint...")
    result = test_endpoint("/api/health")
    if result.get("status") == "ok":
        print("✅ Health endpoint working")
        return True
    else:
        print(f"❌ Health endpoint failed: {result}")
        return False

def test_runs():
    """Test runs endpoint."""
    print("🔍 Testing runs endpoint...")
    result = test_endpoint("/api/runs")
    if result.get("status") == "ok" and "data" in result:
        runs = result["data"]
        print(f"✅ Runs endpoint working - found {len(runs)} runs")
        if runs:
            print(f"   Latest run: {runs[0]['run_id']}")
            return runs[0]['run_id']
        else:
            print("   No runs found")
            return None
    else:
        print(f"❌ Runs endpoint failed: {result}")
        return None

def test_tools():
    """Test tools endpoint."""
    print("🔍 Testing tools endpoint...")
    result = test_endpoint("/api/tools")
    if result.get("status") == "ok" and "data" in result:
        categories = result["data"].get("categories", {})
        print(f"✅ Tools endpoint working - found {len(categories)} categories")
        return True
    else:
        print(f"❌ Tools endpoint failed: {result}")
        return False

def test_analysis_summary(run_id: str):
    """Test analysis summary endpoint."""
    print(f"🔍 Testing analysis summary for run: {run_id}")
    data = {
        "tool_name": "analyze_veritas_summary",
        "params": {"run_id": run_id}
    }
    result = test_endpoint("/api/execute", method="POST", data=data)
    if result.get("status") == "ok":
        print("✅ Analysis summary working")
        return True
    else:
        print(f"❌ Analysis summary failed: {result}")
        return False

def test_analysis_claims(run_id: str):
    """Test analysis claims endpoint."""
    print(f"🔍 Testing analysis claims for run: {run_id}")
    data = {
        "tool_name": "analyze_veritas_claims",
        "params": {"run_id": run_id}
    }
    result = test_endpoint("/api/execute", method="POST", data=data)
    if result.get("status") == "ok":
        print("✅ Analysis claims working")
        return True
    else:
        print(f"❌ Analysis claims failed: {result}")
        return False

def test_ui_access():
    """Test UI accessibility."""
    print("🔍 Testing UI accessibility...")
    url = f"{API_BASE}/static/ui_status_chat.html"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if "html" in response.text.lower():
            print("✅ UI accessible")
            return True
        else:
            print(f"❌ UI not accessible - no HTML content")
            return False
    except Exception as e:
        print(f"❌ UI not accessible: {e}")
        return False

def main():
    """Run all tests systematically."""
    print("🚀 Starting Living Truth Engine UI Test Suite")
    print("=" * 50)
    
    # Test 1: Health endpoint
    if not test_health():
        print("❌ Health test failed - stopping")
        sys.exit(1)
    
    # Test 2: Tools endpoint
    if not test_tools():
        print("❌ Tools test failed - stopping")
        sys.exit(1)
    
    # Test 3: Runs endpoint
    run_id = test_runs()
    if run_id is None:
        print("⚠️  No runs found - skipping analysis tests")
    else:
        # Test 4: Analysis summary
        if not test_analysis_summary(run_id):
            print("❌ Analysis summary test failed - stopping")
            sys.exit(1)
        
        # Test 5: Analysis claims
        if not test_analysis_claims(run_id):
            print("❌ Analysis claims test failed - stopping")
            sys.exit(1)
    
    # Test 6: UI accessibility
    if not test_ui_access():
        print("❌ UI accessibility test failed - stopping")
        sys.exit(1)
    
    print("=" * 50)
    print("🎉 All tests passed! New UI is ready to use.")
    print(f"📱 Access the UI at: {API_BASE}/static/ui_status_chat.html")
    print("🔧 Click 'Proof-of-Life' to test the complete workflow")

if __name__ == "__main__":
    main()
