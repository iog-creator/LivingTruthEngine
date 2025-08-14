---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['PHASE_X_PLAN.md', 'PHASE_X_COMPLETION_SUMMARY.md', 'PHASE_9_MASTER_PLAN__MCP_ADDENDA.md', 'config/tool_registry.json', 'PHASE_9.md', 'project_master_log.md']
---

# MCP + Rules Enforcement Master Reference

## 📋 **Overview**
This document consolidates all MCP tool, Cursor Rules, and MDC enforcement requirements from Phase 9 to ensure future phases follow the correct process. It serves as the authoritative reference for MCP tool validation, cursor rule enforcement, and development workflow requirements.

## 🎯 **Primary Goals**
- Ensure **every phase** has MCP tools, Cursor Rules, and MDC updates **as needed**
- Ensure MCP server functions are validated and errors surfaced (never silently skipped)
- Maintain **documentation discipline** — master log, completion summaries, and MCP tool specs must be updated per phase

---

## 1. **Cursor Rules Enforcement**

### **Validation Before Completion**
1. **Validation Before Completion**
   - Run `validate_cursor_rules()` before closing a phase
   - Phase cannot be marked complete if validation fails

2. **Rule Update Requirements**
   - Any new phase introducing APIs, data models, or workflows must update relevant Cursor Rules
   - Add phase-specific rules to `.cursor/rules/` with:
     - Frontmatter metadata (phase, description, enforcement scope)
     - Build-Verify-Iterate section
     - References to updated MCP tools

3. **Rule Archive**
   - Outdated rules moved to `archive/` with phase tag

## 2. **MCP Server Requirements**

### **Tool Lifecycle**
1. **Tool Lifecycle**
   - Add or update MCP tools per phase scope
   - Each MCP tool:
     - Has `spec` JSON file in `/specs`
     - Has unit tests in `/tests/mcp_tools/`
     - Implements full envelope response: `{status, data?, error?}`

2. **Function Validation**
   - Test MCP server functions with known good inputs
   - Fail phase if any tool errors out during validation

3. **Error Handling**
   - No silent failures: log every MCP server error
   - Fallbacks explicitly reported in MCP tool output

## 3. **MDC (Master Development Contract) Enforcement**

### **Per-Phase MDC Addenda**
1. **Per-Phase MDC Addenda**
   - Each phase updates `PHASE_9_MASTER_PLAN__MCP_ADDENDA.md`
   - Addenda must include:
     - New MCP tools
     - Updated Cursor Rules
     - New CI/CD gates

2. **Exit Gate Checks**
   - MDC requires these checks before phase close:
     - MCP validation
     - CI green with all new tests
     - Documentation updates committed
     - Master log updated

## 4. **CI/CD Integration Requirements**

### **Validation Scripts**
1. **Validation Scripts**
   - `scripts/ci/validate_phaseX.sh` must:
     - Validate MCP tools
     - Run unit/integration tests
     - Verify cursor rules are updated

2. **Performance/Error Gates**
   - Performance budgets enforced in CI (p95 latencies, LCP, bundle sizes)
   - Error budgets enforced in CI starting Phase 9.5.5

## 5. **MCP Tool Categories (Phase 9 Baseline)**

### **System Health**
- `get_health_status`
- `validate_cursor_rules`
- `list_tools`

### **Data & Analysis**
- `build_graph`
- `fetch_timeline`
- `analyze_veritas_summary`
- `analyze_veritas_claims`

### **Ingestion & Adapters**
- `test_youtube_adapter`
- `test_web_adapter`
- `test_pdf_adapter`
- `run_multi_source_job`

### **Monitoring & Recovery**
- `get_error_budget_status` (Phase 9.5.5)
- `trigger_recovery_action` (Phase 9.5.5)
- `run_chaos_test` (Phase 9.5.5)

### **MCP Enforcement**
- `validate_mcp_requirements_reference` - Validate MCP requirements reference document
- `enforce_mcp_compliance` - Enforce MCP compliance before phase completion
- `update_mcp_requirements_reference` - Update sections in MCP requirements reference

