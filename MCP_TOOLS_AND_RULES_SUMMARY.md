# MCP Tools and Rules Summary

## 🎯 **Overview**

This document summarizes the comprehensive work completed to fix MCP tools, update MDC files, implement the alwaysApply policy, and establish User Rules guidelines for the Living Truth Engine project.

## 📋 **Work Completed**

### **Phase 8.3: Fix MCP Tools and Add Comprehensive Validation**
- **Fixed MCP validation tools** to properly detect duplicate frontmatter vs content
- **Updated global rule** to include mandatory MCP checks in tool rituals
- **Enhanced MCP enforcement rule** with comprehensive validation requirements
- **Fixed all 33 MDC files** to have proper frontmatter format
- **Added CI workflow** for Playwright tests
- **Both Phase9 and FastMCP servers** now validate correctly

### **Phase 8.4: Implement AlwaysApply Policy**
- **Updated alwaysApply policy**: only `00-global.mdc` has `alwaysApply: true`
- **All other rules** now use `alwaysApply: false` (agent decides)
- **Updated archive rules** to use `alwaysApply: false`
- **Enhanced MCP enforcement rule** with comprehensive alwaysApply policy
- **Fixed duplicate content** in global rule

### **Phase 8.5: Add User Rules Policy**
- **Added comprehensive User Rules policy** based on Cursor documentation
- **Documented guidelines** for User Rules (Cursor Settings → Rules)
- **Added Rule Type Guidelines table** with usage recommendations
- **Updated validation requirements** to check User Rules
- **Enhanced phase close checklist** to include User Rules review

## 🔧 **Technical Fixes**

### **MCP Tool Improvements**

#### **Phase9 MCP Server** (`src/mcp_servers/phase9_mcp_server.py`)
- **Enhanced `validate_cursor_rules()`**: Now correctly detects duplicate frontmatter by looking for multiple YAML-like sections
- **Improved `fix_cursor_rule_frontmatter()`**: Properly extracts main content after any frontmatter and prepends a single, correctly formatted frontmatter block
- **Smart content extraction**: Correctly identifies the start of main content after frontmatter sections

#### **FastMCP Server** (`src/mcp_servers/living_truth_fastmcp_server.py`)
- **Mirrored improvements** from Phase9 MCP server
- **Consistent validation logic** across both servers
- **Enhanced error detection** for frontmatter issues

### **MDC File Fixes**
- **Fixed 33 MDC files** with proper frontmatter format
- **Removed duplicate frontmatter** sections
- **Standardized descriptions** and metadata
- **Ensured consistent formatting** across all rule files

## 📋 **New Policies Implemented**

### **AlwaysApply Policy**
```
- Only 00-global.mdc should have alwaysApply: true
- All other rules must use alwaysApply: false (agent decides)
- This prevents rule bloat and ensures the AI can choose relevant rules based on context
- The global rule contains the essential, always-applicable guidelines
```

### **User Rules Policy**
```
- User Rules (Cursor Settings → Rules) should be minimal and focused
- Use User Rules for global preferences like communication style or coding conventions
- Avoid duplicating project-specific rules in User Rules
- Keep User Rules concise and cross-project applicable
```

### **Rule Type Guidelines**
| Rule Type | When to Use | Example |
|-----------|-------------|---------|
| **Always** | Only for essential global guidelines | `00-global.mdc` |
| **Auto Attached** | File-specific patterns | Component rules for `ui/**` |
| **Agent Requested** | Specialized knowledge | Domain-specific rules |
| **Manual** | Rarely used utilities | `@ruleName` invocation |

## 🛠️ **Tool Rituals (Mandatory for ALL Changes)**

### **MCP Validation (Non-Negotiable)**
```bash
# 1. MCP Sync and Logging Check
python scripts/mcp_sync.py && python scripts/logging_schema_check.py

# 2. Phase9 MCP Server Validation
python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.validate_cursor_rules(); print('MCP Validation:', result)"

# 3. FastMCP Server Validation
python -c "from src.mcp_servers.living_truth_fastmcp_server import validate_cursor_rules; result = validate_cursor_rules(); print('FastMCP Validation:', result)"
```

### **Enforcement Policy**
- **Block completion** if any MCP validation fails
- **Always run all three checks** before marking any change complete
- **No exceptions** - MCP validation is mandatory for all development work

## 📁 **File Structure**

### **Project Rules** (`.cursor/rules/`)
- **Global Rule**: `00-global.mdc` - Always applies, contains core workflow
- **Specialized Rules**: All other `.mdc` files - Agent decides based on context
- **Archive Rules**: `.cursor/rules/archive/` - Historical rules, never auto-applied

