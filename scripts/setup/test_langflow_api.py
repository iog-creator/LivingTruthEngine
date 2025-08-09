#!/usr/bin/env python3
"""
Test Langflow API Directly
=========================

Test Langflow API endpoints directly.
"""

import requests
import json
import os
from pathlib import Path

def test_langflow_api():
    """Test Langflow API endpoints."""
    
    # Load environment
    if Path(".env").exists():
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
    
    LANGFLOW_API_ENDPOINT = "http://localhost:7860"
    LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY", "admin")
    
    print(f"🔧 Testing Langflow API")
    print(f"   Endpoint: {LANGFLOW_API_ENDPOINT}")
    print(f"   API Key: {LANGFLOW_API_KEY[:10]}...")
    print("=" * 50)
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": LANGFLOW_API_KEY
    }
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(f"{LANGFLOW_API_ENDPOINT}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
    
    # Test 2: List flows
    print("\n2. Testing list flows...")
    try:
        response = requests.get(f"{LANGFLOW_API_ENDPOINT}/api/v1/flows/", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            flows = response.json()
            print(f"   Found {len(flows)} flows")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ List flows failed: {e}")
    
    # Test 3: Create flow
    print("\n3. Testing create flow...")
    try:
        flow_data = {
            "name": "Test Flow",
            "description": "Test flow for API",
            "data": {
                "nodes": [],
                "edges": []
            }
        }
        response = requests.post(f"{LANGFLOW_API_ENDPOINT}/api/v1/flows/", 
                               json=flow_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Flow created: {result.get('id', 'unknown')}")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Create flow failed: {e}")

if __name__ == "__main__":
    test_langflow_api() 