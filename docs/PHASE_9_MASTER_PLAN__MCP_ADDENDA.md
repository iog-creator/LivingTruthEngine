---
phase: 9.3
status: active
last_reviewed: 2025-08-13
related_files: ['PHASE_9.md', 'scripts/perf_harness.py']
---

# MCP Addenda for Phase 9 Plans

## Overview

This document provides **Gates** blocks that should be pasted into each Phase 9 plan. These gates define the required MCP operations for validation and completion of each sub-phase.

## Gates Format

Each plan should include a **Gates** section with:
- **Preflight**: Operations to run before coding begins
- **Exit**: Operations to run before marking the phase complete

## Phase-Specific Gates

### **For 9.4.0 (DevOps Cutover Skeleton)**
**Gates (run via MCP, enforced in PR)**
- **Preflight**: 
  - `mcp.project.rules.validate`
  - `mcp.lte.health.get_full`
  - `mcp.lte.models.registry_show`
- **Exit**: 
  - `mcp.lte.proxy.smoke` (root HTML + `/api/…` ok)
  - `mcp.lte.smoke.run_phase` with `scripts/p9_4_0_smoke.sh`

### **For 9.4.1–9.4.7 (UI series)**
**Gates**
- **Preflight**: `mcp.project.rules.validate`
- **Exit**: 
  - `mcp.lte.ui.contracts.validate_envelopes` (the endpoints the page uses)
  - `mcp.lte.ui.contracts.playwright_smoke` (specs for the touched pages)

### **For 9.5.0 (Real Adapters)**
**Gates**
- **Exit**:
  - `mcp.lte.adapters.test_sources` {"sources":["youtube","web","pdf"],"limit":1}
  - `mcp.lte.smoke.run_phase` with `scripts/p9_5_0_smoke.sh`

### **For 9.5.1 (Model‑Aware Embedding Storage)**
**Gates**
- **Exit**:
  - `mcp.lte.pgvector.db_dim` (both tables)
  - `mcp.lte.models.assert_embedding_dim`
  - `mcp.lte.pgvector.reindex_ann`

### **For 9.5.2 (GPU Scheduler + Health)**
**Gates**
- **Exit**: 
  - `mcp.lte.gpu.status`
  - `mcp.lte.gpu.simulate_low_vram` (fallback visible in `/api/health/full`)

### **For 9.5.3 (Timeline)**
**Gates**
- **Exit**: 
  - `mcp.lte.timeline.preview` (SLA: response in < 1s for sample run)

### **For 9.5.4 (Perf Gates & Hardening)**
**Gates**
- **Exit**:
  - Run `scripts/perf_harness.py` and attach results to PR
  - Confirm budgets in completion summary (p95 API latencies, LCP, bundle size)

## Implementation Notes

### **Gate Execution**
- All gates must pass before marking a phase complete
- Gate failures should be documented in the completion summary
- Gates can be run manually or integrated into CI/CD pipelines

### **Gate Validation**
- Preflight gates ensure the environment is ready for development
- Exit gates validate that the implementation meets requirements
- Gate results should be included in PR descriptions

### **Gate Customization**
- Gates can be customized based on specific phase requirements
- Additional gates can be added for phase-specific validation
- Gate parameters can be adjusted based on implementation details

## Example Usage

### **In a Phase Plan**
```markdown
## Gates

**Preflight (run via MCP)**
- `mcp.project.rules.validate`
- `mcp.lte.health.get_full`

**Exit (run via MCP)**
- `mcp.lte.ui.contracts.validate_envelopes`
- `mcp.lte.smoke.run_phase` with `scripts/p9_4_2_smoke.sh`
```

### **In Completion Summary**
```markdown
## Gate Results

**Preflight Gates**
- ✅ `mcp.project.rules.validate` - All rules valid
- ✅ `mcp.lte.health.get_full` - System healthy

**Exit Gates**
- ✅ `mcp.lte.ui.contracts.validate_envelopes` - All endpoints valid
- ✅ `mcp.lte.smoke.run_phase` - Smoke tests passed
```

## References

- [Phase 9 Master Plan](../PHASE_9_MASTER_PLAN.md)
- [MCP Tool Specifications](../tools/mcp/specs/)
- [Implementation Summary](../PHASE_9_RULES_AND_MCP_IMPLEMENTATION_SUMMARY.md)
- [CI Validation Script](../scripts/ci/validate_phase9.sh)

