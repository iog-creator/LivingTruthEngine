"""
Multi-source ingestion runner supporting YouTube, Web, and PDF sources.
Handles parallel processing with health gates and source tagging.
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
import os

from ..common.model_registry import ModelRegistry
from ..common.gpu_scheduler import gpu_scheduler
from ..storage.pgvector_store import PgVectorStore

logger = logging.getLogger(__name__)


@dataclass
class SourceConfig:
    """Configuration for a single source."""

    source_type: str  # 'youtube', 'web', 'pdf'
    params: Dict[str, Any]
    health_gate: str  # MCP tool name for health check


@dataclass
class MultiSourceJob:
    """Multi-source ingestion job."""

    job_id: str
    sources: List[SourceConfig]
    created_at: datetime
    status: str = "pending"  # pending, running, completed, failed
    results: Dict[str, Any] = None
    error: str = None
    job_label: str = None
    completed_at: datetime = None


class MultiSourceRunner:
    """Handles multi-source ingestion with health gates and parallel processing."""

    def __init__(self):
        self.model_registry = ModelRegistry()
        self.active_jobs: Dict[str, MultiSourceJob] = {}

        # Initialize pgvector store
        dsn = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:pass@postgres:5432/living_truth_engine",
        )
        # For now, initialize without embedder (mock mode)
        self.pgvector_store = PgVectorStore(dsn, embedder=None)

        # Source type to health gate mapping
        self.source_health_gates = {
            "youtube": "veritas_tools",
            "web": "veritas_tools",
            "pdf": "veritas_tools",
        }

        # Mock source adapters (to be replaced with actual implementations)
        self.source_adapters = {
            "youtube": self._mock_youtube_adapter,
            "web": self._mock_web_adapter,
            "pdf": self._mock_pdf_adapter,
        }

    async def check_health_gates(self, sources: List[str]) -> Dict[str, bool]:
        """
        Check health gates for all requested sources.

        Args:
            sources: List of source types to check

        Returns:
            Dict mapping source type to health status
        """
        health_results = {}

        for source_type in sources:
            if source_type not in self.source_health_gates:
                health_results[source_type] = False
                logger.error(f"Unknown source type: {source_type}")
                continue

            tool_name = self.source_health_gates[source_type]

            # Check health gate for the source
            try:
                health_results[source_type] = await self._check_health_gate(tool_name)
                logger.info(
                    f"Health gate for {source_type} ({tool_name}): {health_results[source_type]}"  # noqa: E501
                )
            except Exception as e:
                logger.error(f"Health gate failed for {source_type}: {e}")
                health_results[source_type] = False

        return health_results

    async def start_job(self, sources: List[str], params: Dict[str, Any] = None) -> str:
        """
        Start a multi-source ingestion job.

        Args:
            sources: List of source types ('youtube', 'web', 'pdf')
            params: Common parameters for all sources

        Returns:
            Job ID

        Raises:
            ValueError: If health gates fail
        """
        # Check health gates first
        health_results = await self.check_health_gates(sources)
        failed_sources = [s for s, healthy in health_results.items() if not healthy]

        if failed_sources:
            error_msg = f"Health gates failed for sources: {failed_sources}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Create job
        job_id = str(uuid.uuid4())
        source_configs = []

        for source_type in sources:
            source_configs.append(
                SourceConfig(
                    source_type=source_type,
                    params=params or {},
                    health_gate=self.source_health_gates[source_type],
                )
            )

        job = MultiSourceJob(
            job_id=job_id,
            sources=source_configs,
            created_at=datetime.utcnow(),
            job_label=params.get("label") if params else None,
        )

        self.active_jobs[job_id] = job

        # Start processing in background
        asyncio.create_task(self._process_job(job))

        logger.info(f"Started multi-source job {job_id} with sources: {sources}")
        return job_id

    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a job."""
        if job_id not in self.active_jobs:
            return None

        job = self.active_jobs[job_id]
        return {
            "job_id": job.job_id,
            "status": job.status,
            "sources": [s.source_type for s in job.sources],
            "created_at": job.created_at.isoformat(),
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "job_label": job.job_label,
            "results": job.results,
            "error": job.error,
        }

    async def _process_job(self, job: MultiSourceJob):
        """Process a multi-source job."""
        try:
            job.status = "running"
            logger.info(f"Processing job {job.job_id}")

            # Process sources in parallel
            tasks = []
            for source_config in job.sources:
                task = self._process_source(source_config)
                tasks.append(task)

            # Wait for all sources to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Aggregate results
            aggregated_results = {
                "total_documents": 0,
                "sources": {},
                "gpu_allocation": gpu_scheduler.get_gpu_status(),
            }

            for i, result in enumerate(results):
                source_type = job.sources[i].source_type

                if isinstance(result, Exception):
                    aggregated_results["sources"][source_type] = {
                        "status": "failed",
                        "error": str(result),
                        "documents": 0,
                    }
                    logger.error(f"Source {source_type} failed: {result}")
                else:
                    aggregated_results["sources"][source_type] = {
                        "status": "completed",
                        "documents": len(result),
                        "documents_with_source_type": [
                            {**doc, "source_type": source_type} for doc in result
                        ],
                    }
                    aggregated_results["total_documents"] += len(result)
                    logger.info(
                        f"Source {source_type} completed with {len(result)} documents"
                    )

            # Store documents in pgvector
            all_documents = []
            for source_type, source_result in aggregated_results["sources"].items():
                if source_result["status"] == "completed":
                    all_documents.extend(source_result["documents_with_source_type"])

            if all_documents:
                try:
                    self.pgvector_store.upsert_docs(job.job_id, all_documents)
                    logger.info(
                        f"Stored {len(all_documents)} documents in pgvector for job {job.job_id}"  # noqa: E501
                    )
                except Exception as e:
                    logger.error(f"Failed to store documents in pgvector: {e}")
                    # Don't fail the job, just log the error

            job.results = aggregated_results
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            logger.info(
                f"Job {job.job_id} completed with {aggregated_results['total_documents']} total documents"  # noqa: E501
            )

        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            logger.error(f"Job {job.job_id} failed: {e}")

    async def _process_source(
        self, source_config: SourceConfig
    ) -> List[Dict[str, Any]]:
        """Process a single source."""
        source_type = source_config.source_type

        if source_type not in self.source_adapters:
            raise ValueError(f"No adapter available for source type: {source_type}")

        adapter = self.source_adapters[source_type]

        # Log device allocation
        device = gpu_scheduler.get_optimal_device(
            "embedding"
        )  # Most sources need embeddings
        gpu_scheduler.log_device_allocation(
            "embedding", device, f"for {source_type} processing"
        )

        # Process with adapter
        documents = await adapter(source_config.params)

        # Add source metadata
        for doc in documents:
            doc["source_type"] = source_type
            doc["processed_at"] = datetime.utcnow().isoformat()

        return documents

    # Mock adapters (replace with actual implementations)
    async def _mock_youtube_adapter(
        self, params: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Mock YouTube adapter."""
        await asyncio.sleep(1)  # Simulate processing time
        return [
            {
                "id": f"yt_{uuid.uuid4().hex[:8]}",
                "title": "Mock YouTube Video",
                "content": "This is mock content from YouTube",
                "url": "https://youtube.com/watch?v=mock",
                "metadata": {"channel": "Mock Channel", "duration": "10:00"},
            }
        ]

    async def _mock_web_adapter(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mock Web adapter."""
        await asyncio.sleep(1)  # Simulate processing time
        return [
            {
                "id": f"web_{uuid.uuid4().hex[:8]}",
                "title": "Mock Web Page",
                "content": "This is mock content from web",
                "url": "https://example.com/mock",
                "metadata": {"domain": "example.com", "language": "en"},
            }
        ]

    async def _mock_pdf_adapter(self, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Mock PDF adapter."""
        await asyncio.sleep(1)  # Simulate processing time
        return [
            {
                "id": f"pdf_{uuid.uuid4().hex[:8]}",
                "title": "Mock PDF Document",
                "content": "This is mock content from PDF",
                "url": "file://mock.pdf",
                "metadata": {"pages": 5, "author": "Mock Author"},
            }
        ]

    async def _check_health_gate(self, gate_name: str) -> bool:
        """Check health gate for specific service."""
        try:
            import httpx

            async with httpx.AsyncClient(timeout=5) as client:
                # Check the specific health gate
                if gate_name == "pgvector":
                    # Check if pgvector is available via health endpoint
                    response = await client.get("http://localhost:8050/api/health/full")
                    if response.status_code == 200:
                        data = response.json()
                        return (
                            data.get("data", {})
                            .get("pgvector", {})
                            .get("enabled", False)
                        )
                elif gate_name == "rulego":
                    # Check rulego health
                    response = await client.get("http://localhost:8050/api/health/full")
                    if response.status_code == 200:
                        data = response.json()
                        return (
                            data.get("data", {}).get("rulego", {}).get("status") == "ok"
                        )
                elif gate_name == "lmstudio":
                    # Check LM Studio health
                    response = await client.get("http://localhost:8050/api/health/full")
                    if response.status_code == 200:
                        data = response.json()
                        return (
                            data.get("data", {})
                            .get("gates", {})
                            .get("lm_studio", False)
                        )
                else:
                    # For other gates, check the health endpoint
                    response = await client.get("http://localhost:8050/api/health/full")
                    if response.status_code == 200:
                        data = response.json()
                        gates = data.get("data", {}).get("gates", {})
                        return gates.get(gate_name, False)
                return False
        except Exception as e:
            logger.error(f"Health gate check failed for {gate_name}: {e}")
            return False


# Global runner instance
multi_source_runner = MultiSourceRunner()
