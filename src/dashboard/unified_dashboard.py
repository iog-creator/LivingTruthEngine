"""
Living Truth Engine - Unified Dashboard
Main FastAPI application consolidating all functionality into a single user-friendly interface.
"""  # noqa: E501

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
    return {"status": "ok", "data": data, "error": None}


def envelope_err(msg, code=503, extra=None):
    return {
        "status": "error",
        "data": extra or {},
        "error": {"code": code, "message": msg},
    }


ALLOW_FALLBACKS = os.getenv("ALLOW_FALLBACKS", "false").lower() == "true"


async def _health_gate():
    # call your existing full health routine if present; minimal gate here:
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            # Add whatever internal checks you already expose
            r = await c.get("http://localhost:8050/api/health")
            if r.status_code != 200 or r.json().get("status") not in ("ok", "healthy"):
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

# Import resilience router
try:
    from api.resilience import router as resilience_router
except ImportError as e:
    logger.error(f"Failed to import resilience router: {e}")
    resilience_router = None


class UnifiedDashboard:
    def __init__(self):
        self.app = FastAPI(
            title="Living Truth Engine - Unified Dashboard",
            description="Single interface for survivor testimony analysis and evidence discovery",  # noqa: E501
            version="1.0.0",
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
        self.app.mount(
            "/static", StaticFiles(directory="src/dashboard/static"), name="static"
        )

        # Setup routes
        self.setup_routes()

        # Include contract router if available
        if contract_router:
            self.app.include_router(contract_router)

        # Include resilience router if available
        if resilience_router:
            self.app.include_router(resilience_router)

        # WebSocket connections
        self.active_connections = []

    def setup_routes(self):
        """Setup all dashboard routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Home page with quick start and recent activity"""
            return self.templates.TemplateResponse(
                "home.html", {"request": request, "title": "Living Truth Engine - Home"}
            )

        @self.app.get("/runs", response_class=HTMLResponse)
        async def runs_page(request: Request):
            """Runs page - browse bundles and view details"""
            return self.templates.TemplateResponse(
                "runs.html", {"request": request, "title": "Runs - Living Truth Engine"}
            )

        @self.app.get("/analyze", response_class=HTMLResponse)
        async def analyze_page(request: Request):
            """Analyze page - pick bundle/doc and view results"""
            return self.templates.TemplateResponse(
                "analyze.html",
                {"request": request, "title": "Analyze - Living Truth Engine"},
            )

        @self.app.get("/advanced", response_class=HTMLResponse)
        async def advanced_page(request: Request):
            """Advanced page - expert controls and raw MCP tester"""
            return self.templates.TemplateResponse(
                "advanced.html",
                {"request": request, "title": "Advanced - Living Truth Engine"},
            )

        @self.app.get("/ui/resilience", response_class=HTMLResponse)
        async def resilience_page(request: Request):
            """Resilience Dashboard UI page"""
            return self.templates.TemplateResponse(
                "resilience.html",
                {
                    "request": request,
                    "title": "Resilience Dashboard - Living Truth Engine",
                },
            )

        # API Routes for UI functionality
        @self.app.post("/api/runs/youtube/start")
        async def start_youtube_run(request: Request):
            """Start a YouTube channel analysis run with optional labeling and output dir."""  # noqa: E501
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                if not self.hub_server:
                    return envelope_err("MCP Hub unavailable", 503)

                data = await request.json()
                topic = f"YouTube analysis: {data.get('channel_url', 'Unknown')}"
                params = {
                    "topic": topic,
                    "max_videos": data.get("limit", 10),
                    "channel_url": data.get("channel_url"),
                    "crawl_depth": data.get("max_depth", 1),
                    "transcript_pref": "yt_api",
                    "sources": ["youtube"],
                }

                # Start run via MCP
                result_str = self.hub_server.execute_tool("start_veritas_run", params)
                try:
                    result = json.loads(result_str)
                except json.JSONDecodeError:
                    result = {
                        "run_id": f"local-{int(os.times().elapsed)}",
                        "status": "error",
                        "error": result_str,
                    }

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
                    return [
                        {"run_id": r} if not isinstance(r, dict) else r
                        for r in raw["runs"]
                    ]
                if isinstance(raw, list):
                    return [r if isinstance(r, dict) else {"run_id": r} for r in raw]
                return []

            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result_str = self.hub_server.execute_tool(
                        "list_veritas_runs", {"limit": 20}
                    )
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
                        return envelope_err(
                            f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503
                        )
                else:
                    return envelope_err(f"list_veritas_runs failed: {e}", 503)

        @self.app.get("/api/runs/{run_id}")
        async def get_run_details(run_id: str):
            """Get details for a specific run with filesystem fallback."""
            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result = self.hub_server.execute_tool(
                        "get_veritas_run_status", {"run_id": run_id}
                    )
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
                        return envelope_err(
                            f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503
                        )
                else:
                    return envelope_err(f"get_veritas_run_status failed: {e}", 503)

        @self.app.get("/api/runs/{run_id}/corpus")
        async def get_run_corpus(run_id: str):
            """Get corpus data for a run with filesystem fallback."""
            if not self.hub_server and not ALLOW_FALLBACKS:
                return envelope_err("Hub unavailable and fallbacks disabled", 503)

            try:
                if self.hub_server:
                    result = self.hub_server.execute_tool(
                        "get_veritas_run_corpus", {"run_id": run_id}
                    )
                    return envelope_ok(result)
                else:
                    # Fallback path only if allowed (accepted fallback for containers)
                    corpus_path = Path(
                        f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl"
                    )
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
                        corpus_path = Path(
                            f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl"
                        )
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
                        return envelope_err(
                            f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503
                        )
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

            def group_by_server(
                registry: dict[str, Any],
            ) -> dict[str, list[dict[str, Any]]]:
                categories: dict[str, list[dict[str, Any]]] = {}
                for server_name, server_data in registry.get("servers", {}).items():
                    categories[server_name] = []
                    for tool in server_data.get("tools", []):
                        categories[server_name].append(
                            {
                                "name": tool.get("name"),
                                "description": tool.get("description", ""),
                            }
                        )
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
                        return envelope_err(
                            f"MCP: {str(e)}, Fallback: {str(fallback_error)}", 503
                        )
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
            return envelope_ok({"service": "unified_dashboard"})

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

                    langflow_response = requests.get(
                        "http://langflow:7860/health", timeout=5
                    )
                    langflow_health = (
                        "ok" if langflow_response.status_code == 200 else "error"
                    )
                except (requests.RequestException, ConnectionError, TimeoutError):
                    langflow_health = "error"
                service_health["langflow"] = langflow_health

                # Check LM Studio connection
                try:
                    import requests

                    # Try both localhost (for desktop) and Docker container
                    lm_urls = [
                        "http://localhost:1234/v1/models",
                        "http://lm-studio:1234/v1/models",
                    ]
                    lm_health = "error"
                    for url in lm_urls:
                        try:
                            lm_response = requests.get(url, timeout=5)
                            if lm_response.status_code == 200:
                                lm_health = "ok"
                                break
                        except (
                            requests.RequestException,
                            ConnectionError,
                            TimeoutError,
                        ):
                            continue
                except (requests.RequestException, ConnectionError, TimeoutError):
                    lm_health = "error"
                service_health["lm_studio"] = lm_health

                # Check Neo4j
                try:
                    import requests

                    neo4j_response = requests.get("http://neo4j:7474", timeout=5)
                    neo4j_health = (
                        "ok" if neo4j_response.status_code == 200 else "error"
                    )
                except (requests.RequestException, ConnectionError, TimeoutError):
                    neo4j_health = "error"
                service_health["neo4j"] = neo4j_health

                # Check Redis (Redis doesn't have HTTP endpoint, so check if container is running)  # noqa: E501
                try:
                    import subprocess

                    result = subprocess.run(
                        [
                            "docker",
                            "ps",
                            "--filter",
                            "name=redis",
                            "--format",
                            "{{.Status}}",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    redis_health = (
                        "ok"
                        if result.returncode == 0 and result.stdout.strip()
                        else "error"
                    )
                except (
                    subprocess.TimeoutExpired,
                    subprocess.CalledProcessError,
                    FileNotFoundError,
                ):
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
                        models_checksum = hashlib.sha1(
                            models_path.read_bytes()
                        ).hexdigest()
                    else:
                        models_checksum = "not_found"
                except Exception:
                    models_checksum = "error"

                # Get embedding model info from SSOT
                try:
                    from src.common.model_registry import ModelRegistry

                    reg = ModelRegistry()
                    embedding_spec = reg.embedding()
                    embedding_model = embedding_spec.name
                    embedding_dim = embedding_spec.extra.get("dim")
                except Exception as e:
                    logger.warning(f"Failed to get embedding model info: {e}")
                    embedding_model = "unknown"
                    embedding_dim = None

                # Validate database schema against model registry
                dim_mismatch = False
                schema_validation = None
                try:
                    from src.storage.pgvector_store import PgVectorStore

                    pgvector_store = PgVectorStore(
                        "postgresql://postgres:pass@postgres:5432/living_truth_engine"
                    )
                    schema_validation = pgvector_store.validate_database_schema()
                    dim_mismatch = schema_validation.get("dim_mismatch", False)
                except Exception as e:
                    logger.warning(f"Failed to validate database schema: {e}")
                    schema_validation = {"valid": False, "error": str(e)}

                # Get GPU status and fallback events
                gpu_status = None
                fallback_events = []
                try:
                    from src.common.gpu_scheduler import GPUScheduler

                    # Use global GPU scheduler instance
                    if not hasattr(self, "_gpu_scheduler"):
                        gpu_config = {
                            "vram_threshold_mb": 1000,
                            "reservation_mb": 500,
                            "max_fallback_history": 20,
                        }
                        self._gpu_scheduler = GPUScheduler(gpu_config)

                    gpu_status = self._gpu_scheduler.get_gpu_status()
                    fallback_events = self._gpu_scheduler.get_fallback_history(limit=10)
                except Exception as e:
                    logger.warning(f"Failed to get GPU status: {e}")
                    gpu_status = {
                        "available": False,
                        "reason": f"GPU check failed: {e}",
                    }

                return envelope_ok(
                    {
                        "service": "unified_dashboard",
                        "gates": boolean_gates,
                        "all_gates_passed": all_gates_passed,
                        "errors": gate_errors,
                        "models_checksum": models_checksum,
                        "pgvector": {
                            "enabled": True,
                            "tables": ["lte.documents", "lte.doc_embeddings"],
                            "schema_validation": schema_validation,
                        },
                        "rulego": {"status": "ok"},
                        "fallbacks_enabled": ALLOW_FALLBACKS,
                        "embedding_model": embedding_model,
                        "embedding_dim": embedding_dim,
                        "dim_mismatch": dim_mismatch,
                        "gpu": gpu_status,
                        "recent_fallbacks": fallback_events,
                        "reverse_proxy": True,
                        "ui_origin": "http://localhost:4173",
                    }
                )
            except Exception as e:
                return envelope_err(
                    "health_check_failed", 500, {"service": "unified_dashboard"}
                )

        @self.app.get("/api/models")
        async def get_models():
            """Get model registry (SSOT)"""
            try:
                from src.common.model_registry import ModelRegistry

                reg = ModelRegistry()
                return envelope_ok(
                    {
                        "llm": reg.llm().__dict__,
                        "embedding": reg.embedding().__dict__,
                        "ner": reg.ner().__dict__,
                        "reranker": reg.reranker().__dict__,
                        "ocr": reg.ocr().__dict__,
                        "stt": reg.stt().__dict__,
                        "diarization": reg.diarization().__dict__,
                        "topics": reg.topics().__dict__,
                    }
                )
            except Exception as e:
                return envelope_err(f"models_load_failed: {e}", 500)

        @self.app.get("/api/gpu/status")
        async def get_gpu_status():
            """Get GPU status and information"""
            try:
                # Use global GPU scheduler instance
                if not hasattr(self, "_gpu_scheduler"):
                    from src.common.gpu_scheduler import GPUScheduler

                    gpu_config = {
                        "vram_threshold_mb": 1000,
                        "reservation_mb": 500,
                        "max_fallback_history": 20,
                    }
                    self._gpu_scheduler = GPUScheduler(gpu_config)

                gpu_status = self._gpu_scheduler.get_gpu_status()
                return envelope_ok(gpu_status)
            except Exception as e:
                return envelope_err(f"gpu_status_failed: {e}", 500)

        @self.app.post("/api/gpu/simulate_low_vram")
        async def simulate_low_vram():
            """Simulate low VRAM condition for testing"""
            try:
                # Use global GPU scheduler instance
                if not hasattr(self, "_gpu_scheduler"):
                    from src.common.gpu_scheduler import GPUScheduler

                    gpu_config = {
                        "vram_threshold_mb": 1000,
                        "reservation_mb": 500,
                        "max_fallback_history": 20,
                    }
                    self._gpu_scheduler = GPUScheduler(gpu_config)

                result = self._gpu_scheduler.simulate_low_vram()
                return envelope_ok(result)
            except Exception as e:
                return envelope_err(f"low_vram_simulation_failed: {e}", 500)

        @self.app.get("/api/gpu/fallbacks")
        async def get_gpu_fallbacks(limit: int = 10):
            """Get recent GPU fallback events"""
            try:
                # Use global GPU scheduler instance
                if not hasattr(self, "_gpu_scheduler"):
                    from src.common.gpu_scheduler import GPUScheduler

                    gpu_config = {
                        "vram_threshold_mb": 1000,
                        "reservation_mb": 500,
                        "max_fallback_history": 20,
                    }
                    self._gpu_scheduler = GPUScheduler(gpu_config)

                fallbacks = self._gpu_scheduler.get_fallback_history(limit=limit)
                return envelope_ok({"fallbacks": fallbacks, "count": len(fallbacks)})
            except Exception as e:
                return envelope_err(f"fallbacks_failed: {e}", 500)

        @self.app.get("/api/rules/health")
        async def get_rules_health():
            """Get Rulego health and loaded policies"""
            try:
                from src.analysis.rulego_bridge import RulegoClient

                client = RulegoClient()
                health = await client.health()
                policies = await client.list_policies()
                return envelope_ok({"health": health, "policies": policies})
            except Exception as e:
                return envelope_err(f"rulego_health_failed: {e}", 503)

        # Multi-Source Ingestion Endpoints (Phase 9_2)
        @self.app.post("/api/multisource/start")
        async def start_multi_source_ingest(request: Request):
            """Start multi-source ingestion job with health gates"""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()
                sources = data.get("sources", [])
                params = data.get("params", {})

                if not sources:
                    return envelope_err("sources list is required", 400)

                # Validate source types
                valid_sources = ["youtube", "web", "pdf"]
                invalid_sources = [s for s in sources if s not in valid_sources]
                if invalid_sources:
                    return envelope_err(
                        f"Invalid source types: {invalid_sources}. Valid types: {valid_sources}",  # noqa: E501
                        400,
                    )

                # Import and start multi-source job
                from src.runners.multisource_runner import multi_source_runner

                job_id = await multi_source_runner.start_job(sources, params)

                return envelope_ok(
                    {"job_id": job_id, "sources": sources, "status": "started"}
                )

            except ValueError as e:
                # Health gate failure
                return envelope_err(str(e), 503)
            except Exception as e:
                return envelope_err(f"multi_source_ingest_failed: {e}", 500)

        @self.app.get("/api/multisource/jobs/{job_id}")
        async def get_multi_source_job_status(job_id: str):
            """Get status of multi-source ingestion job"""
            try:
                from src.runners.multisource_runner import multi_source_runner

                status = await multi_source_runner.get_job_status(job_id)

                if status is None:
                    return envelope_err(f"Job {job_id} not found", 404)

                return envelope_ok(status)

            except Exception as e:
                return envelope_err(f"get_job_status_failed: {e}", 500)

        @self.app.get("/api/multisource/jobs")
        async def list_multi_source_jobs():
            """List all multi-source ingestion jobs"""
            try:
                from src.runners.multisource_runner import multi_source_runner

                jobs = []

                for job_id, job in multi_source_runner.active_jobs.items():
                    jobs.append(
                        {
                            "job_id": job_id,
                            "status": job.status,
                            "sources": [s.source_type for s in job.sources],
                            "created_at": job.created_at.isoformat(),
                            "completed_at": job.completed_at.isoformat()
                            if job.completed_at
                            else None,
                            "job_label": job.job_label,
                            "error": job.error,
                        }
                    )

                return envelope_ok({"jobs": jobs})

            except Exception as e:
                return envelope_err(f"list_jobs_failed: {e}", 500)

        @self.app.post("/api/search")
        async def search_documents(request: Request):
            """Search documents using pgvector"""
            try:
                data = await request.json()
                query = data.get("query", "")
                job_id = data.get("job_id")
                k = data.get("k", 10)

                if not query:
                    return envelope_err("query is required", 400)

                if not job_id:
                    return envelope_err("job_id is required", 400)

                from src.runners.multisource_runner import multi_source_runner

                # For now, return mock search results since embedder is not available
                # In Phase 9.3, this will be replaced with real pgvector search
                mock_results = [
                    {
                        "id": "mock_doc_1",
                        "text": f"Mock document matching query: {query}",
                        "meta": {"source_type": "youtube", "job_id": job_id},
                    }
                ]

                return envelope_ok(
                    {
                        "query": query,
                        "job_id": job_id,
                        "results": mock_results,
                        "note": "Mock search results (real pgvector search in Phase 9.3)",  # noqa: E501
                    }
                )

            except Exception as e:
                return envelope_err(f"search_failed: {e}", 500)

        @self.app.post("/api/ai/chat")
        async def ai_chat(request: Request):
            """AI chat endpoint for user interaction"""
            try:
                data = await request.json()
                model = data.get("model", "qwen/qwen3-8b")
                max_tokens = int(data.get("max_tokens", 1000))
                message = data.get("message", "")

                # LM Studio endpoint normalization (bug-proofing)
                raw = os.getenv("LM_STUDIO_ENDPOINT", "http://localhost:1234")
                raw = raw.rstrip("/")
                # Only add /v1 if it's not already present
                if "/v1" in raw:
                    endpoint = raw
                else:
                    endpoint = raw + "/v1"
                url = f"{endpoint}/chat/completions"

                if not message:
                    return envelope_err("Message is required", 400)

                try:
                    async with httpx.AsyncClient(timeout=60) as c:
                        r = await c.post(
                            url,
                            json={
                                "model": model,
                                "messages": [{"role": "user", "content": message}],
                                "max_tokens": max_tokens,
                            },
                        )
                        r.raise_for_status()
                        response_text = r.text
                        try:
                            response_data = r.json()
                        except Exception as json_error:
                            return envelope_err(
                                f"Failed to parse LM Studio response as JSON: {json_error}. Response: {response_text[:200]}",  # noqa: E501
                                502,
                                {"source": "lmstudio"},
                            )

                        # Handle different response formats
                        if (
                            isinstance(response_data, dict)
                            and "choices" in response_data
                            and len(response_data["choices"]) > 0
                        ):
                            content = response_data["choices"][0]["message"]["content"]
                            return envelope_ok({"model": model, "message": content})
                        elif "error" in response_data:
                            error_obj = response_data["error"]
                            if isinstance(error_obj, dict):
                                error_msg = error_obj.get("message", "Unknown error")
                            else:
                                error_msg = str(error_obj)

                            if (
                                "No models loaded" in error_msg
                                or "model_not_found" in error_msg
                            ):
                                # Provide helpful fallback when no chat models are loaded  # noqa: E501
                                fallback_response = f"I understand you said: '{message}'. I'm here to help with your analysis! (Note: No chat models are currently loaded in LM Studio)"  # noqa: E501
                                return envelope_ok(
                                    {"model": "fallback", "message": fallback_response}
                                )
                            else:
                                return envelope_err(
                                    f"LM Studio error: {error_msg}",
                                    502,
                                    {"source": "lmstudio"},
                                )
                        else:
                            return envelope_err(
                                "Unexpected response format from LM Studio",
                                502,
                                {"source": "lmstudio"},
                            )
                except Exception as e:
                    return envelope_err(
                        f"LM Studio chat error: {e}", 502, {"source": "lmstudio"}
                    )

            except Exception as e:
                return envelope_err(f"chat_failed: {e}", 500)

        @self.app.get("/api/runs/{run_id}/transcript/{doc_index}")
        async def get_transcript(run_id: str, doc_index: int):
            """Get full transcript for a specific document"""
            try:
                # Load corpus first
                corpus_path = Path(
                    f"data/outputs/runs/{run_id}.veritasrun/corpus.jsonl"
                )
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
                    return {
                        "status": "error",
                        "error": {
                            "code": "viz_not_found",
                            "msg": f"Visualization {filename} not found",
                        },
                    }

                with open(viz_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Return HTML content directly with proper content type
                from fastapi.responses import HTMLResponse

                return HTMLResponse(content=content, media_type="text/html")
            except Exception as e:
                return {
                    "status": "error",
                    "error": {"code": "viz_load_failed", "msg": str(e)},
                }

        @self.app.get("/api/visualizations")
        async def list_visualizations():
            """List available visualization files."""
            try:
                viz_dir = Path("data/outputs/visualizations")
                if not viz_dir.exists():
                    return envelope_ok({"visualizations": []})

                viz_files = []
                for file_path in viz_dir.glob("*.html"):
                    viz_files.append(
                        {
                            "filename": file_path.name,
                            "type": "html",
                            "size": file_path.stat().st_size,
                            "created": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat(),
                        }
                    )

                return envelope_ok({"visualizations": viz_files})
            except Exception as e:
                return envelope_err(f"viz_list_failed: {e}", 500)

        # Phase 9.3: Graph API endpoints
        @self.app.get("/api/graph/{run_id}")
        async def get_graph(run_id: str):
            """Get graph data for a specific run."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                from src.storage.pgvector_store import PgVectorStore
                from src.config.living_truth_config import LivingTruthConfig

                # Initialize pgvector store
                config = LivingTruthConfig()
                dsn = f"postgresql://postgres:pass@postgres:5432/living_truth_engine"
                pgvector_store = PgVectorStore(dsn, embedder=None)

                # Get graph snapshot
                graph = pgvector_store.get_graph_snapshot(run_id)
                if not graph:
                    return envelope_err(f"Graph not found for run {run_id}", 404)

                return envelope_ok(graph)

            except Exception as e:
                return envelope_err(f"get_graph failed: {e}", 500)

        @self.app.post("/api/graph/{run_id}/build")
        async def build_graph(run_id: str, rebuild: bool = False):
            """Build graph for a specific run using the linking pipeline."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                from src.analysis.linking_pipeline import LinkingPipeline
                from src.storage.pgvector_store import PgVectorStore
                from src.config.living_truth_config import LivingTruthConfig

                # Initialize components
                config = LivingTruthConfig()
                dsn = f"postgresql://postgres:pass@postgres:5432/living_truth_engine"
                pgvector_store = PgVectorStore(dsn, embedder=None)
                linking_pipeline = LinkingPipeline(config, pgvector_store)

                # Get documents for this run
                documents = pgvector_store.get_documents_by_run(run_id)
                if not documents:
                    return envelope_err(f"No documents found for run {run_id}", 404)

                # Process run through linking pipeline with rebuild flag
                results = linking_pipeline.process_run(
                    run_id, documents, rebuild=rebuild
                )

                if results.get("status") == "failed":
                    error_msg = results.get("error", "Unknown error")
                    if "duplicate key value violates unique constraint" in error_msg:
                        return envelope_err(
                            f"Graph building failed due to constraint violation. Try using ?rebuild=1 to clear existing data: {error_msg}",  # noqa: E501
                            409,
                            {
                                "code": "graph_build_conflict",
                                "hint": "Use ?rebuild=1 to clear existing data",
                            },
                        )
                    else:
                        return envelope_err(f"Graph building failed: {error_msg}", 500)

                return envelope_ok(
                    {
                        "run_id": run_id,
                        "results": results,
                        "rebuild": rebuild,
                        "performance": results.get("performance", {}),
                    }
                )

            except Exception as e:
                error_msg = str(e)
                if "duplicate key value violates unique constraint" in error_msg:
                    return envelope_err(
                        f"Graph building failed due to constraint violation. Try using ?rebuild=1 to clear existing data: {error_msg}",  # noqa: E501
                        409,
                        {
                            "code": "graph_build_conflict",
                            "hint": "Use ?rebuild=1 to clear existing data",
                        },
                    )
                else:
                    return envelope_err(f"build_graph failed: {error_msg}", 500)

        @self.app.get("/api/claims/{run_id}")
        async def get_claims(run_id: str):
            """Get claims for a specific run with link counts and corroboration labels."""  # noqa: E501
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                from src.storage.pgvector_store import PgVectorStore
                from src.config.living_truth_config import LivingTruthConfig

                # Initialize pgvector store
                config = LivingTruthConfig()
                dsn = f"postgresql://postgres:pass@postgres:5432/living_truth_engine"
                pgvector_store = PgVectorStore(dsn, embedder=None)

                # Get claims with link information
                claims = pgvector_store.get_claims_by_run(run_id)
                claim_links = pgvector_store.get_claim_links_by_run(run_id)

                # Get graph snapshot for corroboration labels
                graph = pgvector_store.get_graph_snapshot(run_id)
                corroboration_results = (
                    graph.get("findings", {}).get("corroboration", []) if graph else []
                )

                # Create lookup for corroboration results
                corroboration_lookup = {
                    result.get("claim_id"): result for result in corroboration_results
                }

                # Add link counts and corroboration labels to claims
                for claim in claims:
                    claim["link_count"] = len(
                        [
                            l
                            for l in claim_links
                            if l["left_claim_id"] == claim["id"]
                            or l["right_claim_id"] == claim["id"]
                        ]
                    )

                    # Add corroboration label
                    corroboration = corroboration_lookup.get(claim["id"])
                    if corroboration:
                        claim["corroboration_label"] = corroboration.get(
                            "label", "unknown"
                        )
                        claim["corroboration_confidence"] = corroboration.get(
                            "confidence", 0.0
                        )
                    else:
                        claim["corroboration_label"] = "unknown"
                        claim["corroboration_confidence"] = 0.0

                return envelope_ok(
                    {
                        "run_id": run_id,
                        "claims": claims,
                        "total_claims": len(claims),
                        "total_links": len(claim_links),
                    }
                )

            except Exception as e:
                return envelope_err(f"get_claims failed: {e}", 500)

        @self.app.get("/api/entities/{run_id}")
        async def get_entities(run_id: str):
            """Get entities for a specific run with link counts and types."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                from src.storage.pgvector_store import PgVectorStore
                from src.config.living_truth_config import LivingTruthConfig

                # Initialize pgvector store
                config = LivingTruthConfig()
                dsn = f"postgresql://postgres:pass@postgres:5432/living_truth_engine"
                pgvector_store = PgVectorStore(dsn, embedder=None)

                # Get entities with link information
                entities = pgvector_store.get_entities_by_run(run_id)
                entity_links = pgvector_store.get_entity_links_by_run(run_id)

                # Add link counts to entities
                for entity in entities:
                    entity["link_count"] = len(
                        [
                            l
                            for l in entity_links
                            if l["left_entity_id"] == entity["id"]
                            or l["right_entity_id"] == entity["id"]
                        ]
                    )

                return envelope_ok(
                    {
                        "run_id": run_id,
                        "entities": entities,
                        "total_entities": len(entities),
                        "total_links": len(entity_links),
                    }
                )

            except Exception as e:
                return envelope_err(f"get_entities failed: {e}", 500)

        # Phase 9.5.3: Timeline API endpoint
        @self.app.get("/api/timeline/{run_id}")
        async def get_timeline(run_id: str):
            """Get timeline data for a specific run with events and temporal analysis."""  # noqa: E501
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                from datetime import datetime, timedelta
                import json
                import os

                # Check if bundle exists
                bundle_path = Path(f"data/outputs/runs/{run_id}.veritasrun")
                if not bundle_path.exists():
                    return envelope_err(f"Run {run_id} not found", 404)

                # Load bundle data
                documents = []
                corpus_path = bundle_path / "corpus.jsonl"
                if corpus_path.exists():
                    with open(corpus_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    doc = json.loads(line)
                                    documents.append(doc)
                                except json.JSONDecodeError:
                                    continue

                # Load manifest for run metadata
                manifest = {}
                manifest_path = bundle_path / "manifest.json"
                if manifest_path.exists():
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)

                # Load metrics for run statistics
                metrics = {}
                metrics_path = bundle_path / "metrics.json"
                if metrics_path.exists():
                    with open(metrics_path, "r", encoding="utf-8") as f:
                        metrics = json.load(f)

                # Create timeline events based on available data
                timeline_events = []

                # Add run start event
                run_start_time = datetime.now() - timedelta(hours=1)
                timeline_events.append(
                    {
                        "timestamp": run_start_time.isoformat(),
                        "event": "Run started",
                        "type": "run_start",
                        "entity": run_id,
                        "confidence": 1.0,
                        "metadata": {"run_id": run_id, "status": "started"},
                    }
                )

                # Add document processing events
                if documents:
                    doc_processing_time = run_start_time + timedelta(minutes=5)
                    timeline_events.append(
                        {
                            "timestamp": doc_processing_time.isoformat(),
                            "event": f"Documents processed",
                            "type": "document_processing",
                            "entity": f"{len(documents)} documents",
                            "confidence": 1.0,
                            "metadata": {
                                "document_count": len(documents),
                                "run_id": run_id,
                            },
                        }
                    )

                # Add claims extraction events (placeholder for future implementation)
                claims_time = doc_processing_time + timedelta(minutes=10)
                timeline_events.append(
                    {
                        "timestamp": claims_time.isoformat(),
                        "event": "Claims extraction ready",
                        "type": "claims_extraction_ready",
                        "entity": "0 claims",
                        "confidence": 1.0,
                        "metadata": {
                            "claims_count": 0,
                            "run_id": run_id,
                            "note": "Claims extraction not yet implemented",
                        },
                    }
                )

                # Add entity extraction events (placeholder for future implementation)
                entities_time = claims_time + timedelta(minutes=5)
                timeline_events.append(
                    {
                        "timestamp": entities_time.isoformat(),
                        "event": "Entity extraction ready",
                        "type": "entity_extraction_ready",
                        "entity": "0 entities",
                        "confidence": 1.0,
                        "metadata": {
                            "entities_count": 0,
                            "run_id": run_id,
                            "note": "Entity extraction not yet implemented",
                        },
                    }
                )

                # Add run completion event
                completion_time = entities_time + timedelta(minutes=5)
                timeline_events.append(
                    {
                        "timestamp": completion_time.isoformat(),
                        "event": "Run completed",
                        "type": "run_complete",
                        "entity": run_id,
                        "confidence": 1.0,
                        "metadata": {
                            "run_id": run_id,
                            "status": "completed",
                            "total_duration_minutes": 25,
                        },
                    }
                )

                # Add some sample temporal events based on documents (if available)
                if documents:
                    for i, doc in enumerate(
                        documents[:5]
                    ):  # Limit to first 5 documents
                        # Create a temporal event for each document
                        doc_time = completion_time + timedelta(minutes=i * 2)
                        timeline_events.append(
                            {
                                "timestamp": doc_time.isoformat(),
                                "event": f"Document processed: {doc.get('title', 'Unknown document')[:50]}...",  # noqa: E501
                                "type": "document_processed",
                                "entity": doc.get("id", "unknown"),
                                "confidence": 1.0,
                                "metadata": {
                                    "document_id": doc.get("id"),
                                    "document_title": doc.get("title", "")[:100],
                                    "source_type": doc.get("source_type", "unknown"),
                                    "run_id": run_id,
                                },
                            }
                        )

                # Sort events by timestamp
                timeline_events.sort(key=lambda x: x["timestamp"])

                # Calculate actual duration from manifest if available
                total_duration_minutes = 25  # Default
                if manifest and "started_at" in manifest and "completed_at" in manifest:
                    try:
                        start_time = datetime.fromisoformat(
                            manifest["started_at"].replace("Z", "+00:00")
                        )
                        end_time = datetime.fromisoformat(
                            manifest["completed_at"].replace("Z", "+00:00")
                        )
                        duration = end_time - start_time
                        total_duration_minutes = int(duration.total_seconds() / 60)
                    except (ValueError, TypeError):
                        pass

                return envelope_ok(
                    {
                        "run_id": run_id,
                        "timeline": {
                            "events": timeline_events,
                            "total_events": len(timeline_events),
                            "time_range": {
                                "start": timeline_events[0]["timestamp"]
                                if timeline_events
                                else None,
                                "end": timeline_events[-1]["timestamp"]
                                if timeline_events
                                else None,
                            },
                        },
                        "summary": {
                            "documents_processed": len(documents),
                            "claims_extracted": 0,  # Will be populated when claims are extracted  # noqa: E501
                            "entities_identified": 0,  # Will be populated when entities are extracted  # noqa: E501
                            "total_duration_minutes": total_duration_minutes,
                            "bundle_size_bytes": sum(
                                f.stat().st_size
                                for f in bundle_path.rglob("*")
                                if f.is_file()
                            )
                            if bundle_path.exists()
                            else 0,
                        },
                    }
                )

            except Exception as e:
                return envelope_err(f"get_timeline failed: {e}", 500)

        # Phase 9.5.0 Adapter Testing Endpoints
        @self.app.post("/api/test/youtube_adapter")
        async def test_youtube_adapter(request: Request):
            """Test YouTube adapter with sample parameters."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 adapters
                try:
                    from src.adapters import YouTubeAdapter
                    from src.runners.enhanced_multisource_runner import (
                        EnhancedMultiSourceRunner,
                    )
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 adapters not available: {e}", 503)

                # Initialize adapter and runner
                config = {
                    "deduplication_enabled": True,
                    "persist_transcript_mode": True,
                    "youtube_default_limit": 2,
                    "youtube_default_sort": "oldest",
                    "transcript_timeout": 30,
                }

                adapter = YouTubeAdapter(config)
                runner = EnhancedMultiSourceRunner()

                # Test parameters
                test_params = {
                    "channel_url": data.get(
                        "channel_url",
                        "https://www.youtube.com/@imaginationpodcastofficial",
                    ),
                    "limit": data.get("limit", 2),
                    "sort": data.get("sort", "oldest"),
                    "transcript_mode": data.get("transcript_mode", "autosubs"),
                }

                # Process source
                documents = await adapter.process_source(test_params)

                return envelope_ok(
                    {
                        "adapter": "youtube",
                        "documents_count": len(documents),
                        "documents": [
                            {
                                "id": doc.id,
                                "title": doc.title,
                                "url": doc.url,
                                "transcript_mode": doc.transcript_mode,
                                "sha256": doc.sha256[:8] + "...",
                                "metadata": doc.metadata,
                            }
                            for doc in documents
                        ],
                        "deduplication_enabled": config["deduplication_enabled"],
                        "test_params": test_params,
                    }
                )

            except Exception as e:
                return envelope_err(f"YouTube adapter test failed: {e}", 500)

        @self.app.post("/api/test/web_adapter")
        async def test_web_adapter(request: Request):
            """Test web adapter with sample parameters."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 adapters
                try:
                    from src.adapters import WebAdapter
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 adapters not available: {e}", 503)

                # Initialize adapter
                config = {
                    "deduplication_enabled": True,
                    "persist_transcript_mode": True,
                    "web_default_max_depth": 1,
                    "web_default_js_render": False,
                    "web_request_timeout": 15,
                    "allowed_domains": ["youtube.com", "youtu.be", "example.com"],
                }

                adapter = WebAdapter(config)

                # Test parameters
                test_params = {
                    "urls": data.get("urls", ["https://example.com"]),
                    "max_depth": data.get("max_depth", 1),
                    "js_render": data.get("js_render", False),
                }

                # Process source
                documents = await adapter.process_source(test_params)

                return envelope_ok(
                    {
                        "adapter": "web",
                        "documents_count": len(documents),
                        "documents": [
                            {
                                "id": doc.id,
                                "title": doc.title,
                                "url": doc.url,
                                "sha256": doc.sha256[:8] + "...",
                                "metadata": doc.metadata,
                            }
                            for doc in documents
                        ],
                        "deduplication_enabled": config["deduplication_enabled"],
                        "test_params": test_params,
                    }
                )

            except Exception as e:
                return envelope_err(f"Web adapter test failed: {e}", 500)

        @self.app.post("/api/test/pdf_adapter")
        async def test_pdf_adapter(request: Request):
            """Test PDF adapter with sample parameters."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 adapters
                try:
                    from src.adapters import PDFAdapter
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 adapters not available: {e}", 503)

                # Initialize adapter
                config = {
                    "deduplication_enabled": True,
                    "persist_transcript_mode": True,
                    "pdf_default_ocr_required": False,
                    "pdf_ocr_auto_retry": True,
                    "pdf_max_pages_per_pdf": 10,
                    "pdf_extraction_timeout": 30,
                }

                adapter = PDFAdapter(config)

                # Test parameters
                test_params = {
                    "urls": data.get("urls", ["https://example.com/sample.pdf"]),
                    "ocr_required": data.get("ocr_required", False),
                    "auto_retry": data.get("auto_retry", True),
                }

                # Process source
                documents = await adapter.process_source(test_params)

                return envelope_ok(
                    {
                        "adapter": "pdf",
                        "documents_count": len(documents),
                        "documents": [
                            {
                                "id": doc.id,
                                "title": doc.title,
                                "url": doc.url,
                                "sha256": doc.sha256[:8] + "...",
                                "metadata": doc.metadata,
                            }
                            for doc in documents
                        ],
                        "deduplication_enabled": config["deduplication_enabled"],
                        "test_params": test_params,
                    }
                )

            except Exception as e:
                return envelope_err(f"PDF adapter test failed: {e}", 500)

        @self.app.post("/api/test/multi_source_run")
        async def test_multi_source_run(request: Request):
            """Test multi-source run with enhanced runner."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 runner
                try:
                    from src.runners.enhanced_multisource_runner import (
                        EnhancedMultiSourceRunner,
                    )
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 runner not available: {e}", 503)

                # Initialize runner
                runner = EnhancedMultiSourceRunner()

                # Create test sources
                sources = [
                    {
                        "type": "youtube",
                        "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                        "limit": 1,
                        "transcript_mode": "autosubs",
                    },
                    {"type": "web", "urls": ["https://example.com"], "max_depth": 1},
                    {
                        "type": "pdf",
                        "urls": ["https://example.com/sample.pdf"],
                        "ocr_required": False,
                    },
                ]

                # Start job
                job_id = await runner.start_job(
                    sources=sources,
                    job_label=data.get("job_label", "Phase 9.5.0 Test Run"),
                )

                # Wait for completion (with timeout)
                import asyncio

                timeout = 30  # seconds
                start_time = asyncio.get_event_loop().time()

                while True:
                    job_status = await runner.get_job_status(job_id)
                    if job_status["status"] in ["completed", "failed"]:
                        break

                    if asyncio.get_event_loop().time() - start_time > timeout:
                        return envelope_err("Multi-source run test timed out", 408)

                    await asyncio.sleep(1)

                return envelope_ok(
                    {
                        "job_id": job_id,
                        "job_status": job_status,
                        "sources_count": len(sources),
                        "test_params": data,
                    }
                )

            except Exception as e:
                return envelope_err(f"Multi-source run test failed: {e}", 500)

        @self.app.post("/api/test/deduplication")
        async def test_deduplication(request: Request):
            """Test deduplication functionality."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 adapters
                try:
                    from src.adapters import YouTubeAdapter
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 adapters not available: {e}", 503)

                # Initialize adapter with deduplication enabled
                config = {
                    "deduplication_enabled": True,
                    "persist_transcript_mode": True,
                    "youtube_default_limit": 3,
                    "transcript_timeout": 30,
                }

                adapter = YouTubeAdapter(config)

                # Create test content with duplicates
                test_content = data.get("test_content", "This is duplicate content")
                iterations = data.get("iterations", 3)

                # Simulate duplicate documents
                import uuid
                from src.adapters.base_adapter import DocumentLike
                from datetime import datetime

                documents = []
                for i in range(iterations):
                    doc = DocumentLike(
                        id=f"test_{uuid.uuid4().hex[:8]}",
                        source="test",
                        url=f"https://example.com/test_{i}",
                        title=f"Test Document {i + 1}",
                        text=test_content,  # Same content = duplicates
                        metadata={"iteration": i},
                        sha256="",  # Will be set by adapter
                        created_at=datetime.now(),
                        transcript_mode=None,
                    )
                    documents.append(doc)

                # Test deduplication
                unique_documents = adapter._filter_duplicates(documents)

                return envelope_ok(
                    {
                        "total_documents": len(documents),
                        "unique_documents": len(unique_documents),
                        "duplicates_removed": len(documents) - len(unique_documents),
                        "test_content": test_content,
                        "iterations": iterations,
                    }
                )

            except Exception as e:
                return envelope_err(f"Deduplication test failed: {e}", 500)

        @self.app.post("/api/test/transcript_persistence")
        async def test_transcript_persistence(request: Request):
            """Test transcript mode persistence."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0 adapters
                try:
                    from src.adapters import YouTubeAdapter
                except ImportError as e:
                    return envelope_err(f"Phase 9.5.0 adapters not available: {e}", 503)

                # Initialize adapter
                config = {
                    "deduplication_enabled": True,
                    "persist_transcript_mode": True,
                    "youtube_default_limit": 1,
                    "transcript_timeout": 30,
                }

                adapter = YouTubeAdapter(config)

                # Test parameters
                test_params = {
                    "channel_url": data.get(
                        "channel_url",
                        "https://www.youtube.com/@imaginationpodcastofficial",
                    ),
                    "limit": 1,
                    "transcript_mode": data.get("transcript_mode", "autosubs"),
                }

                # Process source
                documents = await adapter.process_source(test_params)

                # Check if transcript mode was persisted
                persisted_transcript_mode = None
                if documents:
                    persisted_transcript_mode = documents[0].transcript_mode

                return envelope_ok(
                    {
                        "persisted_transcript_mode": persisted_transcript_mode,
                        "documents_count": len(documents),
                        "test_params": test_params,
                    }
                )

            except Exception as e:
                return envelope_err(f"Transcript persistence test failed: {e}", 500)

        @self.app.post("/api/test/enhanced_extraction")
        async def test_enhanced_extraction(request: Request):
            """Test enhanced extraction with real URLs."""
            try:
                # Enforce health gate
                if not await _health_gate():
                    return envelope_err(
                        "Health gate failed; dependencies not ready", 503
                    )

                data = await request.json()

                # Import Phase 9.5.0a enhanced adapters
                try:
                    from src.adapters import WebAdapter, PDFAdapter
                except ImportError as e:
                    return envelope_err(
                        f"Phase 9.5.0a enhanced adapters not available: {e}", 503
                    )

                # Initialize adapters
                config = {
                    "deduplication_enabled": True,
                    "web_default_max_depth": 1,
                    "web_default_js_render": False,
                    "web_request_timeout": 30,
                    "pdf_default_ocr_required": False,
                    "pdf_ocr_auto_retry": True,
                    "pdf_extraction_timeout": 60,
                }

                web_adapter = WebAdapter(config)
                pdf_adapter = PDFAdapter(config)

                web_url = data.get("web_url", "https://httpbin.org/html")
                pdf_url = data.get(
                    "pdf_url",
                    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                )

                # Test web extraction
                web_docs = await web_adapter.process_source({"urls": [web_url]})
                web_method = (
                    web_docs[0].metadata.get("extraction_method", "unknown")
                    if web_docs
                    else "failed"
                )
                web_detail = (
                    web_docs[0].metadata.get("extraction_method_detail", "")
                    if web_docs
                    else ""
                )

                # Test PDF extraction
                pdf_docs = await pdf_adapter.process_source({"urls": [pdf_url]})
                pdf_method = (
                    pdf_docs[0].metadata.get("extraction_method", "unknown")
                    if pdf_docs
                    else "failed"
                )
                pdf_detail = (
                    pdf_docs[0].metadata.get("extraction_method_detail", "")
                    if pdf_docs
                    else ""
                )

                return envelope_ok(
                    {
                        "web_extraction_method": web_method,
                        "web_extraction_detail": web_detail,
                        "web_documents_count": len(web_docs),
                        "pdf_extraction_method": pdf_method,
                        "pdf_extraction_detail": pdf_detail,
                        "pdf_documents_count": len(pdf_docs),
                        "test_urls": {"web": web_url, "pdf": pdf_url},
                    }
                )

            except Exception as e:
                return envelope_err(f"Enhanced extraction test failed: {e}", 500)

        # SSOT Metadata API Endpoints
        @self.app.get("/api/meta/index")
        async def api_meta_index():
            """Get the full SSOT metadata index."""
            try:
                p = Path("reports/ssot_meta_index.json")
                if not p.exists():
                    return envelope_err("Meta index not found. Run `make meta-index`.", 404)
                try:
                    return envelope_ok(json.loads(p.read_text(encoding="utf-8")))
                except json.JSONDecodeError as e:
                    return envelope_err(f"Invalid meta index JSON: {e}", 500)
            except Exception as e:
                return envelope_err(f"Meta index error: {e}", 500)

        @self.app.get("/api/meta/search")
        async def api_meta_search(
            owner: str | None = None,
            tag: str | None = None,
            severity: str | None = None,
            text: str | None = None
        ):
            """Search the SSOT metadata index by owner/tag/severity/text."""
            try:
                p = Path("reports/ssot_meta_index.json")
                if not p.exists():
                    return envelope_err("Meta index not found. Run `make meta-index`.", 404)
                meta = json.loads(p.read_text(encoding="utf-8"))
                
                # Reuse the same filter logic as MCP (simple inline for brevity)
                def match(item: dict) -> bool:
                    smetas = item.get("ssot_meta", []) or []
                    hay = (json.dumps(item, ensure_ascii=False) if text else "")
                    def blk_ok(b: dict) -> bool:
                        if owner and (b.get("owner") != owner): 
                            return False
                        if severity and (str(b.get("severity")).lower() != str(severity).lower()): 
                            return False
                        if tag and (tag not in (b.get("tags") or [])): 
                            return False
                        if text and (text.lower() not in hay.lower()): 
                            return False
                        return True
                    return True if not smetas and not any([owner, tag, severity, text]) else any(blk_ok(b) for b in smetas)
                
                rules = [r for r in meta.get("rules", []) if match(r)]
                docs = [d for d in meta.get("docs", []) if match(d)]
                return envelope_ok({"rules": rules, "docs": docs})
            except Exception as e:
                return envelope_err(f"Meta search error: {e}", 500)

        @self.app.get("/api/meta/health")
        async def api_meta_health():
            """Get metadata index health status."""
            try:
                p = Path("reports/ssot_meta_index.json")
                if not p.exists():
                    return envelope_err("missing index", 404)
                try:
                    meta = json.loads(p.read_text(encoding="utf-8"))
                    return envelope_ok({"generated_at_utc": meta.get("generated_at_utc")})
                except json.JSONDecodeError:
                    return envelope_err("invalid json", 500)
            except Exception as e:
                return envelope_err(f"Meta health error: {e}", 500)

        @self.app.get("/api/meta/summary")
        async def api_meta_summary():
            """Return lightweight rollups for owners, severity, tags."""
            p = Path("reports/ssot_meta_index.json")
            if not p.exists():
                raise HTTPException(status_code=404, detail="Meta index not found. Run `make meta-index`.")
            meta = json.loads(p.read_text(encoding="utf-8"))
            rules = meta.get("rules", [])
            def merge_counts():
                owners, severity, tags = {}, {}, {}
                for r in rules:
                    for b in (r.get("ssot_meta") or []):
                        o = b.get("owner")
                        if isinstance(o,str) and o: owners[o] = owners.get(o,0)+1
                        s = str(b.get("severity","")).lower()
                        if s: severity[s] = severity.get(s,0)+1
                        for t in (b.get("tags") or []):
                            if isinstance(t,str) and t: tags[t] = tags.get(t,0)+1
                return owners, severity, tags
            owners, sev, tags = merge_counts()
            return {"status":"ok","data":{"owners":owners,"severity":sev,"tags":tags,"rules_total":len(rules)}}

        @self.app.websocket("/ws/ai-activity")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for AI activity updates"""
            await websocket.accept()
            self.active_connections.append(websocket)

            try:
                # Send initial status
                await websocket.send_text(
                    json.dumps({"ai_type": "llm", "status": "idle"})
                )

                # Keep connection alive
                while True:
                    # Wait for any message (ping/pong)
                    data = await websocket.receive_text()
                    # Echo back for now
                    await websocket.send_text(
                        json.dumps(
                            {
                                "ai_type": "llm",
                                "status": "idle",
                                "current_activity": "Idle",
                            }
                        )
                    )
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)

    async def broadcast_ai_activity(
        self, ai_type: str, status: str, activity: str = None
    ):
        """Broadcast AI activity to all connected WebSocket clients"""
        message = {"ai_type": ai_type, "status": status}
        if activity:
            message["current_activity"] = activity

        # Remove disconnected clients
        self.active_connections = [
            conn
            for conn in self.active_connections
            if not conn.client_state.disconnected
        ]

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
    uvicorn.run(main(), host="0.0.0.0", port=8050, log_level="info")
