# Phase 8 Langflow Setup Guide for MCP Integration

This guide will help you set up the Phase 8 real data ingestion pipeline flows in Langflow and expose them as MCP tools.

## 🎯 Overview

Based on the [Langflow MCP server documentation](https://docs.langflow.org/mcp-server), we need to:
1. Import the Phase 8 flows into Langflow
2. Ensure they have **Chat Output** components (required for MCP exposure)
3. Configure the MCP server to expose the flows as tools
4. Connect to Cursor or other MCP clients

## 📁 Files Created

The following files have been created in `data/visualizations/`:

- `phase8_basic_flow.json` - Basic Phase 8 pipeline with single input
- `phase8_advanced_flow.json` - Advanced Phase 8 pipeline with configurable parameters
- `phase8_langflow_project.json` - Complete project structure
- `phase8_pipeline_visualization.html` - HTML visualization of the pipeline

## 🔧 Step-by-Step Setup

### Step 1: Access Langflow

1. Open your browser and go to: **http://localhost:7860**
2. Login with: **admin/admin**
3. You should see the Langflow dashboard

### Step 2: Import Phase 8 Flows

#### Option A: Manual Import (Recommended)

1. **Create New Project**:
   - Click "Create New Project"
   - Name it: "Phase 8 Real Data Ingestion"
   - Description: "YouTube channel ingestion with depth-limited expansion and verifiable bundles"

2. **Import Basic Flow**:
   - Click "Import Flow"
   - Select the file: `data/visualizations/phase8_basic_flow.json`
   - The flow should appear with:
     - Input Node: YouTube Channel URL
     - LLM Chain: Phase 8 Pipeline Processor
     - Chat Output: Phase 8 Pipeline Results

3. **Import Advanced Flow**:
   - Click "Import Flow" again
   - Select the file: `data/visualizations/phase8_advanced_flow.json`
   - This flow has multiple inputs and more detailed processing

#### Option B: Copy-Paste Flow Data

If manual import doesn't work, you can create the flows manually:

1. **Create Basic Flow**:
   - Click "Create New Flow"
   - Name it: "Phase 8 Basic Pipeline"
   - Add components from the left sidebar:
     - Input Node (for YouTube Channel URL)
     - LLM Chain (for processing)
     - Chat Output (REQUIRED for MCP)

2. **Configure Components**:
   - Input Node: Set type to "str", name to "text"
   - LLM Chain: Configure with the prompt template from the JSON
   - Chat Output: Connect to LLM Chain output

### Step 3: Configure MCP Server

1. **Access MCP Server Tab**:
   - In your Langflow project, click the **"MCP Server"** tab
   - Or go to any flow and click **"Share > MCP Server"**

2. **Edit Tools**:
   - Click **"Edit Tools"**
   - Select the flows you want to expose as MCP tools
   - Recommended: Enable both "Phase 8 Basic Pipeline" and "Phase 8 Advanced Pipeline"

3. **Configure Tool Names and Descriptions**:

   **For Basic Pipeline:**
   - **Tool Name**: `phase8_basic_ingestion`
   - **Tool Description**: `Process YouTube channel ingestion with basic parameters. Input: YouTube channel URL. Output: Detailed pipeline processing summary and expected bundle structure.`

   **For Advanced Pipeline:**
   - **Tool Name**: `phase8_advanced_ingestion`
   - **Tool Description**: `Advanced YouTube channel ingestion with configurable parameters (max videos, crawl depth). Input: Channel URL, max videos, crawl depth. Output: Comprehensive processing summary with bundle details.`

4. **Save Configuration**:
   - Close the "MCP Server Tools" window
   - Your changes will be saved automatically

### Step 4: Connect to Cursor

1. **Get MCP Configuration**:
   - In the MCP Server tab, copy the JSON configuration from the **"JSON"** tab
   - It should look like:
   ```json
   {
     "mcpServers": {
       "PHASE_8_PROJECT": {
         "command": "uvx",
         "args": [
           "mcp-proxy",
           "http://localhost:7860/api/v1/mcp/project/YOUR_PROJECT_ID/sse"
         ]
       }
     }
   }
   ```

2. **Add to Cursor**:
   - In Cursor, go to **Cursor Settings > MCP**
   - Click **"Add New Global MCP Server"**
   - Paste the JSON configuration
   - Save the file

3. **Verify Connection**:
   - Restart Cursor if needed
   - Check that the MCP server appears in the MCP Servers section
   - You should see green dots indicating successful connection

### Step 5: Test the MCP Tools

1. **In Cursor**, try asking:
   ```
   Use the Phase 8 ingestion pipeline to process the Imagination Station YouTube channel
   ```

2. **The agent should**:
   - Recognize the available Phase 8 tools
   - Ask permission to use the appropriate tool
   - Execute the flow and return results

## 🔍 Flow Details

### Basic Flow Structure
```
Input Node (YouTube Channel URL) 
    ↓
LLM Chain (Phase 8 Pipeline Processor)
    ↓
Chat Output (Results)
```

### Advanced Flow Structure
```
Input Node (Channel URL)     Input Node (Max Videos)     Input Node (Crawl Depth)
    ↓                              ↓                           ↓
Text Combiner (Combine Parameters)
    ↓
LLM Chain (Advanced Phase 8 Processor)
    ↓
Chat Output (Detailed Results)
```

## 📋 MCP Tool Requirements Met

✅ **Chat Output Component**: Both flows include Chat Output (required for MCP exposure)
✅ **Clear Tool Names**: Descriptive names for agent understanding
✅ **Detailed Descriptions**: Explain what each tool does and when to use it
✅ **Proper Input/Output**: Structured data flow with clear connections
✅ **Project Configuration**: Proper Langflow project setup

## 🎯 Expected Behavior

When you ask Cursor to use the Phase 8 pipeline:

1. **Tool Selection**: Agent recognizes the appropriate Phase 8 tool
2. **Permission Request**: Agent asks permission to use the tool
3. **Flow Execution**: Langflow processes the request through the pipeline
4. **Results**: Returns detailed summary of what would be processed

## 🔧 Troubleshooting

### If flows don't appear in MCP tools:
- Ensure Chat Output component is present
- Check that flows are enabled in MCP Server configuration
- Verify tool names and descriptions are set

### If Cursor can't connect:
- Check that Langflow is running on http://localhost:7860
- Verify the project ID in the MCP configuration
- Ensure the JSON configuration is properly formatted

### If tools don't work as expected:
- Test the flows manually in Langflow first
- Check the LLM configuration in the flows
- Verify input/output connections

## 📊 Success Indicators

✅ **Langflow**: Flows imported and working
✅ **MCP Server**: Tools configured and exposed
✅ **Cursor**: MCP server connected (green dots)
✅ **Tool Usage**: Agent can use Phase 8 tools when appropriate
✅ **Results**: Detailed pipeline processing summaries returned

## 🎉 Next Steps

Once the MCP tools are working:

1. **Test with real requests**: Ask Cursor to process different YouTube channels
2. **Customize flows**: Modify the prompts or add more components
3. **Add more tools**: Create additional flows for specific use cases
4. **Deploy externally**: Use ngrok for public access if needed

---

**Status**: ✅ Phase 8 Langflow flows created with proper MCP integration
**Files**: All required JSON files and documentation created
**Next**: Follow this guide to import and configure in Langflow


