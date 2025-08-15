#!/usr/bin/env python3
"""
Test AI Integration with LM Studio for SSOT Validation
"""
import requests
import json
import sys

def test_lm_studio_connection():
    """Test basic LM Studio connection"""
    print("🔍 Testing LM Studio connection...")
    
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ LM Studio connected. Available models: {len(models.get('data', []))}")
            for model in models.get('data', [])[:3]:
                print(f"  - {model.get('id', 'Unknown')}")
            return True
        else:
            print(f"❌ LM Studio responded with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ LM Studio connection failed: {e}")
        return False

def test_simple_ai_query():
    """Test a simple AI query"""
    print("\n🤖 Testing simple AI query...")
    
    try:
        payload = {
            "model": "qwen/qwen3-8b",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'Hello, AI integration test successful!' and nothing else."}
            ],
            "temperature": 0.1,
            "max_tokens": 50
        }
        
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ AI query successful: {content}")
            return True
        else:
            print(f"❌ AI query failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI query failed: {e}")
        return False

def main():
    """Run AI integration tests"""
    print("🚀 AI Integration Test for SSOT Validation")
    print("=" * 50)
    
    # Test connection
    connection_ok = test_lm_studio_connection()
    
    if connection_ok:
        # Test AI query
        ai_ok = test_simple_ai_query()
        
        if ai_ok:
            print("\n🎉 All AI integration tests passed!")
            print("✅ You can now run: python scripts/verify_complete_ssot_system.py --ai")
            sys.exit(0)
        else:
            print("\n❌ AI query test failed")
            sys.exit(1)
    else:
        print("\n❌ LM Studio connection test failed")
        print("💡 Make sure LM Studio is running on localhost:1234")
        sys.exit(1)

if __name__ == "__main__":
    main()
