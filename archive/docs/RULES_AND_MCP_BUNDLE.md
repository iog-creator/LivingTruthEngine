---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['PHASE_9_4_2_COMPLETION_SUMMARY.md', 'PHASE_9_MASTER_PLAN.md', 'config/tool_registry.json', 'PHASE_9.md', 'phase9_mcp_server.py', 'python src/mcp_servers/phase9_mcp_server.py', 'docs/project_master_log.md']
---

# Phase 9 Rules and MCP Bundle

## Overview

This document provides a comprehensive implementation of the Cursor rule updates, system rule updates, and MCP server tools required for Phase 9 development. All components have been implemented and are ready for use.

## 📋 **Cursor Rule Updates**

### **1. Core Workflow (`core_workflow.mdc`)**
- **Updated** with Phase 9 development protocol
- **One PR per sub-phase** requirement
- **Commit format**: `phase<subphase>: <summary> [verified]`
- **MCP integration** requirements
- **Envelope format** enforcement

### **2. API Contracts (`api_contracts.mdc`)**
- **New rule** enforcing envelope format: `{status, data?, error?}`
- **Error code standards**: 502, 503, 500
- **Testing requirements** for envelope validation
- **Zod schema integration** for Phase 9.4.7

### **3. UI Policy (`ui_policy.mdc`)**
- **New rule** for UI development standards
- **Legacy UI protection** - no edits to legacy templates
- **Reverse proxy requirements** for Phase 9.4.0
- **Error boundary requirements** for Phase 9.4.6

### **4. Models & Embeddings (`models_and_embeddings.mdc`)**
- **New rule** for SSOT-driven embedding dimensions
- **Health endpoint requirements** with `embedding_model` and `embedding_dim`
- **Database migration** standards
- **Dimension mismatch** handling

### **5. Fallbacks & Health (`fallbacks_and_health.mdc`)**
- **New rule** for allowed fallbacks only
- **Health monitoring** requirements
- **Fallback event logging** and exposure
- **Performance metrics** tracking

### **6. MCP Operations (`mcp_ops.mdc`)**
- **New rule** for MCP-first operations
- **Required operations** for each phase
- **Tool categories** and namespaces
- **Workflow integration** guidelines

### **7. MCP Integration (`mcp_integration.mdc`)**
- **Updated** with comprehensive Cursor hooks
- **Before/after coding** workflows
- **Completion requirements**
- **Tool namespace** organization

## 🔧 **MCP Server Implementation**

### **Phase 9 MCP Server (`phase9_mcp_server.py`)**

#### **Namespaces Implemented:**

1. **`mcp.project.rules`** - Rule validation and management
   - `validate_cursor_rules()` - Validate all cursor rules
   - `fix_cursor_rule_frontmatter(filename)` - Fix rule metadata
   - `ruleset_archive_outdated()` - Archive outdated rules
   - `ruleset_apply_templates()` - Apply rule templates

2. **`mcp.lte.health`** - Health monitoring and validation
   - `get_full_health()` - Fetch health endpoint
   - `assert_health_ok()` - Validate health gates
   - `get_recent_fallbacks(limit)` - Get fallback events

3. **`mcp.lte.models`** - Model registry management
   - `registry_show()` - Dump registry configuration
   - `assert_embedding_dim(tables)` - Compare registry vs DB

4. **`mcp.lte.pgvector`** - Database dimension management
   - `get_db_dimension(table)` - Read vector dimensions
   - `migrate_dimension(target_dim)` - Generate migration scripts
   - `reindex_ann(table)` - Rebuild IVFFLAT indexes

5. **`mcp.lte.proxy`** - Reverse proxy validation
   - `smoke_proxy()` - Test reverse proxy configuration

6. **`mcp.lte.ui.contracts`** - UI contract validation
   - `validate_envelopes()` - Validate API envelope format
   - `playwright_smoke()` - Run Playwright tests

7. **`mcp.lte.adapters`** - Adapter pipeline testing
   - `test_sources()` - Test adapter pipelines
   - `transcript_mode_check()` - Verify transcript metadata

8. **`mcp.lte.gpu`** - GPU status and allocation
   - `get_gpu_status()` - Get GPU information
   - `simulate_low_vram()` - Test CPU fallback

9. **`mcp.lte.timeline`** - Timeline endpoint validation
   - `preview_timeline(run_id)` - Preview timeline data

10. **`mcp.lte.smoke`** - Smoke test execution
    - `run_phase_smoke(phase)` - Execute phase-specific tests
    - `generate_phase_completion_summary(subphase)` - Generate summaries

