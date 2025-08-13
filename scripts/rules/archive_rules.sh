#!/usr/bin/env bash
set -euo pipefail
mkdir -p .cursor/rules/archive
for f in build_verify_iterate.mdc workflow.mdc current_working_state.mdc cursor_rule_management.mdc mcp_hub_server.mdc mcp_red_dot.mdc phase_8_1_implementation.mdc migrated_functionality.mdc; do
  [ -f ".cursor/rules/$f" ] && git mv ".cursor/rules/$f" ".cursor/rules/archive/$f" || true
done
