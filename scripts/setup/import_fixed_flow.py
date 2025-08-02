#!/usr/bin/env python3
"""
Import Fixed Flowise Flow Script

This script imports the fixed Living Truth Engine Flowise flow
and replaces the existing broken flow with a properly configured version.
"""

import json
import requests
import os
import sys
from pathlib import Path

def import_flowise_flow():
    """Import the fixed Flowise flow."""
    
    # Configuration
    FLOWISE_URL = "http://localhost:3000"
    API_KEY = os.getenv("FLOWISE_API_KEY", "")
    
    # Paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    flow_file = project_root / "LivingTruthFlowise_Fixed.json"
    
    if not flow_file.exists():
        print(f"❌ Flow file not found: {flow_file}")
        return False
    
    try:
        # Load the fixed flow
        with open(flow_file, 'r') as f:
            flow_data = json.load(f)
        
        print("📋 Loaded fixed flow configuration")
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json"
        }
        
        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"
        
        # Import the flow
        import_url = f"{FLOWISE_URL}/api/v1/chatflows"
        
        response = requests.post(
            import_url,
            headers=headers,
            json=flow_data,
            timeout=30
        )
        
        if response.status_code == 201:
            print("✅ Successfully imported fixed flow")
            flow_id = response.json().get("id")
            print(f"📝 Flow ID: {flow_id}")
            print(f"🌐 Access at: {FLOWISE_URL}/chatflows/{flow_id}")
            return True
        else:
            print(f"❌ Failed to import flow: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing flow: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Living Truth Engine - Flowise Flow Import")
    print("=" * 50)
    
    # Check if Flowise is running
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code != 200:
            print("❌ Flowise is not running on localhost:3000")
            print("💡 Start Flowise first with: ./scripts/setup/start_services.sh")
            return False
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Flowise on localhost:3000")
        print("💡 Start Flowise first with: ./scripts/setup/start_services.sh")
        return False
    
    print("✅ Flowise is running")
    
    # Import the flow
    success = import_flowise_flow()
    
    if success:
        print("\n🎉 Flow import completed successfully!")
        print("\n📋 Next steps:")
        print("1. Open Flowise at http://localhost:3000")
        print("2. Navigate to the imported flow")
        print("3. Configure any missing credentials")
        print("4. Test the flow with a research query")
    else:
        print("\n❌ Flow import failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 