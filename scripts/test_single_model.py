#!/usr/bin/env python3
"""
Test Single Model - Llama 3.2 3B Instruct Only
"""
import requests
import json
import re

def test_single_model():
    """Test only the Llama 3.2 3B Instruct model"""
    print("🚀 Testing Llama 3.2 3B Instruct Model Only")
    print("=" * 50)
    
    model_id = "llama-3.2-3b-instruct"
    
    # Test TODO analysis
    print("📋 Testing TODO analysis...")
    try:
        payload = {
            "model": model_id,
            "messages": [
                {"role": "system", "content": "You are a JSON-only responder. Never explain, only provide valid JSON."},
                {"role": "user", "content": "TODO: Fix error handling in main.py\nFile: main.py\nRespond ONLY with JSON: {\"task_type\": \"bug|feature|improvement\", \"priority\": \"high|medium|low\", \"effort\": \"low|medium|high\"}"}
            ],
            "temperature": 0.1,
            "max_tokens": 50
        }
        
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ Response: {content}")
            
            # Try to extract JSON
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                print(f"✅ Parsed JSON: {parsed}")
                print(f"✅ Model {model_id} is working correctly!")
                return True
            else:
                print(f"❌ No JSON found in response")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_single_model()
    if success:
        print("\n🎉 Single model test passed! Ready for SSOT validation.")
    else:
        print("\n❌ Single model test failed.")
