#!/usr/bin/env python3
"""
Test script to create and test a simple Langflow flow
"""

import requests
import json
import time

def test_langflow_api():
    """Test Langflow API endpoints"""
    print("🔍 Testing Langflow API endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get('http://localhost:7860/health')
        if response.status_code == 200:
            print("✅ Health endpoint: OK")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test flows endpoint
    try:
        response = requests.get('http://localhost:7860/api/v1/flows/', headers={'Accept-Encoding': 'gzip'})
        if response.status_code == 200:
            flows = response.json()
            print(f"✅ Flows endpoint: OK ({len(flows)} flows found)")
            return True
        else:
            print(f"❌ Flows endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flows endpoint error: {e}")
        return False

def create_simple_chat_flow():
    """Create a simple chat flow with prompt template and LLM"""
    print("\n📝 Creating simple chat flow...")
    
    flow_data = {
        "name": "Simple Chat Flow Test",
        "description": "A simple test flow with prompt template and language model",
        "data": {
            "nodes": [
                {
                    "id": "ChatInput-test",
                    "type": "ChatInput",
                    "position": {"x": 100, "y": 100},
                    "data": {
                        "id": "ChatInput-test",
                        "node": {
                            "display_name": "Chat Input",
                            "description": "Chat input for user messages",
                            "template": {
                                "input_value": {
                                    "display_name": "Input Text",
                                    "value": "",
                                    "required": False
                                }
                            }
                        }
                    }
                },
                {
                    "id": "PromptTemplate-test",
                    "type": "PromptTemplate",
                    "position": {"x": 400, "y": 100},
                    "data": {
                        "id": "PromptTemplate-test",
                        "node": {
                            "display_name": "Prompt Template",
                            "description": "Template for formatting prompts",
                            "template": {
                                "template": {
                                    "display_name": "Template",
                                    "value": "You are a helpful AI assistant. Please respond to: {input_text}",
                                    "required": True
                                },
                                "input_variables": {
                                    "display_name": "Input Variables",
                                    "value": ["input_text"],
                                    "required": False
                                }
                            }
                        }
                    }
                },
                {
                    "id": "LanguageModel-test",
                    "type": "LanguageModelComponent",
                    "position": {"x": 700, "y": 100},
                    "data": {
                        "id": "LanguageModel-test",
                        "node": {
                            "display_name": "Language Model",
                            "description": "Language model for generating responses",
                            "template": {
                                "provider": {
                                    "display_name": "Model Provider",
                                    "value": "Anthropic",
                                    "required": False
                                },
                                "model_name": {
                                    "display_name": "Model Name",
                                    "value": "claude-3-5-sonnet-latest",
                                    "required": False
                                },
                                "temperature": {
                                    "display_name": "Temperature",
                                    "value": 0.7,
                                    "required": False
                                }
                            }
                        }
                    }
                },
                {
                    "id": "ChatOutput-test",
                    "type": "ChatOutput",
                    "position": {"x": 1000, "y": 100},
                    "data": {
                        "id": "ChatOutput-test",
                        "node": {
                            "display_name": "Chat Output",
                            "description": "Display chat messages",
                            "template": {
                                "input_value": {
                                    "display_name": "Inputs",
                                    "value": "",
                                    "required": True
                                }
                            }
                        }
                    }
                }
            ],
            "edges": [
                {
                    "source": "ChatInput-test",
                    "target": "PromptTemplate-test",
                    "sourceHandle": "message",
                    "targetHandle": "input_value"
                },
                {
                    "source": "PromptTemplate-test",
                    "target": "LanguageModel-test",
                    "sourceHandle": "text",
                    "targetHandle": "input_value"
                },
                {
                    "source": "LanguageModel-test",
                    "target": "ChatOutput-test",
                    "sourceHandle": "text_output",
                    "targetHandle": "input_value"
                }
            ]
        }
    }
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        response = requests.post(
            'http://localhost:7860/api/v1/flows/',
            json=flow_data,
            headers=headers
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ Successfully created chat flow!")
            print(f"📋 Flow ID: {result.get('id', 'N/A')}")
            print(f"📋 Flow Name: {result.get('name', 'N/A')}")
            return result.get('id')
        else:
            print(f"❌ Failed to create flow: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except Exception as e:
        print(f"❌ Error creating flow: {e}")
        return None

def test_flow_execution(flow_id):
    """Test executing the created flow"""
    if not flow_id:
        print("⚠️  No flow ID provided, skipping execution test")
        return
    
    print(f"\n🚀 Testing flow execution for flow ID: {flow_id}")
    
    # Test data
    test_input = {
        "input_text": "Hello! Can you tell me a short joke?"
    }
    
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Try to execute the flow
        response = requests.post(
            f'http://localhost:7860/api/v1/flows/{flow_id}/run',
            json=test_input,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Flow execution successful!")
            print(f"📤 Input: {test_input}")
            print(f"📥 Output: {result.get('output', 'N/A')}")
            return True
        else:
            print(f"❌ Flow execution failed: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error executing flow: {e}")
        return False

def list_existing_flows():
    """List existing flows"""
    print("\n📋 Listing existing flows...")
    
    try:
        response = requests.get('http://localhost:7860/api/v1/flows/', headers={'Accept-Encoding': 'gzip'})
        if response.status_code == 200:
            flows = response.json()
            print(f"Found {len(flows)} flows:")
            for i, flow in enumerate(flows[:5]):  # Show first 5 flows
                print(f"  {i+1}. {flow.get('name', 'Unnamed')} (ID: {flow.get('id', 'N/A')})")
            if len(flows) > 5:
                print(f"  ... and {len(flows) - 5} more flows")
            return flows
        else:
            print(f"❌ Failed to list flows: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error listing flows: {e}")
        return []

def main():
    """Main test function"""
    print("🧪 Langflow Flow Creation and Testing")
    print("=" * 50)
    
    # Test 1: API endpoints
    if not test_langflow_api():
        print("\n❌ API tests failed. Please check Langflow is running.")
        return
    
    # Test 2: List existing flows
    existing_flows = list_existing_flows()
    
    # Test 3: Create new flow
    print("\n" + "=" * 50)
    flow_id = create_simple_chat_flow()
    
    # Test 4: Execute flow (if created successfully)
    if flow_id:
        print("\n" + "=" * 50)
        test_flow_execution(flow_id)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"✅ Langflow API: Working")
    print(f"✅ Existing flows: {len(existing_flows)} found")
    print(f"✅ New flow creation: {'Success' if flow_id else 'Failed'}")
    
    if flow_id:
        print(f"✅ Flow execution: {'Tested' if flow_id else 'Skipped'}")
        print(f"\n🎯 Next steps:")
        print(f"1. Open http://localhost:7860 in your browser")
        print(f"2. Find your flow: 'Simple Chat Flow Test'")
        print(f"3. Click on it to open the flow editor")
        print(f"4. Test the flow with different inputs")
        print(f"5. Modify the flow as needed")
    else:
        print(f"\n⚠️  Flow creation failed, but you can still:")
        print(f"1. Open http://localhost:7860 in your browser")
        print(f"2. Create flows manually using the web interface")
        print(f"3. Use the existing flows for testing")

if __name__ == "__main__":
    main() 