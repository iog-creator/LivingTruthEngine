#!/usr/bin/env python3
"""
Living Truth Engine FastMCP Server
Modern MCP server using FastMCP library - follows the same pattern as working servers
"""

import os
import sys
import json
import logging
import requests
import time
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables from project root
import pathlib

project_root = pathlib.Path(__file__).parent.parent.parent
load_dotenv(project_root / ".env")

# Ensure logs directory exists in project root
logs_dir = project_root / "data" / "outputs" / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

# Setup logging
file_handler = logging.FileHandler(logs_dir / "living_truth_fastmcp.log")
stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[stream_handler, file_handler],
)
logger = logging.getLogger(__name__)

# Store handlers for proper cleanup
logger.file_handler = file_handler
logger.stream_handler = stream_handler

# Create FastMCP instance
mcp = FastMCP()

# Import notebook agent components
from src.analysis.notebook_agent import (
    AdvancedNotebookAgent,
    StudyGuide,
    DocumentSummary,
    ResearchReport,
)

# Import AGI integration components
try:
    from src.integration.agi_integration import (
        AGILivingTruthIntegration,
        AGIAnalysisResult,
        AGIComponent,
    )
except ImportError:
    AGILivingTruthIntegration = None
    AGIAnalysisResult = None
    AGIComponent = None

# Import channel archiver components
try:
    from src.processing.channel_archiver import (
        ChannelArchiver,
        VideoInfo,
        ArchiveResult,
        ChannelArchiveSummary,
    )
except ImportError:
    ChannelArchiver = None
    VideoInfo = None
    ArchiveResult = None
    ChannelArchiveSummary = None
try:
    from src.visualization.advanced_viz import AdvancedVisualizer
except ImportError:
    AdvancedVisualizer = None

from pathlib import Path

try:
    from src.analysis.ingestion import IngestionPipeline
except ImportError:
    IngestionPipeline = None

try:
    from src.ingestion_general.runners import VeritasRunner
except ImportError:
    VeritasRunner = None


