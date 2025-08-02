# Revised Instructions for Cursor AI to Fix Alignment Issues in Living Truth Engine

These instructions have been updated based on the latest README.md (August 2, 2025), which reflects the current Langflow-based system, integrated services (e.g., Redis, Neo4j, LM Studio), extensive MCP tools, and the new Ubuntu Cursor Fix section. Key revisions: Emphasize Langflow over Flowise equivalents; incorporate README's service URLs and MCP tool list (e.g., use existing `generate_viz` for visualizations, `query_langflow` for audio if integrated); align with updated project structure (e.g., scripts/setup/ for automation); reference the Cursor Fix for Ubuntu stability; use fresh GitHub summaries for optional servers (Rulego: Go-based with MCP auto-registration, no native Docker; Director: No exact repo found—use alternative from awesome-mcp-servers like mcp-solver for routing; DevDocs: Docker-supported with crawl scripts). Prioritize minimal changes for stability, following "if it ain't broke, don't fix it." Use MCP tools for automation (e.g., `mcp_living_truth_fastmcp_server_auto_update_all_documentation()` post-changes). Follow cursor rules: @mcp_server_integration.mdc for additions, @docker_best_practices.mdc for Docker, @coding_standards.mdc for code. Test with `mcp_living_truth_fastmcp_server_comprehensive_health_check()`. Project root: `/home/mccoy/Projects/NotebookLM/LivingTruthEngine`.

## Step 1: Verify and Add Dash Service for Visualizations (If Needed)
README mentions DASHBOARD_PORT=8050 but no dedicated service in docker-compose.yml (visualizations via `generate_viz` and outputs/visualizations volume). Check if current MCP/Langflow handles interactive dashboards; if not, add Dash for plan alignment.

1. **Prompt for Verification**:
   - In Cursor: "Reference README.md and @project_overview.mdc: Test if `mcp_living_truth_fastmcp_server_generate_viz(viz_type="network")` provides interactive dashboards (e.g., Plotly via Langflow). If insufficient for structured outputs/visualizations, generate Dash service addition to docker/docker-compose.yml per @docker_best_practices.mdc: python:3.12-slim base, non-root user, curl healthcheck on /health, volumes for data/outputs/visualizations, depends_on langflow/postgres/redis/neo4j, network living-truth-network. Expose 8050. Integrate with existing analysis modules."

2. **Implementation Steps (If Addition Needed)**:
   - Add to `docker/docker-compose.yml`:
     ```
     dashboard:
       build:
         context: ..
         dockerfile: docker/Dockerfile.dash  # Create if needed
       container_name: living-truth-dashboard
       ports:
         - "8050:8050"
       volumes:
         - ../data/outputs/visualizations:/app/visualizations
       environment:
         - PYTHONPATH=/app/src
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8050/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 60s
       depends_on:
         langflow:
           condition: service_healthy
         postgres:
           condition: service_healthy
         redis:
           condition: service_healthy
         living-truth-neo4j:
           condition: service_healthy
       restart: unless-stopped
       networks:
         - living-truth-network
     ```
   - Create `docker/Dockerfile.dash`:
     ```
     FROM python:3.12-slim
     RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*
     RUN useradd -m appuser
     WORKDIR /app
     COPY requirements.txt .
     RUN pip install --no-cache-dir -r requirements.txt dash plotly pandas
     COPY src/ /app/src/
     USER appuser
     CMD ["uvicorn", "src.analysis.dash_app:app", "--host", "0.0.0.0", "--port", "8050"]
     HEALTHCHECK CMD curl -f http://localhost:8050/health || exit 1
     ```
   - Test: `docker compose -f docker/docker-compose.yml up -d`, curl http://localhost:8050. Update README.md Service URLs and Quick Reference.

3. **Validation**: Run `mcp_living_truth_fastmcp_server_generate_viz()`. If Ubuntu issues during testing, apply README's Cursor Fix: `./scripts/setup/fix_cursor_apparmor.sh`.

## Step 2: Verify Audio Outputs
README aligns with TTS config (en_US-lessac-medium.onnx); verify structured audio outputs via Langflow/MCP.

1. **Prompt for Verification**:
   - In Cursor: "Per README.md MCP tools and @development_workflow.mdc: Test audio via `mcp_living_truth_fastmcp_server_query_langflow(query="Sample testimony", output_type="audio", anonymize=true)`. If fails, add to src/mcp_servers/living_truth_fastmcp_server.py LivingTruthEngine class: Method `generate_audio(text: str) -> str` using piper-tts (import if needed), save to data/outputs/audio/. Create MCP tool `generate_audio`. Follow @coding_standards.mdc with error handling."

