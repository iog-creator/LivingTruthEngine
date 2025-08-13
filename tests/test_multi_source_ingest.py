"""
Tests for multi-source ingestion functionality (Phase 9_2).
Tests GPU/CPU-aware model scheduling, health gates, and parallel processing.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from src.ingestion_general.multi_source_runner import (
    MultiSourceRunner, 
    SourceConfig, 
    MultiSourceJob
)
from src.common.model_registry import ModelRegistry
from src.common.gpu_scheduler import GPUScheduler


class TestMultiSourceRunner:
    """Test multi-source ingestion runner functionality."""
    
    @pytest.fixture
    def runner(self):
        """Create a test runner instance."""
        return MultiSourceRunner()
    
    @pytest.fixture
    def mock_job(self):
        """Create a mock job for testing."""
        return MultiSourceJob(
            job_id="test-job-123",
            sources=[
                SourceConfig("youtube", {"limit": 1}, "mcp_youtube"),
                SourceConfig("web", {"limit": 1}, "mcp_webfetch")
            ],
            created_at=datetime.utcnow()
        )
    
    def test_runner_initialization(self, runner):
        """Test runner initializes correctly."""
        assert runner.model_registry is not None
        assert isinstance(runner.active_jobs, dict)
        assert len(runner.source_health_gates) == 3
        assert "youtube" in runner.source_health_gates
        assert "web" in runner.source_health_gates
        assert "pdf" in runner.source_health_gates
    
    def test_source_health_gates_mapping(self, runner):
        """Test source type to MCP tool mapping."""
        assert runner.source_health_gates["youtube"] == "mcp_youtube"
        assert runner.source_health_gates["web"] == "mcp_webfetch"
        assert runner.source_health_gates["pdf"] == "mcp_pdf"
    
    @pytest.mark.asyncio
    async def test_check_health_gates_success(self, runner):
        """Test health gate checking with successful results."""
        with patch.object(runner, '_mock_health_check', return_value=True):
            results = await runner.check_health_gates(["youtube", "web"])
            
            assert results["youtube"] is True
            assert results["web"] is True
    
    @pytest.mark.asyncio
    async def test_check_health_gates_failure(self, runner):
        """Test health gate checking with failed results."""
        with patch.object(runner, '_mock_health_check', return_value=False):
            results = await runner.check_health_gates(["youtube", "web"])
            
            assert results["youtube"] is False
            assert results["web"] is False
    
    @pytest.mark.asyncio
    async def test_check_health_gates_unknown_source(self, runner):
        """Test health gate checking with unknown source type."""
        results = await runner.check_health_gates(["unknown_source"])
        
        assert results["unknown_source"] is False
    
    @pytest.mark.asyncio
    async def test_start_job_success(self, runner):
        """Test successful job start."""
        with patch.object(runner, 'check_health_gates', return_value={"youtube": True}):
            job_id = await runner.start_job(["youtube"], {"limit": 1})
            
            assert job_id is not None
            assert job_id in runner.active_jobs
            assert runner.active_jobs[job_id].status == "pending"
    
    @pytest.mark.asyncio
    async def test_start_job_health_gate_failure(self, runner):
        """Test job start with health gate failure."""
        with patch.object(runner, 'check_health_gates', return_value={"youtube": False}):
            with pytest.raises(ValueError, match="Health gates failed for sources"):
                await runner.start_job(["youtube"], {"limit": 1})
    
    @pytest.mark.asyncio
    async def test_get_job_status_existing(self, runner, mock_job):
        """Test getting status of existing job."""
        runner.active_jobs[mock_job.job_id] = mock_job
        
        status = await runner.get_job_status(mock_job.job_id)
        
        assert status is not None
        assert status["job_id"] == mock_job.job_id
        assert status["status"] == mock_job.status
        assert status["sources"] == ["youtube", "web"]
    
    @pytest.mark.asyncio
    async def test_get_job_status_nonexistent(self, runner):
        """Test getting status of nonexistent job."""
        status = await runner.get_job_status("nonexistent-job")
        
        assert status is None
    
    @pytest.mark.asyncio
    async def test_process_source_youtube(self, runner):
        """Test processing YouTube source."""
        source_config = SourceConfig("youtube", {"limit": 1}, "mcp_youtube")
        
        # Mock the adapter in the source_adapters dictionary
        mock_adapter = AsyncMock(return_value=[{"id": "test"}])
        runner.source_adapters["youtube"] = mock_adapter
        
        documents = await runner._process_source(source_config)
        
        assert len(documents) == 1
        assert documents[0]["source_type"] == "youtube"
        assert "processed_at" in documents[0]
        mock_adapter.assert_called_once_with({"limit": 1})
    
    @pytest.mark.asyncio
    async def test_process_source_web(self, runner):
        """Test processing web source."""
        source_config = SourceConfig("web", {"limit": 1}, "mcp_webfetch")
        
        # Mock the adapter method directly
        runner._mock_web_adapter = AsyncMock(return_value=[{"id": "test"}])
        
        documents = await runner._process_source(source_config)
        
        assert len(documents) == 1
        assert documents[0]["source_type"] == "web"
        assert "processed_at" in documents[0]
        runner._mock_web_adapter.assert_called_once_with({"limit": 1})
    
    @pytest.mark.asyncio
    async def test_process_source_pdf(self, runner):
        """Test processing PDF source."""
        source_config = SourceConfig("pdf", {"limit": 1}, "mcp_pdf")
        
        # Mock the adapter method directly
        runner._mock_pdf_adapter = AsyncMock(return_value=[{"id": "test"}])
        
        documents = await runner._process_source(source_config)
        
        assert len(documents) == 1
        assert documents[0]["source_type"] == "pdf"
        assert "processed_at" in documents[0]
        runner._mock_pdf_adapter.assert_called_once_with({"limit": 1})
    
    @pytest.mark.asyncio
    async def test_process_source_unknown(self, runner):
        """Test processing unknown source type."""
        source_config = SourceConfig("unknown", {"limit": 1}, "mcp_unknown")
        
        with pytest.raises(ValueError, match="No adapter available for source type"):
            await runner._process_source(source_config)
    
    @pytest.mark.asyncio
    async def test_process_job_success(self, runner, mock_job):
        """Test successful job processing."""
        runner.active_jobs[mock_job.job_id] = mock_job
        
        with patch.object(runner, '_process_source') as mock_process:
            mock_process.return_value = [{"id": "test", "content": "test content"}]
            
            await runner._process_job(mock_job)
            
            assert mock_job.status == "completed"
            assert mock_job.results is not None
            assert mock_job.results["total_documents"] == 2
            assert "youtube" in mock_job.results["sources"]
            assert "web" in mock_job.results["sources"]
            assert mock_job.results["sources"]["youtube"]["status"] == "completed"
            assert mock_job.results["sources"]["web"]["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_process_job_failure(self, runner, mock_job):
        """Test job processing with failure."""
        runner.active_jobs[mock_job.job_id] = mock_job
        
        # Mock the process_source method to raise an exception
        runner._process_source = AsyncMock(side_effect=Exception("Processing failed"))
        
        await runner._process_job(mock_job)
        
        assert mock_job.status == "failed"
        assert mock_job.error == "Processing failed"
    
    @pytest.mark.asyncio
    async def test_mock_adapters(self, runner):
        """Test mock adapters return expected data."""
        # Test YouTube adapter
        youtube_docs = await runner._mock_youtube_adapter({"limit": 1})
        assert len(youtube_docs) == 1
        assert youtube_docs[0]["title"] == "Mock YouTube Video"
        assert "yt_" in youtube_docs[0]["id"]
        
        # Test web adapter
        web_docs = await runner._mock_web_adapter({"limit": 1})
        assert len(web_docs) == 1
        assert web_docs[0]["title"] == "Mock Web Page"
        assert "web_" in web_docs[0]["id"]
        
        # Test PDF adapter
        pdf_docs = await runner._mock_pdf_adapter({"limit": 1})
        assert len(pdf_docs) == 1
        assert pdf_docs[0]["title"] == "Mock PDF Document"
        assert "pdf_" in pdf_docs[0]["id"]


class TestModelRegistry:
    """Test model registry with device allocation."""
    
    @pytest.fixture
    def registry(self):
        """Create a test registry instance."""
        return ModelRegistry()
    
    def test_device_resolution_cuda_if_available(self, registry):
        """Test device resolution for cuda_if_available preference."""
        # Reset the cached GPU availability
        registry._gpu_available = True
        device = registry._resolve_device("cuda_if_available")
        assert device == "cuda"
        
        registry._gpu_available = False
        device = registry._resolve_device("cuda_if_available")
        assert device == "cpu"
    
    def test_device_resolution_cuda(self, registry):
        """Test device resolution for cuda preference."""
        # Reset the cached GPU availability
        registry._gpu_available = True
        device = registry._resolve_device("cuda")
        assert device == "cuda"
        
        registry._gpu_available = False
        device = registry._resolve_device("cuda")
        assert device == "cpu"
    
    def test_device_resolution_cuda_preferred_cpu_fallback(self, registry):
        """Test device resolution for cuda_preferred_cpu_fallback preference."""
        # Test with no GPU available
        registry._gpu_available = False
        device = registry._resolve_device("cuda_preferred_cpu_fallback")
        assert device == "cpu"
        
        # Test with GPU available and low memory usage
        registry._gpu_available = True
        with patch('torch.cuda.memory_allocated', return_value=1000000000):
            with patch('torch.cuda.get_device_properties') as mock_props:
                mock_props.return_value.total_memory = 2000000000  # 2GB
                device = registry._resolve_device("cuda_preferred_cpu_fallback")
                assert device == "cuda"
        
        # Test with GPU available and high memory usage
        with patch('torch.cuda.memory_allocated', return_value=1800000000):
            with patch('torch.cuda.get_device_properties') as mock_props:
                mock_props.return_value.total_memory = 2000000000  # 2GB
                device = registry._resolve_device("cuda_preferred_cpu_fallback")
                assert device == "cpu"
    
    def test_llm_with_device(self, registry):
        """Test LLM model spec includes device information."""
        with patch.object(registry, '_get_model_config') as mock_config:
            mock_config.return_value = (
                {"provider": "lmstudio", "model": "test", "endpoint": "http://test"},
                "cuda"
            )
            
            spec = registry.llm()
            assert spec.device == "cuda"
            assert spec.extra["device"] == "cuda"
    
    def test_embedding_with_device(self, registry):
        """Test embedding model spec includes device information."""
        with patch.object(registry, '_get_model_config') as mock_config:
            mock_config.return_value = (
                {"provider": "hf", "model": "test", "dim": 384},
                "cuda"
            )
            
            spec = registry.embedding()
            assert spec.device == "cuda"
            assert spec.extra["device"] == "cuda"
    
    def test_reranker_with_device(self, registry):
        """Test reranker model spec includes device information."""
        with patch.object(registry, '_get_model_config') as mock_config:
            mock_config.return_value = (
                {"provider": "hf", "model": "test"},
                "cpu"
            )
            
            spec = registry.reranker()
            assert spec.device == "cpu"
            assert spec.extra["device"] == "cpu"


class TestGPUScheduler:
    """Test GPU scheduler functionality."""
    
    @pytest.fixture
    def scheduler(self):
        """Create a test scheduler instance."""
        return GPUScheduler()
    
    def test_scheduler_initialization(self, scheduler):
        """Test scheduler initializes correctly."""
        assert scheduler.memory_threshold == 0.8
        assert hasattr(scheduler, '_gpu_available')
    
    def test_get_gpu_status_no_gpu(self, scheduler):
        """Test GPU status when no GPU is available."""
        # Reset the cached GPU availability
        scheduler._gpu_available = False
        status = scheduler.get_gpu_status()
        
        assert status["available"] is False
        assert status["memory_threshold"] == 0.8
    
    def test_get_gpu_status_with_gpu(self, scheduler):
        """Test GPU status when GPU is available."""
        # Reset the cached GPU availability
        scheduler._gpu_available = True
        with patch('torch.cuda.memory_allocated', return_value=1000000000):
            with patch('torch.cuda.get_device_properties') as mock_props:
                mock_props.return_value.total_memory = 2000000000
                mock_props.return_value.name = "Test GPU"
                
                status = scheduler.get_gpu_status()
                
                assert status["available"] is True
                assert status["memory_threshold"] == 0.8
                assert abs(status["memory_used_mb"] - 1000.0) < 1.0  # Allow small precision differences
                assert status["memory_total_mb"] == 2000.0
                assert status["memory_load_percent"] == 50.0
                assert status["below_threshold"] is True
                assert status["device_name"] == "Test GPU"
    
    def test_should_use_gpu_no_gpu(self, scheduler):
        """Test GPU decision when no GPU is available."""
        # Reset the cached GPU availability
        scheduler._gpu_available = False
        assert scheduler.should_use_gpu("llm") is False
        assert scheduler.should_use_gpu("embedding") is False
        assert scheduler.should_use_gpu("reranker") is False
    
    def test_should_use_gpu_with_gpu(self, scheduler):
        """Test GPU decision when GPU is available."""
        with patch('torch.cuda.is_available', return_value=True):
            # LLM and embedding should always use GPU
            assert scheduler.should_use_gpu("llm") is True
            assert scheduler.should_use_gpu("embedding") is True
            
            # Reranker depends on memory load
            with patch('torch.cuda.memory_allocated', return_value=1000000000):
                with patch('torch.cuda.get_device_properties') as mock_props:
                    mock_props.return_value.total_memory = 2000000000
                    assert scheduler.should_use_gpu("reranker") is True
            
            with patch('torch.cuda.memory_allocated', return_value=1800000000):
                with patch('torch.cuda.get_device_properties') as mock_props:
                    mock_props.return_value.total_memory = 2000000000
                    assert scheduler.should_use_gpu("reranker") is False
    
    def test_get_optimal_device(self, scheduler):
        """Test optimal device selection."""
        with patch.object(scheduler, 'should_use_gpu', return_value=True):
            assert scheduler.get_optimal_device("llm") == "cuda"
        
        with patch.object(scheduler, 'should_use_gpu', return_value=False):
            assert scheduler.get_optimal_device("reranker") == "cpu"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
