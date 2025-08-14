---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['cursor_mcp_config.json', 'data/visualizations/phase8_flow_for_import.json', 'phase8_flow_for_import.json']
---


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
