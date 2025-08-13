"""
GPU-aware scheduler for model allocation decisions.
Monitors GPU usage and decides where to run each model type.
"""

import torch
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class GPUScheduler:
    def __init__(self, memory_threshold: float = 0.8):
        """
        Initialize GPU scheduler.
        
        Args:
            memory_threshold: GPU memory threshold (0.0-1.0) for fallback decisions
        """
        self.memory_threshold = memory_threshold
        self._gpu_available = torch.cuda.is_available()
        
        if self._gpu_available:
            logger.info(f"GPU scheduler initialized with {self.memory_threshold:.1%} memory threshold")
        else:
            logger.info("GPU scheduler initialized - no CUDA available, using CPU only")

    def get_gpu_status(self) -> Dict:
        """Get current GPU status for monitoring."""
        status = {
            "available": self._gpu_available,
            "memory_threshold": self.memory_threshold
        }
        
        if self._gpu_available:
            try:
                gpu_memory_used = torch.cuda.memory_allocated()
                gpu_memory_total = torch.cuda.get_device_properties(0).total_memory
                gpu_load = gpu_memory_used / gpu_memory_total
                
                status.update({
                    "memory_used_mb": round(gpu_memory_used / 1024 / 1024, 2),
                    "memory_total_mb": round(gpu_memory_total / 1024 / 1024, 2),
                    "memory_load_percent": round(gpu_load * 100, 2),
                    "below_threshold": gpu_load < self.memory_threshold,
                    "device_name": torch.cuda.get_device_name(0)
                })
            except Exception as e:
                logger.warning(f"Could not get GPU status: {e}")
                status["error"] = str(e)
        
        return status

    def should_use_gpu(self, model_type: str) -> bool:
        """
        Determine if a model type should use GPU based on current load.
        
        Args:
            model_type: Type of model ('llm', 'embedding', 'reranker', etc.)
            
        Returns:
            True if GPU should be used, False for CPU
        """
        if not self._gpu_available:
            return False
            
        # Always use GPU for LLM and embedding models
        if model_type in ['llm', 'embedding']:
            return True
            
        # For reranker, check memory load
        if model_type == 'reranker':
            try:
                gpu_memory_used = torch.cuda.memory_allocated()
                gpu_memory_total = torch.cuda.get_device_properties(0).total_memory
                gpu_load = gpu_memory_used / gpu_memory_total
                
                should_use = gpu_load < self.memory_threshold
                logger.info(f"Reranker GPU decision: load={gpu_load:.2%}, threshold={self.memory_threshold:.2%}, use_gpu={should_use}")
                return should_use
                
            except Exception as e:
                logger.warning(f"Could not check GPU memory for reranker: {e}, using CPU")
                return False
        
        # Default to GPU for other model types
        return True

    def get_optimal_device(self, model_type: str) -> str:
        """
        Get optimal device for a model type.
        
        Args:
            model_type: Type of model
            
        Returns:
            Device string ('cuda' or 'cpu')
        """
        return "cuda" if self.should_use_gpu(model_type) else "cpu"

    def log_device_allocation(self, model_type: str, device: str, reason: str = ""):
        """Log device allocation decision."""
        gpu_status = self.get_gpu_status()
        logger.info(f"Device allocation: {model_type} -> {device} {reason}")
        
        if self._gpu_available and device == "cuda":
            logger.info(f"  GPU memory: {gpu_status.get('memory_used_mb', 'N/A')}MB / {gpu_status.get('memory_total_mb', 'N/A')}MB ({gpu_status.get('memory_load_percent', 'N/A')}%)")

# Global scheduler instance
gpu_scheduler = GPUScheduler()

