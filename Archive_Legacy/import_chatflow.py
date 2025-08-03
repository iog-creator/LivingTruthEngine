#!/usr/bin/env python3
"""
Import Living Truth Engine Chatflow into Flowise
This script imports the corrected chatflow configuration into Flowise
"""

import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_chatflow():
    """Update the existing chatflow in Flowise."""
    
    # Configuration
    flowise_url = os.getenv('FLOWISE_API_ENDPOINT', 'http://localhost:3000')
    api_key = os.getenv('FLOWISE_API_KEY')
    chatflow_id = os.getenv('FLOWISE_CHATFLOW_ID')
    
    if not api_key or api_key == 'your_flowise_api_key_here':
        print("❌ FLOWISE_API_KEY not configured in .env file")
        print("Please set FLOWISE_API_KEY in your .env file")
        return False
    
    if not chatflow_id:
        print("❌ FLOWISE_CHATFLOW_ID not configured in .env file")
        return False
    
    # Load the corrected chatflow
    chatflow_path = Path(__file__).parent.parent.parent / 'config' / 'living_truth_full_flow.json'
    
    if not chatflow_path.exists():
        print(f"❌ Chatflow file not found: {chatflow_path}")
        return False
    
    try:
        with open(chatflow_path, 'r') as f:
            chatflow_data = json.load(f)
        
        print(f"✅ Loaded chatflow from: {chatflow_path}")
        
        # Prepare the update payload
        update_payload = {
            "name": "Living Truth Engine",
            "flowData": json.dumps(chatflow_data),
            "deployed": True
        }
        
        # Update the existing chatflow
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        update_url = f"{flowise_url}/api/v1/chatflows/{chatflow_id}"
        
        response = requests.put(update_url, json=update_payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chatflow updated successfully!")
            print(f"📋 Chatflow ID: {chatflow_id}")
            print(f"📋 Chatflow Name: {result.get('name', 'Living Truth Engine')}")
            print(f"📋 Deployed: {result.get('deployed', False)}")
            return True
            
        else:
            print(f"❌ Failed to update chatflow: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating chatflow: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Updating Living Truth Engine Chatflow in Flowise...")
    print("=" * 50)
    
    success = update_chatflow()
    
    if success:
        print("\n✅ Chatflow update completed successfully!")
        print("🔄 Please restart the MCP server to pick up the changes:")
        print("   docker compose -f docker/docker-compose.yml restart living-truth-mcp")
    else:
        print("\n❌ Chatflow update failed!")
        print("Please check the error messages above and try again.")

if __name__ == "__main__":
    main() 