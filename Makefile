.PHONY: check fix check-full ai ai-quick ai-only ssot ssot-agent masterlog lm-tools lm-mcp ruff-check ruff-fix ruff-comprehensive ruff-line-length fix-fallbacks rules-validate rules-fix enable-githooks
check:
	@$(MAKE) rules-validate
	@python scripts/verify_complete_ssot_system.py --fix
	@if [ "$${REPORT:-0}" = "1" ]; then \
		echo "REPORT=1 → also generating SSOT agent report"; \
		$(MAKE) ssot-agent; \
	fi
fix:
	python scripts/verify_complete_ssot_system.py --scope full --fix
check-full:
	python scripts/verify_complete_ssot_system.py --scope full
ai:
	SSOT_AI=1 python scripts/verify_complete_ssot_system.py --scope ai --ai
ai-quick:
	python scripts/test_ai_quick.py
ai-only:
	python scripts/test_ai_only.py
ssot: fix
ssot-agent:
	python -m src.agents.ssot_langchain_agent --config config/agents/ssot_agent.yaml
masterlog:
	@python build_master_log.py rebuild
	@echo "docs/project_master_log.md rebuilt"

lm-tools:
	LMSTUDIO_TOOLS_PORT=8756 python scripts/bridge/lmstudio_tools_bridge.py

lm-mcp:
	python src/mcp_servers/phase9_mcp_server.py

mcp-diagnostics:
	python scripts/mcp_router_diagnostics.py --cmd "make lm-mcp" --timeout 8 --max-seconds 20

# Code quality tools (Ruff-based)
ruff-check:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.run_ruff_check(); print('Ruff check result:', result)"
ruff-fix:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.run_ruff_check(fix=True); print('Ruff fix result:', result)"
ruff-comprehensive:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.run_ruff_comprehensive(); print('Ruff comprehensive result:', result)"
ruff-line-length:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.run_ruff_line_length_fix(); print('Ruff line length fix result:', result)"
fix-fallbacks:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; server = Phase9MCPServer(); result = server.fix_silent_fallbacks(); print('Fix silent fallbacks result:', result)"

# Validate all Cursor rules frontmatter (strict schema + checksum)
rules-validate:
	@python scripts/validate_cursor_rules_frontmatter.py --strict

# Best-effort fixer: adds/repairs missing frontmatter (preserves body); re-run validate after
rules-fix:
	@python scripts/fix_cursor_rules_frontmatter.py
	@$(MAKE) rules-validate

# One-time: enable project githooks (pre-commit runs rules-validate)
enable-githooks:
	@mkdir -p .githooks
	@printf '%s\n' '#!/usr/bin/env bash' 'python scripts/validate_cursor_rules_frontmatter.py --strict' > .githooks/pre-commit
	@chmod +x .githooks/pre-commit
	@git config core.hooksPath .githooks
	@echo "✓ Git hooks enabled (rules-validate on pre-commit)"





