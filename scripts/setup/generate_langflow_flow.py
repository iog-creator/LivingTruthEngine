#!/usr/bin/env python3
"""
Generate Living Truth Engine Langflow Flow
=========================================

Generate a Langflow JSON flow using extracted component schemas
for the Living Truth Engine multi-agent system.
"""

import json
import uuid
from pathlib import Path
from typing import Dict, Any, List

def load_schemas(schemas_path: str) -> Dict[str, Any]:
    """Load extracted component schemas."""
    
    with open(schemas_path, 'r') as f:
        return json.load(f)

def create_node_template(component_name: str, schemas: Dict[str, Any]) -> Dict[str, Any]:
    """Create a node template using extracted schemas."""
    
    if component_name not in schemas:
        # Fallback template
        return {
            "template": {
                "input_value": {
                    "type": "str",
                    "required": False,
                    "default": "",
                    "placeholder": "Input value"
                }
            }
        }
    
    component_schema = schemas[component_name]
    template = component_schema.get("template", {})
    
    # Add default template if empty
    if not template:
        template = {
            "input_value": {
                "type": "str",
                "required": False,
                "default": "",
                "placeholder": "Input value"
            }
        }
    
    return {
        "template": template
    }

def generate_living_truth_engine_flow(schemas: Dict[str, Any]) -> Dict[str, Any]:
    """Generate the Living Truth Engine flow JSON."""
    
    # Generate unique IDs for nodes
    node_ids = {
        "start": f"start-{uuid.uuid4().hex[:8]}",
        "chatlocalai": f"llm-{uuid.uuid4().hex[:8]}",
        "planner": f"agent-{uuid.uuid4().hex[:8]}",
        "iteration": f"iteration-{uuid.uuid4().hex[:8]}",
        "subagent": f"subagent-{uuid.uuid4().hex[:8]}",
        "writer": f"writer-{uuid.uuid4().hex[:8]}",
        "condition": f"condition-{uuid.uuid4().hex[:8]}",
        "loop": f"loop-{uuid.uuid4().hex[:8]}",
        "output": f"output-{uuid.uuid4().hex[:8]}"
    }
    
    # Create nodes
    nodes = [
        {
            "id": node_ids["start"],
            "type": "ChatInput",
            "data": {
                "label": "Start",
                "node": {
                    "template": {
                        "input_value": {
                            "type": "str",
                            "required": True,
                            "placeholder": "Enter query (e.g., transcript, entity list)"
                        },
                        "anonymize": {
                            "type": "bool",
                            "required": False,
                            "default": False
                        },
                        "output_type": {
                            "type": "str",
                            "required": False,
                            "default": "summary",
                            "options": ["summary", "network", "timeline", "audio"]
                        }
                    },
                    "display_name": "Chat Input"
                }
            },
            "position": {"x": -240, "y": 85}
        },
        {
            "id": node_ids["chatlocalai"],
            "type": "LLM",
            "data": {
                "label": "ChatLocalAI (Qwen3-8B)",
                "node": {
                    "template": {
                        "model_name": {"type": "str", "required": True, "value": "Qwen3-8B"},
                        "api_endpoint": {"type": "str", "required": True, "value": "http://localhost:1234/v1"},
                        "temperature": {"type": "float", "required": False, "value": 0.7},
                        "max_tokens": {"type": "int", "required": False, "value": 512}
                    },
                    "display_name": "OpenAI"
                }
            },
            "position": {"x": -150, "y": 200}
        },
        {
            "id": node_ids["planner"],
            "type": "Agent",
            "data": {
                "label": "Planner",
                "node": {
                    "template": {
                        "model": {"type": "str", "required": True, "value": "Qwen3-8B"},
                        "system_prompt": {
                            "type": "str",
                            "required": True,
                            "value": "You are an expert research lead focused on high-level strategy, planning, and efficient delegation to subagents for uncovering elite networks and entity relationships. Current date: 08/03/2025. <research_process>1. Assess query: Identify key entities, relationships, required data. Note output_type. 2. Classify query: Depth-first, Breadth-first, or Straightforward. 3. Plan: Allocate tasks to subagents, define boundaries, synthesis methods. 4. Execute: Deploy subagents via MCP tools, monitor, adapt.</research_process><delegation_instructions>Use mcp_hub_server_execute_tool for tools like query_langflow. Avoid overlap, synthesize results.</delegation_instructions><answer_formatting>Output JSON array of subagent tasks in Markdown.</answer_formatting>"
                        },
                        "user_prompt": {
                            "type": "str",
                            "required": True,
                            "value": "Query: {{ query }}\nAnonymize: {{ anonymize }}\nOutput Type: {{ output_type }}"
                        }
                    },
                    "display_name": "Model Provider"
                }
            },
            "position": {"x": -111, "y": 83}
        },
        {
            "id": node_ids["iteration"],
            "type": "Loop",
            "data": {
                "label": "Spawn SubAgents",
                "node": {
                    "template": {
                        "input": {"type": "str", "required": True, "value": "{{ planner.output }}"}
                    },
                    "display_name": "Loop"
                }
            },
            "position": {"x": 126, "y": -5}
        },
        {
            "id": node_ids["subagent"],
            "type": "Agent",
            "data": {
                "label": "SubAgent",
                "node": {
                    "template": {
                        "model": {"type": "str", "required": True, "value": "Qwen3-0.6B"},
                        "system_prompt": {
                            "type": "str",
                            "required": True,
                            "value": "You are a research subagent for uncovering elite networks. Date: 08/03/2025. Task: {{ iteration.task }}. <research_process>1. Plan: Budget 2-5 tool calls. 2. Tools: Use mcp_hub_server_execute_tool (query_langflow, analyze_transcript, list_sources, generate_viz), BraveSearch, WebScraper, pgVectorSearch (elite_network_db, Qwen3-0.6B). 3. OODA loop: Execute at least two tool calls.</research_process><research_guidelines>Focus on high-value data, flag conflicts.</research_guidelines>"
                        },
                        "tools": [
                            {"type": "BraveSearch"},
                            {"type": "WebScraper", "maxDepth": 1, "maxPages": 2},
                            {
                                "type": "Custom",
                                "name": "MCPTool",
                                "code": "import requests\ndef mcp_tool(tool_name: str, params: dict) -> str:\n    response = requests.post('http://localhost:7860/execute', json={'tool': tool_name, 'params': params}, headers={'x-api-key': '${LANGFLOW_API_KEY}'})\n    return response.text"
                            },
                            {
                                "type": "VectorStore",
                                "vectorStore": "elite_network_db",
                                "embeddingModel": "Qwen3-0.6B",
                                "knowledgeName": "Entity Relationships",
                                "returnSourceDocuments": True
                            }
                        ]
                    },
                    "display_name": "Model Provider"
                }
            },
            "position": {"x": 53, "y": 77}
        },
        {
            "id": node_ids["writer"],
            "type": "Agent",
            "data": {
                "label": "Writer Agent",
                "node": {
                    "template": {
                        "model": {"type": "str", "required": True, "value": "Qwen3-8B"},
                        "system_prompt": {
                            "type": "str",
                            "required": True,
                            "value": "Generate a high-quality Markdown report from research findings for uncovering elite networks. Preserve context, structure with headings, match output_type (summary, network, timeline, audio). Anonymize if requested. Style: analytical, objective."
                        },
                        "user_prompt": {
                            "type": "str",
                            "required": True,
                            "value": "<query>{{ query }}</query><findings>{{ subagent_outputs }}</findings><anonymize>{{ anonymize }}</anonymize><output_type>{{ output_type }}</output_type>"
                        }
                    },
                    "display_name": "Model Provider"
                }
            },
            "position": {"x": 457, "y": 83}
        },
        {
            "id": node_ids["condition"],
            "type": "Condition",
            "data": {
                "label": "More SubAgents?",
                "node": {
                    "template": {
                        "model": {"type": "str", "required": True, "value": "Qwen3-0.6B"},
                        "instruction": {
                            "type": "str",
                            "required": True,
                            "value": "Determine if more subagents are needed based on query, subagent outputs, and findings"
                        },
                        "input": {
                            "type": "str",
                            "required": True,
                            "value": "<query>{{ query }}</query><subagents>{{ planner.output }}</subagents><findings>{{ writer.output }}</findings><anonymize>{{ anonymize }}</anonymize><output_type>{{ output_type }}</output_type>"
                        },
                        "conditions": ["More subagents needed", "Findings sufficient"]
                    },
                    "display_name": "If-Else"
                }
            },
            "position": {"x": 775, "y": 79}
        },
        {
            "id": node_ids["loop"],
            "type": "Loop",
            "data": {
                "label": "Back to Planner",
                "node": {
                    "template": {
                        "target": {"type": "str", "required": True, "value": node_ids["planner"]},
                        "max_iterations": {"type": "int", "required": False, "value": 5}
                    },
                    "display_name": "Loop"
                }
            },
            "position": {"x": 1041, "y": 20}
        },
        {
            "id": node_ids["output"],
            "type": "ChatOutput",
            "data": {
                "label": "Generate Report",
                "node": {
                    "template": {
                        "input_value": {"type": "str", "required": True, "value": "{{ writer.output }}"}
                    },
                    "display_name": "Chat Input"
                }
            },
            "position": {"x": 1046, "y": 140}
        }
    ]
    
    # Create edges
    edges = [
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["start"],
            "target": node_ids["chatlocalai"],
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["chatlocalai"],
            "target": node_ids["planner"],
            "sourceHandle": "output",
            "targetHandle": "model"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["start"],
            "target": node_ids["planner"],
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["planner"],
            "target": node_ids["iteration"],
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["iteration"],
            "target": node_ids["writer"],
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["writer"],
            "target": node_ids["condition"],
            "sourceHandle": "output",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["condition"],
            "target": node_ids["loop"],
            "sourceHandle": "More subagents needed",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["condition"],
            "target": node_ids["output"],
            "sourceHandle": "Findings sufficient",
            "targetHandle": "input"
        },
        {
            "id": f"edge-{uuid.uuid4().hex[:8]}",
            "source": node_ids["loop"],
            "target": node_ids["planner"],
            "sourceHandle": "output",
            "targetHandle": "input"
        }
    ]
    
    # Create the flow
    flow = {
        "name": "Living Truth Engine Flow",
        "description": "Multi-agent system for investigative research, uncovering elite networks with MCP Hub Server tools",
        "data": {
            "nodes": nodes,
            "edges": edges
        }
    }
    
    return flow

