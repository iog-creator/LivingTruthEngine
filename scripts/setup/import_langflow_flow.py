#!/usr/bin/env python3
"""
Import Langflow Flow Script
==========================

This script imports the Living Truth Engine flow into Langflow via API.
"""

import json
import os
from pathlib import Path

import requests


def import_langflow_flow():
    """Import the Living Truth Engine flow into Langflow."""

    # Load environment
    if Path(".env").exists():
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

    # Configuration
    LANGFLOW_API_ENDPOINT = "http://localhost:7860"
    LANGFLOW_API_KEY = os.getenv("LANGFLOW_API_KEY", "admin")
    FLOW_FILE = (
        Path(__file__).parent.parent.parent / "flows" / "living_truth_engine_flow.json"
    )

    print(f"🔄 Importing Langflow flow from: {FLOW_FILE}")

    # Check if flow file exists
    if not FLOW_FILE.exists():
        print(f"❌ Flow file not found: {FLOW_FILE}")
        return False

    # Load flow JSON
    try:
        with open(FLOW_FILE, "r") as f:
            flow_config = json.load(f)
        print("✅ Flow JSON loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load flow JSON: {e}")
        return False

    # Prepare API request
    headers = {"Content-Type": "application/json", "x-api-key": LANGFLOW_API_KEY}

    # Import flow via API
    try:
        response = requests.post(
            f"{LANGFLOW_API_ENDPOINT}/api/v1/flows/", json=flow_config, headers=headers
        )

        if response.status_code in [200, 201]:
            result = response.json()
            flow_id = result.get("id")
            flow_name = result.get("name", "Living Truth Engine Flow")
            print(f"✅ Flow imported successfully!")
            print(f"📋 Flow ID: {flow_id}")
            print(f"📋 Flow Name: {flow_name}")
            print(f"🌐 Access at: {LANGFLOW_API_ENDPOINT}/flows/{flow_id}")
            return True
        else:
            print(f"❌ Failed to import flow: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ API request failed: {e}")
        return False


def test_langflow_connection():
    """Test connection to Langflow."""
    try:
        response = requests.get("http://localhost:7860/health")
        if response.status_code == 200:
            print("✅ Langflow connection successful")
            return True
        else:
            print(f"❌ Langflow health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Langflow connection failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Living Truth Engine - Langflow Flow Import")
    print("=" * 50)

    # Test connection
    if not test_langflow_connection():
        print("❌ Cannot connect to Langflow. Please ensure it's running on port 7860.")
        exit(1)

    # Import flow
    if import_langflow_flow():
        print("\n🎉 Flow import completed successfully!")
        print("📝 Next steps:")
        print("   1. Access Langflow UI: http://localhost:7860")
        print("   2. Login with: admin/admin")
        print("   3. Find your imported flow in the flows list")
        print(
            "   4. Test with query: 'Investigate Entity A connections, output as network'"
        )
    else:
        print("\n❌ Flow import failed. Check the logs above.")
        exit(1)
