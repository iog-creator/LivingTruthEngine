from dataclasses import dataclass
from pathlib import Path
import tomllib

@dataclass
class ModelSpec:
    provider: str
    name: str
    extra: dict

class ModelRegistry:
    def __init__(self, path: str = "config/models.toml"):
        self.cfg = tomllib.loads(Path(path).read_text(encoding="utf-8"))

    def llm(self, key="default") -> ModelSpec:
        c = self.cfg["llm"][key]
        return ModelSpec(c["provider"], c["model"], {"endpoint": c.get("endpoint")})

    def embedding(self, key="default") -> ModelSpec:
        c = self.cfg["embedding"][key]
        return ModelSpec(c["provider"], c["model"], {"dim": c.get("dim")})

    def ner(self, key="default") -> ModelSpec:
        c = self.cfg["ner"][key]
        return ModelSpec(c["provider"], c["model"], {})

    def reranker(self, key="default") -> ModelSpec:
        c = self.cfg["reranker"][key]
        return ModelSpec(c["provider"], c["model"], {})

    def ocr(self, key="default") -> ModelSpec:
        c = self.cfg["ocr"][key]
        return ModelSpec(c["provider"], c.get("model", "tesseract"), {"lang": c.get("lang")})

    def stt(self, key="default") -> ModelSpec:
        c = self.cfg["stt"][key]
        return ModelSpec(c["provider"], c.get("model", "whisper"), {})

    def diarization(self, key="default") -> ModelSpec:
        c = self.cfg["diarization"][key]
        return ModelSpec(c["provider"], c.get("pipeline", "pyannote/speaker-diarization"), {})

    def topics(self, key="default") -> ModelSpec:
        c = self.cfg["topics"][key]
        return ModelSpec(c["provider"], c.get("backend", "sentence-transformers/all-MiniLM-L6-v2"), {})
