#!/usr/bin/env python3
"""
Create Phase 8 Flow via MCP Hub Server

This script uses the existing MCP Hub Server to create the Phase 8 flow in Langflow
using the available Langflow MCP tools.
"""

import json
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from mcp_servers.mcp_hub_server import MCPHubServer

def create_phase8_flow_via_mcp():
    """Create Phase 8 flow using the MCP Hub Server."""
    
    print("🎯 Creating Phase 8 Flow via MCP Hub Server...")
    
    # Initialize the MCP Hub Server
    hub_server = MCPHubServer()
    
    # Phase 8 flow configuration
    phase8_flow_config = {
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
    
    try:
        # Use the MCP Hub Server to create the flow
        print("📝 Creating Phase 8 flow via Langflow MCP tools...")
        
        # First, let's check what Langflow tools are available
        result = hub_server.execute_tool("list_langflow_tools", {})
        print(f"✅ Available Langflow tools: {result}")
        
        # Try to create the flow using the Langflow MCP tools
        create_result = hub_server.execute_tool("create_langflow", {
            "flow_config": json.dumps(phase8_flow_config)
        })
        
        print(f"✅ Flow creation result: {create_result}")
        
        # Save the flow configuration for manual import if needed
        output_dir = Path("data/visualizations")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        flow_file = output_dir / "phase8_flow_mcp_created.json"
        with open(flow_file, 'w') as f:
            json.dump(phase8_flow_config, f, indent=2)
        
        print(f"✅ Flow configuration saved to: {flow_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating flow via MCP: {e}")
        
        # Fallback: save the flow configuration for manual creation
        output_dir = Path("data/visualizations")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        flow_file = output_dir / "phase8_flow_manual_creation.json"
        with open(flow_file, 'w') as f:
            json.dump(phase8_flow_config, f, indent=2)
        
        print(f"✅ Flow configuration saved for manual creation: {flow_file}")
        return False

def create_mcp_configuration():
    """Create the proper MCP configuration for Phase 8."""
    
    # The correct MCP configuration should use the existing MCP Hub Server
    # and add the Phase 8 flow as a tool in Langflow
    
    mcp_config = {
        "mcpServers": {
            "mcp_hub_server": {
                "command": "python3",
                "args": [
                    "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/src/mcp_servers/mcp_hub_server.py"
                ],
                "env": {
                    "LANGFLOW_API_ENDPOINT": "http://localhost:7860",
                    "LANGFLOW_API_KEY": "${LANGFLOW_API_KEY}",
                    "LANGFLOW_PROJECT_ID": "399a0977-d08a-4d61-ba52-fd9811676762",
                    "LM_STUDIO_ENDPOINT": "http://localhost:1234",
                    "PYTHONPATH": "/home/mccoy/Projects/NotebookLM/LivingTruthEngine/src"
                },
                "description": "MCP Hub Server - Includes Phase 8 Langflow tools"
            }
        }
    }
    
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mcp_file = output_dir / "phase8_mcp_config.json"
    with open(mcp_file, 'w') as f:
        json.dump(mcp_config, f, indent=2)
    
    print(f"✅ MCP configuration saved to: {mcp_file}")
    return mcp_config

def create_manual_setup_instructions():
    """Create instructions for manual setup in Langflow."""
    
    instructions = """
# Phase 8 Flow Manual Setup Instructions

## 🎯 Overview
Since you can see the MCP server tools in Langflow, we'll create the Phase 8 flow manually and then configure it as an MCP tool.

## 📁 Files Created
- `phase8_flow_manual_creation.json` - Flow configuration for manual creation
- `phase8_mcp_config.json` - MCP configuration for Cursor

## 🔧 Manual Setup Steps

### Step 1: Create the Flow in Langflow
1. **Open Langflow** at http://localhost:7860
2. **Create a new project**: "Phase 8 Real Data Ingestion"
3. **Create a new flow**: "Phase 8 Pipeline"
4. **Add components** from the left sidebar:
   - **Input Node**: Set type to "str", name to "text", display name to "YouTube Channel URL"
   - **LLM Chain**: Configure with the prompt template from the JSON file
   - **Chat Output**: Connect to LLM Chain output (REQUIRED for MCP)

### Step 2: Configure the LLM Chain
1. **Open the LLM Chain component**
2. **Set the prompt template** to the one from `phase8_flow_manual_creation.json`
3. **Configure the LLM** to use your preferred model
4. **Test the flow** with a sample YouTube channel URL

### Step 3: Configure MCP Server Tools
1. **Go to MCP Server tab** in your Langflow project
2. **Click "Edit Tools"**
3. **Enable the Phase 8 flow** as an MCP tool
4. **Configure tool name**: `phase8_ingestion`
5. **Configure tool description**: `Process YouTube channel ingestion with Phase 8 pipeline. Input: YouTube channel URL. Output: Detailed processing summary and bundle structure.`

### Step 4: Test the MCP Tool
1. **Save the MCP configuration**
2. **Test the tool** in Langflow
3. **Verify the Chat Output** works correctly

### Step 5: Connect to Cursor
1. **The MCP Hub Server** already includes Langflow tools
2. **Restart Cursor** to see the new Phase 8 tool
3. **Test with**: `mcp_mcp_hub_server_execute_langflow_tool("phase8_ingestion", {"text": "https://www.youtube.com/@imaginationpodcastofficial"})`

## ✅ Success Indicators
- Flow creates successfully in Langflow
- Chat Output component is present and working
- MCP Server shows the Phase 8 tool as available
- Tool can be tested with sample inputs
- Cursor can access the tool via MCP Hub Server

## 🔗 Next Steps
After setup:
1. Test the flow manually in Langflow
2. Test the MCP tool in Cursor
3. Use with real YouTube channel URLs
4. Monitor bundle creation and processing

Generated: 2025-08-10
"""
    
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    instructions_file = output_dir / "PHASE_8_MANUAL_SETUP.md"
    with open(instructions_file, 'w') as f:
        f.write(instructions)
    
    print(f"✅ Manual setup instructions saved to: {instructions_file}")

def main():
    """Main function."""
    
    print("🎯 Creating Phase 8 Flow via MCP Hub Server...")
    
    # Try to create the flow via MCP
    success = create_phase8_flow_via_mcp()
    
    # Create MCP configuration
    mcp_config = create_mcp_configuration()
    
    # Create manual setup instructions
    create_manual_setup_instructions()
    
    print(f"\n🎉 Phase 8 Flow Setup Complete!")
    
    if success:
        print(f"\n✅ Flow created successfully via MCP!")
    else:
        print(f"\n📋 Manual creation required - see PHASE_8_MANUAL_SETUP.md")
    
    print(f"\n📁 Files created in data/visualizations/:")
    print(f"   - phase8_flow_manual_creation.json")
    print(f"   - phase8_mcp_config.json")
    print(f"   - PHASE_8_MANUAL_SETUP.md")
    
    print(f"\n🔗 Next Steps:")
    print(f"1. Open Langflow at http://localhost:7860")
    print(f"2. Create the Phase 8 flow manually")
    print(f"3. Configure it as an MCP tool")
    print(f"4. Test via MCP Hub Server in Cursor")

if __name__ == "__main__":
    main()

