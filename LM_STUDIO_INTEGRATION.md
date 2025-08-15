# LM Studio Integration (Local Only)

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