def save_flow(flow: Dict[str, Any], output_path: str) -> None:
    """Save the generated flow to JSON file."""
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(flow, f, indent=2)
    
    print(f"💾 Flow saved to: {output_file}")

def main():
    """Main function to generate the Living Truth Engine flow."""
    
    print("🚀 Living Truth Engine Flow Generation")
    print("=" * 50)
    
    # Load schemas
    schemas_path = "config/langflow_schemas.json"
    if not Path(schemas_path).exists():
        print(f"❌ Schemas file not found: {schemas_path}")
        print("Please run extract_langflow_schemas_simple.py first")
        return
    
    print(f"📦 Loading schemas from: {schemas_path}")
    schemas = load_schemas(schemas_path)
    print(f"✅ Loaded {len(schemas)} component schemas")
    
    # Generate flow
    print("\n🔧 Generating Living Truth Engine flow...")
    flow = generate_living_truth_engine_flow(schemas)
    
    # Save flow
    output_path = "flows/living_truth_engine_flow.json"
    save_flow(flow, output_path)
    
    print(f"\n✅ Flow generated successfully!")
    print(f"📋 Nodes: {len(flow['data']['nodes'])}")
    print(f"🔗 Edges: {len(flow['data']['edges'])}")
    print(f"📁 Output: {output_path}")
    print("\n🎯 Ready for import into Langflow!")

if __name__ == "__main__":
    main() 