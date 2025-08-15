#!/usr/bin/env python3
"""
Quick Test of Optimized AI Integration with Different Models
"""
import requests
import json
import re

def test_model(model_id, test_name):
    """Test a specific model"""
    print(f"\n🤖 Testing {model_id} ({test_name})...")
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
                try:
                    parsed = json.loads(json_match.group())
                    print(f"✅ Parsed JSON: {parsed}")
                    return True
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON in response")
                    return False
            else:
                print(f"❌ No JSON found in response")
                return False
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_quick_ai():
    """Test different models for structured output"""
    print("🚀 Testing Different Models for Structured Output")
    print("=" * 50)
    
    # Test different models
    models_to_test = [
        ("llama-3.2-3b-instruct", "Llama 3.2 3B Instruct"),
        ("llama-3.2-1b-instruct", "Llama 3.2 1B Instruct"),
        ("meta/llama-3.3-70b", "Llama 3.3 70B"),
        ("mistralai/devstral-small-2505", "Mistral Devstral Small"),
        ("google/gemma-3-4b", "Gemma 3 4B"),
        ("qwen/qwen3-8b", "Qwen 3 8B (current)")
    ]
    
    results = {}
    for model_id, model_name in models_to_test:
        success = test_model(model_id, model_name)
        results[model_id] = {"name": model_name, "success": success}
    
    # Summary
    print("\n📊 Model Test Results:")
    print("=" * 30)
    for model_id, result in results.items():
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"{status} {result['name']} ({model_id})")
    
    # Recommend best model
    working_models = [mid for mid, result in results.items() if result["success"]]
    if working_models:
        print(f"\n🎯 Recommended model: {working_models[0]}")
        print(f"   Update the script to use: {working_models[0]}")
    else:
        print("\n❌ No models produced valid JSON output")

if __name__ == "__main__":
    test_quick_ai()
