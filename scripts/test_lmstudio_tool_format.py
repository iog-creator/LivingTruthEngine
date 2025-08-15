#!/usr/bin/env python3
"""
Test to determine the correct LM Studio tool format
"""
import requests
import json

def test_lmstudio_api():
    """Test LM Studio's API to understand the correct format"""
    print("🔍 Testing LM Studio API to determine correct tool format...")
    
    try:
        # Test 1: Check if LM Studio has a tools endpoint
        response = requests.get("http://localhost:1234/v1/tools", timeout=5)
        print(f"Tools endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        
        # Test 2: Check models endpoint to see available models
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        print(f"Models endpoint: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"Available models: {[m['id'] for m in models.get('data', [])]}")
        
        # Test 3: Try to understand the chat completion format
        print("\n📋 LM Studio Chat Completion Format:")
        print("LM Studio uses OpenAI-compatible API. For tools, you need to:")
        print("1. Send tools in the chat completion request")
        print("2. Use the 'tools' parameter in the messages")
        print("3. LM Studio will call the tools via HTTP")
        
        # Example format
        example_request = {
            "model": "llama-3.2-3b-instruct",
            "messages": [
                {"role": "user", "content": "Can you verify the SSOT status?"}
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "verify_ssot",
                        "description": "Run SSOT validation check",
                        "parameters": {
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    }
                }
            ],
            "tool_choice": "auto"
        }
        
        print(f"\n🎯 Example request format:")
        print(json.dumps(example_request, indent=2))
        
        print(f"\n💡 To use tools with LM Studio:")
        print(f"1. Send requests with 'tools' parameter")
        print(f"2. LM Studio will call the tools via HTTP")
        print(f"3. Tools should be available at the specified URLs")
        
    except Exception as e:
        print(f"❌ Error testing LM Studio API: {e}")

if __name__ == "__main__":
    test_lmstudio_api()
