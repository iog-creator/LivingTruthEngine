#!/usr/bin/env python3
"""
Create Phase 8 Flow in Langflow

This script creates an actual Langflow flow that demonstrates the Phase 8
real data ingestion pipeline using Langflow's API.
"""

import json
import requests
from pathlib import Path

def create_langflow_flow():
    """Create a Langflow flow for Phase 8 real data ingestion."""
    
    # Langflow API endpoint
    base_url = "http://localhost:7860"
    
    # Flow configuration
    flow_data = {
        "name": "Phase 8 Real Data Ingestion Pipeline",
        "description": "Visual representation of YouTube channel ingestion with depth-limited expansion and verifiable bundles",
        "data": {
            "nodes": [
                # Input nodes
                {
                    "id": "input_channel_url",
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
                    "id": "input_max_videos",
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
                    "id": "input_crawl_depth",
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
                
                # Process nodes
                {
                    "id": "youtube_discovery",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "youtube_discovery",
                                "display_name": "YouTube Channel Discovery",
                                "description": "Discover videos from YouTube channel using yt-dlp"
                            }
                        }
                    },
                    "position": {"x": 300, "y": 150}
                },
                {
                    "id": "transcript_extraction",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "transcript_extraction",
                                "display_name": "Transcript Extraction",
                                "description": "Extract transcripts using YouTube Transcript API"
                            }
                        }
                    },
                    "position": {"x": 500, "y": 150}
                },
                {
                    "id": "url_extraction",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "url_extraction",
                                "display_name": "URL Extraction",
                                "description": "Extract URLs from transcripts and descriptions"
                            }
                        }
                    },
                    "position": {"x": 700, "y": 150}
                },
                {
                    "id": "depth_expansion",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "depth_expansion",
                                "display_name": "Depth-Limited Expansion",
                                "description": "Expand external links up to specified depth"
                            }
                        }
                    },
                    "position": {"x": 900, "y": 150}
                },
                {
                    "id": "content_fetching",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "content_fetching",
                                "display_name": "Content Fetching",
                                "description": "Fetch web content and PDFs with optional OCR"
                            }
                        }
                    },
                    "position": {"x": 1100, "y": 150}
                },
                {
                    "id": "canonicalization",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "canonicalization",
                                "display_name": "Canonicalization",
                                "description": "Convert all content to standardized JSONL format"
                            }
                        }
                    },
                    "position": {"x": 1300, "y": 150}
                },
                {
                    "id": "provenance_generation",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "provenance_generation",
                                "display_name": "Provenance Generation",
                                "description": "Generate SHA-256 proofs and Merkle tree"
                            }
                        }
                    },
                    "position": {"x": 1500, "y": 150}
                },
                {
                    "id": "bundle_creation",
                    "type": "CustomComponent",
                    "data": {
                        "node": {
                            "template": {
                                "name": "bundle_creation",
                                "display_name": "Bundle Creation",
                                "description": "Create .veritasrun bundle with all components"
                            }
                        }
                    },
                    "position": {"x": 1700, "y": 150}
                },
                
                # Output nodes
                {
                    "id": "bundle_summary",
                    "type": "OutputNode",
                    "data": {
                        "node": {
                            "template": {
                                "name": "bundle_summary",
                                "display_name": "Bundle Summary",
                                "description": "Summary of created bundle with statistics"
                            }
                        }
                    },
                    "position": {"x": 1900, "y": 100}
                },
                {
                    "id": "bundle_location",
                    "type": "OutputNode",
                    "data": {
                        "node": {
                            "template": {
                                "name": "bundle_location",
                                "display_name": "Bundle Location",
                                "description": "File path to the created .veritasrun bundle"
                            }
                        }
                    },
                    "position": {"x": 1900, "y": 200}
                }
            ],
            "edges": [
                # Input connections
                {
                    "source": "input_channel_url",
                    "target": "youtube_discovery",
                    "sourceHandle": "channel_url",
                    "targetHandle": "input"
                },
                {
                    "source": "input_max_videos",
                    "target": "youtube_discovery",
                    "sourceHandle": "max_videos",
                    "targetHandle": "input"
                },
                {
                    "source": "input_crawl_depth",
                    "target": "depth_expansion",
                    "sourceHandle": "crawl_depth",
                    "targetHandle": "input"
                },
                
                # Process flow
                {
                    "source": "youtube_discovery",
                    "target": "transcript_extraction",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "transcript_extraction",
                    "target": "url_extraction",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "url_extraction",
                    "target": "depth_expansion",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "depth_expansion",
                    "target": "content_fetching",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "content_fetching",
                    "target": "canonicalization",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "canonicalization",
                    "target": "provenance_generation",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "provenance_generation",
                    "target": "bundle_creation",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                
                # Output connections
                {
                    "source": "bundle_creation",
                    "target": "bundle_summary",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                },
                {
                    "source": "bundle_creation",
                    "target": "bundle_location",
                    "sourceHandle": "output",
                    "targetHandle": "input"
                }
            ]
        }
    }
    
    return flow_data

