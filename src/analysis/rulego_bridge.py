import httpx
from typing import Dict, Any

class RulegoClient:
    def __init__(self, base: str = "http://localhost:9127"):
        self.base = base
    
    async def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate payload against Rulego policies"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/evaluate", json=payload)
            r.raise_for_status()
            return r.json()
    
    async def health(self) -> Dict[str, Any]:
        """Check Rulego service health"""
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{self.base}/health")
            r.raise_for_status()
            return r.json()
    
    async def list_policies(self) -> Dict[str, Any]:
        """List loaded policies"""
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get(f"{self.base}/policies")
            r.raise_for_status()
            return r.json()
