# LM Studio Integration (Local Only)

This document describes how to integrate LM Studio with the Living Truth Engine's Single Source of Truth (SSOT) validation system.

## What you get
- **OpenAI tools-style bridge** at `http://127.0.0.1:8756`:
  - `POST /tools/verify_ssot` → runs deterministic SSOT check (CI-safe mode)
  - `POST /tools/read_ssot_report` → returns JSON report
  - `POST /tools/draft_patches` → returns minimal patch specs (no writes)
  - `POST /tools/run_repo_inventory` → optional inventory summary
- **MCP server** (existing): `src/mcp_servers/phase9_mcp_server.py` (stdio). LM Studio can connect as MCP client.

## How to run
- Terminal A: `make lm-tools`  (starts FastAPI bridge on 127.0.0.1:8756)
- Terminal B: Optional `make lm-mcp` (runs our MCP server over stdio)

## MCP Setup for LM Studio

### Option 1: Direct MCP Connection
1. In LM Studio UI: **Settings → MCP**
2. Add server with command: `python src/mcp_servers/phase9_mcp_server.py`
3. Ask questions like:
   - "Can you validate the cursor rules?"
   - "Can you run health checks?"
   - "Can you validate the SSOT bundle?"

### Option 2: LM Studio Plugin (Recommended)
1. Build the plugin:
   ```bash
   cd lmstudio-mcp-tools
   npm install
   npm run build
   ```
2. Copy to LM Studio plugins directory:
   ```bash
   cp -r lmstudio-mcp-tools /path/to/lmstudio/plugins/
   ```
3. Restart LM Studio
4. Ask the same questions - you'll see inference in developer logs!

## Recommended LM Studio setup
- Use your preferred model (e.g., `llama-3.2-3b-instruct`) with **function/tools** enabled.
- Register tools as simple HTTP calls to the endpoints above, or connect to MCP:
  - Tools example:
    - `verify_ssot()` → POST `http://127.0.0.1:8756/tools/verify_ssot`
    - `read_ssot_report()` → POST `http://127.0.0.1:8756/tools/read_ssot_report`
    - `draft_patches()` → POST `http://127.0.0.1:8756/tools/draft_patches`
    - `run_repo_inventory()` → POST `http://127.0.0.1:8756/tools/run_repo_inventory`
- **Do not** grant write actions from LM Studio. Draft patches only.
  Cursor (with SSOT guards) remains the executor of edits and commits.

## Safety boundaries
- SSOT enforcement remains the arbiter; LM Studio only drafts.
- No `--fix` or write operations are exposed via the bridge.
- CI does not call LM Studio.

## Agent Mode (Phase 9.5.7.4.7)

A deterministic, read‑only agent sequences SSOT tasks via the local bridge. It never writes to the repo; Cursor applies patches with SSOT gating.

**Run (deterministic, no LLM path):**
```bash
make ssot-agent
# or
python -m src.agents.ssot_langchain_agent --config config/agents/ssot_agent.yaml
```

**Optional LangChain path (still read‑only):**
```bash
python -m src.agents.ssot_langchain_agent --config config/agents/ssot_agent.yaml --langchain
```

**Output**
- JSON envelope saved to `reports/ssot_agent_output_<UTC>.json`
- Also printed to STDOUT as `{status,data?,error?}`

**Safety**
- Bridge is local-only (`127.0.0.1:8756`)
- CI does not call the agent
- SSOT enforcement remains the gate for all edits