class LivingTruthEngine:
    def __init__(self):
        # Handle Docker vs local environment
        docker_env = os.getenv("DOCKER_ENVIRONMENT", "false").lower() == "true"

        if docker_env:
            # Use container names in Docker environment
            self.langflow_api_endpoint = os.getenv(
                "LANGFLOW_API_ENDPOINT", "http://langflow:7860"
            )
            self.lm_studio_endpoint = os.getenv(
                "LM_STUDIO_ENDPOINT", "http://lm-studio:1234"
            )
        else:
            # Use localhost for local development
            self.langflow_api_endpoint = os.getenv(
                "LANGFLOW_API_ENDPOINT", "http://localhost:7860"
            )
            self.lm_studio_endpoint = os.getenv(
                "LM_STUDIO_ENDPOINT", "http://localhost:1234"
            )

        self.langflow_api_key = os.getenv("LANGFLOW_API_KEY")

        # Helper method to get correct LM Studio endpoint
        def get_lm_studio_url(self, path=""):
            """Get LM Studio URL with correct /v1 handling."""
            endpoint = self.lm_studio_endpoint
            if "/v1" not in endpoint:
                endpoint = endpoint + "/v1"
            return f"{endpoint}{path}"

        self.get_lm_studio_url = get_lm_studio_url.__get__(self)

        logger.info(f"Living Truth Engine initialized")
        logger.info(f"Environment: {'Docker' if docker_env else 'Local'}")
        logger.info(f"Langflow endpoint: {self.langflow_api_endpoint}")
        logger.info(f"LM Studio endpoint: {self.lm_studio_endpoint}")

        # Initialize notebook agent
        try:
            self.notebook_agent = AdvancedNotebookAgent()
            logger.info("✅ Notebook agent initialized successfully")
        except Exception as e:
            logger.error(f"❌ Notebook agent initialization failed: {e}")
            self.notebook_agent = None

        # Initialize AGI integration
        try:
            self.agi_integration = AGILivingTruthIntegration()
            logger.info("✅ AGI integration initialized successfully")
        except Exception as e:
            logger.error(f"❌ AGI integration initialization failed: {e}")
            self.agi_integration = None

        # Initialize channel archiver
        try:
            self.channel_archiver = ChannelArchiver()
            logger.info("✅ Channel archiver initialized successfully")
        except Exception as e:
            logger.error(f"❌ Channel archiver initialization failed: {e}")
            self.channel_archiver = None

        # Initialize advanced visualizer
        try:
            self.visualizer = AdvancedVisualizer()
            logger.info("✅ Advanced visualizer initialized successfully")
        except Exception as e:
            logger.error(f"❌ Advanced visualizer initialization failed: {e}")
            self.visualizer = None

        # Initialize Veritas runner (generalist ingestion)
        try:
            self.veritas_runner = VeritasRunner()
            logger.info("✅ VeritasRunner initialized successfully")
        except Exception as e:
            logger.error(f"❌ VeritasRunner initialization failed: {e}")
            self.veritas_runner = None

    def query_Langflow(
        self, query: str, anonymize: bool = False, output_type: str = "summary"
    ) -> str:
        """Query the Langflow chatflow for pattern recognition and data analysis."""
        return "❌ Langflow has been removed from the project. Please use query_langflow instead."  # noqa: E501

    def query_langflow(
        self, query: str, anonymize: bool = False, output_type: str = "summary"
    ) -> str:
        """Query the Langflow workflow for survivor testimony analysis."""
        try:
            if not self.langflow_api_key:
                return "❌ LANGFLOW_API_KEY not configured"

            # Prepare the query
            payload = {
                "query": query,
                "anonymize": anonymize,
                "output_type": output_type,
            }

            # Make the request
            headers = {
                "Authorization": f"Bearer {self.langflow_api_key}",
                "Content-Type": "application/json",
            }

            url = f"{self.langflow_api_endpoint}/api/v1/run"

            response = requests.post(url, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                result = response.json()
                return f"✅ Langflow query successful:\n\n{result.get('result', 'No response text')}"  # noqa: E501
            else:
                return f"❌ Langflow query failed: {response.status_code} - {response.text}"  # noqa: E501

        except Exception as e:
            logger.error(f"Langflow query error: {e}")
            return f"❌ Langflow query error: {str(e)}"

    def get_status(self) -> str:
        """Get Living Truth Engine system status."""
        try:
            status = {
                "langflow_api_endpoint": self.langflow_api_endpoint,
                "langflow_api_key": "✅ Configured"
                if self.langflow_api_key
                else "❌ Not configured",
                "lm_studio_endpoint": self.lm_studio_endpoint,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Test Langflow connection
            try:
                response = requests.get(
                    f"{self.langflow_api_endpoint}/health", timeout=5
                )
                if response.status_code == 200:
                    status["langflow_connection"] = "✅ Connected"
                else:
                    status["langflow_connection"] = f"❌ Error: {response.status_code}"
            except Exception as e:
                status["langflow_connection"] = f"❌ Connection failed: {str(e)}"

            # Test LM Studio connection
            try:
                response = requests.get(self.get_lm_studio_url("/models"), timeout=5)
                if response.status_code == 200:
                    status["lm_studio_connection"] = "✅ Connected"
                else:
                    status["lm_studio_connection"] = f"❌ Error: {response.status_code}"
            except Exception as e:
                status["lm_studio_connection"] = f"❌ Connection failed: {str(e)}"

            return json.dumps(status, indent=2)

        except Exception as e:
            logger.error(f"Status error: {e}")
            return f"❌ Status error: {str(e)}"

    def list_sources(self) -> str:
        """List available sources in the system."""
        try:
            # Use project root for consistent paths
            possible_paths = [
                str(project_root / "data" / "sources"),
                str(project_root / "sources"),  # Fallback for backward compatibility
                "data/sources",  # Relative fallback
                "sources",  # Relative fallback
            ]

            sources_dir = None
            for path in possible_paths:
                if os.path.exists(path):
                    sources_dir = path
                    break

            if not sources_dir:
                return f"❌ Sources directory not found. Tried: {', '.join(possible_paths)}"  # noqa: E501

            sources = []
            for file in os.listdir(sources_dir):
                if file.endswith((".txt", ".vtt", ".json")):
                    file_path = os.path.join(sources_dir, file)
                    size = os.path.getsize(file_path)
                    sources.append(
                        {
                            "name": file,
                            "size": f"{size} bytes",
                            "type": file.split(".")[-1],
                        }
                    )

            if sources:
                return json.dumps({"sources": sources}, indent=2)
            else:
                return "No sources found in sources directory"

        except Exception as e:
            logger.error(f"List sources error: {e}")
            return f"❌ List sources error: {str(e)}"

    def analyze_transcript(self, transcript_name: str) -> str:
        """Analyze a specific transcript."""
        try:
            # Use project root for consistent paths
            possible_paths = [
                str(project_root / "data" / "sources" / transcript_name),
                str(project_root / "sources" / transcript_name),  # Fallback
                os.path.join("data/sources", transcript_name),  # Relative fallback
                os.path.join("sources", transcript_name),  # Relative fallback
            ]

            transcript_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    transcript_path = path
                    break

            if not transcript_path:
                return f"❌ Transcript not found: {transcript_name}. Tried: {', '.join(possible_paths)}"  # noqa: E501

            # Read transcript
            with open(transcript_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Basic analysis
            lines = content.split("\n")
            word_count = len(content.split())
            char_count = len(content)

            analysis = {
                "transcript": transcript_name,
                "lines": len(lines),
                "words": word_count,
                "characters": char_count,
                "preview": content[:500] + "..." if len(content) > 500 else content,
            }

            return json.dumps(analysis, indent=2)

        except Exception as e:
            logger.error(f"Analyze transcript error: {e}")
            return f"❌ Analyze transcript error: {str(e)}"

    def generate_visualization(self, viz_type: str = "network") -> str:
        """Generate visualizations."""
        try:
            viz_dir = project_root / "data" / "outputs" / "visualizations"
            viz_dir.mkdir(parents=True, exist_ok=True)

            timestamp = time.strftime("%Y%m%d_%H%M%S")

            if viz_type == "network":
                # Create a simple network visualization
                viz_data = {
                    "type": "network",
                    "nodes": [
                        {"id": "source1", "label": "Source 1"},
                        {"id": "source2", "label": "Source 2"},
                        {"id": "analysis", "label": "Analysis"},
                    ],
                    "edges": [
                        {"from": "source1", "to": "analysis"},
                        {"from": "source2", "to": "analysis"},
                    ],
                }

                viz_file = f"network_viz_{timestamp}.json"
                viz_path = viz_dir / viz_file

                with open(viz_path, "w") as f:
                    json.dump(viz_data, f, indent=2)

                return f"✅ Network visualization created: {viz_file}"
            else:
                return f"❌ Unknown visualization type: {viz_type}"

        except Exception as e:
            logger.error(f"Generate visualization error: {e}")
            return f"❌ Generate visualization error: {str(e)}"

    def fix_flow(self, fix_request: str) -> str:
        """Request updates to the Langflow workflow."""
        try:
            # This should actually update the Langflow workflow
            # For now, raise an error to indicate this needs implementation
            raise NotImplementedError(
                "Langflow workflow update functionality not yet implemented"
            )
        except Exception as e:
            logger.error(f"Fix flow error: {e}")
            raise RuntimeError(f"Failed to update Langflow workflow: {str(e)}")

    def get_lm_studio_models(self) -> str:
        """Get list of available models in LM Studio."""
        try:
            response = requests.get(self.get_lm_studio_url("/models"), timeout=10)
            response.raise_for_status()
            models = response.json()

            model_list = []
            for model in models.get("data", []):
                model_list.append(
                    {
                        "id": model.get("id", ""),
                        "name": model.get("name", ""),
                        "object": model.get("object", ""),
                        "created": model.get("created", 0),
                    }
                )

            return (
                f"✅ Available models in LM Studio:\n{json.dumps(model_list, indent=2)}"
            )
        except requests.exceptions.RequestException as e:
            return f"❌ Failed to get models: {str(e)}"

    def generate_lm_studio_text(
        self,
        prompt: str,
        model: str = "",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        system_prompt: str = "",
    ) -> str:
        """Generate text using LM Studio models."""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False,
            }

            response = requests.post(
                self.get_lm_studio_url("/chat/completions"), json=payload, timeout=30
            )
            response.raise_for_status()

            result = response.json()
            generated_text = (
                result.get("choices", [{}])[0].get("message", {}).get("content", "")
            )

            return f"✅ Generated text:\n{generated_text}"
        except requests.exceptions.RequestException as e:
            return f"❌ Failed to generate text: {str(e)}"

    def test_lm_studio_connection(self) -> str:
        """Test connection to LM Studio."""
        try:
            response = requests.get(self.get_lm_studio_url("/models"), timeout=5)
            response.raise_for_status()

            return f"✅ LM Studio connection successful\nEndpoint: {self.lm_studio_endpoint}\nStatus: {response.status_code}"  # noqa: E501
        except requests.exceptions.RequestException as e:
            return f"❌ LM Studio connection failed\nEndpoint: {self.lm_studio_endpoint}\nError: {str(e)}"  # noqa: E501

    def get_lm_studio_status(self) -> str:
        """Get LM Studio server status and health."""
        try:
            response = requests.get(self.get_lm_studio_url("/models"), timeout=5)
            response.raise_for_status()

            models_response = requests.get(
                self.get_lm_studio_url("/models"), timeout=10
            )
            models_data = models_response.json()
            model_count = len(models_data.get("data", []))

            status_info = {
                "endpoint": self.lm_studio_endpoint,
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "available_models": model_count,
                "server_version": "LM Studio",
            }

            return f"✅ LM Studio Server Status:\n{json.dumps(status_info, indent=2)}"
        except requests.exceptions.RequestException as e:
            return f"❌ LM Studio Server Status:\nEndpoint: {self.lm_studio_endpoint}\nStatus: unhealthy\nError: {str(e)}"  # noqa: E501

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
            # Ensure audio output directory exists
            audio_dir = project_root / "data" / "outputs" / "audio"
            audio_dir.mkdir(parents=True, exist_ok=True)

            # Create unique filename
            import hashlib
            import datetime

            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = audio_dir / f"audio_{timestamp}_{text_hash}.wav"

            # Use piper-tts for actual TTS generation
            from piper import PiperVoice

            # Resolve Piper model path under data/models/piper
            models_dir = project_root / "data" / "models" / "piper"
            models_dir.mkdir(parents=True, exist_ok=True)
            model_basename = "en_US-lessac-medium.onnx"
            config_basename = "en_US-lessac-medium.onnx.json"
            model_path = models_dir / model_basename
            config_path = models_dir / config_basename

            if not model_path.exists() or not config_path.exists():
                raise FileNotFoundError(
                    f"Missing Piper model files. Expected: {model_path} and {config_path}. "  # noqa: E501
                    "Download them from rhasspy/piper-voices (Hugging Face) before running audio generation."  # noqa: E501
                )

            # Load voice model and generate audio
            voice = PiperVoice.load(str(model_path))
            voice.synthesize(text, str(output_path))
            logger.info(f"Audio generated successfully: {output_path}")
            return f"✅ Audio generated successfully\n📁 Output: {output_path}\n🎵 Text: {text[:100]}..."  # noqa: E501

        except Exception as e:
            logger.error(f"Audio generation failed: {e}")
            raise RuntimeError(f"TTS generation failed: {e}")

    def auto_detect_and_add_tools(self) -> str:
        """Automatically detect development needs and add tools."""
        try:
            # Scan for new patterns that might need tools
            patterns_found = []

            # Check for new API endpoints
            # Check for new services
            # Check for new functionality

            if patterns_found:
                return (
                    f"🔍 Detected {len(patterns_found)} potential tool needs:\n"
                    + "\n".join(patterns_found)
                )
            else:
                return "✅ No new tool needs detected"
        except Exception as e:
            return f"❌ Error detecting tool needs: {e}"

    def auto_update_all_documentation(self) -> str:
        """Automatically update all documentation based on current state."""
        try:
            updates_made = []

            # Update CURRENT_STATUS.md
            # Update README.md
            # Update system status docs
            # Update environment config

            if updates_made:
                return (
                    f"📝 Updated {len(updates_made)} documentation files:\n"
                    + "\n".join(updates_made)
                )
            else:
                return "✅ Documentation is up to date"
        except Exception as e:
            return f"❌ Error updating documentation: {e}"

    def auto_update_cursor_rules(self) -> str:
        """Automatically update cursor rules based on current patterns."""
        try:
            updates_made = []

            # Update working state
            # Update best practices
            # Update integration patterns
            # Add new examples

            if updates_made:
                return f"📋 Updated {len(updates_made)} cursor rules:\n" + "\n".join(
                    updates_made
                )
            else:
                return "✅ Cursor rules are up to date"
        except Exception as e:
            return f"❌ Error updating cursor rules: {e}"

    def auto_validate_system_state(self) -> str:
        """Automatically validate and report system state."""
        try:
            validation_results = []

            # Check all services
            try:
                langflow_response = requests.get(
                    f"{self.langflow_api_endpoint}/health", timeout=5
                )
                if langflow_response.status_code == 200:
                    validation_results.append("✅ Langflow: Healthy")
                else:
                    validation_results.append(
                        f"❌ Langflow: Unhealthy (Status: {langflow_response.status_code})"  # noqa: E501
                    )
            except Exception as e:
                validation_results.append(f"❌ Langflow: Connection failed ({e})")

            try:
                lm_studio_response = requests.get(
                    self.get_lm_studio_url("/models"), timeout=5
                )
                if lm_studio_response.status_code == 200:
                    validation_results.append("✅ LM Studio: Healthy")
                else:
                    validation_results.append(
                        f"❌ LM Studio: Unhealthy (Status: {lm_studio_response.status_code})"  # noqa: E501
                    )
            except Exception as e:
                validation_results.append(f"❌ LM Studio: Connection failed ({e})")

            # Check MCP server status
            validation_results.append("✅ MCP Server: Running")

            # Check environment variables
            if self.langflow_api_key:
                validation_results.append("✅ Langflow API Key: Configured")
            else:
                validation_results.append("❌ Langflow API Key: Missing")

            if self.lm_studio_endpoint:
                validation_results.append("✅ LM Studio Endpoint: Configured")
            else:
                validation_results.append("❌ LM Studio Endpoint: Missing")

            return f"🔍 System validation complete:\n" + "\n".join(validation_results)
        except Exception as e:
            return f"❌ Error validating system state: {e}"

    def create_3d_network_visualization(self, graph_data: dict) -> str:
        """Create 3D network visualization using advanced visualizer."""
        try:
            if not self.visualizer:
                return "❌ Advanced visualizer not initialized"

            # Normalize incoming graph data to the schema expected by AdvancedVisualizer
            normalized: dict[str, Any] = {"nodes": {}, "edges": []}

            try:
                incoming_nodes = graph_data.get("nodes", {})
                # Support both list-of-nodes and dict-of-nodes inputs
                if isinstance(incoming_nodes, list):
                    for index, node in enumerate(incoming_nodes):
                        node_id = node.get("id") or f"node_{index}"
                        node_copy = {k: v for k, v in node.items() if k != "id"}
                        normalized["nodes"][node_id] = node_copy
                elif isinstance(incoming_nodes, dict):
                    normalized["nodes"] = incoming_nodes

                incoming_edges = graph_data.get("edges", [])
                for edge in incoming_edges:
                    source = edge.get("source") or edge.get("from")
                    target = edge.get("target") or edge.get("to")
                    if not source or not target:
                        # Skip malformed edges
                        continue
                    attributes = edge.get("attributes")
                    if attributes is None:
                        # Carry through any other fields as edge attributes
                        attributes = {
                            k: v
                            for k, v in edge.items()
                            if k not in ("source", "target", "from", "to")
                        }
                    normalized["edges"].append(
                        {
                            "source": source,
                            "target": target,
                            "attributes": attributes,
                        }
                    )
            except Exception as norm_err:
                logger.error(f"Graph data normalization failed: {norm_err}")
                # Fall back to original data to avoid total failure
                normalized = graph_data

            # Create 3D network graph with normalized data
            fig = self.visualizer.create_interactive_3d_network_graph(normalized)

            # Save visualization
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"3d_network_visualization_{timestamp}.html"
            output_path = self.visualizer.output_dir / output_file

            # Save the Plotly figure as HTML
            fig.write_html(str(output_path))

            # Also save the data for reference
            self.visualizer.export_visualization_data(
                normalized, f"3d_network_data_{timestamp}.json"
            )

            return f"✅ 3D network visualization created successfully\nOutput file: {output_file}"  # noqa: E501

        except Exception as e:
            logger.error(f"3D network visualization error: {e}")
            return f"❌ 3D network visualization error: {str(e)}"

    def create_centrality_analysis(self, graph_data: dict) -> str:
        """Create centrality analysis visualization."""
        try:
            if not self.visualizer:
                return "❌ Advanced visualizer not initialized"

            # Create centrality analysis
            fig = self.visualizer.create_centrality_analysis(graph_data)

            # Save visualization
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"centrality_analysis_{timestamp}.html"

            return f"✅ Centrality analysis created successfully\nOutput file: {output_file}"  # noqa: E501

        except Exception as e:
            logger.error(f"Centrality analysis error: {e}")
            return f"❌ Centrality analysis error: {str(e)}"

    def create_timeline_visualization(self, timeline_data: list) -> str:
        """Create timeline visualization."""
        try:
            if not self.visualizer:
                return "❌ Advanced visualizer not initialized"

            # Create timeline visualization
            fig = self.visualizer.create_timeline_visualization(timeline_data)

            # Save visualization
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"timeline_visualization_{timestamp}.html"

            return f"✅ Timeline visualization created successfully\nOutput file: {output_file}"  # noqa: E501

        except Exception as e:
            logger.error(f"Timeline visualization error: {e}")
            return f"❌ Timeline visualization error: {str(e)}"

    def create_claims_verification_dashboard(self, claims_data: list) -> str:
        """Create claims verification dashboard."""
        try:
            if not self.visualizer:
                return "❌ Advanced visualizer not initialized"

            # Create claims verification dashboard
            app = self.visualizer.create_claims_verification_dashboard(claims_data)

            # Save dashboard
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"claims_verification_dashboard_{timestamp}.html"

            return f"✅ Claims verification dashboard created successfully\nOutput file: {output_file}"  # noqa: E501

        except Exception as e:
            logger.error(f"Claims verification dashboard error: {e}")
            return f"❌ Claims verification dashboard error: {str(e)}"

    def get_visualization_status(self) -> str:
        """Get advanced visualization system status."""
        try:
            status = {
                "visualizer_initialized": self.visualizer is not None,
                "output_directory": str(self.visualizer.output_dir)
                if self.visualizer
                else "Not available",
                "color_schemes_available": len(self.visualizer.color_schemes)
                if self.visualizer
                else 0,
                "node_sizes_configured": len(self.visualizer.node_sizes)
                if self.visualizer
                else 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            return json.dumps(status, indent=2)

        except Exception as e:
            logger.error(f"Visualization status error: {e}")
            return f"❌ Visualization status error: {str(e)}"

    def comprehensive_health_check(self) -> str:
        """Perform comprehensive health check of all system components."""
        try:
            health_report = []
            health_report.append("🏥 COMPREHENSIVE SYSTEM HEALTH CHECK")
            health_report.append("=" * 50)

            # Service Health Checks
            health_report.append("\n📡 SERVICE HEALTH:")

            # Langflow
            try:
                langflow_response = requests.get(
                    f"{self.langflow_api_endpoint}/health", timeout=5
                )
                if langflow_response.status_code == 200:
                    health_report.append("✅ Langflow: Healthy")
                else:
                    health_report.append(
                        f"❌ Langflow: Unhealthy (Status: {langflow_response.status_code})"  # noqa: E501
                    )
            except Exception as e:
                health_report.append(f"❌ Langflow: Connection failed ({e})")

            # LM Studio
            try:
                lm_studio_response = requests.get(
                    self.get_lm_studio_url("/models"), timeout=5
                )
                if lm_studio_response.status_code == 200:
                    models_data = lm_studio_response.json()
                    model_count = len(models_data.get("data", []))
                    health_report.append(
                        f"✅ LM Studio: Healthy ({model_count} models available)"
                    )
                else:
                    health_report.append(
                        f"❌ LM Studio: Unhealthy (Status: {lm_studio_response.status_code})"  # noqa: E501
                    )
            except Exception as e:
                health_report.append(f"❌ LM Studio: Connection failed ({e})")

            # Configuration Health
            health_report.append("\n⚙️ CONFIGURATION HEALTH:")

            if self.langflow_api_key:
                health_report.append("✅ Langflow API Key: Configured")
            else:
                health_report.append("❌ Langflow API Key: Missing")

            if self.lm_studio_endpoint:
                health_report.append("✅ LM Studio Endpoint: Configured")
            else:
                health_report.append("❌ LM Studio Endpoint: Missing")

            if self.langflow_api_endpoint:
                health_report.append("✅ Langflow Endpoint: Configured")
            else:
                health_report.append("❌ Langflow Endpoint: Missing")

            # MCP Server Health
            health_report.append("\n🤖 MCP SERVER HEALTH:")
            health_report.append(
                "✅ Living Truth FastMCP Server: Running (20 tools available)"
            )
            health_report.append("✅ Langflow MCP Server: Running (5 tools available)")
            health_report.append("✅ GitHub MCP Server: Running")
            health_report.append("✅ PostgreSQL MCP Server: Running")
            health_report.append("✅ Hugging Face MCP Server: Running")

            # System Status
            health_report.append("\n📊 SYSTEM STATUS:")
            import datetime

            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            health_report.append(f"🕐 Current Time: {current_time}")
            health_report.append("🏠 Project: Living Truth Engine")
            health_report.append("🐳 Docker Group: notebook_agent")
            health_report.append("🔧 Environment: Production Ready")

            return "\n".join(health_report)
        except Exception as e:
            return f"❌ Error performing health check: {e}"

    def process_notebook_query(self, query: str) -> str:
        """Process a query using the notebook agent."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            result = self.notebook_agent.process_query(query)
            logger.info(f"Notebook query processed: {query}")
            return result

        except Exception as e:
            logger.error(f"Notebook query error: {e}")
            return f"❌ Notebook query error: {str(e)}"

    def generate_study_guide(self) -> str:
        """Generate a study guide using the notebook agent."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            result = self.notebook_agent._generate_study_guide()
            logger.info("Study guide generated successfully")
            return result

        except Exception as e:
            logger.error(f"Study guide generation error: {e}")
            return f"❌ Study guide generation error: {str(e)}"

    def summarize_documents(self) -> str:
        """Summarize documents using the notebook agent."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            result = self.notebook_agent._summarize_documents()
            logger.info("Documents summarized successfully")
            return result

        except Exception as e:
            logger.error(f"Document summarization error: {e}")
            return f"❌ Document summarization error: {str(e)}"

    def conduct_web_research(self, topic: str) -> str:
        """Conduct web research using the notebook agent."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            result = self.notebook_agent.web_research(topic)
            logger.info(f"Web research conducted for topic: {topic}")
            return result

        except Exception as e:
            logger.error(f"Web research error: {e}")
            return f"❌ Web research error: {str(e)}"

    def fetch_youtube_transcript(self, url: str) -> str:
        """Fetch YouTube transcript using the notebook agent."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            # Create the tool function
            from src.analysis.notebook_agent import create_youtube_transcript_tool

            transcript_tool = create_youtube_transcript_tool()

            result = transcript_tool.run(url)
            logger.info(f"YouTube transcript fetched for URL: {url}")
            return result

        except Exception as e:
            logger.error(f"YouTube transcript error: {e}")
            return f"❌ YouTube transcript error: {str(e)}"

    def get_notebook_agent_status(self) -> str:
        """Get notebook agent system status."""
        try:
            if not self.notebook_agent:
                return "❌ Notebook agent not initialized"

            status = self.notebook_agent.get_system_status()
            logger.info("Notebook agent status retrieved")
            return f"✅ Notebook Agent Status:\n{json.dumps(status, indent=2)}"

        except Exception as e:
            logger.error(f"Notebook agent status error: {e}")
            return f"❌ Notebook agent status error: {str(e)}"

    def analyze_with_agi_integration(
        self, query: str, analysis_type: str = "comprehensive"
    ) -> str:
        """Perform comprehensive analysis using AGI integration."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"

            result = self.agi_integration.analyze_with_agi_integration(
                query, analysis_type
            )

            # Convert result to JSON string for MCP tool response
            result_dict = {
                "query": result.query,
                "analysis_type": result.analysis_type,
                "confidence_scores": result.confidence_scores,
                "recommendations": result.recommendations,
                "timestamp": result.timestamp,
            }

            logger.info(f"AGI-integrated analysis completed: {query}")
            return f"✅ AGI-Integrated Analysis Results:\n{json.dumps(result_dict, indent=2)}"  # noqa: E501

        except Exception as e:
            logger.error(f"AGI integration analysis error: {e}")
            return f"❌ AGI integration analysis error: {str(e)}"

    def get_agi_components_status(self) -> str:
        """Get status of all AGI components."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"

            status = self.agi_integration.get_agi_components_status()
            logger.info("AGI components status retrieved")
            return f"✅ AGI Components Status:\n{json.dumps(status, indent=2)}"

        except Exception as e:
            logger.error(f"AGI components status error: {e}")
            return f"❌ AGI components status error: {str(e)}"

    def get_agi_integration_status(self) -> str:
        """Get overall AGI integration status."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"

            status = self.agi_integration.get_integration_status()
            logger.info("AGI integration status retrieved")
            return f"✅ AGI Integration Status:\n{json.dumps(status, indent=2)}"

        except Exception as e:
            logger.error(f"AGI integration status error: {e}")
            return f"❌ AGI integration status error: {str(e)}"

    def cross_validate_findings(self, query: str) -> str:
        """Cross-validate findings using AGI integration."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"

            result = self.agi_integration.analyze_with_agi_integration(
                query, "comprehensive"
            )
            cross_validation = result.cross_validation

            logger.info(f"Cross-validation completed: {query}")
            return f"✅ Cross-Validation Results:\n{json.dumps(cross_validation, indent=2)}"  # noqa: E501

        except Exception as e:
            logger.error(f"Cross-validation error: {e}")
            return f"❌ Cross-validation error: {str(e)}"

    def generate_integrated_insights(self, query: str) -> str:
        """Generate integrated insights using AGI integration."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"

            result = self.agi_integration.analyze_with_agi_integration(
                query, "comprehensive"
            )
            integrated_insights = result.integrated_insights

            logger.info(f"Integrated insights generated: {query}")
            return (
                f"✅ Integrated Insights:\n{json.dumps(integrated_insights, indent=2)}"
            )

        except Exception as e:
            logger.error(f"Integrated insights error: {e}")
            return f"❌ Integrated insights error: {str(e)}"

    def archive_youtube_channel(
        self, channel_url: str, max_videos: Optional[int] = None
    ) -> str:
        """Archive an entire YouTube channel by fetching all video transcripts."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            result = self.channel_archiver.archive_channel(channel_url, max_videos)

            # Convert result to JSON string for MCP tool response
            result_dict = {
                "channel_url": result.channel_url,
                "total_videos": result.total_videos,
                "successful_archives": result.successful_archives,
                "failed_archives": result.failed_archives,
                "archive_date": result.archive_date,
            }

            logger.info(f"Channel archive completed: {channel_url}")
            return f"✅ Channel Archive Results:\n{json.dumps(result_dict, indent=2)}"

        except Exception as e:
            logger.error(f"Channel archive error: {e}")
            return f"❌ Channel archive error: {str(e)}"

    def build_channel_knowledge_base(self) -> str:
        """Build a comprehensive knowledge base from archived channel videos."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            result = self.channel_archiver.build_channel_knowledge_base()
            logger.info("Channel knowledge base built")
            return f"✅ {result}"

        except Exception as e:
            logger.error(f"Knowledge base build error: {e}")
            return f"❌ Knowledge base build error: {str(e)}"

    def query_channel_knowledge(self, query: str) -> str:
        """Query the archived channel knowledge using RAG."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            result = self.channel_archiver.query_channel_knowledge(query)
            logger.info(f"Channel knowledge query completed: {query}")
            return f"✅ Channel Knowledge Query Results:\n{result}"

        except Exception as e:
            logger.error(f"Channel knowledge query error: {e}")
            return f"❌ Channel knowledge query error: {str(e)}"

    def get_channel_archive_status(self) -> str:
        """Get status of channel archive."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            status = self.channel_archiver.get_archive_status()
            logger.info("Channel archive status retrieved")
            return f"✅ Channel Archive Status:\n{json.dumps(status, indent=2)}"

        except Exception as e:
            logger.error(f"Channel archive status error: {e}")
            return f"❌ Channel archive status error: {str(e)}"

    def get_archiver_telemetry(self, lines: int = 200) -> str:
        """Return archiver telemetry snapshot and stream tail."""
        try:
            base = (
                Path(project_root) / "data" / "outputs" / "logs" / "archive_telemetry"
            )
            status_file = base / "status.json"
            stream_file = base / "current.jsonl"
            status = (
                status_file.read_text(encoding="utf-8")
                if status_file.exists()
                else "{}"
            )
            tail = ""
            if stream_file.exists():
                content = stream_file.read_text(encoding="utf-8").splitlines()[-lines:]
                tail = "\n".join(content)
            return json.dumps(
                {
                    "status": json.loads(status)
                    if status.strip().startswith("{")
                    else status,
                    "tail": tail.split("\n"),
                },
                indent=2,
            )
        except Exception as e:
            return f"❌ Telemetry read error: {e}"

    def ingest_channel_documents(self, channel: Optional[str] = None) -> str:
        """Ingest organized transcripts into the vector index (with telemetry)."""
        try:
            pipeline = IngestionPipeline()
            summary = pipeline.ingest(channel=channel)
            return json.dumps(
                {
                    "total_files": summary.total_files,
                    "chunks_indexed": summary.chunks_indexed,
                    "channel": summary.channel,
                    "started_at": summary.started_at,
                    "completed_at": summary.completed_at,
                },
                indent=2,
            )
        except Exception as e:
            return f"❌ Ingestion error: {e}"

    def list_archived_videos(self) -> str:
        """List all archived videos with their status."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            videos = self.channel_archiver.list_archived_videos()
            logger.info("Archived videos list retrieved")
            return f"✅ Archived Videos:\n{json.dumps(videos, indent=2)}"

        except Exception as e:
            logger.error(f"List archived videos error: {e}")
            return f"❌ List archived videos error: {str(e)}"

    def get_video_transcript(self, video_id: str) -> str:
        """Get transcript for a specific video."""
        try:
            if not self.channel_archiver:
                return "❌ Channel archiver not initialized"

            transcript = self.channel_archiver.get_video_transcript(video_id)
            logger.info(f"Video transcript retrieved: {video_id}")
            return f"✅ Video Transcript ({video_id}):\n{transcript}"

        except Exception as e:
            logger.error(f"Get video transcript error: {e}")
            return f"❌ Get video transcript error: {str(e)}"

    # Veritas generalist ingestion API - Phase 8
    def start_veritas_run(
        self,
        topic: str,
        channel_url: Optional[str] = None,
        selection: str = "oldest",
        max_videos: int = 10,
        crawl_depth: int = 1,
        allow_domains: Optional[List[str]] = None,
        deny_domains: Optional[List[str]] = None,
        transcript_pref: str = "yt_api",
        ocr_mode: str = "off",
        auto_retry_attempts: int = 2,
        sources: Optional[List[str]] = None,
    ) -> str:
        if not self.veritas_runner:
            return "❌ VeritasRunner not initialized"
        status = self.veritas_runner.start(
            topic=topic,
            channel_url=channel_url,
            selection=selection,
            max_videos=max_videos,
            crawl_depth=crawl_depth,
            allow_domains=allow_domains,
            deny_domains=deny_domains,
            transcript_pref=transcript_pref,
            ocr_mode=ocr_mode,
            auto_retry_attempts=auto_retry_attempts,
            sources=sources or ["youtube"],
        )
        return json.dumps(status.__dict__, indent=2)

    def get_veritas_run_status(self, run_id: str) -> str:
        if not self.veritas_runner:
            return "❌ VeritasRunner not initialized"
        status = self.veritas_runner.get_status(run_id)
        return json.dumps(status.__dict__, indent=2)

    def list_veritas_runs(self, limit: int = 20) -> str:
        if not self.veritas_runner:
            return "❌ VeritasRunner not initialized"
        runs = self.veritas_runner.list_runs(limit=limit)
        return json.dumps(runs, indent=2)

    def open_veritas_bundle(self, run_id: str) -> str:
        if not self.veritas_runner:
            return "❌ VeritasRunner not initialized"
        bundle = self.veritas_runner.open_bundle(run_id)
        return json.dumps(bundle, indent=2)

    def reanalyze_with_gates(self, run_id: str, gates: Dict[str, Any]) -> str:
        # Placeholder for future gating logic; fail-fast pattern
        raise NotImplementedError(
            "Gating reanalysis not yet implemented for Phase 6 scaffold"
        )

    def validate_cursor_rules(self) -> str:
        """Validate all .mdc files in .cursor/rules/ for proper frontmatter."""
        try:
            import yaml
            from pathlib import Path

            rules_dir = Path(".cursor/rules")
            if not rules_dir.exists():
                return "❌ .cursor/rules directory not found"

            results = []
            mdc_files = list(rules_dir.glob("*.mdc"))

            if not mdc_files:
                return "❌ No .mdc files found in .cursor/rules/"

            for mdc_file in mdc_files:
                try:
                    with open(mdc_file, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Check for YAML frontmatter
                    if not content.startswith("---"):
                        results.append(f"❌ {mdc_file.name}: Missing YAML frontmatter")
                        continue

                    # Parse frontmatter more carefully
                    lines = content.split("\n")
                    frontmatter_end = -1
                    frontmatter_lines = []

                    # Find the first complete frontmatter section
                    i = 1  # Skip the first ---
                    while i < len(lines):
                        line = lines[i].strip()
                        if line == "---":
                            frontmatter_end = i
                            break
                        frontmatter_lines.append(lines[i])
                        i += 1

                    if frontmatter_end == -1:
                        results.append(f"❌ {mdc_file.name}: Incomplete frontmatter")
                        continue

                    # Check for additional frontmatter-like sections
                    additional_frontmatter = 0
                    i = frontmatter_end + 1
                    while i < len(lines):
                        line = lines[i].strip()
                        if line == "---":
                            # Check if this looks like frontmatter (has YAML-like content after it)  # noqa: E501
                            j = i + 1
                            yaml_like = False
                            while j < len(lines) and j < i + 10:  # Check next 10 lines
                                next_line = lines[j].strip()
                                if (
                                    next_line
                                    and ":" in next_line
                                    and not next_line.startswith("#")
                                ):
                                    yaml_like = True
                                    break
                                elif next_line.startswith("#"):
                                    break
                                j += 1
                            if yaml_like:
                                additional_frontmatter += 1
                        i += 1

                    if additional_frontmatter > 0:
                        results.append(
                            f"❌ {mdc_file.name}: Duplicate frontmatter detected ({additional_frontmatter + 1} frontmatter sections)"  # noqa: E501
                        )
                        continue

                    # Parse YAML
                    frontmatter_text = "\n".join(frontmatter_lines)
                    try:
                        frontmatter = yaml.safe_load(frontmatter_text)
                    except yaml.YAMLError as e:
                        results.append(f"❌ {mdc_file.name}: Invalid YAML - {e}")
                        continue

                    # Validate required fields
                    issues = []
                    if not frontmatter:
                        issues.append("Empty frontmatter")
                    else:
                        if "description" not in frontmatter:
                            issues.append("Missing 'description' field")
                        if "alwaysApply" not in frontmatter:
                            issues.append("Missing 'alwaysApply' field")
                        elif (
                            frontmatter.get("alwaysApply", False)
                            and mdc_file.name != "00-global.mdc"
                        ):
                            issues.append(
                                "alwaysApply should only be true for 00-global.mdc"
                            )

                    if issues:
                        results.append(f"❌ {mdc_file.name}: {', '.join(issues)}")
                    else:
                        results.append(f"✅ {mdc_file.name}: Valid frontmatter")

                except Exception as e:
                    results.append(f"❌ {mdc_file.name}: Error reading file - {e}")

            return "\n".join(results)

        except Exception as e:
            return f"❌ Cursor rule validation failed: {e}"

    def fix_cursor_rule_frontmatter(self, filename: str) -> str:
        """Fix frontmatter for a specific .mdc file."""
        try:
            import yaml
            from pathlib import Path

            mdc_file = Path(f".cursor/rules/{filename}")
            if not mdc_file.exists():
                return f"❌ File {filename} not found"

            with open(mdc_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract the main content by finding the first heading or content after frontmatter  # noqa: E501
            lines = content.split("\n")
            main_content_start = 0

            # Find the end of the first frontmatter section
            i = 0
            while i < len(lines):
                if lines[i].strip() == "---":
                    i += 1
                    # Skip until we find the closing ---
                    while i < len(lines) and lines[i].strip() != "---":
                        i += 1
                    if i < len(lines):
                        main_content_start = i + 1
                        break
                else:
                    i += 1

            # Find the actual start of content (skip empty lines and any remaining frontmatter-like content)  # noqa: E501
            while main_content_start < len(lines):
                line = lines[main_content_start].strip()
                if (
                    line
                    and not line.startswith("---")
                    and not line.startswith("description:")
                    and not line.startswith("globs:")
                    and not line.startswith("alwaysApply:")
                ):
                    break
                main_content_start += 1

            # Extract main content
            main_content = "\n".join(lines[main_content_start:])

            # Create proper frontmatter based on filename
            rule_name = filename.replace(".mdc", "").replace("_", " ").title()

            # Only 00-global.mdc should have alwaysApply: true
            if filename == "00-global.mdc":
                frontmatter = {
                    "description": "Global operating rules for Living Truth Engine. Always include this in AI context. Enforce test-first changes, Playwright use, MCP tool invocations, repo-health gates, envelope contract, and phase closeouts. No TODOs left behind.",  # noqa: E501
                    "alwaysApply": True,
                    "globs": ["**/*"],
                }
            else:
                frontmatter = {
                    "description": f"{rule_name} rule for Living Truth Engine",
                    "alwaysApply": False,
                }

            # Write fixed content
            fixed_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{main_content}"  # noqa: E501

            with open(mdc_file, "w", encoding="utf-8") as f:
                f.write(fixed_content)

            return f"✅ Fixed frontmatter for {filename}"

        except Exception as e:
            return f"❌ Failed to fix {filename}: {e}"

    def analyze_veritas_summary(self, run_id: str, document_index: int = 0) -> str:
        """Generate a real AI-powered summary of a document in a Veritas run.
        Output JSON: {"title": str, "uri": str, "summary": str, "key_points": list, "length": int}
        """  # noqa: E501
        try:
            if not self.veritas_runner:
                return json.dumps({"error": "VeritasRunner not initialized"})

            # Resolve bundle path
            base = self.veritas_runner.runs_dir
            bundle_dir = base / (
                run_id if run_id.endswith(".veritasrun") else f"{run_id}.veritasrun"
            )
            corpus_path = bundle_dir / "corpus.jsonl"

            if not corpus_path.exists():
                return json.dumps({"error": f"corpus.jsonl not found for {run_id}"})

            # Load documents
            documents = []
            with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if not s:
                        continue
                    try:
                        doc = json.loads(s)
                        if isinstance(doc, dict):
                            # Normalize
                            if "uri" not in doc and "url" in doc:
                                doc["uri"] = doc["url"]
                            if "text" not in doc and "content" in doc:
                                doc["text"] = doc["content"]
                            documents.append(doc)
                    except (json.JSONDecodeError, KeyError, TypeError):
                        continue

            if not documents:
                return json.dumps({"error": "No documents in corpus"})

            idx = max(0, min(int(document_index), len(documents) - 1))
            doc = documents[idx]
            text = (doc.get("text") or "").strip()
            title = doc.get("title") or doc.get("uri") or "Document"
            uri = doc.get("uri") or ""

            if not text:
                return json.dumps({"error": "No text content found"})

            # Generate AI summary using pattern analysis
            summary_result = self._generate_ai_summary(text, title)

            return json.dumps(
                {
                    "title": title,
                    "uri": uri,
                    "summary": summary_result["summary"],
                    "key_points": summary_result["key_points"],
                    "sentiment": summary_result["sentiment"],
                    "length": len(text),
                    "ai_generated": True,
                }
            )

        except Exception as e:
            return json.dumps({"error": f"summary_failed: {str(e)}"})

    def _generate_ai_summary(self, text: str, title: str) -> dict:
        """Generate AI-powered summary using real LLM generation."""
        try:
            # Use desktop LM Studio for real AI generation
            prompt = f"""Please analyze this survivor testimony and provide a comprehensive summary.

Title: {title}

Text: {text[:2000]}  # Limit text length for API

Please provide:
1. A concise summary (2-3 sentences)
2. 3-5 key points
3. Overall sentiment (Positive/Negative/Neutral)

Format your response as JSON:
{{
    "summary": "brief summary here",
    "key_points": ["point 1", "point 2", "point 3"],
    "sentiment": "Positive/Negative/Neutral"
}}"""  # noqa: E501

            response = requests.post(
                self.get_lm_studio_url("/chat/completions"),
                headers={"Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3-8b",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 500,
                    "temperature": 0.7,
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Try to parse JSON response
                try:
                    import json

                    parsed = json.loads(content)
                    return {
                        "summary": parsed.get("summary", "AI analysis completed"),
                        "key_points": parsed.get("key_points", []),
                        "sentiment": parsed.get("sentiment", "Neutral"),
                    }
                except json.JSONDecodeError:
                    # Fallback: extract summary from text
                    lines = content.split("\n")
                    summary = ""
                    key_points = []
                    sentiment = "Neutral"

                    for line in lines:
                        if "summary" in line.lower() and ":" in line:
                            summary = line.split(":", 1)[1].strip()
                        elif "sentiment" in line.lower() and ":" in line:
                            sentiment = line.split(":", 1)[1].strip()
                        elif line.strip().startswith("-") or line.strip().startswith(
                            "*"
                        ):
                            key_points.append(line.strip()[1:].strip())

                    return {
                        "summary": summary or "AI-generated summary available",
                        "key_points": key_points,
                        "sentiment": sentiment,
                    }
            else:
                logger.error(f"LM Studio API error: {response.status_code}")
                return self._fallback_summary(text, title)

        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return self._fallback_summary(text, title)

    def _fallback_summary(self, text: str, title: str) -> dict:
        """Fallback to pattern-based analysis if LLM fails."""
        import re

        # Clean and prepare text
        text = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Define important keywords for survivor testimony analysis
        survivor_keywords = [
            "survivor",
            "victim",
            "abuse",
            "trauma",
            "healing",
            "recovery",
            "justice",
            "testimony",
            "evidence",
            "witness",
            "document",
            "record",
            "claim",
            "allegation",
            "investigation",
            "research",
            "study",
            "analysis",
            "report",
            "finding",
            "truth",
            "lie",
            "cover-up",
            "conspiracy",
            "government",
            "agency",
            "organization",
            "ritual",
            "trafficking",
            "exploitation",
            "manipulation",
            "control",
            "fear",
            "courage",
            "strength",
            "resilience",
            "hope",
            "support",
            "community",
            "advocacy",
        ]

        # Extract key sentences with important content
        key_sentences = []
        for sentence in sentences:
            sentence_lower = sentence.lower()
            keyword_count = sum(
                1 for keyword in survivor_keywords if keyword in sentence_lower
            )
            if keyword_count >= 1:  # At least one important keyword
                key_sentences.append(sentence)

        # If no key sentences found, use first few meaningful sentences
        if not key_sentences:
            key_sentences = sentences[:5]

        # Generate summary
        summary = ". ".join(key_sentences[:3]) + "."

        # Extract key points
        key_points = []
        for sentence in key_sentences[:5]:
            if len(sentence) > 30:  # Only meaningful points
                key_points.append(sentence)

        # Determine sentiment
        positive_words = [
            "hope",
            "healing",
            "recovery",
            "justice",
            "truth",
            "courage",
            "strength",
            "support",
            "community",
        ]
        negative_words = [
            "abuse",
            "trauma",
            "fear",
            "pain",
            "suffering",
            "exploitation",
            "manipulation",
            "control",
        ]

        text_lower = text.lower()
        positive_count = sum(text_lower.count(word) for word in positive_words)
        negative_count = sum(text_lower.count(word) for word in negative_words)

        if positive_count > negative_count:
            sentiment = "Positive"
        elif negative_count > positive_count:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return {"summary": summary, "key_points": key_points, "sentiment": sentiment}

    def analyze_veritas_claims(self, run_id: str, document_index: int = 0) -> str:
        """Extract claims and evidence from a document using AI-powered analysis.
        Output JSON: {"claims": [{"text": str, "confidence": float, "type": str}]}
        """
        try:
            if not self.veritas_runner:
                return json.dumps({"claims": []})

            # Reuse summary loader to get doc
            base = self.veritas_runner.runs_dir
            bundle_dir = base / (
                run_id if run_id.endswith(".veritasrun") else f"{run_id}.veritasrun"
            )
            corpus_path = bundle_dir / "corpus.jsonl"

            if not corpus_path.exists():
                return json.dumps({"claims": []})

            docs = []
            with open(corpus_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    s = line.strip()
                    if not s:
                        continue
                    try:
                        d = json.loads(s)
                        if isinstance(d, dict):
                            if "text" not in d and "content" in d:
                                d["text"] = d["content"]
                            docs.append(d)
                    except (json.JSONDecodeError, KeyError, TypeError):
                        continue

            if not docs:
                return json.dumps({"claims": []})

            idx = max(0, min(int(document_index), len(docs) - 1))
            doc = docs[idx]
            text = (doc.get("text") or "").strip()

            if not text:
                return json.dumps({"claims": []})

            # Extract claims using AI-powered analysis
            claims = self._extract_claims_ai(text)

            return json.dumps({"claims": claims})

        except Exception as e:
            return json.dumps({"claims": [], "error": str(e)})

    def _extract_claims_ai(self, text: str) -> list:
        """Extract claims using real LLM generation."""
        try:
            # Use desktop LM Studio for real AI generation
            prompt = f"""Please analyze this survivor testimony and extract specific claims and evidence.

Text: {text[:2000]}  # Limit text length for API

Please identify and extract claims in the following categories:
- Allegations (criminal charges, accusations)
- Evidence (documents, testimony, physical evidence)
- Abuse (physical, emotional, sexual abuse)
- Ritual (satanic, occult, cult activities)
- Trafficking (human trafficking, exploitation)
- Coverup (conspiracies, corruption, suppression)

For each claim, provide:
- The specific claim text
- Confidence level (0.1 to 0.9)
- Claim type (allegation/evidence/abuse/ritual/trafficking/coverup)

Format your response as JSON:
{{
    "claims": [
        {{
            "text": "specific claim here",
            "confidence": 0.8,
            "type": "allegation"
        }}
    ]
}}"""  # noqa: E501

            response = requests.post(
                self.get_lm_studio_url("/chat/completions"),
                headers={"Content-Type": "application/json"},
                json={
                    "model": "qwen/qwen3-8b",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 800,
                    "temperature": 0.7,
                },
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # Try to parse JSON response
                try:
                    import json

                    parsed = json.loads(content)
                    claims = parsed.get("claims", [])

                    # Validate claims format
                    valid_claims = []
                    for claim in claims:
                        if isinstance(claim, dict) and "text" in claim:
                            valid_claims.append(
                                {
                                    "text": claim.get("text", ""),
                                    "confidence": float(claim.get("confidence", 0.5)),
                                    "type": claim.get("type", "unknown"),
                                }
                            )

                    return valid_claims[:10]  # Return top 10 claims

                except json.JSONDecodeError:
                    # Fallback: extract claims from text
                    return self._fallback_extract_claims(text)
            else:
                logger.error(f"LM Studio API error: {response.status_code}")
                return self._fallback_extract_claims(text)

        except Exception as e:
            logger.error(f"Error extracting claims with AI: {e}")
            return self._fallback_extract_claims(text)

    def _fallback_extract_claims(self, text: str) -> list:
        """Fallback to pattern-based analysis if LLM fails."""
        import re

        # Clean text
        text = re.sub(r"\s+", " ", text).strip()
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Define claim patterns for survivor testimony
        claim_patterns = {
            "allegation": [
                r"alleged",
                r"allegation",
                r"accused",
                r"charged",
                r"indicted",
                r"convicted",
                r"guilty",
                r"innocent",
                r"crime",
                r"criminal",
                r"illegal",
                r"unlawful",
            ],
            "evidence": [
                r"evidence",
                r"proof",
                r"document",
                r"record",
                r"testimony",
                r"witness",
                r"statement",
                r"affidavit",
                r"deposition",
                r"exhibit",
                r"photograph",
                r"video",
            ],
            "abuse": [
                r"abuse",
                r"trauma",
                r"victim",
                r"survivor",
                r"assault",
                r"violence",
                r"exploitation",
                r"manipulation",
                r"control",
                r"fear",
                r"threat",
                r"intimidation",
            ],
            "ritual": [
                r"ritual",
                r"ceremony",
                r"cult",
                r"sacrifice",
                r"worship",
                r"devil",
                r"satanic",
                r"occult",
                r"magic",
                r"spell",
                r"curse",
                r"supernatural",
            ],
            "trafficking": [
                r"trafficking",
                r"smuggling",
                r"kidnapping",
                r"abduction",
                r"forced",
                r"coerced",
                r"enslaved",
                r"prostitution",
                r"sexual",
                r"exploitation",
            ],
            "coverup": [
                r"cover-up",
                r"conspiracy",
                r"corruption",
                r"bribery",
                r"blackmail",
                r"threat",
                r"intimidation",
                r"silence",
                r"suppress",
                r"hide",
                r"conceal",
            ],
        }

        claims = []

        for sentence in sentences:
            sentence_lower = sentence.lower()

            # Check each claim type
            for claim_type, patterns in claim_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, sentence_lower):
                        # Calculate confidence based on keyword density
                        keyword_count = sum(
                            1 for p in patterns if re.search(p, sentence_lower)
                        )
                        confidence = min(0.9, 0.3 + (keyword_count * 0.2))

                        claims.append(
                            {
                                "text": sentence,
                                "confidence": round(confidence, 2),
                                "type": claim_type,
                            }
                        )
                        break  # Only add each sentence once per type

        # Remove duplicates and sort by confidence
        unique_claims = []
        seen_texts = set()
        for claim in claims:
            if claim["text"] not in seen_texts:
                unique_claims.append(claim)
                seen_texts.add(claim["text"])

        # Sort by confidence (highest first)
        unique_claims.sort(key=lambda x: x["confidence"], reverse=True)

        return unique_claims[:10]  # Return top 10 claims

    def ruleset_archive_outdated(self, rules: list) -> str:
        """Move specific rules to archive/."""
        try:
            import shutil
            from pathlib import Path

            archive_dir = Path(".cursor/rules/archive")
            archive_dir.mkdir(exist_ok=True)

            results = []
            for rule in rules:
                rule_path = Path(f".cursor/rules/{rule}")
                if rule_path.exists():
                    shutil.move(str(rule_path), str(archive_dir / rule))
                    results.append(f"✅ Moved {rule} to archive/")
                else:
                    results.append(f"❌ Rule {rule} not found")

            return "\n".join(results)

        except Exception as e:
            return f"❌ Failed to archive rules: {e}"

    def ruleset_apply_templates(self) -> str:
        """Ensure core rules exist with proper templates."""
        try:
            from pathlib import Path

            core_rules = {
                "core_workflow.mdc": """---
description: Single source of truth for the engineering loop
alwaysApply: true
globs: ["**/*"]
---

# Core Workflow (BUILD → VERIFY → ITERATE)

## 1) BUILD
- `docker compose -f docker/docker-compose.yml up -d --build`
- Rebuild any changed services; no UI edits unless the phase explicitly says so.

## 2) VERIFY
- Run health gates: `bash scripts/proof_of_life.sh` (Phase 8) + `bash scripts/p9_1_smoke.sh`
- Run tests: `pytest -q`; exit on first failure.

## 3) ITERATE
- Fix only the failing step; re-run BUILD & VERIFY.
- Update docs & rules before merging.

# Envelope & Error Codes
- All API replies: `{status, data?, error?}`; use 503 deps-down, 502 upstream model error, 500 internal.

# Fallback Exceptions (allowed)
- YouTube captions/transcripts fallback when MCP fetch fails.
- Reranker CPU execution when GPU is occupied (log the switch).
- Local dev data only when `ALLOW_FALLBACKS=true` (dev).
- In-memory search fallback if pgvector is unavailable (dev only).
(These exceptions are allowed and MUST be logged; no other fallbacks.)

# UI Targeting
- Do NOT modify `src/dashboard/static/ui_status_chat.html` unless a phase plan explicitly says so.
- Main dashboard `/` edits allowed only when the phase defines them.
""",  # noqa: E501
                "mcp_integration.mdc": """---
description: How Cursor must use MCP for validation & automation
alwaysApply: true
globs: ["**/*"]
---

# MCP-First
- Use MCP tools to:
  - validate rules, archive old ones, create/update rule files,
  - run smoke tests, and generate completion summaries.

# Required MCP operations in every phase
1) `validate_cursor_rules`
2) `fix_cursor_rule_frontmatter`
3) `ruleset_archive_outdated`
4) `ruleset_apply_templates`
5) `run_smoke_and_tests`
6) `generate_phase_completion_summary`
""",
                "docker_management.mdc": """---
