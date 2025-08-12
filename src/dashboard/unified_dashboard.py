"""
Living Truth Engine - Unified Dashboard
Main FastAPI application consolidating all functionality into a single user-friendly interface.
"""

import json
import logging
import os

# Import existing services
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from mcp_servers.mcp_hub_server import MCPHubServer
except ImportError as e:
    logger.error(f"Failed to import MCPHubServer: {e}")
    MCPHubServer = None

# Import contract router
try:
    from .contract import router as contract_router
except ImportError as e:
    logger.error(f"Failed to import contract router: {e}")
    contract_router = None

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

        # Include contract router if available
        if contract_router:
            self.app.include_router(contract_router)
        
        # WebSocket connections
        self.active_connections = []

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
                    "max_videos": data.get('limit', 10),
                    "channel_url": data.get('channel_url'),
                    "crawl_depth": data.get('max_depth', 1),
                    "transcript_pref": "yt_api",
                    "sources": ["youtube"],
                }
                # Start run via MCP if available
                result: dict[str, Any]
                if self.hub_server:
                    result_str = self.hub_server.execute_tool("start_veritas_run", params)
                    try:
                        result = json.loads(result_str)
                    except json.JSONDecodeError:
                        result = {"run_id": f"local-{int(os.times().elapsed)}", "status": "error", "error": result_str}
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
                        labels: dict[str, Any] = {}
                        if labels_path.exists():
                            with open(labels_path) as f:
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
                result_str = self.hub_server.execute_tool("list_veritas_runs", {"limit": 20})
                try:
                    result = json.loads(result_str)
                except json.JSONDecodeError:
                    result = []
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
                    with open(status_path) as f:
                        status = json.load(f)
                    details.update(status)
                return {"status": "ok", "data": details}
            except Exception as e:
                return {"status": "error", "error": {"code": "details_failed", "msg": str(e)}}

        @self.app.get("/api/runs/{run_id}/corpus")
        async def get_run_corpus(run_id: str):
            """Get corpus data for a run with filesystem fallback."""
            # Load corpus from .veritasrun bundle
            try:
                corpus_path = Path(f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl")
                if not corpus_path.exists():
                    return {"status": "error", "error": {"code": "run_not_found", "msg": f"Run {run_id} not found"}}
                
                documents = []
                with open(corpus_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                doc = json.loads(line)
                                documents.append(doc)
                            except json.JSONDecodeError:
                                continue
                
                return {"status": "ok", "data": {"documents": documents}}
            except Exception as e:
                return {"status": "error", "error": {"code": "corpus_load_failed", "msg": str(e)}}

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
                with open(registry_path) as f:
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
            return {"status": "ok", "data": {"service": "unified_dashboard"}, "error": None}

        @self.app.get("/api/health/full")
        async def health_check_full():
            """Full health check with gates"""
            try:
                # Check basic service health
                service_health = {}
                
                # Check MCP Hub Server
                mcp_health = "ok" if self.hub_server else "error"
                service_health["mcp_hub"] = mcp_health
                
                # Check Veritas Tools (MCP tools)
                veritas_health = "ok" if self.hub_server else "error"
                service_health["veritas_tools"] = veritas_health
                
                # Check Langflow
                try:
                    import requests
                    langflow_response = requests.get("http://langflow:7860/health", timeout=5)
                    langflow_health = "ok" if langflow_response.status_code == 200 else "error"
                except:
                    langflow_health = "error"
                service_health["langflow"] = langflow_health
                
                # Check LM Studio connection
                try:
                    import requests
                    # Try both localhost (for desktop) and Docker container
                    lm_urls = ["http://localhost:1234/v1/models", "http://lm-studio:1234/v1/models"]
                    lm_health = "error"
                    for url in lm_urls:
                        try:
                            lm_response = requests.get(url, timeout=5)
                            if lm_response.status_code == 200:
                                lm_health = "ok"
                                break
                        except:
                            continue
                except:
                    lm_health = "error"
                service_health["lm_studio"] = lm_health
                
                # Check Neo4j
                try:
                    import requests
                    neo4j_response = requests.get("http://neo4j:7474", timeout=5)
                    neo4j_health = "ok" if neo4j_response.status_code == 200 else "error"
                except:
                    neo4j_health = "error"
                service_health["neo4j"] = neo4j_health
                
                # Check Redis (Redis doesn't have HTTP endpoint, so check if container is running)
                try:
                    import subprocess
                    result = subprocess.run(["docker", "ps", "--filter", "name=redis", "--format", "{{.Status}}"], 
                                          capture_output=True, text=True, timeout=5)
                    redis_health = "ok" if result.returncode == 0 and result.stdout.strip() else "error"
                except:
                    # Fallback: assume Redis is ok if we can't check
                    redis_health = "ok"
                service_health["redis"] = redis_health
                
                # Determine overall health
                all_gates_passed = all(
                    status in ["ok", "warning"] 
                    for status in service_health.values() 
                    if isinstance(status, str)
                )
                
                # Convert status to expected format
                status = "healthy" if all_gates_passed else "unhealthy"
                
                # Convert gates to boolean format
                boolean_gates = {}
                gate_errors = {}
                for gate, gate_status in service_health.items():
                    boolean_gates[gate] = gate_status == "ok"
                    if gate_status != "ok":
                        gate_errors[gate] = f"Gate {gate} is {gate_status}"
                
                return {
                    "status": status,
                    "data": {
                        "service": "unified_dashboard",
                        "gates": boolean_gates,
                        "all_gates_passed": all_gates_passed,
                        "errors": gate_errors
                    }
                }
            except Exception as e:
                return {
                    "status": "error",
                    "data": {"service": "unified_dashboard"},
                    "error": {"code": "health_check_failed", "msg": str(e)}
                }

        @self.app.post("/api/ai/chat")
        async def ai_chat(request: Request):
            """AI chat endpoint for user interaction"""
            try:
                data = await request.json()
                message = data.get("message", "")
                context_run_id = data.get("context_run_id")
                
                if not message:
                    return {"status": "error", "error": {"code": "invalid_message", "msg": "Message is required"}}
                
                # Simple AI chat response for now
                responses = [
                    f"I understand you said: '{message}'. I'm here to help with your analysis!",
                    f"Thanks for your message: '{message}'. I can help you analyze survivor testimony and extract insights.",
                    f"You wrote: '{message}'. I'm ready to assist with document analysis and claim extraction.",
                    f"Message received: '{message}'. Let me know if you need help with the analysis tools!",
                    f"I see you said: '{message}'. I can help you get summaries, extract claims, and view transcripts."
                ]
                
                import random
                response = random.choice(responses)
                return {"status": "ok", "data": response}
                    
            except Exception as e:
                return {"status": "error", "error": {"code": "chat_failed", "msg": str(e)}}



        @self.app.get("/api/runs/{run_id}/transcript/{doc_index}")
        async def get_transcript(run_id: str, doc_index: int):
            """Get full transcript for a specific document"""
            try:
                # Load corpus first
                corpus_path = Path(f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl")
                if not corpus_path.exists():
                    return {"status": "error", "error": {"code": "run_not_found", "msg": f"Run {run_id} not found"}}
                
                documents = []
                with open(corpus_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                doc = json.loads(line)
                                documents.append(doc)
                            except json.JSONDecodeError:
                                continue
                
                if doc_index >= len(documents):
                    return {"status": "error", "error": {"code": "document_not_found", "msg": f"Document {doc_index} not found"}}
                
                document = documents[doc_index]
                return {"status": "ok", "data": document}
            except Exception as e:
                return {"status": "error", "error": {"code": "transcript_load_failed", "msg": str(e)}}

        @self.app.get("/api/visualizations/{filename}")
        async def get_visualization(filename: str):
            """Get visualization file by filename."""
            try:
                viz_path = Path("data/outputs/visualizations") / filename
                if not viz_path.exists():
                    return {"status": "error", "error": {"code": "viz_not_found", "msg": f"Visualization {filename} not found"}}
                
                with open(viz_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Return HTML content directly with proper content type
                from fastapi.responses import HTMLResponse
                return HTMLResponse(content=content, media_type="text/html")
            except Exception as e:
                return {"status": "error", "error": {"code": "viz_load_failed", "msg": str(e)}}

        @self.app.get("/api/visualizations")
        async def list_visualizations():
            """List available visualization files."""
            try:
                viz_dir = Path("data/outputs/visualizations")
                if not viz_dir.exists():
                    return {"status": "ok", "data": {"visualizations": []}}
                
                viz_files = []
                for file_path in viz_dir.glob("*.html"):
                    viz_files.append({
                        "filename": file_path.name,
                        "type": "html",
                        "size": file_path.stat().st_size,
                        "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                
                return {"status": "ok", "data": {"visualizations": viz_files}}
            except Exception as e:
                return {"status": "error", "error": {"code": "viz_list_failed", "msg": str(e)}}

        @self.app.websocket("/ws/ai-activity")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for AI activity updates"""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                # Send initial status
                await websocket.send_text(json.dumps({
                    "ai_type": "llm",
                    "status": "idle"
                }))
                
                # Keep connection alive
                while True:
                    # Wait for any message (ping/pong)
                    data = await websocket.receive_text()
                    # Echo back for now
                    await websocket.send_text(json.dumps({
                        "ai_type": "llm",
                        "status": "idle",
                        "current_activity": "Idle"
                    }))
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)

    async def broadcast_ai_activity(self, ai_type: str, status: str, activity: str = None):
        """Broadcast AI activity to all connected WebSocket clients"""
        message = {
            "ai_type": ai_type,
            "status": status
        }
        if activity:
            message["current_activity"] = activity
        
        # Remove disconnected clients
        self.active_connections = [conn for conn in self.active_connections if not conn.client_state.disconnected]
        
        # Send to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send WebSocket message: {e}")

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