def create_simple_langflow_flow():
    """Create a simpler Langflow flow using basic components."""
    
    # Simple flow with basic Langflow components
    flow_data = {
        "name": "Phase 8 Real Data Ingestion Pipeline",
        "description": "Visual representation of YouTube channel ingestion pipeline",
        "data": {
            "nodes": [
                # Input
                {
                    "id": "input_text",
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
                                "description": "Process YouTube channel ingestion pipeline"
                            }
                        }
                    },
                    "position": {"x": 300, "y": 100}
                },
                
                # Output
                {
                    "id": "output_text",
                    "type": "OutputNode",
                    "data": {
                        "node": {
                            "template": {
                                "name": "text",
                                "display_name": "Bundle Summary",
                                "description": "Summary of created bundle"
                            }
                        }
                    },
                    "position": {"x": 500, "y": 100}
                }
            ],
            "edges": [
                {
                    "source": "input_text",
                    "target": "llm_chain",
                    "sourceHandle": "text",
                    "targetHandle": "input"
                },
                {
                    "source": "llm_chain",
                    "target": "output_text",
                    "sourceHandle": "output",
                    "targetHandle": "text"
                }
            ]
        }
    }
    
    return flow_data

def main():
    """Main function to create the Langflow flow."""
    
    print("🎯 Creating Phase 8 Langflow Flow...")
    
    # Create output directory
    output_dir = Path("data/visualizations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create flow data
    flow_data = create_simple_langflow_flow()
    flow_file = output_dir / "phase8_langflow_flow.json"
    
    with open(flow_file, 'w') as f:
        json.dump(flow_data, f, indent=2)
    
    print(f"✅ Langflow flow data created: {flow_file}")
    
    # Try to create the flow in Langflow
    try:
        base_url = "http://localhost:7860"
        
        # Check if Langflow is running
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Langflow is running")
            
            # Create flow via API
            flow_response = requests.post(
                f"{base_url}/api/v1/flows",
                json=flow_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if flow_response.status_code == 200:
                flow_id = flow_response.json().get("id")
                print(f"✅ Flow created in Langflow with ID: {flow_id}")
                print(f"🌐 Access flow at: {base_url}/flows/{flow_id}")
            else:
                print(f"❌ Failed to create flow: {flow_response.status_code}")
                print(f"Response: {flow_response.text}")
        else:
            print(f"❌ Langflow not responding: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to Langflow: {e}")
        print("💡 Make sure Langflow is running on http://localhost:7860")
    
    print("\n📁 Files created:")
    print(f"   - {flow_file}")
    print(f"   - {output_dir}/phase8_pipeline_visualization.html")
    print(f"   - {output_dir}/phase8_flow.json")
    print(f"   - {output_dir}/phase8_sample_bundle.json")
    
    print("\n🔗 Access visualizations:")
    print(f"   HTML: file://{output_dir.absolute()}/phase8_pipeline_visualization.html")
    print(f"   Langflow: http://localhost:7860 (if flow was created successfully)")

if __name__ == "__main__":
    main()


