.PHONY: check fix check-full ai ai-quick ai-only ssot masterlog lm-tools lm-mcp
check:
	python scripts/verify_complete_ssot_system.py --scope fast
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
masterlog:
	@python build_master_log.py rebuild
	@echo "docs/project_master_log.md rebuilt"

lm-tools:
	LMSTUDIO_TOOLS_PORT=8756 python scripts/bridge/lmstudio_tools_bridge.py

lm-mcp:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; Phase9MCPServer().serve_stdio()"





