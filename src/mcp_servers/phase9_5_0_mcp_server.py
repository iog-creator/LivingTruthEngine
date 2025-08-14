"""
Phase 9.5.0 MCP Server

Provides MCP tools for testing real adapters and running smoke tests
for the Phase 9.5.0 - Real Adapters implementation.
"""

import logging
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path

from .phase9_mcp_server import Phase9MCPServer
from ..adapters import YouTubeAdapter, WebAdapter, PDFAdapter
from ..runners.enhanced_multisource_runner import EnhancedMultiSourceRunner

logger = logging.getLogger(__name__)

class Phase95MCPServer(Phase9MCPServer):
    """Phase 9.5.0 MCP Server with adapter testing capabilities."""
    
    def __init__(self):
        super().__init__()
        
        # Initialize adapters for testing
        self.config = self._load_adapter_config()
        self.adapters = {
            "youtube": YouTubeAdapter(self.config),
            "web": WebAdapter(self.config),
            "pdf": PDFAdapter(self.config)
        }
        
        # Initialize enhanced runner
        self.enhanced_runner = EnhancedMultiSourceRunner()
    
    def _load_adapter_config(self) -> Dict[str, Any]:
        """Load configuration for adapters."""
        return {
            # Base configuration
            "deduplication_enabled": True,
            "persist_transcript_mode": True,
            
            # YouTube configuration
            "youtube_default_limit": 3,  # Reduced for testing
            "youtube_default_sort": "oldest",
            "youtube_max_depth": 2,
            "transcript_timeout": 30,
            
            # Web configuration
            "web_default_max_depth": 1,
            "web_default_js_render": False,
            "web_request_timeout": 15,
            "web_max_pages_per_run": 10,
            "allowed_domains": ["youtube.com", "youtu.be", "example.com"],
            
            # PDF configuration
            "pdf_default_ocr_required": False,  # Disabled for testing
            "pdf_ocr_auto_retry": True,
            "pdf_max_pages_per_pdf": 10,
            "pdf_extraction_timeout": 30,
        }
    
    async def test_youtube_adapter(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test YouTube adapter with sample parameters."""
        try:
            test_params = {
                "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                "limit": 2,
                "sort": "oldest",
                "transcript_mode": "autosubs",
                **params
            }
            
            documents = await self.adapters["youtube"].process_source(test_params)
            
            return {
                "status": "ok",
                "data": {
                    "adapter": "youtube",
                    "documents_count": len(documents),
                    "documents": [
                        {
                            "id": doc.id,
                            "title": doc.title,
                            "url": doc.url,
                            "transcript_mode": doc.transcript_mode,
                            "sha256": doc.sha256[:8] + "...",
                            "metadata": doc.metadata
                        }
                        for doc in documents
                    ],
                    "deduplication_enabled": self.config["deduplication_enabled"],
                    "test_params": test_params
                }
            }
        except Exception as e:
            logger.error(f"YouTube adapter test failed: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"YouTube adapter test failed: {e}"
                }
            }
    
    async def test_web_adapter(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test web adapter with sample parameters."""
        try:
            test_params = {
                "urls": ["https://example.com"],
                "max_depth": 1,
                "js_render": False,
                **params
            }
            
            documents = await self.adapters["web"].process_source(test_params)
            
            return {
                "status": "ok",
                "data": {
                    "adapter": "web",
                    "documents_count": len(documents),
                    "documents": [
                        {
                            "id": doc.id,
                            "title": doc.title,
                            "url": doc.url,
                            "sha256": doc.sha256[:8] + "...",
                            "metadata": doc.metadata
                        }
                        for doc in documents
                    ],
                    "deduplication_enabled": self.config["deduplication_enabled"],
                    "test_params": test_params
                }
            }
        except Exception as e:
            logger.error(f"Web adapter test failed: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"Web adapter test failed: {e}"
                }
            }
    
    async def test_pdf_adapter(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test PDF adapter with sample parameters."""
        try:
            test_params = {
                "urls": ["https://example.com/sample.pdf"],
                "ocr_required": False,
                "auto_retry": True,
                **params
            }
            
            documents = await self.adapters["pdf"].process_source(test_params)
            
            return {
                "status": "ok",
                "data": {
                    "adapter": "pdf",
                    "documents_count": len(documents),
                    "documents": [
                        {
                            "id": doc.id,
                            "title": doc.title,
                            "url": doc.url,
                            "sha256": doc.sha256[:8] + "...",
                            "metadata": doc.metadata
                        }
                        for doc in documents
                    ],
                    "deduplication_enabled": self.config["deduplication_enabled"],
                    "test_params": test_params
                }
            }
        except Exception as e:
            logger.error(f"PDF adapter test failed: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"PDF adapter test failed: {e}"
                }
            }
    
    async def test_multi_source_run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test multi-source run with enhanced runner."""
        try:
            # Create test sources
            sources = [
                {
                    "type": "youtube",
                    "channel_url": "https://www.youtube.com/@imaginationpodcastofficial",
                    "limit": 1,
                    "transcript_mode": "autosubs"
                },
                {
                    "type": "web",
                    "urls": ["https://example.com"],
                    "max_depth": 1
                },
                {
                    "type": "pdf",
                    "urls": ["https://example.com/sample.pdf"],
                    "ocr_required": False
                }
            ]
            
            # Start job
            job_id = await self.enhanced_runner.start_job(
                sources=sources,
                job_label="Phase 9.5.0 Test Run"
            )
            
            # Wait for completion (with timeout)
            timeout = 30  # seconds
            start_time = asyncio.get_event_loop().time()
            
            while True:
                job_status = await self.enhanced_runner.get_job_status(job_id)
                if job_status["status"] in ["completed", "failed"]:
                    break
                
                if asyncio.get_event_loop().time() - start_time > timeout:
                    return {
                        "status": "error",
                        "error": {
                            "code": 408,
                            "message": "Multi-source run test timed out"
                        }
                    }
                
                await asyncio.sleep(1)
            
            return {
                "status": "ok",
                "data": {
                    "job_id": job_id,
                    "job_status": job_status,
                    "sources_count": len(sources),
                    "test_params": params
                }
            }
        except Exception as e:
            logger.error(f"Multi-source run test failed: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"Multi-source run test failed: {e}"
                }
            }
    
    async def run_phase_9_5_0_smoke(self) -> Dict[str, Any]:
        """Run Phase 9.5.0 smoke test."""
        try:
            logger.info("Starting Phase 9.5.0 smoke test")
            
            results = {
                "phase": "9.5.0",
                "tests": {},
                "summary": {
                    "total_tests": 4,
                    "passed": 0,
                    "failed": 0
                }
            }
            
            # Test YouTube adapter
            youtube_result = await self.test_youtube_adapter({})
            results["tests"]["youtube_adapter"] = youtube_result
            if youtube_result["status"] == "ok":
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
            
            # Test web adapter
            web_result = await self.test_web_adapter({})
            results["tests"]["web_adapter"] = web_result
            if web_result["status"] == "ok":
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
            
            # Test PDF adapter
            pdf_result = await self.test_pdf_adapter({})
            results["tests"]["pdf_adapter"] = pdf_result
            if pdf_result["status"] == "ok":
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
            
            # Test multi-source run
            multi_result = await self.test_multi_source_run({})
            results["tests"]["multi_source_run"] = multi_result
            if multi_result["status"] == "ok":
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
            
            # Determine overall status
            if results["summary"]["failed"] == 0:
                results["status"] = "ok"
                results["message"] = "All Phase 9.5.0 tests passed"
            else:
                results["status"] = "error"
                results["message"] = f"{results['summary']['failed']} tests failed"
            
            logger.info(f"Phase 9.5.0 smoke test completed: {results['summary']['passed']}/{results['summary']['total_tests']} passed")
            
            return results
            
        except Exception as e:
            logger.error(f"Phase 9.5.0 smoke test failed: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"Phase 9.5.0 smoke test failed: {e}"
                }
            }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available MCP tools for Phase 9.5.0."""
        base_tools = super().get_tools()
        
        phase9_5_0_tools = [
            {
                "name": "test_youtube_adapter",
                "description": "Test YouTube adapter with sample parameters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "channel_url": {"type": "string", "description": "YouTube channel URL"},
                        "limit": {"type": "integer", "description": "Number of videos to fetch"},
                        "transcript_mode": {"type": "string", "enum": ["autosubs", "official", "whisper_local"]}
                    }
                }
            },
            {
                "name": "test_web_adapter",
                "description": "Test web adapter with sample parameters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "urls": {"type": "array", "items": {"type": "string"}, "description": "URLs to fetch"},
                        "max_depth": {"type": "integer", "description": "Crawl depth"},
                        "js_render": {"type": "boolean", "description": "Enable JavaScript rendering"}
                    }
                }
            },
            {
                "name": "test_pdf_adapter",
                "description": "Test PDF adapter with sample parameters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "urls": {"type": "array", "items": {"type": "string"}, "description": "PDF URLs to extract"},
                        "ocr_required": {"type": "boolean", "description": "Require OCR processing"},
                        "auto_retry": {"type": "boolean", "description": "Auto-retry failed extractions"}
                    }
                }
            },
            {
                "name": "test_multi_source_run",
                "description": "Test multi-source run with enhanced runner",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "job_label": {"type": "string", "description": "Label for the test job"}
                    }
                }
            },
            {
                "name": "run_phase_9_5_0_smoke",
                "description": "Run complete Phase 9.5.0 smoke test suite",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        return base_tools + phase9_5_0_tools
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute Phase 9.5.0 MCP tools."""
        try:
            if tool_name == "test_youtube_adapter":
                return await self.test_youtube_adapter(params)
            elif tool_name == "test_web_adapter":
                return await self.test_web_adapter(params)
            elif tool_name == "test_pdf_adapter":
                return await self.test_pdf_adapter(params)
            elif tool_name == "test_multi_source_run":
                return await self.test_multi_source_run(params)
            elif tool_name == "run_phase_9_5_0_smoke":
                return await self.run_phase_9_5_0_smoke()
            else:
                # Fall back to parent class tools
                return await super().execute_tool(tool_name, params)
                
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {
                "status": "error",
                "error": {
                    "code": 500,
                    "message": f"Tool execution failed: {e}"
                }
            }
