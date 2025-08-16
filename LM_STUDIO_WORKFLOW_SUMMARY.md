# LM Studio Integration Workflow Summary

## 🎯 **Clear Integration Architecture**

This document provides a **definitive guide** to the LM Studio integration workflow, eliminating confusion and providing clear decision paths.

## 🏗️ **Three Integration Methods (Choose One)**

### **Method 1: HTTP Bridge (Recommended for Tools)**
- **Purpose**: OpenAI-compatible tools API
- **Best for**: Structured analysis, automated workflows
- **Start**: `make lm-tools`
- **Endpoint**: `http://127.0.0.1:8756`
- **Tools**: `verify_ssot()`, `read_ssot_report()`, `draft_patches()`

### **Method 2: MCP Server (Recommended for Chat)**
- **Purpose**: Direct MCP protocol connection
- **Best for**: Conversational interaction, complex queries
- **Start**: `make lm-mcp`
- **Command**: `python src/mcp_servers/phase9_mcp_server.py`
- **Tools**: All Phase 9 MCP tools including enhanced ruff tools

### **Method 3: SSOT Agent (Automated Workflows)**
- **Purpose**: Deterministic, read-only task sequencing
- **Best for**: CI integration, automated validation
- **Start**: `make ssot-agent`
- **Output**: JSON envelope to `reports/ssot_agent_output_<UTC>.json`

## 🔄 **Recommended Workflow**

### **For Development (Choose Method 1 or 2)**

#### **Option A: HTTP Bridge Workflow**
```bash
# Terminal 1: Start tools bridge
make lm-tools

# Terminal 2: In LM Studio, configure tools to call:
# POST http://127.0.0.1:8756/tools/verify_ssot
# POST http://127.0.0.1:8756/tools/read_ssot_report
# POST http://127.0.0.1:8756/tools/draft_patches

# Terminal 3: Apply changes in Cursor
# 1. LM Studio suggests changes
# 2. Cursor applies approved changes
# 3. Run validation: make check
# 4. Commit: git commit -m "[SSOT Verified] fix: ..."
```

#### **Option B: MCP Server Workflow**
```bash
# Terminal 1: Start MCP server
make lm-mcp

# Terminal 2: In LM Studio, add MCP server with command:
# python src/mcp_servers/phase9_mcp_server.py

# Terminal 3: Ask questions like:
# - "Can you validate the cursor rules?"
# - "Run comprehensive ruff checks on the codebase"
# - "Check the health status of all services"

# Terminal 4: Apply changes in Cursor
# 1. LM Studio suggests changes
# 2. Cursor applies approved changes
# 3. Run validation: make check
# 4. Commit: git commit -m "[SSOT Verified] fix: ..."
```

### **For Automated Validation (Method 3)**
```bash
# Run deterministic agent
make ssot-agent

# Check output
cat reports/ssot_agent_output_*.json

# Apply any suggested changes in Cursor
# Run validation: make check
# Commit: git commit -m "[SSOT Verified] fix: ..."
```

## 🛠️ **Enhanced Ruff Tools (Available via MCP)**

The MCP server provides powerful automated code quality tools:

### **Available Ruff Tools**
- `run_ruff_comprehensive()` - All rules except line length
- `run_ruff_line_length_fix()` - Intelligent line breaking
- `run_ruff_add_noqa()` - Add suppression directives
- `fix_silent_fallbacks()` - Auto-fix bare except statements

### **Usage Examples**
```bash
# Via MCP server (Method 2)
# Ask LM Studio: "Run comprehensive ruff checks on the codebase"

# Via Makefile (direct)
make ruff-comprehensive
make ruff-line-length
make fix-fallbacks
```

## 🛡️ **Safety Boundaries (Non-Negotiable)**

### **What LM Studio CAN Do**
- ✅ Analyze code and documentation
- ✅ Suggest patches and improvements
- ✅ Run validation checks
- ✅ Generate reports and summaries
- ✅ Identify issues and inconsistencies