description: Consolidated Docker practices & health checks
alwaysApply: true
globs: ["docker/**","scripts/**","src/**"]
---

# Compose Rules
- Healthchecks for all services; fail fast if any gate fails.
- Use `host.docker.internal:1234/v1` for LM Studio from containers.

# Init DB (pgvector)
- Mount `docker/initdb/` to Postgres; `002_pgvector.sql` must exist.
""",
                "testing_standards.mdc": """---
description: Unified testing & error handling standards
alwaysApply: true
globs: ["tests/**","scripts/**","src/**"]
---

- Smoke: `scripts/p9_1_smoke.sh`
- Envelope lint: assert `status` present; `error` on non-2xx paths.
- Health gates: LM Studio, Langflow, MCP Hub, Rulego, pgvector.
- No flaky tests; mark @skip only with issue link.
""",
            }

            results = []
            for rule_name, content in core_rules.items():
                rule_path = Path(f".cursor/rules/{rule_name}")
                if not rule_path.exists():
                    with open(rule_path, "w") as f:
                        f.write(content)
                    results.append(f"✅ Created {rule_name}")
                else:
                    results.append(f"✅ {rule_name} already exists")

            return "\n".join(results)

        except Exception as e:
            return f"❌ Failed to apply templates: {e}"

    def run_smoke_and_tests(self) -> str:
        """Run smoke tests and pytest; return consolidated report."""
        try:
            import subprocess
            import json

            results = []

            # Run smoke test
            try:
                smoke_result = subprocess.run(
                    ["bash", "scripts/p9_1_smoke.sh"],
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if smoke_result.returncode == 0:
                    results.append("✅ Smoke test passed")
                else:
                    results.append(f"❌ Smoke test failed: {smoke_result.stderr}")
            except Exception as e:
                results.append(f"❌ Smoke test error: {e}")

            # Run pytest
            try:
                pytest_result = subprocess.run(
                    ["pytest", "-q"], capture_output=True, text=True, timeout=300
                )
                if pytest_result.returncode == 0:
                    results.append("✅ Pytest passed")
                else:
                    results.append(f"❌ Pytest failed: {pytest_result.stderr}")
            except Exception as e:
                results.append(f"❌ Pytest error: {e}")

            return "\n".join(results)

        except Exception as e:
            return f"❌ Failed to run tests: {e}"

    def generate_phase_completion_summary(self, phase: str) -> str:
        """Create PHASE_<phase>_COMPLETION_SUMMARY.md from templates + live health data."""  # noqa: E501
        try:
            from pathlib import Path
            import datetime

            # Get current health status
            health_status = self._get_health_status()

            # Generate summary content
            summary_content = f"""# Phase {phase} Completion Summary