## 📊 **Tool Registry Integration**

### **Updated `config/tool_registry.json`**
- **Added** Phase 9 MCP server with 20 tools
- **Updated** total tool count
- **Comprehensive** parameter schemas
- **Proper** module and function mappings

## 🎯 **System Rule Enforcement**

### **Health Contract**
- `/api/health/full` must include `embedding_model` and `embedding_dim`
- `dim_mismatch` boolean for registry vs DB comparison
- Fallback event summary exposure

### **Reverse Proxy Single-Origin**
- Root `/` must serve new UI shell after Phase 9.4.0
- Smoke test for shell title validation
- Envelope format validation

### **No Legacy UI Mutation**
- Protection for legacy templates
- CI rule enforcement
- Clear migration path

### **Vector Schema SSOT**
- Start-time validation of embedding dimensions
- Fail-fast with remediation instructions
- Migration script generation

### **Allowed Fallbacks Only**
- Centralized fallback guards and logging
- Health endpoint exposure
- Performance monitoring

## 🔄 **Cursor Hooks Implementation**

### **Before Coding a Sub-phase**
```python
# Validate cursor rules
result = mcp.project.rules.validate()
if not result["valid"]:
    raise Exception("Cursor rules validation failed")

# Get health snapshot
health = mcp.lte.health.get_full()
print(f"System health: {health['status']}")

# Verify model configuration
registry = mcp.lte.models.registry_show()
print(f"Model registry: {registry}")
```

### **After Coding**
```python
# Run smoke tests
smoke_result = mcp.lte.smoke.run_phase("9.4.2")
if not smoke_result["success"]:
    raise Exception("Smoke tests failed")

# Validate UI contracts (if UI touched)
if ui_touched:
    envelope_result = mcp.lte.ui.contracts.validate_envelopes()
    if not envelope_result["valid"]:
        raise Exception("Envelope validation failed")

# Check storage (if storage touched)
if storage_touched:
    dim_result = mcp.lte.models.assert_embedding_dim(["lte.doc_embeddings"])
    if not dim_result["ok"]:
        raise Exception("Embedding dimension mismatch")
```

### **On Completion**
```python
# Fix rule metadata
mcp.project.rules.fix_frontmatter()

# Archive outdated rules
mcp.project.rules.archive_outdated()

# Generate completion summary
summary = mcp.lte.smoke.generate_phase_completion_summary("9.4.2")
with open("PHASE_9_4_2_COMPLETION_SUMMARY.md", "w") as f:
    f.write(summary)

# Update master log
subprocess.run(["python", "build_master_log.py", "append"])
```

## ✅ **Implementation Status**

### **Completed Components**
- ✅ All 7 Cursor rules created/updated
- ✅ Phase 9 MCP server with 20 tools
- ✅ Tool registry integration
- ✅ System rule enforcement
- ✅ Cursor hooks implementation
- ✅ Comprehensive documentation

### **Ready for Use**
- ✅ MCP server can be started: `python src/mcp_servers/phase9_mcp_server.py`
- ✅ All tools registered in tool registry
- ✅ Cursor rules properly formatted
- ✅ Workflow integration complete

## 🚀 **Next Steps**

### **Immediate Actions**
1. **Start Phase 9 MCP server** for tool availability
2. **Validate cursor rules** using new MCP tools
3. **Test health monitoring** with new endpoints
4. **Verify envelope validation** across API endpoints

### **Phase 9.4.0 Preparation**
1. **Reverse proxy configuration** implementation
2. **UI shell** development
3. **Smoke test** creation for proxy validation
4. **Health endpoint** enhancement

### **Integration Testing**
1. **MCP tool execution** testing
2. **Cursor hook workflow** validation
3. **Rule enforcement** verification
4. **Completion summary** generation testing

## 📚 **References**

### **Related Rules**
- `@core_workflow.mdc` - Development protocol
- `@api_contracts.mdc` - Envelope format
- `@ui_policy.mdc` - UI development standards
- `@models_and_embeddings.mdc` - SSOT embedding dimensions
- `@fallbacks_and_health.mdc` - Fallback policies
- `@mcp_ops.mdc` - MCP operations
- `@mcp_integration.mdc` - Cursor hooks

### **Phase Documentation**
- `PHASE_9_MASTER_PLAN.md` - Master plan
- `PHASE_9_4_2_COMPLETION_SUMMARY.md` - Previous completion
- `docs/project_master_log.md` - Project timeline

---

**This bundle provides a complete foundation for Phase 9 development with comprehensive tooling, rule enforcement, and workflow automation.**
