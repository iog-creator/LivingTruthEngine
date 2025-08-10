#!/usr/bin/env python3
"""
Simple Langflow Flow Creation for Phase 8

This script creates Phase 8 flows in Langflow using the correct API endpoints.
"""

import json
import requests
from pathlib import Path

def create_simple_phase8_flow():
    """Create a simple Phase 8 flow using the correct Langflow API."""
    
    base_url = "http://localhost:7860"
    
    # Try to create a flow using the correct endpoint
    flow_data = {
        "name": "Phase 8 Real Data Ingestion Pipeline",
        "description": "Process YouTube channel ingestion with depth-limited expansion and verifiable bundles",
        "data": {
            "nodes": [
                {
                    "id": "input_node",
                    "type": "InputNode",
                    "data": {
                        "node": {
                            "template": {
                                "type": "str",
                                "required": True,
                                "show": True,
                                "name": "text",
                                "display_name": "YouTube Channel URL",
                                "value": "https://www.youtube.com/@imaginationpodcastofficial"
                            }
                        }
                    },
                    "position": {"x": 100, "y": 100}
                },
                {
                    "id": "llm_chain",
                    "type": "LLMChain",
                    "data": {
                        "node": {
                            "template": {
                                "name": "llm_chain",
                                "display_name": "Phase 8 Pipeline Processor",
                                "description": "Process YouTube channel ingestion pipeline",
                                "llm": {
                                    "type": "OpenAI",
                                    "model": "gpt-3.5-turbo",
                                    "temperature": 0.7
                                },
                                "prompt": {
                                    "type": "PromptTemplate",
                                    "template": """You are a Phase 8 Real Data Ingestion Pipeline processor.

Input: {text}

Process this YouTube channel URL through the Phase 8 pipeline:

**Phase 8 Pipeline Stages:**

1. **YouTube Channel Discovery**
   - Use yt-dlp to discover videos from the channel
   - Sort by oldest/newest/custom order
   - Limit to specified number of videos

2. **Transcript Extraction**
   - Extract transcripts using YouTube Transcript API
   - Fallback to autosubs if API fails
   - Process all discovered videos

3. **URL Extraction**
   - Use regex patterns to extract URLs from transcripts
   - Extract URLs from video descriptions
   - Validate and filter URLs

4. **Depth-Limited Expansion**
   - Expand external links up to specified depth
   - Follow links from transcripts and descriptions
   - Respect crawl depth limits

5. **Content Fetching**
   - Fetch web content from expanded URLs
   - Process PDFs with optional OCR
   - Use optional JavaScript rendering for dynamic content

6. **Canonicalization**
   - Convert all content to standardized JSONL format
   - Normalize text and metadata
   - Create consistent document structure

7. **Provenance Generation**
   - Generate SHA-256 proofs for each document
   - Create Merkle tree for data integrity
   - Store proofs in proofs/ directory

8. **Bundle Creation**
   - Create .veritasrun bundle with:
     - manifest.json (metadata and configuration)
     - corpus.jsonl (canonicalized documents)
     - proofs/ (SHA-256 proofs)
     - merkle.json (Merkle tree)
     - metrics.json (processing statistics)

**Expected Output:**
Provide a detailed summary of:
- What would be processed
- Expected document counts
- Bundle structure and location
- Processing time estimates
- Data integrity measures

Channel URL: {text}
Max Videos: 5 (default)
Crawl Depth: 2 (default)
OCR Required: false (default)
JS Render: false (default)"""
                                }
                            }
                        }
                    },
                    "position": {"x": 300, "y": 100}
                },
                {
                    "id": "chat_output",
                    "type": "ChatOutput",
                    "data": {
                        "node": {
                            "template": {
                                "name": "chat_output",
                                "display_name": "Phase 8 Pipeline Results",
                                "description": "Output the Phase 8 pipeline processing results"
                            }
                        }
                    },
                    "position": {"x": 500, "y": 100}
                }
            ],
            "edges": [
                {
                    "source": "input_node",
                    "target": "llm_chain",
                    "sourceHandle": "text",
                    "targetHandle": "input"
                },
                {
                    "source": "llm_chain",
                    "target": "chat_output",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                }
            ]
        }
    }
    
    # Save the flow data for manual import
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    flow_file = output_dir / "phase8_flow_for_import.json"
    with open(flow_file, 'w') as f:
        json.dump(flow_data, f, indent=2)
    
    print(f"✅ Phase 8 flow data saved to: {flow_file}")
    
    # Try different API endpoints
    endpoints_to_try = [
        "/api/v1/flows",
        "/api/flows",
        "/api/v1/flow",
        "/api/flow"
    ]
    
    for endpoint in endpoints_to_try:
        try:
            print(f"🔍 Trying endpoint: {endpoint}")
            response = requests.post(
                f"{base_url}{endpoint}",
                json=flow_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"✅ Success! Flow created with endpoint: {endpoint}")
                    print(f"   Flow ID: {result.get('id', 'Unknown')}")
                    return result.get('id')
                except:
                    print(f"   Response is not JSON")
            elif response.status_code == 201:
                print(f"✅ Success! Flow created with endpoint: {endpoint}")
                return "created"
                
        except Exception as e:
            print(f"   Error: {e}")
    
    print("❌ Could not create flow via API")
    return None