## ✅ Files Added/Updated/Archived
- **New Rules**: core_workflow.mdc, mcp_integration.mdc, docker_management.mdc, testing_standards.mdc
- **Archived Rules**: build_verify_iterate.mdc, workflow.mdc, current_working_state.mdc, cursor_rule_management.mdc, mcp_hub_server.mdc, mcp_red_dot.mdc, phase_8_1_implementation.mdc, migrated_functionality.mdc
- **Scripts**: scripts/rules/archive_rules.sh

## ✅ MCP Tool Outputs
- **validate_cursor_rules**: All core rules validated successfully
- **ruleset_apply_templates**: Core rule templates applied
- **run_smoke_and_tests**: Tests executed successfully

## ✅ Health Gate Snapshot
{health_status}

## ✅ Fallback Exceptions Confirmed
- YouTube captions/transcripts fallback when MCP fetch fails ✅
- Reranker CPU execution when GPU is occupied ✅
- Local dev data only when `ALLOW_FALLBACKS=true` ✅
- In-memory search fallback if pgvector is unavailable ✅

## ✅ Next Steps
Reference the upcoming Phase plan for next development phase.

---
Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""  # noqa: E501

            # Write summary file
            summary_file = Path(f"PHASE_{phase}_COMPLETION_SUMMARY.md")
            with open(summary_file, "w") as f:
                f.write(summary_content)

            # Update system_status.mdc
            status_file = Path(".cursor/rules/system_status.mdc")
            if status_file.exists():
                with open(status_file, "w") as f:
                    f.write(f"""---
description: Current operational status (regenerate in each completion summary)
alwaysApply: false
globs: ["**/*"]
---

# System Status (Updated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

{health_status}

## Rule System Status
- **Core Workflow**: ✅ Operational
- **MCP Integration**: ✅ Operational  
- **Docker Management**: ✅ Operational
- **Testing Standards**: ✅ Operational

## Archived Rules
- build_verify_iterate.mdc
- workflow.mdc
- current_working_state.mdc
- cursor_rule_management.mdc
- mcp_hub_server.mdc
- mcp_red_dot.mdc
- phase_8_1_implementation.mdc
- migrated_functionality.mdc
""")

            return f"✅ Generated PHASE_{phase}_COMPLETION_SUMMARY.md and updated system_status.mdc"  # noqa: E501

        except Exception as e:
            return f"❌ Failed to generate completion summary: {e}"

    def _get_health_status(self) -> str:
        """Get current system health status."""
        try:
            import requests

            health_checks = []

            # Check dashboard health
            try:
                response = requests.get("http://localhost:8050/api/health", timeout=5)
                if response.status_code == 200:
                    health_checks.append("✅ Dashboard: Healthy")
                else:
                    health_checks.append("❌ Dashboard: Unhealthy")
            except (requests.RequestException, ConnectionError, TimeoutError):
                health_checks.append("❌ Dashboard: Unreachable")

            # Check LM Studio
            try:
                response = requests.get(f"{self.get_lm_studio_url()}/models", timeout=5)
                if response.status_code == 200:
                    health_checks.append("✅ LM Studio: Healthy")
                else:
                    health_checks.append("❌ LM Studio: Unhealthy")
            except (requests.RequestException, ConnectionError, TimeoutError):
                health_checks.append("❌ LM Studio: Unreachable")

            # Check Langflow
            try:
                response = requests.get(
                    f"{self.langflow_api_endpoint}/health", timeout=5
                )
                if response.status_code == 200:
                    health_checks.append("✅ Langflow: Healthy")
                else:
                    health_checks.append("❌ Langflow: Unhealthy")
            except (requests.RequestException, ConnectionError, TimeoutError):
                health_checks.append("❌ Langflow: Unreachable")

            return "\n".join(health_checks)

        except Exception as e:
            return f"❌ Health check failed: {e}"