2. **Implementation Steps (If Fix Needed)**:
   - Add to `LivingTruthEngine`:
     ```python
     def generate_audio(self, text: str) -> str:
         """Generate audio from text using TTS model.
         
         Args:
             text: Input text for audio generation.
         
         Returns:
             Path to generated audio file.
         
         Raises:
             ValueError: If text is empty.
             RuntimeError: If TTS fails.
         """
         if not text:
             raise ValueError("Text cannot be empty")
         try:
             from piper import PiperVoice  # Add to requirements.txt if missing
             voice = PiperVoice.load(self.tts_model_path)
             output_path = f"data/outputs/audio/{hash(text)}.wav"
             voice.synthesize(text, output_path)
             return output_path
         except Exception as e:
             raise RuntimeError(f"TTS generation failed: {e}")
     ```
   - Add MCP tool:
     ```python
     @mcp.tool()
     def generate_audio(text: str) -> str:
         """Generate audio from text."""
         return engine.generate_audio(text)
     ```
   - Test query; update README.md tools list via MCP auto-update.

3. **Validation**: Check outputs/audio/; run `mcp_living_truth_fastmcp_server_auto_update_all_documentation()`.

## Step 3: Confirm LangSmith Metrics for Performance Tracing
README emphasizes <2s API responses; verify <5s plan goal with LangSmith (enabled in env).

1. **Prompt for Verification**:
   - In Cursor: "Align with README.md performance metrics: Create scripts/testing/trace_performance.sh per @system_management.mdc: Activate venv, run `query_langflow` samples, measure/log times (>5s warning). If slow, optimize LM Studio env in compose (e.g., THREADS=auto to higher, GPU_LAYERS if available)."

2. **Implementation Steps (If Needed)**:
   - Create script:
     ```bash
     #!/bin/bash
     source ../living_venv/bin/activate
     python -c "
     import time
     from mcp import mcp_living_truth_fastmcp_server_query_langflow
     queries = ['Test query 1', 'Test query 2']
     for q in queries:
         start = time.time()
         result = mcp_living_truth_fastmcp_server_query_langflow(q)
         duration = time.time() - start
         print(f'Query \"{q}\": {duration}s')
         if duration > 5:
             print('WARNING: Exceeds 5s')
     "
     ```
   - Test and adjust compose if needed.

3. **Validation**: Aim for <2s per README; update CURRENT_STATUS.md.

## Step 4: Add Optional MCP Servers (Rulego, Director, DevDocs)
README has 5 MCP servers; add plan's optionals using fresh GitHub info (Rulego: Go-based, MCP auto-register, compile/build; Director: No exact repo—use mcp-solver from search as alt for solving/routing; DevDocs: Docker via docker-start.sh, .env, crawling). Integrate into fastmcp if possible; else separate. Follow @mcp_server_integration.mdc.

1. **General Prompt for Each**:
   - In Cursor: "Add [Server Name] per README.md MCP integration and @mcp_server_integration.mdc: Create src/mcp_servers/[server]_mcp_server.py with FastMCP, add tools (e.g., query_workflow), integrate LM Studio/Qwen3. Update .cursor/mcp.json. Add Docker service if supported. Test green dot, use `auto_detect_and_add_tools`. Update README.md tools."

2. **Specific for Rulego (Workflow Orchestration)**:
   - Compile: Use code_execution: `go build -tags with_extend cmd/server`.
   - Config: config.conf with [mcp] enable=true.
   - Docker: Create manual (golang base, copy binary/config, CMD ./server -c=config.conf).
   - Tools: `query_rulego_chain`, `get_rulego_status`.
   - Pros vs Langflow: Lighter (no DB), hot updates, visualization; Cons: Less AI-focused.
   - Test: Start server, MCP tools.

3. **Specific for Director (LLM Routing—Use mcp-solver Alt)**:
   - From search: Use https://github.com/szeider/mcp-solver (integrates SAT/SMT with LLMs via MCP).
   - Setup: Clone, follow README for Python/venv.
   - Docker: Not specified; add if possible.
   - Tools: `solve_constraint`, `route_llm`.
   - Integration: Proxy/routing to models.
   - Test as separate server.

4. **Specific for DevDocs (Document Retrieval)**:
   - Setup: git clone, cp .env.template .env (NEXT_PUBLIC_BACKEND_URL=http://localhost:24125), ./docker-start.sh (Mac/Linux) or docker-start.bat (Windows—experimental).
   - Docker: Built-in compose; add service (ports for UI/backend, volumes for crawl_results).
   - Tools: `crawl_docs(depth=3)`, `retrieve_docs`.
   - Pros vs PGVector: Faster crawl (1000/min), free teams; Cons: Less scalable, no vectors.
   - Test: Crawl sample docs to sources/.

5. **Post-Addition**:
   - Run `docker compose up -d`.
   - Test tools; auto-update docs/rules.
   - Prioritize: DevDocs (retrieval enhancement), Rulego (workflows), mcp-solver (routing alt).
   - If Ubuntu issues: Apply README Cursor Fix.

## Final Validation
- Run `mcp_living_truth_fastmcp_server_auto_validate_system_state()`.
- Commit; update README.md/CURRENT_STATUS.md with new services/tools.
- Create troubleshooting rule if needed via @how_to_make_a_cursor_rule.mdc.