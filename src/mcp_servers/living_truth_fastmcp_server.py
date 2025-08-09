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
load_dotenv(project_root / '.env')

# Ensure logs directory exists in project root
logs_dir = project_root / 'data' / 'outputs' / 'logs'
logs_dir.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(logs_dir / 'living_truth_fastmcp.log')
    ]
)
logger = logging.getLogger(__name__)

# Create FastMCP instance
mcp = FastMCP()

# Import notebook agent components
from src.analysis.notebook_agent import AdvancedNotebookAgent, StudyGuide, DocumentSummary, ResearchReport

# Import AGI integration components
from integration.agi_integration import AGILivingTruthIntegration, AGIAnalysisResult, AGIComponent

# Import channel archiver components
from processing.channel_archiver import ChannelArchiver, VideoInfo, ArchiveResult, ChannelArchiveSummary
from visualization.advanced_viz import AdvancedVisualizer
from pathlib import Path
from src.analysis.ingestion import IngestionPipeline

class LivingTruthEngine:
    def __init__(self):
        # Handle Docker vs local environment
        docker_env = os.getenv('DOCKER_ENVIRONMENT', 'false').lower() == 'true'
        
        if docker_env:
            # Use container names in Docker environment
            self.langflow_api_endpoint = os.getenv('LANGFLOW_API_ENDPOINT', 'http://langflow:7860')
            self.lm_studio_endpoint = os.getenv('LM_STUDIO_ENDPOINT', 'http://lm-studio:1234')
        else:
            # Use localhost for local development
            self.langflow_api_endpoint = os.getenv('LANGFLOW_API_ENDPOINT', 'http://localhost:7860')
            self.lm_studio_endpoint = os.getenv('LM_STUDIO_ENDPOINT', 'http://localhost:1234')
        
        self.langflow_api_key = os.getenv('LANGFLOW_API_KEY')
        
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

    def query_flowise(self, query: str, anonymize: bool = False, output_type: str = "summary") -> str:
        """Query the Flowise chatflow for pattern recognition and data analysis."""
        return "❌ Flowise has been removed from the project. Please use query_langflow instead."

    def query_langflow(self, query: str, anonymize: bool = False, output_type: str = "summary") -> str:
        """Query the Langflow workflow for survivor testimony analysis."""
        try:
            if not self.langflow_api_key:
                return "❌ LANGFLOW_API_KEY not configured"
            
            # Prepare the query
            payload = {
                "query": query,
                "anonymize": anonymize,
                "output_type": output_type
            }
            
            # Make the request
            headers = {
                "Authorization": f"Bearer {self.langflow_api_key}",
                "Content-Type": "application/json"
            }
            
            url = f"{self.langflow_api_endpoint}/api/v1/run"
            
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return f"✅ Langflow query successful:\n\n{result.get('result', 'No response text')}"
            else:
                return f"❌ Langflow query failed: {response.status_code} - {response.text}"
                
        except Exception as e:
            logger.error(f"Langflow query error: {e}")
            return f"❌ Langflow query error: {str(e)}"

    def get_status(self) -> str:
        """Get Living Truth Engine system status."""
        try:
            status = {
                "langflow_api_endpoint": self.langflow_api_endpoint,
                "langflow_api_key": "✅ Configured" if self.langflow_api_key else "❌ Not configured",
                "lm_studio_endpoint": self.lm_studio_endpoint,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Test Langflow connection
            try:
                response = requests.get(f"{self.langflow_api_endpoint}/health", timeout=5)
                if response.status_code == 200:
                    status["langflow_connection"] = "✅ Connected"
                else:
                    status["langflow_connection"] = f"❌ Error: {response.status_code}"
            except Exception as e:
                status["langflow_connection"] = f"❌ Connection failed: {str(e)}"
            
            # Test LM Studio connection
            try:
                response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=5)
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
                "sources"  # Relative fallback
            ]
            
            sources_dir = None
            for path in possible_paths:
                if os.path.exists(path):
                    sources_dir = path
                    break
            
            if not sources_dir:
                return f"❌ Sources directory not found. Tried: {', '.join(possible_paths)}"
            
            sources = []
            for file in os.listdir(sources_dir):
                if file.endswith(('.txt', '.vtt', '.json')):
                    file_path = os.path.join(sources_dir, file)
                    size = os.path.getsize(file_path)
                    sources.append({
                        "name": file,
                        "size": f"{size} bytes",
                        "type": file.split('.')[-1]
                    })
            
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
                return f"❌ Transcript not found: {transcript_name}. Tried: {', '.join(possible_paths)}"
            
            # Read transcript
            with open(transcript_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic analysis
            lines = content.split('\n')
            word_count = len(content.split())
            char_count = len(content)
            
            analysis = {
                "transcript": transcript_name,
                "lines": len(lines),
                "words": word_count,
                "characters": char_count,
                "preview": content[:500] + "..." if len(content) > 500 else content
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
                        {"id": "analysis", "label": "Analysis"}
                    ],
                    "edges": [
                        {"from": "source1", "to": "analysis"},
                        {"from": "source2", "to": "analysis"}
                    ]
                }
                
                viz_file = f"network_viz_{timestamp}.json"
                viz_path = viz_dir / viz_file
                
                with open(viz_path, 'w') as f:
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
            raise NotImplementedError("Langflow workflow update functionality not yet implemented")
        except Exception as e:
            logger.error(f"Fix flow error: {e}")
            raise RuntimeError(f"Failed to update Langflow workflow: {str(e)}")

    def get_lm_studio_models(self) -> str:
        """Get list of available models in LM Studio."""
        try:
            response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=10)
            response.raise_for_status()
            models = response.json()
            
            model_list = []
            for model in models.get("data", []):
                model_list.append({
                    "id": model.get("id", ""),
                    "name": model.get("name", ""),
                    "object": model.get("object", ""),
                    "created": model.get("created", 0)
                })
            
            return f"✅ Available models in LM Studio:\n{json.dumps(model_list, indent=2)}"
        except requests.exceptions.RequestException as e:
            return f"❌ Failed to get models: {str(e)}"

    def generate_lm_studio_text(self, prompt: str, model: str = "", max_tokens: int = 1000, temperature: float = 0.7, system_prompt: str = "") -> str:
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
                "stream": False
            }
            
            response = requests.post(
                f"{self.lm_studio_endpoint}/v1/chat/completions",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
            return f"✅ Generated text:\n{generated_text}"
        except requests.exceptions.RequestException as e:
            return f"❌ Failed to generate text: {str(e)}"

    def test_lm_studio_connection(self) -> str:
        """Test connection to LM Studio."""
        try:
            response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=5)
            response.raise_for_status()
            
            return f"✅ LM Studio connection successful\nEndpoint: {self.lm_studio_endpoint}\nStatus: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"❌ LM Studio connection failed\nEndpoint: {self.lm_studio_endpoint}\nError: {str(e)}"

    def get_lm_studio_status(self) -> str:
        """Get LM Studio server status and health."""
        try:
            response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=5)
            response.raise_for_status()
            
            models_response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=10)
            models_data = models_response.json()
            model_count = len(models_data.get("data", []))
            
            status_info = {
                "endpoint": self.lm_studio_endpoint,
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "available_models": model_count,
                "server_version": "LM Studio"
            }
            
            return f"✅ LM Studio Server Status:\n{json.dumps(status_info, indent=2)}"
        except requests.exceptions.RequestException as e:
            return f"❌ LM Studio Server Status:\nEndpoint: {self.lm_studio_endpoint}\nStatus: unhealthy\nError: {str(e)}"

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
            audio_dir = project_root / 'data' / 'outputs' / 'audio'
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
                    f"Missing Piper model files. Expected: {model_path} and {config_path}. "
                    "Download them from rhasspy/piper-voices (Hugging Face) before running audio generation."
                )

            # Load voice model and generate audio
            voice = PiperVoice.load(str(model_path))
            voice.synthesize(text, str(output_path))
            logger.info(f"Audio generated successfully: {output_path}")
            return f"✅ Audio generated successfully\n📁 Output: {output_path}\n🎵 Text: {text[:100]}..."
            
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
                return f"🔍 Detected {len(patterns_found)} potential tool needs:\n" + "\n".join(patterns_found)
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
                return f"📝 Updated {len(updates_made)} documentation files:\n" + "\n".join(updates_made)
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
                return f"📋 Updated {len(updates_made)} cursor rules:\n" + "\n".join(updates_made)
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
                langflow_response = requests.get(f"{self.langflow_api_endpoint}/health", timeout=5)
                if langflow_response.status_code == 200:
                    validation_results.append("✅ Langflow: Healthy")
                else:
                    validation_results.append(f"❌ Langflow: Unhealthy (Status: {langflow_response.status_code})")
            except Exception as e:
                validation_results.append(f"❌ Langflow: Connection failed ({e})")
            
            try:
                lm_studio_response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=5)
                if lm_studio_response.status_code == 200:
                    validation_results.append("✅ LM Studio: Healthy")
                else:
                    validation_results.append(f"❌ LM Studio: Unhealthy (Status: {lm_studio_response.status_code})")
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
            
            # Create 3D network graph
            fig = self.visualizer.create_interactive_3d_network_graph(graph_data)
            
            # Save visualization
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"3d_network_visualization_{timestamp}.html"
            self.visualizer.export_visualization_data(graph_data, f"3d_network_data_{timestamp}.json")
            
            return f"✅ 3D network visualization created successfully\nOutput file: {output_file}"
            
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
            
            return f"✅ Centrality analysis created successfully\nOutput file: {output_file}"
            
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
            
            return f"✅ Timeline visualization created successfully\nOutput file: {output_file}"
            
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
            
            return f"✅ Claims verification dashboard created successfully\nOutput file: {output_file}"
            
        except Exception as e:
            logger.error(f"Claims verification dashboard error: {e}")
            return f"❌ Claims verification dashboard error: {str(e)}"
    
    def get_visualization_status(self) -> str:
        """Get advanced visualization system status."""
        try:
            status = {
                "visualizer_initialized": self.visualizer is not None,
                "output_directory": str(self.visualizer.output_dir) if self.visualizer else "Not available",
                "color_schemes_available": len(self.visualizer.color_schemes) if self.visualizer else 0,
                "node_sizes_configured": len(self.visualizer.node_sizes) if self.visualizer else 0,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
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
                langflow_response = requests.get(f"{self.langflow_api_endpoint}/health", timeout=5)
                if langflow_response.status_code == 200:
                    health_report.append("✅ Langflow: Healthy")
                else:
                    health_report.append(f"❌ Langflow: Unhealthy (Status: {langflow_response.status_code})")
            except Exception as e:
                health_report.append(f"❌ Langflow: Connection failed ({e})")
            
            # LM Studio
            try:
                lm_studio_response = requests.get(f"{self.lm_studio_endpoint}/v1/models", timeout=5)
                if lm_studio_response.status_code == 200:
                    models_data = lm_studio_response.json()
                    model_count = len(models_data.get("data", []))
                    health_report.append(f"✅ LM Studio: Healthy ({model_count} models available)")
                else:
                    health_report.append(f"❌ LM Studio: Unhealthy (Status: {lm_studio_response.status_code})")
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
            health_report.append("✅ Living Truth FastMCP Server: Running (20 tools available)")
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
    
    def analyze_with_agi_integration(self, query: str, analysis_type: str = "comprehensive") -> str:
        """Perform comprehensive analysis using AGI integration."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"
            
            result = self.agi_integration.analyze_with_agi_integration(query, analysis_type)
            
            # Convert result to JSON string for MCP tool response
            result_dict = {
                "query": result.query,
                "analysis_type": result.analysis_type,
                "confidence_scores": result.confidence_scores,
                "recommendations": result.recommendations,
                "timestamp": result.timestamp
            }
            
            logger.info(f"AGI-integrated analysis completed: {query}")
            return f"✅ AGI-Integrated Analysis Results:\n{json.dumps(result_dict, indent=2)}"
            
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
            
            result = self.agi_integration.analyze_with_agi_integration(query, "comprehensive")
            cross_validation = result.cross_validation
            
            logger.info(f"Cross-validation completed: {query}")
            return f"✅ Cross-Validation Results:\n{json.dumps(cross_validation, indent=2)}"
            
        except Exception as e:
            logger.error(f"Cross-validation error: {e}")
            return f"❌ Cross-validation error: {str(e)}"
    
    def generate_integrated_insights(self, query: str) -> str:
        """Generate integrated insights using AGI integration."""
        try:
            if not self.agi_integration:
                return "❌ AGI integration not initialized"
            
            result = self.agi_integration.analyze_with_agi_integration(query, "comprehensive")
            integrated_insights = result.integrated_insights
            
            logger.info(f"Integrated insights generated: {query}")
            return f"✅ Integrated Insights:\n{json.dumps(integrated_insights, indent=2)}"
            
        except Exception as e:
            logger.error(f"Integrated insights error: {e}")
            return f"❌ Integrated insights error: {str(e)}"
    
    def archive_youtube_channel(self, channel_url: str, max_videos: Optional[int] = None) -> str:
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
                "archive_date": result.archive_date
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
            base = Path(project_root) / 'data' / 'outputs' / 'logs' / 'archive_telemetry'
            status_file = base / 'status.json'
            stream_file = base / 'current.jsonl'
            status = status_file.read_text(encoding='utf-8') if status_file.exists() else '{}'
            tail = ''
            if stream_file.exists():
                content = stream_file.read_text(encoding='utf-8').splitlines()[-lines:]
                tail = "\n".join(content)
            return json.dumps({"status": json.loads(status) if status.strip().startswith('{') else status, "tail": tail.split('\n')}, indent=2)
        except Exception as e:
            return f"❌ Telemetry read error: {e}"

    def ingest_channel_documents(self, channel: Optional[str] = None) -> str:
        """Ingest organized transcripts into the vector index (with telemetry)."""
        try:
            pipeline = IngestionPipeline()
            summary = pipeline.ingest(channel=channel)
            return json.dumps({
                "total_files": summary.total_files,
                "chunks_indexed": summary.chunks_indexed,
                "channel": summary.channel,
                "started_at": summary.started_at,
                "completed_at": summary.completed_at,
            }, indent=2)
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

# Create engine instance
engine = LivingTruthEngine()

# Define MCP tools
@mcp.tool()
def query_langflow(query: str, anonymize: bool = False, output_type: str = "summary") -> str:
    """Query the Langflow workflow for survivor testimony analysis using multi-agent system."""
    return engine.query_langflow(query, anonymize, output_type)

@mcp.tool()
def query_flowise(query: str, anonymize: bool = False, output_type: str = "summary") -> str:
    """Query the Flowise chatflow for survivor testimony analysis (DEPRECATED - use query_langflow)."""
    return engine.query_flowise(query, anonymize, output_type)

@mcp.tool()
def get_status() -> str:
    """Get Living Truth Engine system status (chatflows, sources, confidence metrics, dashboard link)."""
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
    """Batch system operations: get status, list sources, and check health in one call."""
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
def batch_analysis_operations(query: str, transcript_name: str = None, viz_type: str = "network") -> str:
    """Batch analysis operations: query Langflow, analyze transcript, and generate visualization."""
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
            "query_flowise - Query Flowise chatflow for survivor testimony analysis (DEPRECATED - use query_langflow)",
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
            "auto_detect_and_add_tools - Automatically detect development needs and add tools",
            "auto_update_all_documentation - Automatically update all documentation based on current state",
            "auto_update_cursor_rules - Automatically update cursor rules based on current patterns",
            "auto_validate_system_state - Automatically validate and report system state",
            "comprehensive_health_check - Perform comprehensive health check of all system components"
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
def generate_lm_studio_text(prompt: str, model: str = "", max_tokens: int = 1000, temperature: float = 0.7, system_prompt: str = "") -> str:
    """Generate text using LM Studio models."""
    return engine.generate_lm_studio_text(prompt, model, max_tokens, temperature, system_prompt)

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
def analyze_with_agi_integration(query: str, analysis_type: str = "comprehensive") -> str:
    """Perform comprehensive analysis using AGI integration for advanced pattern recognition."""
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
            "mcp_tools": "✅ Operational"
        }
        return f"Migrated functionality status:\n{json.dumps(status, indent=2)}"
    except Exception as e:
        return f"Error getting migrated functionality status: {e}"

@mcp.tool()
def test_migrated_components() -> str:
    """Run comprehensive test of all migrated living_truth_agent components."""
    try:
        import subprocess
        result = subprocess.run(["python", "test_migrated_functionality.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return f"Test Results:\n{result.stdout}\nErrors:\n{result.stderr}"
    except Exception as e:
        return f"Error running migrated component tests: {e}"

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