### **User Rules** (Cursor Settings → Rules)
- **Global preferences** that apply across all projects
- **Minimal and focused** on communication style and coding conventions
- **Cross-project applicable** guidelines

## ✅ **Validation Results**

### **Current Status**
- ✅ **Phase9 MCP Server**: All 33 files valid
- ✅ **FastMCP Server**: All 33 files valid
- ✅ **MCP Sync**: Working correctly
- ✅ **Logging Schema**: Passed
- ✅ **AlwaysApply Policy**: Enforced
- ✅ **User Rules Policy**: Documented

### **Files Validated**
```
analysis_batching.mdc, automated_development_management.mdc, core_workflow.mdc, 
veritas_runs.mdc, ui_policy.mdc, how_to_make_a_cursor_rule.mdc, docker_health_checks.mdc, 
docker_best_practices.mdc, mcp_ops.mdc, system_integration_status.mdc, api_contracts.mdc, 
models_and_embeddings.mdc, testing_standards.mdc, project_overview.mdc, 
error_handling_and_testing.mdc, resilience_dashboard_ui.mdc, mcp_enforcement.mdc, 
mcp_server_integration.mdc, mcp_hub_server_status.mdc, ai_integration.mdc, master_log.mdc, 
system_management.mdc, fallbacks_and_health.mdc, visualization_system.mdc, mcp_integration.mdc, 
cursor_apparmor_fix.mdc, complete_analysis_pipeline.mdc, living_truth_agent_integration.mdc, 
00-global.mdc, docker_management.mdc, database_schema_consistency.mdc, coding_standards.mdc, 
system_status.mdc
```

## 🚨 **Critical Requirements**

### **Before Any MCP Change**
1. Run `validate_mcp_requirements_reference()` to check current state
2. Read `MCP_REQUIREMENTS_REFERENCE.md` for current requirements
3. Check if change affects existing MCP tools or rules
4. Plan updates to reference document if needed

### **After Any MCP Change**
1. Run `update_mcp_requirements_reference()` to update the reference document
2. Update `MCP_REQUIREMENTS_REFERENCE.md` with new requirements
3. Validate all MCP tools still function (both servers)
4. Update relevant Cursor rules
5. Update phase documentation

### **Before Phase Completion**
1. Run `enforce_mcp_compliance(phase)` to validate all requirements
2. Ensure `MCP_REQUIREMENTS_REFERENCE.md` reflects all changes
3. Validate all MCP tools and rules (both servers)
4. Update master log and completion summaries
5. Run full CI validation

## 📋 **Phase Close Checklist**
Before closing any phase:
- [ ] MCP tools updated and validated (both servers)
- [ ] Cursor rules updated and validated
- [ ] **AlwaysApply policy verified** - only 00-global.mdc has `alwaysApply: true`
- [ ] **User Rules reviewed** - ensure minimal and not duplicating project rules
- [ ] MDC addenda updated
- [ ] CI green with all new gates/tests
- [ ] Docs: plan + completion + master log updated
- [ ] MCP specs updated
- [ ] All errors handled and logged
- [ ] **MCP_REQUIREMENTS_REFERENCE.md updated**

## 🎯 **Benefits Achieved**

### **Performance**
- Only essential global guidelines auto-apply, reducing context bloat
- AI can choose relevant rules based on specific task context
- Improved response times and reduced token usage

### **Maintainability**
- Clear separation between global and specialized rules
- Consistent formatting across all MDC files
- Automated validation prevents rule drift

### **Quality**
- Comprehensive validation ensures all rules are properly formatted
- MCP tools provide reliable feedback on rule health
- Automated checks prevent incomplete or malformed rules

### **Flexibility**
- Agent can dynamically select the most relevant rules for each task
- Specialized rules can be contextually applied
- Archive rules preserve historical knowledge without cluttering context

## 🔄 **Next Steps**

### **Immediate Actions**
1. **Add Global User Rules** to Cursor Settings → Rules (see separate document)
2. **Monitor MCP validation** on all future changes
3. **Enforce alwaysApply policy** for any new rules created

### **Ongoing Maintenance**
1. **Regular validation** of all MDC files
2. **Update MCP tools** as needed for new rule types
3. **Review User Rules** periodically to ensure they remain minimal and focused

## 📚 **References**

- [Cursor Rules Documentation](https://docs.cursor.com/en/context/rules#user-rules)
- [MCP Requirements Reference](MCP_REQUIREMENTS_REFERENCE.md)
- [Global Rule](.cursor/rules/00-global.mdc)
- [MCP Enforcement Rule](.cursor/rules/mcp_enforcement.mdc)

---

**Last Updated**: August 14, 2025  
**Status**: ✅ Complete and Verified  
**Validation**: All 33 MDC files valid, both MCP servers working correctly