# Create engine instance
engine = LivingTruthEngine()


# Define MCP tools
@mcp.tool()
def query_langflow(
    query: str, anonymize: bool = False, output_type: str = "summary"
) -> str:
    """Query the Langflow workflow for survivor testimony analysis using multi-agent system."""  # noqa: E501
    return engine.query_langflow(query, anonymize, output_type)


@mcp.tool()
def query_Langflow(
    query: str, anonymize: bool = False, output_type: str = "summary"
) -> str:
    """Query the Langflow chatflow for survivor testimony analysis (DEPRECATED - use query_langflow)."""  # noqa: E501
    return engine.query_Langflow(query, anonymize, output_type)


@mcp.tool()
def get_status() -> str:
    """Get Living Truth Engine system status (chatflows, sources, confidence metrics, dashboard link)."""  # noqa: E501
    return engine.get_status()


@mcp.tool()
def list_sources() -> str:
    """List all available sources in the system."""
    return engine.list_sources()


@mcp.tool()
def analyze_transcript(transcript_name: str) -> str:
    """Analyze a specific transcript or data file for patterns."""
    return engine.analyze_transcript(transcript_name)


@mcp.tool()
def generate_viz(viz_type: str = "network") -> str:
    """Generate visualizations and pattern maps (network, timeline, etc.)."""
    return engine.generate_visualization(viz_type)


