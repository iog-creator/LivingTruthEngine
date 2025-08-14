---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['PHASE_9.md', 'config/tool_registry.json', 'src/mcp_servers/phase9_mcp_server.py', 'tools/mcp/specs/*.json']
---

# MCP Tooling (Phase 9)

## Overview

This directory contains MCP tool specifications and implementation guidance for Phase 9 development.

## Structure

- **Specs**: `tools/mcp/specs/*.json` - JSON-RPC style specifications
- **Implementation**: `src/mcp_servers/phase9_mcp_server.py` - Python implementation
- **Registry**: `config/tool_registry.json` - Tool registry integration

## Implementation Guidelines

### **Your MCP server should:**
- Expose each namespace with the method signatures above
- Call local scripts/HTTP endpoints for the real work
- Return structured results consumable by Cursor

### **Suggested Mapping:**
- **HTTP calls** → `requests` (Python) or `fetch` (Node)
- **Local scripts** → `subprocess`/`child_process`
- **DB checks** → `psycopg` queries for vector dims & ANN indexes

## Namespaces

### **mcp.project.rules**
- Rule validation and management
- Frontmatter fixing and archiving
- Project governance tools

### **mcp.lte.health**
- Health monitoring and validation
- Fallback event tracking
- System status checks

### **mcp.lte.models**
- Model registry management
- Embedding dimension validation
- SSOT enforcement

### **mcp.lte.pgvector**
- Database dimension management
- Migration script generation
- IVFFLAT index management

### **mcp.lte.proxy**
- Reverse proxy validation
- Smoke testing for endpoints
- Single-origin verification

### **mcp.lte.ui.contracts**
- UI contract validation
- Envelope format verification
- Playwright smoke testing

### **mcp.lte.adapters**
- Adapter pipeline testing
- Source validation
- Transcript mode checking

### **mcp.lte.gpu**
- GPU status and allocation
- VRAM monitoring
- Fallback simulation

### **mcp.lte.timeline**
- Timeline preview and validation
- SLA compliance checking
- Performance monitoring

### **mcp.lte.smoke**
- Phase-specific smoke testing
- Script execution and validation
- Result reporting

## Usage Examples

### **Pre-flight Validation**
```python
# Validate cursor rules
result = mcp.project.rules.validate()
if not result["ok"]:
    raise Exception("Rule validation failed")

# Check system health
health = mcp.lte.health.get_full()
if health["status"] != "ok":
    raise Exception("Health check failed")
```

### **Post-implementation Testing**
```python
# Run smoke tests
smoke = mcp.lte.smoke.run_phase("scripts/p9_4_0_smoke.sh")
if not smoke["ok"]:
    raise Exception("Smoke tests failed")

# Validate UI contracts
contracts = mcp.lte.ui.contracts.validate_envelopes()
if not contracts["ok"]:
    raise Exception("UI contract validation failed")
```

## Integration with Cursor

These tools are designed to integrate seamlessly with Cursor's MCP protocol:

1. **Automatic Discovery** - Tools are registered in the tool registry
2. **Type Safety** - JSON-RPC specifications provide clear contracts
3. **Error Handling** - Structured error responses for debugging
4. **Performance** - Fast execution for development workflow

## Development Workflow

1. **Before Coding**: Run pre-flight validation
2. **During Development**: Use tools for testing and validation
3. **After Implementation**: Run post-implementation checks
4. **On Completion**: Generate summaries and update logs

## References

- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Python Library](https://github.com/jlowin/fastmcp)
- [Phase 9 Master Plan](../PHASE_9_MASTER_PLAN.md)
- [Implementation Summary](../PHASE_9_RULES_AND_MCP_IMPLEMENTATION_SUMMARY.md)
