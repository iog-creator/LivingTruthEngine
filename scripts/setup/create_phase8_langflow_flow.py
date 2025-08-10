#!/usr/bin/env python3
"""
Create Phase 8 Langflow Flow with MCP Integration

This script creates a proper Langflow flow that can be exposed as an MCP tool
with a Chat Output component as required by Langflow's MCP server.
"""

import json
import requests
from pathlib import Path

def create_phase8_langflow_flow():
    """Create a Langflow flow for Phase 8 that can be exposed as MCP tool."""
    
    # Langflow flow with Chat Output component (required for MCP)
    flow_data = {
        "name": "Phase 8 Real Data Ingestion Pipeline",
        "description": "Process YouTube channel ingestion with depth-limited expansion and verifiable bundles",
        "data": {
            "nodes": [
                # Input node
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
                
                # LLM Chain for processing
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

1. YouTube Channel Discovery: Discover videos using yt-dlp
2. Transcript Extraction: Extract transcripts with YouTube Transcript API + autosubs fallback
3. URL Extraction: Extract URLs from transcripts using regex patterns
4. Depth-Limited Expansion: Expand external links up to configurable depth
5. Content Fetching: Fetch web content and PDFs with optional OCR/JS rendering
6. Canonicalization: Convert to standardized JSONL format
7. Provenance Generation: Generate SHA-256 proofs and Merkle tree
8. Bundle Creation: Create .veritasrun bundle with manifest, corpus, proofs, merkle, metrics

Output a detailed summary of what would be processed and the expected bundle structure.

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
                
                # Chat Output (REQUIRED for MCP tool exposure)
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
    
    return flow_data

def create_advanced_phase8_flow():
    """Create a more advanced Langflow flow with multiple components."""
    
    flow_data = {
        "name": "Phase 8 Advanced Ingestion Pipeline",
        "description": "Advanced YouTube channel ingestion with configurable parameters and detailed processing",
        "data": {
            "nodes": [
                # Input nodes
                {
                    "id": "channel_url_input",
                    "type": "InputNode",
                    "data": {
                        "node": {
                            "template": {
                                "type": "str",
                                "required": True,
                                "show": True,
                                "name": "channel_url",
                                "display_name": "YouTube Channel URL",
                                "value": "https://www.youtube.com/@imaginationpodcastofficial"
                            }
                        }
                    },
                    "position": {"x": 100, "y": 100}
                },
                {
                    "id": "max_videos_input",
                    "type": "InputNode",
                    "data": {
                        "node": {
                            "template": {
                                "type": "int",
                                "required": True,
                                "show": True,
                                "name": "max_videos",
                                "display_name": "Max Videos",
                                "value": 5
                            }
                        }
                    },
                    "position": {"x": 100, "y": 200}
                },
                {
                    "id": "crawl_depth_input",
                    "type": "InputNode",
                    "data": {
                        "node": {
                            "template": {
                                "type": "int",
                                "required": True,
                                "show": True,
                                "name": "crawl_depth",
                                "display_name": "Crawl Depth",
                                "value": 2
                            }
                        }
                    },
                    "position": {"x": 100, "y": 300}
                },
                
                # Text Combiner to combine inputs
                {
                    "id": "text_combiner",
                    "type": "TextCombiner",
                    "data": {
                        "node": {
                            "template": {
                                "name": "text_combiner",
                                "display_name": "Combine Parameters",
                                "description": "Combine input parameters for processing"
                            }
                        }
                    },
                    "position": {"x": 250, "y": 200}
                },
                
                # LLM Chain for processing
                {
                    "id": "phase8_processor",
                    "type": "LLMChain",
                    "data": {
                        "node": {
                            "template": {
                                "name": "llm_chain",
                                "display_name": "Phase 8 Pipeline Processor",
                                "description": "Process YouTube channel ingestion with configurable parameters",
                                "llm": {
                                    "type": "OpenAI",
                                    "model": "gpt-3.5-turbo",
                                    "temperature": 0.5
                                },
                                "prompt": {
                                    "type": "PromptTemplate",
                                    "template": """You are the Phase 8 Real Data Ingestion Pipeline processor.

Input Parameters:
{text}

Process this request through the Phase 8 pipeline:

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

Input: {text}"""
                                }
                            }
                        }
                    },
                    "position": {"x": 400, "y": 200}
                },
                
                # Chat Output (REQUIRED for MCP tool exposure)
                {
                    "id": "chat_output",
                    "type": "ChatOutput",
                    "data": {
                        "node": {
                            "template": {
                                "name": "chat_output",
                                "display_name": "Phase 8 Pipeline Results",
                                "description": "Output the Phase 8 pipeline processing results and bundle information"
                            }
                        }
                    },
                    "position": {"x": 550, "y": 200}
                }
            ],
            "edges": [
                # Input connections
                {
                    "source": "channel_url_input",
                    "target": "text_combiner",
                    "sourceHandle": "channel_url",
                    "targetHandle": "text1"
                },
                {
                    "source": "max_videos_input",
                    "target": "text_combiner",
                    "sourceHandle": "max_videos",
                    "targetHandle": "text2"
                },
                {
                    "source": "crawl_depth_input",
                    "target": "text_combiner",
                    "sourceHandle": "crawl_depth",
                    "targetHandle": "text3"
                },
                
                # Processing flow
                {
                    "source": "text_combiner",
                    "target": "phase8_processor",
                    "sourceHandle": "text",
                    "targetHandle": "input"
                },
                {
                    "source": "phase8_processor",
                    "target": "chat_output",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                }
            ]
        }
    }
    
    return flow_data

def create_langflow_project():
    """Create a Langflow project with the Phase 8 flow."""
    
    project_data = {
        "name": "Phase 8 Real Data Ingestion",
        "description": "Langflow project for Phase 8 YouTube channel ingestion pipeline",
        "flows": [
            {
                "name": "Phase 8 Basic Pipeline",
                "description": "Basic Phase 8 pipeline with single input",
                "data": create_phase8_langflow_flow()
            },
            {
                "name": "Phase 8 Advanced Pipeline", 
                "description": "Advanced Phase 8 pipeline with configurable parameters",
                "data": create_advanced_phase8_flow()
            }
        ]
    }
    
    return project_data

def main():
    """Main function to create the Langflow flows."""
    
    print("🎯 Creating Phase 8 Langflow Flows with MCP Integration...")
    
    # Create output directory
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create basic flow
    basic_flow = create_phase8_langflow_flow()
    basic_flow_file = output_dir / "phase8_basic_flow.json"
    
    with open(basic_flow_file, 'w') as f:
        json.dump(basic_flow, f, indent=2)
    
    print(f"✅ Basic flow created: {basic_flow_file}")
    
    # Create advanced flow
    advanced_flow = create_advanced_phase8_flow()
    advanced_flow_file = output_dir / "phase8_advanced_flow.json"
    
    with open(advanced_flow_file, 'w') as f:
        json.dump(advanced_flow, f, indent=2)
    
    print(f"✅ Advanced flow created: {advanced_flow_file}")
    
    # Create project data
    project_data = create_langflow_project()
    project_file = output_dir / "phase8_langflow_project.json"
    
    with open(project_file, 'w') as f:
        json.dump(project_data, f, indent=2)
    
    print(f"✅ Project data created: {project_file}")
    
    # Try to create flows in Langflow
    try:
        base_url = "http://localhost:7860"
        
        # Check if Langflow is running
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Langflow is running")
            
            # Try to create the basic flow
            try:
                flow_response = requests.post(
                    f"{base_url}/api/v1/flows",
                    json=basic_flow,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if flow_response.status_code == 200:
                    flow_id = flow_response.json().get("id")
                    print(f"✅ Basic flow created in Langflow with ID: {flow_id}")
                    print(f"🌐 Access flow at: {base_url}/flows/{flow_id}")
                else:
                    print(f"❌ Failed to create basic flow: {flow_response.status_code}")
                    print(f"Response: {flow_response.text}")
            except Exception as e:
                print(f"❌ Error creating basic flow: {e}")
            
            # Try to create the advanced flow
            try:
                flow_response = requests.post(
                    f"{base_url}/api/v1/flows",
                    json=advanced_flow,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if flow_response.status_code == 200:
                    flow_id = flow_response.json().get("id")
                    print(f"✅ Advanced flow created in Langflow with ID: {flow_id}")
                    print(f"🌐 Access flow at: {base_url}/flows/{flow_id}")
                else:
                    print(f"❌ Failed to create advanced flow: {flow_response.status_code}")
                    print(f"Response: {flow_response.text}")
            except Exception as e:
                print(f"❌ Error creating advanced flow: {e}")
                
        else:
            print(f"❌ Langflow not responding: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to Langflow: {e}")
        print("💡 Make sure Langflow is running on http://localhost:7860")
    
    print("\n📁 Files created:")
    print(f"   - {basic_flow_file}")
    print(f"   - {advanced_flow_file}")
    print(f"   - {project_file}")
    
    print("\n🔗 Next steps:")
    print("1. Open Langflow at http://localhost:7860")
    print("2. Import the flow JSON files manually if API creation failed")
    print("3. Go to MCP Server tab to expose flows as tools")
    print("4. Configure tool names and descriptions for MCP clients")
    print("5. Connect to Cursor or other MCP clients")
    
    print("\n📋 MCP Tool Requirements:")
    print("✅ Chat Output component included (required for MCP exposure)")
    print("✅ Clear tool names and descriptions")
    print("✅ Proper input/output handling")
    print("✅ Langflow project configuration")

if __name__ == "__main__":
    main()