### **Error Budget & Recovery (Phase 9.5.5)**
- `validate_error_budget` - Validate error budget status and configuration
- `trigger_recovery_action` - Trigger recovery actions for services
- `run_chaos_test` - Execute chaos engineering tests

### **Chaos Engineering & Proactive Resilience (Phase 9.5.6)**
- `trigger_chaos_scenario` - Trigger chaos scenarios with configurable parameters
- `get_resilience_score` - Calculate resilience score based on chaos tests and predictions
- `simulate_proactive_recovery` - Simulate proactive recovery under predicted stress

---

## 6. **Documentation & Logging**

### **Per-Phase Docs**
1. **Per-Phase Docs**
   - `PHASE_X_PLAN.md`
   - `PHASE_X_COMPLETION_SUMMARY.md`
   - Update `project_master_log.md`
   - Update consolidated completion summary

2. **MCP Tool Specs**
   - Update `/specs` with any new or modified tool spec
   - Include:
     - Tool name & version
     - Input schema
     - Output schema
     - Error codes

3. **Logging**
   - MCP server logs must show:
     - Tool start/end
     - Input parameters
     - Outcome (success/fail/fallback)
     - Execution time

---

## 7. **Phase Close Checklist**

Before closing any phase:
- [ ] MCP tools updated and validated
- [ ] Cursor rules updated and validated
- [ ] MDC addenda updated
- [ ] CI green with all new gates/tests
- [ ] Docs: plan + completion + master log updated
- [ ] MCP specs updated
- [ ] All errors handled and logged

---

## 🔒 **Enforcement Summary**
- No phase is complete without **passing MCP + Rules validation**
- No undocumented MCP tool changes allowed
- Cursor must always **self-update** its rules, tools, and docs when phase scope changes
- All MCP errors must be surfaced — silent failure is prohibited

---

## 🎯 **Phase-Specific MCP Requirements**

### **Phase 9.5.4 - Performance Gates**
- Performance measurement tools operational
- Bundle analysis tools functional
- LCP measurement tools working
- CI integration for performance validation

### **Phase 9.5.5 - Error Budgeting & Recovery Automation**
- Error budget monitoring tools
- Recovery action triggers
- Chaos engineering test execution
- Alert and monitoring integration

### **Future Phases**
- GPU model integration tools
- Advanced evidence graph tools
- Real-time monitoring tools
- Advanced recovery automation

---

## 📚 **MCP Best Practices**

### **Tool Development**
- Use descriptive tool names and descriptions
- Implement proper error handling
- Include performance monitoring
- Provide clear parameter documentation

### **Rule Management**
- Keep rules focused and actionable
- Update rules when functionality changes
- Archive outdated rules promptly
- Maintain cross-references between rules

### **CI Integration**
- Validate MCP tools in CI pipeline
- Include performance gates in CI
- Test error budget validation in CI
- Ensure chaos tests pass in CI

### **Documentation**
- Document all MCP tools thoroughly
- Maintain up-to-date rule documentation
- Include examples in tool descriptions
- Provide troubleshooting guides

---

## 🔧 **MCP Troubleshooting**

### **Common Issues**
- MCP server not responding
- Tool registry corruption
- Cursor rule validation failures
- Performance gate failures
- Error budget violations

### **Recovery Procedures**
- Restart MCP server
- Reload tool registry from backup
- Fix cursor rule frontmatter
- Address performance regressions
- Investigate error budget violations

### **Validation Commands**
```bash
# Validate cursor rules
python -c "from src.mcp_servers.mcp_hub_server import validate_cursor_rules; print(validate_cursor_rules())"

# Check MCP server health
curl -s http://localhost:8050/api/health/full | jq .

# Test tool registry
python -c "from src.mcp_servers.mcp_hub_server import test_registry_recovery; print(test_registry_recovery())"
```

---

## 🚦 **CI/CD MCP Integration**

### **Required CI Gates**
- MCP server health check before build
- Cursor rule validation in CI pipeline
- MCP tool functionality validation
- Performance gate validation (Phase 9.5.4+)
- Error budget validation (Phase 9.5.5+)

