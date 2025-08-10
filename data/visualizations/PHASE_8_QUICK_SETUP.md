# Phase 8 Quick Setup Guide

## 🎯 What You Need to Do

Since you can see the MCP server tools in Langflow, here's how to create the Phase 8 flow:

### Step 1: Create the Flow in Langflow
1. **Open Langflow** at http://localhost:7860
2. **Create a new project**: "Phase 8 Real Data Ingestion"
3. **Create a new flow**: "Phase 8 Pipeline"

### Step 2: Add Components
From the left sidebar, add these components:

1. **Input Node**:
   - Type: `str`
   - Name: `text`
   - Display Name: `YouTube Channel URL`
   - Value: `https://www.youtube.com/@imaginationpodcastofficial`

2. **LLM Chain**:
   - Display Name: `Phase 8 Pipeline Processor`
   - Description: `Process YouTube channel ingestion pipeline`
   - LLM: Choose your preferred model (OpenAI, LM Studio, etc.)
   - Temperature: `0.7`

3. **Chat Output**:
   - Display Name: `Phase 8 Pipeline Results`
   - Description: `Output the Phase 8 pipeline processing results`

### Step 3: Configure the LLM Chain Prompt
Set this prompt template in the LLM Chain:

```
You are a Phase 8 Real Data Ingestion Pipeline processor.

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
JS Render: false (default)
```

### Step 4: Connect the Components
1. Connect **Input Node** → **LLM Chain** (text → input)
2. Connect **LLM Chain** → **Chat Output** (output → input)

### Step 5: Configure MCP Server Tools
1. **Go to MCP Server tab** in your Langflow project
2. **Click "Edit Tools"**
3. **Enable the Phase 8 flow** as an MCP tool
4. **Configure tool name**: `phase8_ingestion`
5. **Configure tool description**: `Process YouTube channel ingestion with Phase 8 pipeline. Input: YouTube channel URL. Output: Detailed processing summary and bundle structure.`

### Step 6: Test the Flow
1. **Test in Langflow** with a sample YouTube channel URL
2. **Verify Chat Output** works correctly
3. **Test the MCP tool** in the MCP Server tab

### Step 7: Use in Cursor
Once configured, you can use it in Cursor via the MCP Hub Server:
```python
mcp_mcp_hub_server_execute_langflow_tool("phase8_ingestion", {"text": "https://www.youtube.com/@imaginationpodcastofficial"})
```

## ✅ Success Indicators
- Flow creates successfully in Langflow
- Chat Output component is present and working
- MCP Server shows the Phase 8 tool as available
- Tool can be tested with sample inputs

## 🔗 Next Steps
After setup:
1. Test the flow manually in Langflow
2. Test the MCP tool in Cursor
3. Use with real YouTube channel URLs
4. Monitor bundle creation and processing

Generated: 2025-08-10