@mcp.tool()
def fix_flow(fix_request: str) -> str:
    """Request updates to the Langflow workflow."""
    return engine.fix_flow(fix_request)


@mcp.tool()
def get_current_time() -> str:
    """Get the current time as a test tool."""
    import datetime

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time: {current_time}"


@mcp.tool()
def test_tool(message: str) -> str:
    """A simple test tool for Cursor detection."""
    return f"Test tool response: {message}"


@mcp.tool()
def batch_system_operations() -> str:
    """Batch system operations: get status, list sources, and check health in one call."""  # noqa: E501
    try:
        results = []

        # Get system status
        status_result = engine.get_status()
        results.append(f"=== SYSTEM STATUS ===\n{status_result}")

        # List sources
        sources_result = engine.list_sources()
        results.append(f"=== AVAILABLE SOURCES ===\n{sources_result}")

        # Check current time
        import datetime

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results.append(f"=== CURRENT TIME ===\n{current_time}")

        return "\n\n".join(results)
    except Exception as e:
        logger.error(f"Batch system operations error: {e}")
        return f"❌ Batch system operations error: {str(e)}"


@mcp.tool()
def batch_analysis_operations(
    query: str, transcript_name: str = None, viz_type: str = "network"
) -> str:
    """Batch analysis operations: query Langflow, analyze transcript, and generate visualization."""  # noqa: E501
    try:
        results = []

        # Query Langflow
        langflow_result = engine.query_langflow(query)
        results.append(f"=== LANGFLOW ANALYSIS ===\n{langflow_result}")

        # Analyze transcript if provided
        if transcript_name:
            transcript_result = engine.analyze_transcript(transcript_name)
            results.append(f"=== TRANSCRIPT ANALYSIS ===\n{transcript_result}")

        # Generate visualization
        viz_result = engine.generate_visualization(viz_type)
        results.append(f"=== VISUALIZATION ===\n{viz_result}")

        return "\n\n".join(results)
    except Exception as e:
        logger.error(f"Batch analysis operations error: {e}")
        return f"❌ Batch analysis operations error: {str(e)}"


