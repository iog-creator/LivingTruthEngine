# LM Studio Integration (Local Only)

This document describes how to integrate LM Studio with the Living Truth Engine's Single Source of Truth (SSOT) validation system.

## 🎯 **Integration Overview**

**Primary Goal**: Use LM Studio as a **helper agent** for automated SSOT validation, analysis, and patch drafting while keeping Cursor as the code executor.

**Safety Principle**: LM Studio is **read-only** - it suggests changes but never applies them. Cursor + SSOT scripts remain the gate.

## 🛠️ **Available Integration Methods**

### Method 1: HTTP Bridge (Recommended for Tools)
- **Purpose**: OpenAI-compatible tools API for LM Studio
- **Endpoint**: `http://127.0.0.1:8756`
- **Start**: `make lm-tools`
- **Best for**: Tool calls, structured analysis

### Method 2: MCP Server (Recommended for Chat)
- **Purpose**: Direct MCP protocol connection
- **Start**: `make lm-mcp`
- **Best for**: Conversational interaction, complex queries

### Method 3: SSOT Agent (Automated Workflows)
- **Purpose**: Deterministic, read-only SSOT task sequencing
- **Start**: `make ssot-agent`
- **Best for**: Automated validation, CI integration

## 🚀 **Quick Start**

### For Tool-Based Analysis:
```bash
# Terminal 1: Start the tools bridge
make lm-tools

# Terminal 2: In LM Studio, configure tools to call:
# POST http://127.0.0.1:8756/tools/verify_ssot
# POST http://127.0.0.1:8756/tools/read_ssot_report
# POST http://127.0.0.1:8756/tools/draft_patches
```

### For Conversational Analysis:
```bash
# Terminal 1: Start the MCP server
make lm-mcp

# Terminal 2: In LM Studio, add MCP server with command:
# python src/mcp_servers/phase9_mcp_server.py
```

## 📋 **Available Tools & Capabilities**

### HTTP Bridge Tools (`make lm-tools`)
- `verify_ssot()` - Quick SSOT validation check
- `read_ssot_report()` - Read detailed SSOT reports
- `draft_patches()` - Suggest minimal edits (read-only)
- `run_repo_inventory()` - Repository summary

### MCP Server Tools (`make lm-mcp`)
- **Code Quality**: `run_ruff_comprehensive()`, `run_ruff_line_length_fix()`, `fix_silent_fallbacks()`
- **Project Management**: `validate_cursor_rules()`, `build_master_log()`
- **Health Monitoring**: `check_health_status()`, `run_smoke_tests()`
- **Infrastructure**: `validate_docker_health()`, `check_model_registry()`

### Enhanced Ruff Tools (via MCP)
- `run_ruff_comprehensive()` - All rules except line length
- `run_ruff_line_length_fix()` - Intelligent line breaking
- `run_ruff_add_noqa()` - Add suppression directives
- `fix_silent_fallbacks()` - Auto-fix bare except statements

## 🔧 **LM Studio Configuration**

### For HTTP Bridge (Tools):
1. Enable **Functions/Tools** in LM Studio
2. Configure tools to call the HTTP endpoints
3. Use structured prompts for analysis requests

### For MCP Server (Chat):
1. Go to **Settings → MCP** in LM Studio
2. Add server with command: `python src/mcp_servers/phase9_mcp_server.py`
3. Ask questions like:
   - "Can you validate the cursor rules?"
   - "Run comprehensive ruff checks on the codebase"
   - "Check the health status of all services"

## 🤖 **SSOT Agent (Automated Workflows)**

The SSOT agent provides deterministic, read-only task sequencing:

```bash
# Run deterministic agent (no LLM, just HTTP calls)
make ssot-agent

# Optional: Use LangChain agent (still read-only)
python -m src.agents.ssot_langchain_agent --config config/agents/ssot_agent.yaml --langchain
```

**Output**: JSON envelope saved to `reports/ssot_agent_output_<UTC>.json`

## 🛡️ **Safety Boundaries**

### What LM Studio CAN Do:
- ✅ Analyze code and documentation
- ✅ Suggest patches and improvements
- ✅ Run validation checks
- ✅ Generate reports and summaries
- ✅ Identify issues and inconsistencies

### What LM Studio CANNOT Do:
- ❌ Apply changes to files
- ❌ Run `--fix` operations
- ❌ Commit code changes
- ❌ Bypass SSOT validation
- ❌ Access production systems

### Enforcement:
- **HTTP Bridge**: Only exposes read-only endpoints
- **MCP Server**: Tools are read-only or require explicit confirmation
- **SSOT Agent**: Deterministic, no write operations
- **CI/CD**: Never calls LM Studio; remains deterministic

## 🔄 **Workflow Integration**

### Development Workflow:
1. **LM Studio**: Analyzes code, suggests improvements
2. **Cursor**: Reviews suggestions, applies approved changes
3. **SSOT Scripts**: Validates all changes before commit
4. **CI/CD**: Runs deterministic checks without LM Studio

### Example Session:
```bash
# 1. Start tools bridge
make lm-tools

# 2. In LM Studio, ask: "Analyze the codebase for silent fallbacks"
# LM Studio calls: POST /tools/verify_ssot

# 3. LM Studio suggests: "Found 25 silent fallbacks. Here are the fixes..."

# 4. In Cursor, apply the suggested fixes
# 5. Run validation
make check

# 6. Commit with SSOT verification
git commit -m "[SSOT Verified] fix: resolve silent fallbacks"
```

## 🚨 **Troubleshooting**

### Common Issues:
- **Bridge not starting**: Check if port 8756 is available
- **MCP connection fails**: Verify the command in LM Studio settings
- **Tools not working**: Ensure LM Studio has Functions/Tools enabled
- **No inference visible**: Use MCP server for visible developer logs

### Debug Commands:
```bash
# Test HTTP bridge
curl -X POST http://127.0.0.1:8756/tools/verify_ssot -H "Content-Type: application/json" -d '{}'

# Test MCP server
make mcp-diagnostics

# Test SSOT agent
make ssot-agent
```

## 📚 **Related Documentation**

- [SSOT Validation System](../scripts/verify_complete_ssot_system.py)
- [Phase 9 MCP Server](../src/mcp_servers/phase9_mcp_server.py)
- [SSOT Agent](../src/agents/ssot_langchain_agent.py)
- [Project Master Log](../project_master_log.md)
