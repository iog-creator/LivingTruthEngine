---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['agents/agent.py', 'scripts/setup/extract_langflow_schemas_simple.py', 'logic/loop.py', 'logic/conditional_router.py', 'scripts/setup/generate_langflow_flow.py', 'config/langflow_schemas.json', 'input_output/chat.py', 'flows/living_truth_engine_flow.json', 'openai/openai_chat_model.py', 'agents/mcp_component.py']
---

# Langflow Schema-Based Flow Generation

## Overview

This document describes the schema-based approach for generating Langflow JSON flows using predefined component templates extracted from the local Langflow codebase.

## Architecture

### **Schema Extraction Process**

1. **Component Discovery**: Parse local Langflow component files in `/home/mccoy/Projects/NotebookLM/langflow/src/backend/base/langflow/components/`
2. **Template Extraction**: Extract component templates, inputs, and metadata using regex parsing
3. **Schema Generation**: Create JSON schemas that match Langflow's component structure
4. **Flow Generation**: Use extracted schemas to generate accurate flow JSON

### **Key Components**

| Component | File Path | Purpose |
|-----------|-----------|---------|
| ChatInput | `input_output/chat.py` | User input collection |
| ChatOutput | `input_output/chat.py` | Output display |
| Agent | `agents/agent.py` | Multi-agent orchestration |
| LLM | `openai/openai_chat_model.py` | Language model integration |
| Loop | `logic/loop.py` | Iterative processing |
| Condition | `logic/conditional_router.py` | Decision making |
| MCPComponent | `agents/mcp_component.py` | MCP tool integration |

## Implementation

### **1. Schema Extraction Script**

**File**: `scripts/setup/extract_langflow_schemas_simple.py`

```python
def parse_component_file(file_path: Path) -> Dict[str, Any]:
    """Parse a component file to extract template information."""
    # Extract class information, display_name, description, inputs
    # Create template structure for flow generation
```

**Features**:
- Regex-based parsing to avoid import dependencies
- Extracts component metadata (display_name, description, icon)
- Parses input definitions and creates template structure
- Handles multiple component types from different directories

### **2. Flow Generation Script**

**File**: `scripts/setup/generate_langflow_flow.py`

```python
def generate_living_truth_engine_flow(schemas: Dict[str, Any]) -> Dict[str, Any]:
    """Generate the Living Truth Engine flow JSON."""
    # Create nodes with unique IDs
    # Use extracted schemas for accurate templates
    # Define edges and flow structure
```

**Features**:
- Uses extracted schemas for accurate component templates
- Generates unique node IDs for proper flow structure
- Creates multi-agent system with Planner, SubAgents, Writer
- Integrates MCP tools and local model endpoints

### **3. Generated Schemas**

**File**: `config/langflow_schemas.json`

```json
{
  "ChatInput": {
    "display_name": "Chat Input",
    "description": "Get chat inputs from the Playground.",
    "icon": "MessagesSquare",
    "template": {
      "input_value": {
        "type": "str",
        "required": false,
        "default": "",
        "placeholder": "Input value"
      }
    }
  }
}
```

## Living Truth Engine Flow

### **Flow Structure**

```
Start (ChatInput) → LLM → Planner (Agent) → Iteration (Loop) → SubAgent (Agent) → Writer (Agent) → Condition → Loop/Output
```

### **Key Features**

1. **Multi-Agent Architecture**
   - **Planner**: High-level strategy and task delegation
   - **SubAgents**: Specialized research agents with tools
   - **Writer**: Report generation and synthesis

2. **MCP Integration**
   - Custom MCP tool for `mcp_hub_server_execute_tool`
   - Integration with 63+ underlying tools
   - Direct API calls to Langflow endpoints

3. **Local Model Integration**
   - Qwen3-8B for planning and writing
   - Qwen3-0.6B for subagent tasks
   - LM Studio on port 1234

4. **Vector Search**
   - pgVectorSearch with PostgreSQL
   - Elite network database integration
   - Entity relationship analysis

### **Flow Components**

| Node | Type | Purpose | Model |
|------|------|---------|-------|
| Start | ChatInput | Query input | - |
| LLM | LLM | Model initialization | Qwen3-8B |
| Planner | Agent | Task planning | Qwen3-8B |
| Iteration | Loop | Subagent spawning | - |
| SubAgent | Agent | Research execution | Qwen3-0.6B |
| Writer | Agent | Report generation | Qwen3-8B |
| Condition | Condition | Decision making | Qwen3-0.6B |
| Loop | Loop | Iterative refinement | - |
| Output | ChatOutput | Final report | - |

## Usage

### **1. Extract Schemas**

```bash
python3 scripts/setup/extract_langflow_schemas_simple.py
```

**Output**: `config/langflow_schemas.json`

### **2. Generate Flow**

```bash
python3 scripts/setup/generate_langflow_flow.py
```

**Output**: `flows/living_truth_engine_flow.json`

### **3. Import Flow**

```bash
python3 scripts/setup/import_langflow_flow.py
```

**Output**: Flow imported to Langflow with unique ID

### **4. Access Flow**

- **URL**: http://localhost:7860/flows/90d0cc9d-d590-4734-813e-5664c95f907a
- **Login**: admin/admin
- **Test Query**: "Investigate Entity A connections, output as network"

## Advantages

### **1. Accuracy**
- Uses actual Langflow component schemas
- Matches local Langflow version exactly
- No manual template construction

### **2. Maintainability**
- Automatic schema updates when Langflow changes
- Version-controlled component definitions
- Reproducible flow generation

### **3. Compatibility**
- Works with local Langflow codebase
- No external dependencies
- Handles component structure changes

### **4. Flexibility**
- Easy to modify component mappings
- Supports custom component types
- Extensible for new components

## Troubleshooting

### **Common Issues**

1. **Schema Extraction Fails**
   - Check Langflow path: `/home/mccoy/Projects/NotebookLM/langflow`
   - Verify component files exist
   - Check file permissions

2. **Flow Import Fails**
   - Verify Langflow is running on port 7860
   - Check `LANGFLOW_API_KEY` environment variable
   - Validate JSON structure

3. **Component Not Found**
   - Update component mappings in extraction script
   - Check Langflow version compatibility
   - Verify component file paths

### **Debugging**

```bash
# Check Langflow health
curl -s http://localhost:7860/health | jq .

# Validate JSON
python3 -m json.tool flows/living_truth_engine_flow.json

# Test API connection
python3 scripts/setup/test_langflow_api.py
```

## Future Enhancements

### **1. Enhanced Schema Extraction**
- Support for more component types
- Better input parsing
- Validation of extracted schemas

### **2. Flow Templates**
- Predefined flow patterns
- Template customization
- Flow composition tools

### **3. Integration Improvements**
- Better MCP tool integration
- Enhanced error handling
- Performance optimization

### **4. Documentation**
- Component reference guide
- Flow design patterns
- Best practices documentation

## Conclusion

The schema-based approach provides a robust, maintainable solution for generating Langflow flows that accurately reflect the local component structure. This ensures compatibility and reduces manual configuration errors while providing a foundation for future enhancements. 