#!/usr/bin/env python3
"""
Test script to create a simple Langflow flow
"""

import json
import time

import requests


def test_langflow_connection():
    """Test basic Langflow connection"""
    try:
        response = requests.get("http://localhost:7860/health")
        if response.status_code == 200:
            print("✅ Langflow is running and healthy")
            return True
        else:
            print(f"❌ Langflow health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Langflow: {e}")
        return False


def create_simple_flow():
    """Create a simple test flow"""
    try:
        # Simple flow with a prompt template and LLM
        flow_data = {
            "name": "Simple Test Flow",
            "description": "A simple test flow for verification",
            "data": {
                "nodes": [
                    {
                        "id": "prompt_template_1",
                        "type": "PromptTemplate",
                        "position": {"x": 100, "y": 100},
                        "data": {
                            "template": "Hello! Please respond to: {input_text}",
                            "input_variables": ["input_text"],
                        },
                    },
                    {
                        "id": "llm_1",
                        "type": "LLMChain",
                        "position": {"x": 300, "y": 100},
                        "data": {"model_name": "gpt-3.5-turbo", "temperature": 0.7},
                    },
                ],
                "edges": [
                    {
                        "source": "prompt_template_1",
                        "target": "llm_1",
                        "sourceHandle": "output",
                        "targetHandle": "input",
                    }
                ],
            },
        }

        # Try to create the flow via API
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            "http://localhost:7860/api/v1/flows/", json=flow_data, headers=headers
        )

        if response.status_code in [200, 201]:
            print("✅ Successfully created test flow")
            print(f"Response: {response.text[:200]}...")
            return True
        else:
            print(f"❌ Failed to create flow: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error creating flow: {e}")
        return False


def test_web_interface():
    """Test if web interface is accessible"""
    try:
        response = requests.get("http://localhost:7860/")
        if response.status_code == 200 and "Langflow" in response.text:
            print("✅ Langflow web interface is accessible")
            print("🌐 You can access it at: http://localhost:7860")
            return True
        else:
            print(f"❌ Web interface not accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot access web interface: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Testing Langflow Flow Creation")
    print("=" * 50)

    # Test 1: Connection
    if not test_langflow_connection():
        return

    # Test 2: Web Interface
    if not test_web_interface():
        return

    # Test 3: Flow Creation
    print("\n📝 Attempting to create a simple test flow...")
    if create_simple_flow():
        print("\n✅ All tests passed! Langflow is working correctly.")
        print("\n🎯 Next steps:")
        print("1. Open http://localhost:7860 in your browser")
        print("2. Create a new flow using the web interface")
        print("3. Add a Prompt Template node")
        print("4. Add an LLM Chain node")
        print("5. Connect them and test the flow")
    else:
        print("\n⚠️  Flow creation via API failed, but web interface is available.")
        print("You can still create flows manually through the web interface.")


if __name__ == "__main__":
    main()
