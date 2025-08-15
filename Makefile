.PHONY: masterlog lm-tools lm-mcp
masterlog:
	@python build_master_log.py rebuild
	@echo "docs/project_master_log.md rebuilt"

lm-tools:
	LMSTUDIO_TOOLS_PORT=8756 python scripts/bridge/lmstudio_tools_bridge.py

lm-mcp:
	python -c "from src.mcp_servers.phase9_mcp_server import Phase9MCPServer; Phase9MCPServer().serve_stdio()"