### **What LM Studio CANNOT Do**
- ❌ Apply changes to files
- ❌ Run `--fix` operations
- ❌ Commit code changes
- ❌ Bypass SSOT validation
- ❌ Access production systems

### **Enforcement**
- **HTTP Bridge**: Only exposes read-only endpoints
- **MCP Server**: Tools are read-only or require explicit confirmation
- **SSOT Agent**: Deterministic, no write operations
- **CI/CD**: Never calls LM Studio; remains deterministic

## 🚨 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Bridge Not Starting**
```bash
# Check if port 8756 is available
lsof -i :8756

# Kill any existing process
pkill -f "lmstudio_tools_bridge"

# Restart
make lm-tools
```

#### **MCP Connection Fails**
```bash
# Test MCP server directly
make mcp-diagnostics

# Verify command in LM Studio settings
# Should be: python src/mcp_servers/phase9_mcp_server.py
```

#### **Tools Not Working**
```bash
# Test HTTP bridge
curl -X POST http://127.0.0.1:8756/tools/verify_ssot \
  -H "Content-Type: application/json" \
  -d '{}'

# Test SSOT agent
make ssot-agent
```

#### **No Inference Visible**
- **HTTP Bridge**: Inference not visible in LM Studio logs
- **MCP Server**: Use for visible developer logs
- **SSOT Agent**: Deterministic, no inference needed

## 📋 **Decision Matrix**

| Use Case | Recommended Method | Why |
|----------|-------------------|-----|
| **Structured Analysis** | HTTP Bridge (Method 1) | Clean API, easy to configure |
| **Conversational Chat** | MCP Server (Method 2) | Full tool access, visible logs |
| **Automated CI** | SSOT Agent (Method 3) | Deterministic, no LLM needed |
| **Code Quality** | MCP Server (Method 2) | Access to enhanced ruff tools |
| **Quick Validation** | HTTP Bridge (Method 1) | Fast, simple endpoints |

## 🔧 **Configuration Files**

### **LM Studio MCP Configuration**
```json
// ~/.lmstudio/mcp.json
{
  "mcpServers": {
    "living-truth-engine": {
      "command": "python",
      "args": ["src/mcp_servers/phase9_mcp_server.py"]
    }
  }
}
```

### **SSOT Agent Configuration**
```yaml
# config/agents/ssot_agent.yaml
model: llama-3.2-3b-instruct
bridge_url: http://127.0.0.1:8756
tools:
  - verify_ssot
  - read_ssot_report
  - draft_patches
```

## 📚 **Related Documentation**

- [LM Studio Integration Guide](LM_STUDIO_INTEGRATION.md)
- [Phase 9 MCP Server](../src/mcp_servers/phase9_mcp_server.py)
- [SSOT Agent](../src/agents/ssot_langchain_agent.py)
- [Project Master Log](../project_master_log.md)
- [SSOT Validation System](../scripts/verify_complete_ssot_system.py)

## ✅ **Validation Checklist**

Before using LM Studio integration:

- [ ] Choose appropriate integration method
- [ ] Start required service (`make lm-tools` or `make lm-mcp`)
- [ ] Configure LM Studio with correct settings
- [ ] Test basic functionality
- [ ] Understand safety boundaries
- [ ] Have Cursor ready for applying changes
- [ ] Know how to run SSOT validation (`make check`)

## 🎯 **Success Metrics**

- ✅ LM Studio can analyze code and suggest improvements
- ✅ Cursor applies changes with SSOT validation
- ✅ No write operations bypass SSOT
- ✅ CI remains deterministic
- ✅ Enhanced ruff tools available for bulk fixes
- ✅ Clear workflow with no confusion

---

**Remember**: LM Studio is a **helper agent** - it suggests, Cursor applies, SSOT validates. This separation ensures safety and maintainability.
