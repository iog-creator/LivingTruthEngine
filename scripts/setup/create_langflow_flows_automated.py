#!/usr/bin/env python3
"""
Automated Langflow Flow Creation for Phase 8

This script automatically creates Phase 8 flows in Langflow using the proper API endpoints
and then configures them for MCP integration.
"""

import json
import requests
import time
from pathlib import Path

def create_langflow_flow(flow_data):
    """Create a flow in Langflow using the proper API endpoint."""
    
    base_url = "http://localhost:7860"
    
    # First, get the project ID
    try:
        projects_response = requests.get(f"{base_url}/api/v1/projects", timeout=10)
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if projects:
                project_id = projects[0]['id']  # Use first project
                print(f"✅ Using project ID: {project_id}")
            else:
                # Create a new project if none exists
                project_data = {
                    "name": "Phase 8 Real Data Ingestion",
                    "description": "YouTube channel ingestion with depth-limited expansion and verifiable bundles"
                }
                project_response = requests.post(
                    f"{base_url}/api/v1/projects",
                    json=project_data,
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                if project_response.status_code == 200:
                    project_id = project_response.json()['id']
                    print(f"✅ Created new project with ID: {project_id}")
                else:
                    print(f"❌ Failed to create project: {project_response.status_code}")
                    return None
        else:
            print(f"❌ Failed to get projects: {projects_response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting project: {e}")
        return None
    
    # Now create the flow in the project
    try:
        flow_response = requests.post(
            f"{base_url}/api/v1/projects/{project_id}/flows",
            json=flow_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if flow_response.status_code == 200:
            flow_id = flow_response.json()['id']
            print(f"✅ Flow created with ID: {flow_id}")
            return flow_id
        else:
            print(f"❌ Failed to create flow: {flow_response.status_code}")
            print(f"Response: {flow_response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating flow: {e}")
        return None

def create_phase8_basic_flow():
    """Create the basic Phase 8 flow."""
    
    flow_data = {
        "name": "Phase 8 Basic Pipeline",
        "description": "Basic YouTube channel ingestion with single input",
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
    
    return flow_data

def create_phase8_advanced_flow():
    """Create the advanced Phase 8 flow."""
    
    flow_data = {
        "name": "Phase 8 Advanced Pipeline",
        "description": "Advanced YouTube channel ingestion with configurable parameters",
        "data": {
            "nodes": [
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
                {
                    "id": "phase8_processor",
                    "type": "LLMChain",
                    "data": {
                        "node": {
                            "template": {
                                "name": "llm_chain",
                                "display_name": "Phase 8 Advanced Processor",
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

Process this request through the Phase 8 pipeline with the following configuration:

**Configuration:**
- Channel URL: {channel_url}
- Max Videos: {max_videos}
- Crawl Depth: {crawl_depth}

**Phase 8 Pipeline Stages:**

1. **YouTube Channel Discovery**
   - Use yt-dlp to discover videos from the channel
   - Sort by oldest/newest/custom order
   - Limit to {max_videos} videos

2. **Transcript Extraction**
   - Extract transcripts using YouTube Transcript API
   - Fallback to autosubs if API fails
   - Process all discovered videos

3. **URL Extraction**
   - Use regex patterns to extract URLs from transcripts
   - Extract URLs from video descriptions
   - Validate and filter URLs

4. **Depth-Limited Expansion**
   - Expand external links up to depth {crawl_depth}
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

def get_mcp_configuration():
    """Get the MCP configuration for the project."""
    
    base_url = "http://localhost:7860"
    
    try:
        # Get projects
        projects_response = requests.get(f"{base_url}/api/v1/projects", timeout=10)
        if projects_response.status_code == 200:
            projects = projects_response.json()
            if projects:
                project_id = projects[0]['id']
                
                # Get MCP configuration
                mcp_response = requests.get(f"{base_url}/api/v1/projects/{project_id}/mcp", timeout=10)
                if mcp_response.status_code == 200:
                    mcp_config = mcp_response.json()
                    return mcp_config, project_id
                else:
                    print(f"❌ Failed to get MCP config: {mcp_response.status_code}")
                    return None, project_id
            else:
                print("❌ No projects found")
                return None, None
        else:
            print(f"❌ Failed to get projects: {projects_response.status_code}")
            return None, None
    except Exception as e:
        print(f"❌ Error getting MCP configuration: {e}")
        return None, None

def main():
    """Main function to create Phase 8 flows in Langflow."""
    
    print("🎯 Creating Phase 8 Flows in Langflow...")
    
    # Create basic flow
    print("\n📝 Creating Basic Phase 8 Flow...")
    basic_flow_data = create_phase8_basic_flow()
    basic_flow_id = create_langflow_flow(basic_flow_data)
    
    if basic_flow_id:
        print(f"✅ Basic flow created successfully: {basic_flow_id}")
    else:
        print("❌ Failed to create basic flow")
    
    # Wait a moment
    time.sleep(2)
    
    # Create advanced flow
    print("\n📝 Creating Advanced Phase 8 Flow...")
    advanced_flow_data = create_phase8_advanced_flow()
    advanced_flow_id = create_langflow_flow(advanced_flow_data)
    
    if advanced_flow_id:
        print(f"✅ Advanced flow created successfully: {advanced_flow_id}")
    else:
        print("❌ Failed to create advanced flow")
    
    # Get MCP configuration
    print("\n🔧 Getting MCP Configuration...")
    mcp_config, project_id = get_mcp_configuration()
    
    if mcp_config and project_id:
        print(f"✅ MCP configuration retrieved for project: {project_id}")
        
        # Save MCP configuration
        output_dir = Path("data/visualizations")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        mcp_file = output_dir / "langflow_mcp_config.json"
        with open(mcp_file, 'w') as f:
            json.dump(mcp_config, f, indent=2)
        
        print(f"✅ MCP configuration saved to: {mcp_file}")
        
        # Create Cursor MCP configuration
        cursor_config = {
            "mcpServers": {
                "phase8_langflow": {
                    "command": "uvx",
                    "args": [
                        "mcp-proxy",
                        f"http://localhost:7860/api/v1/mcp/project/{project_id}/sse"
                    ]
                }
            }
        }
        
        cursor_file = output_dir / "cursor_mcp_config.json"
        with open(cursor_file, 'w') as f:
            json.dump(cursor_config, f, indent=2)
        
        print(f"✅ Cursor MCP configuration saved to: {cursor_file}")
        
        print(f"\n🔗 Access your flows:")
        print(f"   Langflow: http://localhost:7860")
        print(f"   Project ID: {project_id}")
        print(f"   Basic Flow ID: {basic_flow_id}")
        print(f"   Advanced Flow ID: {advanced_flow_id}")
        
        print(f"\n📋 Next Steps:")
        print(f"1. Open Langflow at http://localhost:7860")
        print(f"2. Go to MCP Server tab in your project")
        print(f"3. Configure tool names and descriptions")
        print(f"4. Copy the MCP configuration to Cursor")
        
    else:
        print("❌ Failed to get MCP configuration")
    
    print(f"\n🎉 Phase 8 Flow Creation Complete!")

if __name__ == "__main__":
    main()


