#!/usr/bin/env python3
"""
Test LM Studio with tools using the correct OpenAI-compatible format
"""
import requests
import json
import time

def test_lmstudio_with_tools():
    """Test LM Studio with tools using the correct format"""
    print("🤖 Testing LM Studio with tools...")
    
    # The correct format for LM Studio tools
    payload = {
        "model": "llama-3.2-3b-instruct",
        "messages": [
            {"role": "user", "content": "Can you verify the SSOT status of the project?"}
        ],
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "verify_ssot",
                    "description": "Run comprehensive SSOT validation check",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_ssot_report",
                    "description": "Read the latest SSOT validation report",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "draft_patches",
                    "description": "Get suggested code patches (read-only)",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ],
        "tool_choice": "auto",
        "temperature": 0.1,
        "max_tokens": 500
    }
    
    print("🔄 Sending request to LM Studio with tools...")
    print("📋 This should trigger LM Studio to call the tools bridge")
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=60
        )
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ LM Studio responded in {end_time - start_time:.2f}s")
            
            # Check if tools were called
            choices = result.get("choices", [])
            if choices:
                choice = choices[0]
                message = choice.get("message", {})
                
                print(f"🤖 Response: {message.get('content', 'No content')}")
                
                # Check for tool calls
                tool_calls = message.get("tool_calls", [])
                if tool_calls:
                    print(f"🔧 Tool calls made: {len(tool_calls)}")
                    for i, tool_call in enumerate(tool_calls):
                        print(f"  {i+1}. {tool_call.get('function', {}).get('name')}")
                else:
                    print("⚠️  No tool calls detected - LM Studio may not have called the tools")
                    
                # Check finish reason
                finish_reason = choice.get("finish_reason")
                print(f"🏁 Finish reason: {finish_reason}")
                
        else:
            print(f"❌ LM Studio error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🧪 LM Studio Tools Integration Test")
    print("=" * 50)
    
    # Make sure bridge is running
    print("📋 Prerequisites:")
    print("1. LM Studio is running on localhost:1234")
    print("2. Tools bridge is running: make lm-tools")
    print("3. Bridge responds to: curl http://127.0.0.1:8756/tools/verify_ssot")
    
    print("\n🚀 Testing LM Studio with tools...")
    test_lmstudio_with_tools()
    
    print("\n💡 Expected behavior:")
    print("- LM Studio should call the tools bridge")
    print("- You should see HTTP requests in the bridge logs")
    print("- LM Studio should respond with the tool results")

if __name__ == "__main__":
    main()
