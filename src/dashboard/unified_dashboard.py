"""
Living Truth Engine - Unified Dashboard
Main FastAPI application consolidating all functionality into a single user-friendly interface.
"""

from fastapi import FastAPI, HTTPException, Request, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import json
import os
from pathlib import Path
import logging

# Import existing services
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mcp_servers.mcp_hub_server import MCPHubServer
except ImportError as e:
    logger.error(f"Failed to import MCPHubServer: {e}")
    MCPHubServer = None

class UnifiedDashboard:
    def __init__(self):
        self.app = FastAPI(
            title="Living Truth Engine - Unified Dashboard",
            description="Single interface for survivor testimony analysis and evidence discovery",
            version="1.0.0"
        )
        
        # Setup middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize services
        if MCPHubServer:
            try:
                self.hub_server = MCPHubServer()
                logger.info("MCP Hub Server initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize MCP Hub Server: {e}")
                self.hub_server = None
        else:
            self.hub_server = None
            logger.warning("MCP Hub Server not available")
        
        self.templates = Jinja2Templates(directory="src/dashboard/templates")
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory="src/dashboard/static"), name="static")
        
        # Setup routes
        self.setup_routes()
    
    def setup_routes(self):
        """Setup all dashboard routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Home page with quick start and recent activity"""
            return self.templates.TemplateResponse(
                "home.html", 
                {"request": request, "title": "Living Truth Engine - Home"}
            )
        
        @self.app.get("/runs", response_class=HTMLResponse)
        async def runs_page(request: Request):
            """Runs page - browse bundles and view details"""
            return self.templates.TemplateResponse(
                "runs.html", 
                {"request": request, "title": "Runs - Living Truth Engine"}
            )
        
        @self.app.get("/analyze", response_class=HTMLResponse)
        async def analyze_page(request: Request):
            """Analyze page - pick bundle/doc and view results"""
            return self.templates.TemplateResponse(
                "analyze.html", 
                {"request": request, "title": "Analyze - Living Truth Engine"}
            )
        
        @self.app.get("/advanced", response_class=HTMLResponse)
        async def advanced_page(request: Request):
            """Advanced page - expert controls and raw MCP tester"""
            return self.templates.TemplateResponse(
                "advanced.html", 
                {"request": request, "title": "Advanced - Living Truth Engine"}
            )
        
        # API Routes for UI functionality
        @self.app.post("/api/runs/youtube/start")
        async def start_youtube_run(request: Request):
            """Start a YouTube channel analysis run with optional labeling and output dir."""
            try:
                data = await request.json()
                topic = f"YouTube analysis: {data.get('channel_url', 'Unknown')}"
                params = {
                    "topic": topic,
                    "max_docs": data.get('limit', 10),
                    "sources": ["youtube"],
                }
                # Start run via MCP if available
                result: Dict[str, Any]
                if self.hub_server:
                    result = self.hub_server.execute_tool("start_veritas_run", params)
                else:
                    result = {"run_id": f"local-{int(os.times().elapsed)}", "status": "started"}

                run_id = result.get("run_id") or result.get("id")
                label = (data.get("label") or "").strip()
                output_dir = (data.get("output_dir") or "").strip()

                # Persist optional label and create symlink to desired location
                try:
                    if run_id and (label or output_dir):
                        labels_path = Path("data/runs/labels.json")
                        labels_path.parent.mkdir(parents=True, exist_ok=True)
                        labels: Dict[str, Any] = {}
                        if labels_path.exists():
                            with open(labels_path, "r") as f:
                                labels = json.load(f)
                        if label:
                            labels[run_id] = {"label": label}
                            with open(labels_path, "w") as f:
                                json.dump(labels, f, indent=2)
                        if output_dir:
                            src = Path("data/runs") / run_id
                            dst_dir = Path(output_dir)
                            dst_dir.mkdir(parents=True, exist_ok=True)
                            link = dst_dir / (label or run_id)
                            if src.exists() and not link.exists():
                                try:
                                    os.symlink(src.resolve(), link)
                                except Exception:
                                    pass
                except Exception:
                    pass

                return {"status": "ok", "data": result}
            except Exception as e:
                return {"status": "error", "error": {"code": "start_failed", "msg": str(e)}}
        
        @self.app.get("/api/runs")
        async def list_runs():
            """List all available runs/bundles as a normalized list of objects."""
            def normalize_runs(raw: Any) -> list[dict[str, Any]]:
                # Accept {runs: [id,...]} or [ {run_id: ...}, ... ]
                if isinstance(raw, dict) and "runs" in raw:
                    return [{"run_id": r} if not isinstance(r, dict) else r for r in raw["runs"]]
                if isinstance(raw, list):
                    return [r if isinstance(r, dict) else {"run_id": r} for r in raw]
                return []

            if not self.hub_server:
                try:
                    runs_dir = Path("data/runs")
                    runs = []
                    if runs_dir.exists():
                        runs = [d.name for d in runs_dir.iterdir() if d.is_dir()]
                    return {"status": "ok", "data": normalize_runs({"runs": runs})}
                except Exception as e:
                    return {"status": "error", "error": {"code": "list_failed", "msg": f"MCP server unavailable, fallback failed: {str(e)}"}}

            try:
                result = self.hub_server.execute_tool("list_veritas_runs", {"limit": 20})
                return {"status": "ok", "data": normalize_runs(result)}
            except Exception as e:
                try:
                    runs_dir = Path("data/runs")
                    runs = []
                    if runs_dir.exists():
                        runs = [d.name for d in runs_dir.iterdir() if d.is_dir()]
                    return {"status": "ok", "data": normalize_runs({"runs": runs})}
                except Exception as fallback_error:
                    return {"status": "error", "error": {"code": "list_failed", "msg": f"MCP: {str(e)}, Fallback: {str(fallback_error)}"}}
        
        @self.app.get("/api/runs/{run_id}")
        async def get_run_details(run_id: str):
            """Get details for a specific run with filesystem fallback."""
            # Try MCP first
            if self.hub_server:
                try:
                    result = self.hub_server.execute_tool("get_veritas_run_status", {"run_id": run_id})
                    return {"status": "ok", "data": result}
                except Exception:
                    pass

            # Fallback to status.json
            try:
                status_path = Path("data/runs") / run_id / "status.json"
                details: dict[str, Any] = {"run_id": run_id}
                if status_path.exists():
                    with open(status_path, "r") as f:
                        status = json.load(f)
                    details.update(status)
                return {"status": "ok", "data": details}
            except Exception as e:
                return {"status": "error", "error": {"code": "details_failed", "msg": str(e)}}
        
        @self.app.get("/api/runs/{run_id}/corpus")
        async def get_run_corpus(run_id: str):
            """Get corpus data for a run with filesystem fallback."""
            # Try MCP first
            if self.hub_server:
                try:
                    result = self.hub_server.execute_tool("open_veritas_bundle", {"run_id": run_id})
                    return {"status": "ok", "data": result}
                except Exception:
                    pass

            # Fallback to corpus.jsonl
            try:
                run_dir = Path("data/runs") / run_id
                corpus_jsonl = run_dir / "corpus.jsonl"
                documents: list[dict[str, Any]] = []
                if corpus_jsonl.exists():
                    with open(corpus_jsonl, "r") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                documents.append(json.loads(line))
                            except Exception:
                                continue
                return {"status": "ok", "data": {"documents": documents}}
            except Exception as e:
                return {"status": "error", "error": {"code": "corpus_failed", "msg": str(e)}}
        
        @self.app.post("/api/analyze/entities")
        async def analyze_entities(request: Request):
            """Analyze entities for a document"""
            try:
                data = await request.json()
                result = self.hub_server.execute_tool("analyze_transcript", data)
                return {"status": "ok", "data": result}
            except Exception as e:
                return {"status": "error", "error": {"code": "analysis_failed", "msg": str(e)}}
        
        @self.app.post("/api/analyze/claims")
        async def analyze_claims(request: Request):
            """Analyze claims for a document"""
            try:
                data = await request.json()
                result = self.hub_server.execute_tool("query_langflow", data)
                return {"status": "ok", "data": result}
            except Exception as e:
                return {"status": "error", "error": {"code": "claims_failed", "msg": str(e)}}
        
        @self.app.get("/api/status")
        async def get_status():
            """Get system status"""
            try:
                result = self.hub_server.get_status()
                return {"status": "ok", "data": result}
            except Exception as e:
                return {"status": "error", "error": {"code": "status_failed", "msg": str(e)}}
        
        @self.app.get("/api/tools")
        async def get_tools():
            """Get available MCP tools. Falls back to registry file if needed."""
            def group_by_server(registry: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
                categories: dict[str, list[dict[str, Any]]] = {}
                for server_name, server_data in registry.get("servers", {}).items():
                    categories[server_name] = []
                    for tool in server_data.get("tools", []):
                        categories[server_name].append({
                            "name": tool.get("name"),
                            "description": tool.get("description", ""),
                        })
                return categories

            # Try hub server first
            try:
                if self.hub_server:
                    result = self.hub_server.list_tools("", "")
                    # If result is empty or not as expected, fall through
                    if isinstance(result, dict) and result.get("categories"):
                        return {"status": "ok", "data": result}
            except Exception:
                pass

            # Fallback to registry file
            try:
                registry_path = Path("config/tool_registry.json")
                with open(registry_path, "r") as f:
                    registry = json.load(f)
                categories = group_by_server(registry)
                return {"status": "ok", "data": {"categories": categories}}
            except Exception as e:
                return {"status": "error", "error": {"code": "tools_failed", "msg": str(e)}}

        @self.app.post("/api/execute")
        async def execute_tool(request: Request):
            """Execute a tool by name with params."""
            try:
                data = await request.json()
                tool_name = data.get("tool_name")
                params = data.get("params", {})
                if not tool_name:
                    return {"status": "error", "error": {"code": "invalid_request", "msg": "tool_name is required"}}
                if not self.hub_server:
                    return {"status": "error", "error": {"code": "mcp_unavailable", "msg": "MCP server not available"}}
                result = self.hub_server.execute_tool(tool_name, params)
                return {"status": "ok", "data": result}
            except Exception as e:
                return {"status": "error", "error": {"code": "execute_failed", "msg": str(e)}}
        
        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "service": "unified_dashboard"}

def main():
    """Start the unified dashboard server"""
    dashboard = UnifiedDashboard()
    return dashboard.app

# For direct execution
if __name__ == "__main__":
    uvicorn.run(
        main(),
        host="0.0.0.0",
        port=8050,
        log_level="info"
    )

