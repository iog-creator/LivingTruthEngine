from dataclasses import dataclass
from pathlib import Path
import tomllib
import torch
import logging

logger = logging.getLogger(__name__)

@dataclass
class ModelSpec:
    provider: str
    name: str
    extra: dict
    device: str = None

class ModelRegistry:
    def __init__(self, path: str = "config/models.toml"):
        self.cfg = tomllib.loads(Path(path).read_text(encoding="utf-8"))
        self._gpu_available = torch.cuda.is_available()
        self._gpu_memory_threshold = 0.8  # 80% GPU memory threshold

    def _resolve_device(self, device_pref: str) -> str:
        """Resolve device preference to actual device."""
        if device_pref == "cuda_if_available":
            return "cuda" if self._gpu_available else "cpu"
        elif device_pref == "cuda":
            return "cuda" if self._gpu_available else "cpu"
        elif device_pref == "cuda_preferred_cpu_fallback":
            if not self._gpu_available:
                return "cpu"
            # Check GPU memory load
            try:
                gpu_memory_used = torch.cuda.memory_allocated()
                gpu_memory_total = torch.cuda.get_device_properties(0).total_memory
                gpu_load = gpu_memory_used / gpu_memory_total
                if gpu_load < self._gpu_memory_threshold:
                    return "cuda"
                else:
                    logger.info(f"GPU memory load {gpu_load:.2%} exceeds threshold {self._gpu_memory_threshold:.2%}, using CPU")
                    return "cpu"
            except Exception as e:
                logger.warning(f"Could not check GPU memory load: {e}, using CPU")
                return "cpu"
        else:
            return device_pref or "cpu"

    def _get_model_config(self, model_type: str, key: str = "default"):
        """Get model configuration with device resolution."""
        c = self.cfg[model_type][key]
        device_pref = c.get("device")
        resolved_device = self._resolve_device(device_pref)
        
        # Log device decision
        logger.info(f"{model_type}.{key}: {device_pref} -> {resolved_device}")
        
        return c, resolved_device

    def llm(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("llm", key)
        extra = {"endpoint": c.get("endpoint")}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c["model"], extra, device)

    def embedding(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("embedding", key)
        extra = {"dim": c.get("dim")}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c["model"], extra, device)

    def ner(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("ner", key)
        extra = {}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c["model"], extra, device)

    def reranker(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("reranker", key)
        extra = {}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c["model"], extra, device)

    def ocr(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("ocr", key)
        extra = {"lang": c.get("lang")}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c.get("model", "tesseract"), extra, device)

    def stt(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("stt", key)
        extra = {}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c.get("model", "whisper"), extra, device)

    def diarization(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("diarization", key)
        extra = {}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c.get("pipeline", "pyannote/speaker-diarization"), extra, device)

    def topics(self, key="default") -> ModelSpec:
        c, device = self._get_model_config("topics", key)
        extra = {}
        if device:
            extra["device"] = device
        return ModelSpec(c["provider"], c.get("backend", "sentence-transformers/all-MiniLM-L6-v2"), extra, device)

    def get_gpu_status(self) -> dict:
        """Get current GPU status for monitoring."""
        status = {
            "available": self._gpu_available,
            "memory_threshold": self._gpu_memory_threshold
        }
        
        if self._gpu_available:
            try:
                gpu_memory_used = torch.cuda.memory_allocated()
                gpu_memory_total = torch.cuda.get_device_properties(0).total_memory
                gpu_load = gpu_memory_used / gpu_memory_total
                status.update({
                    "memory_used_mb": gpu_memory_used / 1024 / 1024,
                    "memory_total_mb": gpu_memory_total / 1024 / 1024,
                    "memory_load_percent": gpu_load * 100,
                    "below_threshold": gpu_load < self._gpu_memory_threshold
                })
            except Exception as e:
                status["error"] = str(e)
        
        return status
