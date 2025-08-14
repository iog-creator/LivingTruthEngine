"""
GPU Scheduler for Phase 9.5.2
Handles GPU VRAM probing, reservation logic, and fallback management
"""

import logging
import subprocess
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class GPUInfo:
    """GPU information structure"""
    index: int
    name: str
    total_memory_mb: int
    used_memory_mb: int
    free_memory_mb: int
    utilization_percent: int
    temperature_celsius: int
    power_watts: float

@dataclass
class FallbackEvent:
    """Fallback event structure"""
    timestamp: str
    type: str  # "gpu_vram_low", "gpu_unavailable", "cpu_fallback"
    reason: str
    gpu_info: Optional[GPUInfo]
    duration_ms: int

class GPUScheduler:
    """GPU scheduler with VRAM probing and fallback management"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize GPU scheduler with configuration"""
        self.config = config
        self.vram_threshold_mb = config.get("vram_threshold_mb", 1000)  # 1GB threshold
        self.reservation_mb = config.get("reservation_mb", 500)  # 500MB reservation
        self.fallback_events: List[FallbackEvent] = []
        self.max_fallback_history = config.get("max_fallback_history", 50)
        
    def get_gpu_status(self) -> Dict[str, Any]:
        """Get comprehensive GPU status information"""
        try:
            gpus = self._probe_gpus()
            if not gpus:
                return {
                    "available": False,
                    "reason": "No GPUs detected",
                    "gpus": [],
                    "fallback_required": True
                }
            
            # Check if any GPU has sufficient VRAM
            available_gpus = []
            for gpu in gpus:
                if gpu.free_memory_mb >= self.vram_threshold_mb:
                    available_gpus.append(gpu)
            
            if not available_gpus:
                # All GPUs have insufficient VRAM
                self._log_fallback_event("gpu_vram_low", "Insufficient VRAM on all GPUs", gpus[0])
                return {
                    "available": False,
                    "reason": f"Insufficient VRAM (threshold: {self.vram_threshold_mb}MB)",
                    "gpus": [self._gpu_to_dict(gpu) for gpu in gpus],
                    "fallback_required": True
                }
            
            # Select best GPU (most free VRAM)
            best_gpu = max(available_gpus, key=lambda g: g.free_memory_mb)
            
            return {
                "available": True,
                "reason": "GPU available",
                "selected_gpu": self._gpu_to_dict(best_gpu),
                "all_gpus": [self._gpu_to_dict(gpu) for gpu in gpus],
                "fallback_required": False
            }
            
        except Exception as e:
            logger.error(f"GPU status check failed: {e}")
            self._log_fallback_event("gpu_unavailable", f"GPU check failed: {e}", None)
            return {
                "available": False,
                "reason": f"GPU check failed: {e}",
                "gpus": [],
                "fallback_required": True
            }
    
    def reserve_gpu_memory(self, required_mb: int) -> Dict[str, Any]:
        """Reserve GPU memory for a task"""
        try:
            gpu_status = self.get_gpu_status()
            if not gpu_status["available"]:
                return {
                    "success": False,
                    "reason": gpu_status["reason"],
                    "fallback_required": True
                }
            
            selected_gpu = gpu_status["selected_gpu"]
            available_mb = selected_gpu["free_memory_mb"]
            
            if available_mb < required_mb:
                self._log_fallback_event("gpu_vram_low", f"Required {required_mb}MB, available {available_mb}MB", None)
                return {
                    "success": False,
                    "reason": f"Insufficient VRAM: required {required_mb}MB, available {available_mb}MB",
                    "fallback_required": True
                }
            
            # Reserve memory (in a real implementation, this would track reservations)
            logger.info(f"Reserved {required_mb}MB on GPU {selected_gpu['index']}")
            
            return {
                "success": True,
                "gpu_index": selected_gpu["index"],
                "reserved_mb": required_mb,
                "remaining_mb": available_mb - required_mb
            }
            
        except Exception as e:
            logger.error(f"GPU memory reservation failed: {e}")
            return {
                "success": False,
                "reason": f"Reservation failed: {e}",
                "fallback_required": True
            }
    
    def simulate_low_vram(self) -> Dict[str, Any]:
        """Simulate low VRAM condition for testing"""
        try:
            # Temporarily lower the threshold to trigger fallback
            original_threshold = self.vram_threshold_mb
            self.vram_threshold_mb = 10000  # 10GB threshold (unrealistic)
            
            gpu_status = self.get_gpu_status()
            
            # Restore original threshold
            self.vram_threshold_mb = original_threshold
            
            self._log_fallback_event("gpu_vram_low", "Simulated low VRAM condition", None)
            
            return {
                "simulation_success": True,
                "triggered_fallback": gpu_status["fallback_required"],
                "gpu_status": gpu_status
            }
            
        except Exception as e:
            logger.error(f"Low VRAM simulation failed: {e}")
            return {
                "simulation_success": False,
                "error": str(e)
            }
    
    def get_fallback_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent fallback events"""
        recent_events = self.fallback_events[-limit:] if self.fallback_events else []
        return [
            {
                "timestamp": event.timestamp,
                "type": event.type,
                "reason": event.reason,
                "gpu_info": self._gpu_to_dict(event.gpu_info) if event.gpu_info else None,
                "duration_ms": event.duration_ms
            }
            for event in recent_events
        ]
    
    def _probe_gpus(self) -> List[GPUInfo]:
        """Probe system for GPU information"""
        gpus = []
        
        try:
            # Try nvidia-smi first
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu,power.draw", 
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 8:
                            gpu = GPUInfo(
                                index=int(parts[0]),
                                name=parts[1],
                                total_memory_mb=int(parts[2]),
                                used_memory_mb=int(parts[3]),
                                free_memory_mb=int(parts[4]),
                                utilization_percent=int(parts[5]),
                                temperature_celsius=int(parts[6]),
                                power_watts=float(parts[7]) if parts[7] != 'N/A' else 0.0
                            )
                            gpus.append(gpu)
            
            # If no GPUs found, try alternative methods
            if not gpus:
                # Check for CUDA devices
                try:
                    import torch
                    if torch.cuda.is_available():
                        for i in range(torch.cuda.device_count()):
                            props = torch.cuda.get_device_properties(i)
                            gpu = GPUInfo(
                                index=i,
                                name=props.name,
                                total_memory_mb=props.total_memory // (1024 * 1024),
                                used_memory_mb=0,  # PyTorch doesn't provide this easily
                                free_memory_mb=props.total_memory // (1024 * 1024),
                                utilization_percent=0,
                                temperature_celsius=0,
                                power_watts=0.0
                            )
                            gpus.append(gpu)
                except ImportError:
                    pass
            
        except Exception as e:
            logger.warning(f"GPU probing failed: {e}")
        
        return gpus
    
    def _gpu_to_dict(self, gpu: GPUInfo) -> Dict[str, Any]:
        """Convert GPUInfo to dictionary"""
        return {
            "index": gpu.index,
            "name": gpu.name,
            "total_memory_mb": gpu.total_memory_mb,
            "used_memory_mb": gpu.used_memory_mb,
            "free_memory_mb": gpu.free_memory_mb,
            "utilization_percent": gpu.utilization_percent,
            "temperature_celsius": gpu.temperature_celsius,
            "power_watts": gpu.power_watts
        }
    
    def _log_fallback_event(self, event_type: str, reason: str, gpu_info: Optional[GPUInfo]):
        """Log a fallback event"""
        event = FallbackEvent(
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            type=event_type,
            reason=reason,
            gpu_info=gpu_info,
            duration_ms=0  # Could track actual duration in future
        )
        
        self.fallback_events.append(event)
        
        # Keep only recent events
        if len(self.fallback_events) > self.max_fallback_history:
            self.fallback_events = self.fallback_events[-self.max_fallback_history:]
        
        logger.warning(f"GPU fallback event: {event_type} - {reason}")