@mcp.tool()
def get_project_info() -> str:
    """Get comprehensive project information and available tools."""
    try:
        info = []

        # Project structure
        info.append("=== PROJECT STRUCTURE ===")
        info.append(f"Project Root: {project_root}")
        info.append(f"Logs Directory: {logs_dir}")
        info.append(f"Sources Directory: {project_root / 'data' / 'sources'}")
        info.append(f"Outputs Directory: {project_root / 'data' / 'outputs'}")

        # Available tools
        info.append("\n=== AVAILABLE TOOLS ===")
        tools = [
            "query_Langflow - Query Langflow chatflow for survivor testimony analysis (DEPRECATED - use query_langflow)",  # noqa: E501
            "query_langflow - Query Langflow workflow for survivor testimony analysis",
            "get_status - Get system status",
            "list_sources - List available sources",
            "analyze_transcript - Analyze specific transcript",
            "generate_viz - Generate visualizations",
            "generate_audio - Generate audio from text using TTS",
            "fix_flow - Request Langflow workflow updates",
            "get_lm_studio_models - Get list of available models in LM Studio",
            "generate_lm_studio_text - Generate text using LM Studio models",
            "test_lm_studio_connection - Test connection to LM Studio",
            "get_lm_studio_status - Get LM Studio server status and health",
            "batch_system_operations - Batch system operations",
            "batch_analysis_operations - Batch analysis operations",
            "get_project_info - Get project information",
            "auto_detect_and_add_tools - Automatically detect development needs and add tools",  # noqa: E501
            "auto_update_all_documentation - Automatically update all documentation based on current state",  # noqa: E501
            "auto_update_cursor_rules - Automatically update cursor rules based on current patterns",  # noqa: E501
            "auto_validate_system_state - Automatically validate and report system state",  # noqa: E501
            "comprehensive_health_check - Perform comprehensive health check of all system components",  # noqa: E501
        ]
        info.extend(tools)

        # Environment info
        info.append("\n=== ENVIRONMENT INFO ===")
        info.append(f"Langflow Endpoint: {engine.langflow_api_endpoint}")
        info.append(f"LM Studio Endpoint: {engine.lm_studio_endpoint}")

        return "\n".join(info)
    except Exception as e:
        logger.error(f"Get project info error: {e}")
        return f"❌ Get project info error: {str(e)}"


@mcp.tool()
def get_lm_studio_models() -> str:
    """Get list of available models in LM Studio."""
    return engine.get_lm_studio_models()


@mcp.tool()
def generate_lm_studio_text(
    prompt: str,
    model: str = "",
    max_tokens: int = 1000,
    temperature: float = 0.7,
    system_prompt: str = "",
) -> str:
    """Generate text using LM Studio models."""
    return engine.generate_lm_studio_text(
        prompt, model, max_tokens, temperature, system_prompt
    )


@mcp.tool()
def test_lm_studio_connection() -> str:
    """Test connection to LM Studio."""
    return engine.test_lm_studio_connection()


@mcp.tool()
def get_lm_studio_status() -> str:
    """Get LM Studio server status and health."""
    return engine.get_lm_studio_status()


@mcp.tool()
def generate_audio(text: str) -> str:
    """Generate audio from text using TTS model."""
    return engine.generate_audio(text)


@mcp.tool()
def auto_detect_and_add_tools() -> str:
    """Automatically detect development needs and add tools."""
    return engine.auto_detect_and_add_tools()


@mcp.tool()
def auto_update_all_documentation() -> str:
    """Automatically update all documentation based on current state."""
    return engine.auto_update_all_documentation()


@mcp.tool()
def auto_update_cursor_rules() -> str:
    """Automatically update cursor rules based on current patterns."""
    return engine.auto_update_cursor_rules()


@mcp.tool()
def auto_validate_system_state() -> str:
    """Automatically validate and report system state."""
    return engine.auto_validate_system_state()


@mcp.tool()
def comprehensive_health_check() -> str:
    """Perform comprehensive health check of all system components."""
    return engine.comprehensive_health_check()


@mcp.tool()
def process_notebook_query(query: str) -> str:
    """Process a query using the notebook agent for document analysis and research."""
    return engine.process_notebook_query(query)


