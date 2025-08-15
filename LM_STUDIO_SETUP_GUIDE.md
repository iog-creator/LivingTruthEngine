# LM Studio Tools Setup Guide

## ✅ Verification Complete
LM Studio is running and responding (0.07s inference time). The tools bridge is working.

## 🔧 Next Steps: Configure LM Studio to Use Tools

### Option 1: OpenAI Tools Format (Recommended)

1. **In LM Studio, go to Settings → Tools**
2. **Add these tool definitions:**

```json
[
  {
    "name": "verify_ssot",
    "description": "Run comprehensive SSOT validation check",
    "url": "http://127.0.0.1:8756/tools/verify_ssot",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": "{}"
  },
  {
    "name": "read_ssot_report", 
    "description": "Read the latest SSOT validation report",
    "url": "http://127.0.0.1:8756/tools/read_ssot_report",
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": "{}"
  },
  {
    "name": "draft_patches",
    "description": "Get suggested code patches (read-only)",
    "url": "http://127.0.0.1:8756/tools/draft_patches", 
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": "{}"
  }
]
```

3. **Start the bridge**: `make lm-tools` (in terminal)
4. **Test with LM Studio**: Ask "Can you verify the SSOT status of the project?"

### Option 2: MCP Connection

1. **In LM Studio, go to Settings → MCP**
2. **Add MCP server**: `python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; Phase9MCPServer().serve_stdio()"`
3. **Test**: Ask "What MCP tools are available?"

## 🚀 Quick Test

Run this to see LM Studio actually using the tools:

```bash
# Terminal 1: Start bridge
make lm-tools

# Terminal 2: Test with curl
curl -X POST http://127.0.0.1:8756/tools/verify_ssot \
  -H "Content-Type: application/json" \
  -d '{}' | jq .
```

## 🎯 Expected Behavior

Once configured, LM Studio should:
- Call `verify_ssot` when you ask about project validation
- Call `read_ssot_report` when you ask about project status  
- Call `draft_patches` when you ask for code suggestions
- Show inference happening in LM Studio UI

The tools are working - LM Studio just needs to be told to use them!
