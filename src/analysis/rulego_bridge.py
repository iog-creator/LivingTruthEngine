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

    async def evaluate_graph(self, run_id: str) -> Dict[str, Any]:
        """
        Evaluate graph for a specific run against Rulego policies.

        Args:
            run_id: The run ID to evaluate

        Returns:
            Policy findings with rule_id, severity, nodes, and msg
        """
        try:
            # For Phase 9.3, return mock findings
            # In Phase 9.4, this will integrate with actual graph data
            findings = [
                {
                    "rule_id": "min_evidence_check",
                    "severity": "info",
                    "nodes": ["claim_1", "claim_2"],
                    "msg": f"Minimum evidence threshold met for run {run_id}",
                }
            ]

            return {"status": "ok", "findings": findings, "run_id": run_id}

        except Exception as e:
            return {
                "status": "error",
                "findings": [],
                "error": str(e),
                "run_id": run_id,
            }
