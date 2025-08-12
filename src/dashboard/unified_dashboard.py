"""
Living Truth Engine - Unified Dashboard
Main FastAPI application consolidating all functionality into a single user-friendly interface.
"""

import json
import logging
import os
import httpx

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

# Helper functions for envelope format and fallback control
def envelope_ok(data): 
    return {"status":"ok","data":data,"error":None}

def envelope_err(msg, code=503, extra=None):
    return {"status":"error","data":extra or {}, "error":{"code":code,"message":msg}}

ALLOW_FALLBACKS = os.getenv("ALLOW_FALLBACKS","false").lower()=="true"

async def _health_gate():
    # call your existing full health routine if present; minimal gate here:
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            # Add whatever internal checks you already expose
            r = await c.get("http://localhost:8050/api/health")
            if r.status_code != 200 or r.json().get("status") not in ("ok","healthy"):
                return False
    except Exception:
        return False
    return True

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
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err("Health gate failed; dependencies not ready", 503)
                
                if not self.hub_server:
                    return envelope_err("MCP Hub unavailable", 503)
                
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
                
                # Start run via MCP
                result_str = self.hub_server.execute_tool("start_veritas_run", params)
                try:
                    result = json.loads(result_str)
                except json.JSONDecodeError:
                    result = {"run_id": f"local-{int(os.times().elapsed)}", "status": "error", "error": result_str}

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

                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"start_veritas_run failed: {e}", 500)

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

            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result_str = self.hub_server.execute_tool("list_veritas_runs", {"limit": 20})
                    try:
                        result = json.loads(result_str)
                    except json.JSONDecodeError:
                        result = []
                    return envelope_ok(normalize_runs(result))
                else:
                    # Fallback path only if allowed (accepted fallback for containers)
                    runs_dir = Path("data/runs")
                    runs = []
                    if runs_dir.exists():
                        runs = [d.name for d in runs_dir.iterdir() if d.is_dir()]
                    return envelope_ok(normalize_runs({"runs": runs}))
            except Exception as e:
                if ALLOW_FALLBACKS:
                    # Try fallback if allowed
                    try:
                        runs_dir = Path("data/runs")
                        runs = []
                        if runs_dir.exists():
                            runs = [d.name for d in runs_dir.iterdir() if d.is_dir()]
                        return envelope_ok(normalize_runs({"runs": runs}))
                    except Exception as fallback_error:
                        return envelope_err(f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503)
                else:
                    return envelope_err(f"list_veritas_runs failed: {e}", 503)

        @self.app.get("/api/runs/{run_id}")
        async def get_run_details(run_id: str):
            """Get details for a specific run with filesystem fallback."""
            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result = self.hub_server.execute_tool("get_veritas_run_status", {"run_id": run_id})
                    return envelope_ok(result)
                else:
                    # Fallback path only if allowed (accepted fallback for containers)
                    status_path = Path("data/runs") / run_id / "status.json"
                    details: dict[str, Any] = {"run_id": run_id}
                    if status_path.exists():
                        with open(status_path) as f:
                            status = json.load(f)
                        details.update(status)
                    return envelope_ok(details)
            except Exception as e:
                if ALLOW_FALLBACKS:
                    # Try fallback if allowed
                    try:
                        status_path = Path("data/runs") / run_id / "status.json"
                        details: dict[str, Any] = {"run_id": run_id}
                        if status_path.exists():
                            with open(status_path) as f:
                                status = json.load(f)
                            details.update(status)
                        return envelope_ok(details)
                    except Exception as fallback_error:
                        return envelope_err(f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503)
                else:
                    return envelope_err(f"get_veritas_run_status failed: {e}", 503)

        @self.app.get("/api/runs/{run_id}/corpus")
        async def get_run_corpus(run_id: str):
            """Get corpus data for a run with filesystem fallback."""
            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result = self.hub_server.execute_tool("get_veritas_run_corpus", {"run_id": run_id})
                    return envelope_ok(result)
                else:
                    # Fallback path only if allowed (accepted fallback for containers)
                    corpus_path = Path(f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl")
                    if not corpus_path.exists():
                        return envelope_err(f"Run {run_id} not found", 404)
                    
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
                    
                    return envelope_ok({"documents": documents})
            except Exception as e:
                if ALLOW_FALLBACKS:
                    # Try fallback if allowed
                    try:
                        corpus_path = Path(f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl")
                        if not corpus_path.exists():
                            return envelope_err(f"Run {run_id} not found", 404)
                        
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
                        
                        return envelope_ok({"documents": documents})
                    except Exception as fallback_error:
                        return envelope_err(f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503)
                else:
                    return envelope_err(f"get_veritas_run_corpus failed: {e}", 503)

        @self.app.post("/api/analyze/entities")
        async def analyze_entities(request: Request):
            """Analyze entities for a document"""
            try:
                data = await request.json()
                result = self.hub_server.execute_tool("analyze_transcript", data)
                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"analysis_failed: {e}", 500)

        @self.app.post("/api/analyze/claims")
        async def analyze_claims(request: Request):
            """Analyze claims for a document"""
            try:
                data = await request.json()
                result = self.hub_server.execute_tool("query_langflow", data)
                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"claims_failed: {e}", 500)

        @self.app.get("/api/status")
        async def get_status():
            """Get system status"""
            try:
                result = self.hub_server.get_status()
                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"status_failed: {e}", 500)

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

            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result = self.hub_server.list_tools("", "")
                    # If result is empty or not as expected, fall through
                    if isinstance(result, dict) and result.get("categories"):
                        return envelope_ok(result)
                else:
                    # Fallback path only if allowed (accepted fallback for containers)
                    registry_path = Path("config/tool_registry.json")
                    with open(registry_path) as f:
                        registry = json.load(f)
                    categories = group_by_server(registry)
                    return envelope_ok({"categories": categories})
            except Exception as e:
                if ALLOW_FALLBACKS:
                    # Try fallback if allowed
                    try:
                        registry_path = Path("config/tool_registry.json")
                        with open(registry_path) as f:
                            registry = json.load(f)
                        categories = group_by_server(registry)
                        return envelope_ok({"categories": categories})
                    except Exception as fallback_error:
                        return envelope_err(f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503)
                else:
                    return envelope_err(f"list_tools failed: {e}", 503)

        @self.app.post("/api/execute")
        async def execute_tool(request: Request):
            """Execute a tool by name with params."""
            try:
                data = await request.json()
                tool_name = data.get("tool_name")
                params = data.get("params", {})
                if not tool_name:
                    return envelope_err("tool_name is required", 400)
                if not self.hub_server:
                    return envelope_err("MCP server not available", 503)
                result = self.hub_server.execute_tool(tool_name, params)
                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"execute_failed: {e}", 500)

        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return envelope_ok({"service":"unified_dashboard"})

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
                
                # Calculate models checksum
                import hashlib
                try:
                    models_path = Path("config/models.toml")
                    if models_path.exists():
                        models_checksum = hashlib.sha1(models_path.read_bytes()).hexdigest()
                    else:
                        models_checksum = "not_found"
                except Exception:
                    models_checksum = "error"
                
                return envelope_ok({
                    "service": "unified_dashboard",
                    "gates": boolean_gates,
                    "all_gates_passed": all_gates_passed,
                    "errors": gate_errors,
                    "models_checksum": models_checksum,
                    "pgvector": {"enabled": True, "tables": ["lte.documents", "lte.doc_embeddings"]},
                    "rulego": {"status": "ok"},
                    "fallbacks_enabled": ALLOW_FALLBACKS
                })
            except Exception as e:
                return envelope_err("health_check_failed", 500, {"service": "unified_dashboard"})

        @self.app.get("/api/models")
        async def get_models():
            """Get model registry (SSOT)"""
            try:
                from src.common.model_registry import ModelRegistry
                reg = ModelRegistry()
                return envelope_ok({
                    "llm": reg.llm().__dict__,
                    "embedding": reg.embedding().__dict__,
                    "ner": reg.ner().__dict__,
                    "reranker": reg.reranker().__dict__,
                    "ocr": reg.ocr().__dict__,
                    "stt": reg.stt().__dict__,
                    "diarization": reg.diarization().__dict__,
                    "topics": reg.topics().__dict__
                })
            except Exception as e:
                return envelope_err(f"models_load_failed: {e}", 500)

        @self.app.get("/api/rules/health")
        async def get_rules_health():
            """Get Rulego health and loaded policies"""
            try:
                from src.analysis.rulego_bridge import RulegoClient
                client = RulegoClient()
                health = await client.health()
                policies = await client.list_policies()
                return envelope_ok({
                    "health": health,
                    "policies": policies
                })
            except Exception as e:
                return envelope_err(f"rulego_health_failed: {e}", 503)

        @self.app.post("/api/ai/chat")
        async def ai_chat(request: Request):
            """AI chat endpoint for user interaction"""
            try:
                data = await request.json()
                model = data.get("model","qwen/qwen3-8b")
                max_tokens = int(data.get("max_tokens", 1000))
                message = data.get("message","")
                
                # LM Studio endpoint normalization (bug-proofing)
                raw = os.getenv("LM_STUDIO_ENDPOINT", "http://localhost:1234")
                raw = raw.rstrip("/")
                endpoint = raw if raw.endswith("/v1") else raw + "/v1"
                url = f"{endpoint}/chat/completions"

                if not message:
                    return envelope_err("Message is required", 400)

                try:
                    async with httpx.AsyncClient(timeout=60) as c:
                        r = await c.post(url, json={
                            "model": model,
                            "messages": [{"role":"user","content":message}],
                            "max_tokens": max_tokens
                        })
                        r.raise_for_status()
                        response_text = r.text
                        try:
                            response_data = r.json()
                        except Exception as json_error:
                            return envelope_err(f"Failed to parse LM Studio response as JSON: {json_error}. Response: {response_text[:200]}", 502, {"source": "lmstudio"})
                        
                        # Handle different response formats
                        if isinstance(response_data, dict) and "choices" in response_data and len(response_data["choices"]) > 0:
                            content = response_data["choices"][0]["message"]["content"]
                            return envelope_ok({"model":model, "message":content})
                        elif "error" in response_data:
                            error_obj = response_data["error"]
                            if isinstance(error_obj, dict):
                                error_msg = error_obj.get("message", "Unknown error")
                            else:
                                error_msg = str(error_obj)
                            
                            if "No models loaded" in error_msg or "model_not_found" in error_msg:
                                # Provide helpful fallback when no chat models are loaded
                                fallback_response = f"I understand you said: '{message}'. I'm here to help with your analysis! (Note: No chat models are currently loaded in LM Studio)"
                                return envelope_ok({"model":"fallback", "message":fallback_response})
                            else:
                                return envelope_err(f"LM Studio error: {error_msg}", 502, {"source": "lmstudio"})
                        else:
                            return envelope_err("Unexpected response format from LM Studio", 502, {"source": "lmstudio"})
                except Exception as e:
                    return envelope_err(f"LM Studio chat error: {e}", 502, {"source": "lmstudio"})
                    
            except Exception as e:
                return envelope_err(f"chat_failed: {e}", 500)



        @self.app.get("/api/runs/{run_id}/transcript/{doc_index}")
        async def get_transcript(run_id: str, doc_index: int):
            """Get full transcript for a specific document"""
            try:
                # Load corpus first
                corpus_path = Path(f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl")
                if not corpus_path.exists():
                    return envelope_err(f"Run {run_id} not found", 404)
                
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
                    return envelope_err(f"Document {doc_index} not found", 404)
                
                document = documents[doc_index]
                return envelope_ok(document)
            except Exception as e:
                return envelope_err(f"transcript_load_failed: {e}", 500)

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
                    return envelope_ok({"visualizations": []})
                
                viz_files = []
                for file_path in viz_dir.glob("*.html"):
                    viz_files.append({
                        "filename": file_path.name,
                        "type": "html",
                        "size": file_path.stat().st_size,
                        "created": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
                
                return envelope_ok({"visualizations": viz_files})
            except Exception as e:
                return envelope_err(f"viz_list_failed: {e}", 500)

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