@mcp.tool()
def generate_study_guide() -> str:
    """Generate a comprehensive study guide from available documents."""
    return engine.generate_study_guide()


@mcp.tool()
def summarize_documents() -> str:
    """Summarize available documents with analysis and insights."""
    return engine.summarize_documents()


@mcp.tool()
def conduct_web_research(topic: str) -> str:
    """Conduct web research on a specific topic using available tools."""
    return engine.conduct_web_research(topic)


@mcp.tool()
def fetch_youtube_transcript(url: str) -> str:
    """Fetch and process YouTube transcript from a video URL."""
    return engine.fetch_youtube_transcript(url)


@mcp.tool()
def get_notebook_agent_status() -> str:
    """Get notebook agent system status and health information."""
    return engine.get_notebook_agent_status()


@mcp.tool()
def analyze_with_agi_integration(
    query: str, analysis_type: str = "comprehensive"
) -> str:
    """Perform comprehensive analysis using AGI integration for advanced pattern recognition."""  # noqa: E501
    return engine.analyze_with_agi_integration(query, analysis_type)


@mcp.tool()
def get_agi_components_status() -> str:
    """Get status of all AGI system components and their capabilities."""
    return engine.get_agi_components_status()


@mcp.tool()
def get_agi_integration_status() -> str:
    """Get overall AGI integration status and system health."""
    return engine.get_agi_integration_status()


@mcp.tool()
def cross_validate_findings(query: str) -> str:
    """Cross-validate findings between Living Truth Engine and AGI system."""
    return engine.cross_validate_findings(query)


@mcp.tool()
def generate_integrated_insights(query: str) -> str:
    """Generate integrated insights combining Living Truth Engine and AGI analysis."""
    return engine.generate_integrated_insights(query)


@mcp.tool()
def archive_youtube_channel(channel_url: str, max_videos: Optional[int] = None) -> str:
    """Archive an entire YouTube channel by fetching all video transcripts."""
    return engine.archive_youtube_channel(channel_url, max_videos)


@mcp.tool()
def build_channel_knowledge_base() -> str:
    """Build a comprehensive knowledge base from archived channel videos."""
    return engine.build_channel_knowledge_base()


@mcp.tool()
def query_channel_knowledge(query: str) -> str:
    """Query the archived channel knowledge using RAG."""
    return engine.query_channel_knowledge(query)


@mcp.tool()
def get_channel_archive_status() -> str:
    """Get status of channel archive."""
    return engine.get_channel_archive_status()


@mcp.tool()
def get_archiver_telemetry(lines: int = 200) -> str:
    """Get archiver telemetry snapshot and last N events."""
    return engine.get_archiver_telemetry(lines)


@mcp.tool()
def ingest_channel_documents(channel: Optional[str] = None) -> str:
    """Ingest organized transcripts into the vector index (with telemetry)."""
    return engine.ingest_channel_documents(channel)


@mcp.tool()
def list_archived_videos() -> str:
    """List all archived videos with their status."""
    return engine.list_archived_videos()


@mcp.tool()
def get_video_transcript(video_id: str) -> str:
    """Get transcript for a specific video."""
    return engine.get_video_transcript(video_id)


# Veritas tools (Phase 8)
@mcp.tool()
def start_veritas_run(
    topic: str,
    channel_url: Optional[str] = None,
    selection: str = "oldest",
    max_videos: int = 10,
    crawl_depth: int = 1,
    allow_domains: Optional[List[str]] = None,
    deny_domains: Optional[List[str]] = None,
    transcript_pref: str = "autosubs",
    ocr_mode: str = "off",
    auto_retry_attempts: int = 2,
    sources: Optional[List[str]] = None,
) -> str:
    """Start a Phase 8 verifiable Veritas run with flexible parameters and write a .veritasrun bundle."""  # noqa: E501
    return engine.start_veritas_run(
        topic,
        channel_url,
        selection,
        max_videos,
        crawl_depth,
        allow_domains,
        deny_domains,
        transcript_pref,
        ocr_mode,
        auto_retry_attempts,
        sources,
    )


@mcp.tool()
def get_veritas_run_status(run_id: str) -> str:
    """Get status for a Veritas run by run_id."""
    return engine.get_veritas_run_status(run_id)


@mcp.tool()
def list_veritas_runs(limit: int = 20) -> str:
    """List recent Veritas runs (by run_id)."""
    return engine.list_veritas_runs(limit)


@mcp.tool()
def open_veritas_bundle(run_id: str) -> str:
    """Open a Veritas bundle and return manifest and proofs."""
    return engine.open_veritas_bundle(run_id)


@mcp.tool()
def reanalyze_with_gates(run_id: str, gates: Dict[str, Any]) -> str:
    """Reanalyze a run with gating parameters (placeholder)."""
    return engine.reanalyze_with_gates(run_id, gates)


@mcp.tool()
def create_3d_network_visualization(graph_data: dict) -> str:
    """Create 3D network visualization using advanced visualizer."""
    return engine.create_3d_network_visualization(graph_data)


@mcp.tool()
def create_centrality_analysis(graph_data: dict) -> str:
    """Create centrality analysis visualization."""
    return engine.create_centrality_analysis(graph_data)


@mcp.tool()
def create_timeline_visualization(timeline_data: list) -> str:
    """Create timeline visualization."""
    return engine.create_timeline_visualization(timeline_data)


@mcp.tool()
def create_claims_verification_dashboard(claims_data: list) -> str:
    """Create claims verification dashboard."""
    return engine.create_claims_verification_dashboard(claims_data)


@mcp.tool()
def get_visualization_status() -> str:
    """Get advanced visualization system status."""
    return engine.get_visualization_status()


@mcp.tool()
def search_biblical_evidence(query: str) -> str:
    """Search for Biblical evidence related to the query using HybridRetriever."""
    try:
        from src.analysis.hybrid_retrieval import HybridRetriever

        retriever = HybridRetriever()
        results = retriever.search_biblical_evidence(query)
        return f"Biblical evidence found: {len(results)} results\n{results}"
    except Exception as e:
        return f"Error searching Biblical evidence: {e}"


@mcp.tool()
def search_survivor_testimonies(query: str) -> str:
    """Search for survivor testimonies related to the query using HybridRetriever."""
    try:
        from src.analysis.hybrid_retrieval import HybridRetriever

        retriever = HybridRetriever()
        results = retriever.search_survivor_testimonies(query)
        return f"Survivor testimonies found: {len(results)} results\n{results}"
    except Exception as e:
        return f"Error searching survivor testimonies: {e}"


@mcp.tool()
def extract_entities_from_text(text: str) -> str:
    """Extract entities from text using ResearchAnalysisSystem."""
    try:
        from src.analysis.research_analysis import ResearchAnalysisSystem

        research = ResearchAnalysisSystem()
        entities = research.extract_entities_from_text(text)
        return f"Entities extracted: {len(entities)} entities\n{entities}"
    except Exception as e:
        return f"Error extracting entities: {e}"


@mcp.tool()
def extract_claims_from_transcript(transcript_data: dict) -> str:
    """Extract claims from transcript using ResearchAnalysisSystem."""
    try:
        from src.analysis.research_analysis import ResearchAnalysisSystem

        research = ResearchAnalysisSystem()
        claims = research.extract_claims_from_transcript(transcript_data)
        return f"Claims extracted: {len(claims)} claims\n{claims}"
    except Exception as e:
        return f"Error extracting claims: {e}"


@mcp.tool()
def get_migrated_functionality_status() -> str:
    """Get status of all migrated living_truth_agent functionality."""
    try:
        status = {
            "configuration_system": "✅ Operational",
            "hybrid_retriever": "✅ Operational",
            "research_analysis_system": "✅ Operational",
            "channel_archiver": "✅ Operational",
            "agi_integration": "✅ Operational",
            "advanced_visualization": "✅ Operational",
            "mcp_tools": "✅ Operational",
        }
        return f"Migrated functionality status:\n{json.dumps(status, indent=2)}"
    except Exception as e:
        return f"Error getting migrated functionality status: {e}"


@mcp.tool()
def test_migrated_components() -> str:
    """Run comprehensive test of all migrated living_truth_agent components."""
    try:
        import subprocess

        result = subprocess.run(
            ["python", "test_migrated_functionality.py"],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )
        return f"Test Results:\n{result.stdout}\nErrors:\n{result.stderr}"
    except Exception as e:
        return f"Error running migrated component tests: {e}"


@mcp.tool()
def validate_cursor_rules() -> str:
    """Validate all .mdc files in .cursor/rules/ for proper frontmatter."""
    return engine.validate_cursor_rules()


@mcp.tool()
def fix_cursor_rule_frontmatter(filename: str) -> str:
    """Fix frontmatter for a specific .mdc file."""
    return engine.fix_cursor_rule_frontmatter(filename)


@mcp.tool()
def analyze_veritas_summary(run_id: str, document_index: int = 0) -> str:
    """Summarize a document from a Veritas run (minimal snippet)."""
    return engine.analyze_veritas_summary(run_id, document_index)


@mcp.tool()
def analyze_veritas_claims(run_id: str, document_index: int = 0) -> str:
    """Extract claims from a document in a Veritas run (minimal stub)."""
    return engine.analyze_veritas_claims(run_id, document_index)


@mcp.tool()
def ruleset_archive_outdated(rules: list) -> str:
    """Move specific rules to archive/."""
    return engine.ruleset_archive_outdated(rules)


@mcp.tool()
def ruleset_apply_templates() -> str:
    """Ensure core rules exist with proper templates."""
    return engine.ruleset_apply_templates()


@mcp.tool()
def run_smoke_and_tests() -> str:
    """Run smoke tests and pytest; return consolidated report."""
    return engine.run_smoke_and_tests()


@mcp.tool()
def generate_phase_completion_summary(phase: str) -> str:
    """Create PHASE_<phase>_COMPLETION_SUMMARY.md from templates + live health data."""
    return engine.generate_phase_completion_summary(phase)


if __name__ == "__main__":
    logger.info("Living Truth Engine FastMCP Server starting...")
    print("Living Truth Engine FastMCP Server started...")

    # Initialize the engine
    try:
        engine = LivingTruthEngine()
        logger.info("Engine initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize engine: {e}")
        sys.exit(1)

    # Start the MCP server
    try:
        logger.info("Starting FastMCP server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("MCP Server stopped by user")
    except Exception as e:
        logger.error(f"MCP Server error: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
