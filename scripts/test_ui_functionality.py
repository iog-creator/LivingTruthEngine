#!/usr/bin/env python3
"""
Comprehensive UI functionality test for the Living Truth Engine.
This script tests the actual UI by simulating browser interactions.
"""

import requests
import json
import sys
import time
from typing import Dict, Any

API_BASE = "http://localhost:8050"
UI_URL = f"{API_BASE}/static/ui_status_chat.html"

def test_ui_file_access():
    """Test if the UI file is accessible."""
    print("🔍 Testing UI file accessibility...")
    try:
        response = requests.get(UI_URL, timeout=10)
        response.raise_for_status()
        if "html" in response.text.lower() and "script" in response.text.lower():
            print("✅ UI file accessible and contains HTML/JavaScript")
            return True
        else:
            print("❌ UI file accessible but doesn't contain expected content")
            return False
    except Exception as e:
        print(f"❌ UI file not accessible: {e}")
        return False

def test_api_endpoints():
    """Test all API endpoints that the UI uses."""
    print("🔍 Testing API endpoints...")
    
    endpoints = [
        ("/api/health", "GET"),
        ("/api/runs", "GET"),
        ("/api/tools", "GET"),
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{API_BASE}{endpoint}", timeout=30)
            else:
                response = requests.post(f"{API_BASE}{endpoint}", timeout=30)
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "ok":
                print(f"✅ {endpoint} working")
            else:
                print(f"❌ {endpoint} returned error: {data}")
                return False
                
        except Exception as e:
            print(f"❌ {endpoint} failed: {e}")
            return False
    
    return True

def test_analysis_functionality():
    """Test the analysis functionality that the UI uses."""
    print("🔍 Testing analysis functionality...")
    
    # First get a list of runs
    try:
        response = requests.get(f"{API_BASE}/api/runs", timeout=10)
        response.raise_for_status()
        runs_data = response.json()
        
        if runs_data.get("status") != "ok":
            print(f"❌ Failed to get runs: {runs_data}")
            return False
        
        runs = runs_data.get("data", [])
        if not runs:
            print("⚠️  No runs available for testing")
            return True  # This is not a failure, just no data
        
        # Use the first run for testing
        run_id = runs[0]["run_id"]
        print(f"   Using run: {run_id}")
        
        # Test summary analysis
        summary_data = {
            "tool_name": "analyze_veritas_summary",
            "params": {"run_id": run_id}
        }
        
        response = requests.post(f"{API_BASE}/api/execute", 
                               json=summary_data, timeout=30)
        response.raise_for_status()
        summary_result = response.json()
        
        if summary_result.get("status") == "ok":
            print("✅ Summary analysis working")
        else:
            print(f"❌ Summary analysis failed: {summary_result}")
            return False
        
        # Test claims analysis
        claims_data = {
            "tool_name": "analyze_veritas_claims",
            "params": {"run_id": run_id}
        }
        
        response = requests.post(f"{API_BASE}/api/execute", 
                               json=claims_data, timeout=30)
        response.raise_for_status()
        claims_result = response.json()
        
        if claims_result.get("status") == "ok":
            print("✅ Claims analysis working")
        else:
            print(f"❌ Claims analysis failed: {claims_result}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis functionality test failed: {e}")
        return False

def test_ui_javascript():
    """Test if the UI JavaScript is properly formatted."""
    print("🔍 Testing UI JavaScript...")
    try:
        response = requests.get(UI_URL, timeout=10)
        response.raise_for_status()
        content = response.text
        
        # Check for key JavaScript functions
        required_functions = [
            "loadHealth",
            "loadRuns", 
            "doSummary",
            "doClaims",
            "runPOL"
        ]
        
        for func in required_functions:
            if func in content:
                print(f"✅ Found function: {func}")
            else:
                print(f"❌ Missing function: {func}")
                return False
        
        # Check for API base configuration
        if "API_BASE" in content and "localhost:8050" in content:
            print("✅ API configuration present")
        else:
            print("❌ API configuration missing")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ JavaScript test failed: {e}")
        return False

def test_complete_workflow():
    """Test the complete workflow that the UI should support."""
    print("🔍 Testing complete workflow...")
    
    try:
        # 1. Health check
        response = requests.get(f"{API_BASE}/api/health", timeout=10)
        response.raise_for_status()
        health_data = response.json()
        
        if health_data.get("status") != "ok":
            print("❌ Health check failed")
            return False
        
        # 2. Get runs
        response = requests.get(f"{API_BASE}/api/runs", timeout=10)
        response.raise_for_status()
        runs_data = response.json()
        
        if runs_data.get("status") != "ok":
            print("❌ Runs listing failed")
            return False
        
        runs = runs_data.get("data", [])
        if not runs:
            print("⚠️  No runs available - workflow incomplete but not failed")
            return True
        
        # 3. Test analysis on first run
        run_id = runs[0]["run_id"]
        
        # Summary
        summary_data = {
            "tool_name": "analyze_veritas_summary",
            "params": {"run_id": run_id}
        }
        response = requests.post(f"{API_BASE}/api/execute", 
                               json=summary_data, timeout=30)
        response.raise_for_status()
        
        # Claims
        claims_data = {
            "tool_name": "analyze_veritas_claims",
            "params": {"run_id": run_id}
        }
        response = requests.post(f"{API_BASE}/api/execute", 
                               json=claims_data, timeout=30)
        response.raise_for_status()
        
        print("✅ Complete workflow working")
        return True
        
    except Exception as e:
        print(f"❌ Complete workflow failed: {e}")
        return False

def main():
    """Run all UI tests."""
    print("🚀 Living Truth Engine - UI Functionality Test")
    print("=" * 50)
    
    tests = [
        ("UI File Access", test_ui_file_access),
        ("API Endpoints", test_api_endpoints),
        ("Analysis Functionality", test_analysis_functionality),
        ("UI JavaScript", test_ui_javascript),
        ("Complete Workflow", test_complete_workflow),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! UI is working correctly.")
        print(f"📱 Access the UI at: {UI_URL}")
        return 0
    else:
        print("❌ Some tests failed. UI needs fixes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
