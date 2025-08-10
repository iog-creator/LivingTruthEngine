
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