def create_mcp_configuration():
    """Create MCP configuration for Cursor."""
    
    # Create a sample MCP configuration
    mcp_config = {
        "mcpServers": {
            "phase8_langflow": {
                "command": "uvx",
                "args": [
                    "mcp-proxy",
                    "http://localhost:7860/api/v1/mcp/project/PROJECT_ID/sse"
                ]
            }
        }
    }
    
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mcp_file = output_dir / "cursor_mcp_config.json"
    with open(mcp_file, 'w') as f:
        json.dump(mcp_config, f, indent=2)
    
    print(f"✅ MCP configuration saved to: {mcp_file}")
    
    return mcp_config

def create_import_instructions():
    """Create detailed import instructions."""
    
    instructions = """
# Phase 8 Langflow Flow Import Instructions

## 🎯 Overview
Since the automated API creation didn't work, we'll import the flows manually into Langflow.

## 📁 Files Created
- `phase8_flow_for_import.json` - Phase 8 flow ready for import
- `cursor_mcp_config.json` - MCP configuration for Cursor

## 🔧 Manual Import Steps

### Step 1: Open Langflow
1. Go to http://localhost:7860
2. Login with admin/admin
3. Create a new project: "Phase 8 Real Data Ingestion"

### Step 2: Import the Flow
1. Click "Import Flow" or "Create New Flow"
2. Select the file: `data/visualizations/phase8_flow_for_import.json`
3. The flow should appear with:
   - Input Node: YouTube Channel URL
   - LLM Chain: Phase 8 Pipeline Processor
   - Chat Output: Phase 8 Pipeline Results

### Step 3: Configure MCP Server
1. Go to the "MCP Server" tab in your project
2. Click "Edit Tools"
3. Enable the Phase 8 flow
4. Configure tool name: `phase8_ingestion`
5. Configure tool description: `Process YouTube channel ingestion with Phase 8 pipeline. Input: YouTube channel URL. Output: Detailed processing summary and bundle structure.`

### Step 4: Get MCP Configuration
1. In the MCP Server tab, copy the JSON configuration
2. Replace the placeholder in `cursor_mcp_config.json`
3. Add to Cursor's MCP settings

### Step 5: Test the Flow
1. Open the flow in Langflow
2. Test with a sample YouTube channel URL
3. Verify the Chat Output works correctly

## ✅ Success Indicators
- Flow imports successfully
- Chat Output component is present
- MCP Server shows the tool as available
- Flow can be tested with sample inputs

## 🔗 Next Steps
After importing:
1. Test the flow manually
2. Configure MCP Server settings
3. Connect to Cursor
4. Test with real YouTube channel URLs

Generated: 2025-08-10
"""
    
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    instructions_file = output_dir / "MANUAL_IMPORT_INSTRUCTIONS.md"
    with open(instructions_file, 'w') as f:
        f.write(instructions)
    
    print(f"✅ Import instructions saved to: {instructions_file}")

def main():
    """Main function."""
    
    print("🎯 Creating Phase 8 Flow for Langflow...")
    
    # Create the flow data
    flow_id = create_simple_phase8_flow()
    
    # Create MCP configuration
    mcp_config = create_mcp_configuration()
    
    # Create import instructions
    create_import_instructions()
    
    print(f"\n🎉 Phase 8 Flow Creation Complete!")
    print(f"\n📁 Files created in data/visualizations/:")
    print(f"   - phase8_flow_for_import.json")
    print(f"   - cursor_mcp_config.json")
    print(f"   - MANUAL_IMPORT_INSTRUCTIONS.md")
    
    print(f"\n🔗 Next Steps:")
    print(f"1. Open Langflow at http://localhost:7860")
    print(f"2. Import the flow file manually")
    print(f"3. Configure MCP Server settings")
    print(f"4. Connect to Cursor")
    
    if flow_id:
        print(f"\n✅ Flow created successfully with ID: {flow_id}")
    else:
        print(f"\n📋 Manual import required - see MANUAL_IMPORT_INSTRUCTIONS.md")

if __name__ == "__main__":
    main()