### **CI Validation Scripts**
- `scripts/ci/validate_phase9.sh` - Phase 9 validation
- `scripts/perf_harness.sh` - Performance validation
- `scripts/error_budget_test.sh` - Error budget validation
- `scripts/run_chaos_tests.sh` - Chaos engineering tests

### **CI Failure Conditions**
- MCP server not responding
- Cursor rule validation failures
- MCP tool execution failures
- Performance budget violations
- Error budget threshold exceeded

---

## 📊 **MCP Tool Registry Requirements**

### **Tool Registry Structure**
- Central registry in `config/tool_registry.json`
- Backup registry in `config/tool_registry.json.bak`
- Automatic backup creation on registry load
- Validation of tool definitions on load

### **Tool Definition Requirements**
- Required fields: `name`, `description`, `params_schema`
- Valid parameter types: `string`, `int`, `float`, `bool`, `list`, `dict`, `any`
- Tool categorization by namespace
- Performance monitoring integration

### **Registry Management**
- `load_registry()` - Load with automatic backup
- `validate_registry()` - Validate tool definitions
- `reload_registry()` - Reload from file
- `test_registry_recovery()` - Test backup/recovery

---

## 🔍 **MCP Server Health Requirements**

### **Health Endpoint Requirements**
- `/api/health/full` must include:
  - MCP server status
  - Tool registry status
  - Performance metrics
  - Error budget status (Phase 9.5.5+)
  - GPU and fallback information

### **Health Validation**
- All required health gates must pass
- MCP server must be responsive
- Tool registry must be valid
- Performance metrics must be within budgets

### **Health Integration**
- Health checks integrated into smoke tests
- Health validation in CI pipeline
- Health monitoring in production
- Health alerts for critical failures

---

## 🎯 **Phase-Specific MCP Requirements**

### **Phase 9.5.4 - Performance Gates**
- Performance measurement tools operational
- Bundle analysis tools functional
- LCP measurement tools working
- CI integration for performance validation

### **Phase 9.5.5 - Error Budgeting & Recovery Automation**
- Error budget monitoring tools
- Recovery action triggers
- Chaos engineering test execution
- Alert and monitoring integration

### **Future Phases**
- GPU model integration tools
- Advanced evidence graph tools
- Real-time monitoring tools
- Advanced recovery automation

---

## 📚 **MCP Best Practices**

### **Tool Development**
- Use descriptive tool names and descriptions
- Implement proper error handling
- Include performance monitoring
- Provide clear parameter documentation

### **Rule Management**
- Keep rules focused and actionable
- Update rules when functionality changes
- Archive outdated rules promptly
- Maintain cross-references between rules

### **CI Integration**
- Validate MCP tools in CI pipeline
- Include performance gates in CI
- Test error budget validation in CI
- Ensure chaos tests pass in CI

### **Documentation**
- Document all MCP tools thoroughly
- Maintain up-to-date rule documentation
- Include examples in tool descriptions
- Provide troubleshooting guides

---

## 🔧 **MCP Troubleshooting**

### **Common Issues**
- MCP server not responding
- Tool registry corruption
- Cursor rule validation failures
- Performance gate failures
- Error budget violations

### **Recovery Procedures**
- Restart MCP server
- Reload tool registry from backup
- Fix cursor rule frontmatter
- Address performance regressions
- Investigate error budget violations

### **Validation Commands**
```bash
# Validate cursor rules
python -c "from src.mcp_servers.mcp_hub_server import validate_cursor_rules; print(validate_cursor_rules())"

# Check MCP server health
curl -s http://localhost:8050/api/health/full | jq .

# Test tool registry
python -c "from src.mcp_servers.mcp_hub_server import test_registry_recovery; print(test_registry_recovery())"
```

---

**This document serves as the authoritative reference for all MCP requirements in the Living Truth Engine project. Update this document when adding new MCP tools or changing requirements.**

## 📋 **Cursor Rule Integration**
This document is enforced by the Cursor rule: `.cursor/rules/mcp_enforcement.mdc`

**ALWAYS consult this document before making any MCP-related changes or completing any phase.**

**Last Updated**: August 13, 2025 19:45:00
