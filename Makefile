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

# Validate all Cursor rules frontmatter (Cursor-spec: description, globs, alwaysApply)
rules-validate:
	@python scripts/validate_cursor_rules_frontmatter.py

# Best-effort fixer: migrate to Cursor-spec frontmatter; re-run validate after
rules-fix:
	@python scripts/fix_cursor_rules_frontmatter.py
	@$(MAKE) rules-validate

# One-time: enable project githooks (pre-commit runs rules-validate)
enable-githooks:
	@mkdir -p .githooks
	@printf '%s\n' '#!/usr/bin/env bash\nset -euo pipefail\npython scripts/validate_cursor_rules_frontmatter.py\npython scripts/meta_precommit_guard.py\n' > .githooks/pre-commit
	@chmod +x .githooks/pre-commit
	@git config core.hooksPath .githooks
	@echo "✓ Git hooks enabled (rules-validate on pre-commit)"

reports: meta-index meta-validate
	@echo "✓ Reports ready in ./reports"

.PHONY: meta-index
meta-index:
	@python scripts/collect_yaml_meta.py --out reports/ssot_meta_index.json
	@echo "✓ SSOT metadata index: reports/ssot_meta_index.json"

meta-validate:
	@python scripts/validate_ssot_meta_index.py
	@echo "✓ SSOT metadata index validated"

# CI-safe: generate + validate (no silent fallbacks)
meta-ci: meta-index meta-validate
	@echo "✓ SSOT meta CI step ok"

# Focused unit tests for metadata system
test-meta:
	pytest -q tests/test_ssot_meta_index.py





.PHONY: up down rebuild-dashboard health
up:
	 docker compose -f docker/docker-compose.yml up -d

down:
	 docker compose -f docker/docker-compose.yml down --remove-orphans

rebuild-dashboard:
	 COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker compose -f docker/docker-compose.yml build dashboard
	 docker compose -f docker/docker-compose.yml up -d dashboard

health:
	 bash scripts/healthcheck.sh
.PHONY: mcp-smoke snapshot watchdog ci-ssot
mcp-smoke:
	python scripts/mcp_smoke_list.py | tee reports/mcp_smoke.json
snapshot:
	python scripts/ssot_watchdog.py
watchdog: snapshot
ci-ssot:
	make meta-index && make meta-validate
	python scripts/verify_complete_ssot_system.py --scope fast --fix || true
	python scripts/validate_cursor_rules_frontmatter.py

.PHONY: dash-ssot-check
dash-ssot-check:
	@mkdir -p reports
	@ls reports/ssot_snapshot_*.json >/dev/null 2>&1 || make snapshot
	@echo "▶ /api/health" && curl -sf http://127.0.0.1:8050/api/health | jq -e ".status==\"ok\"" >/dev/null
	@echo "▶ /api/ssot/snapshot/latest" && curl -sf http://127.0.0.1:8050/api/ssot/snapshot/latest | jq -e ".status==\"ok\" and .data.file!=null" >/dev/null
