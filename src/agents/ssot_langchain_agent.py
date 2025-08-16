#!/usr/bin/env python3
"""
SSOT LangChain Agent (deterministic, read-only)

Purpose
- Sequence SSOT tasks via the LM Studio HTTP bridge:
  1) verify_ssot
  2) read_ssot_report
  3) draft_patches
- Save an envelope JSON to reports/ with results.
- Never writes to the repo; Cursor remains the executor.
- Default path is deterministic (no LLM). Optional --langchain builds a LangChain Agent if available.

Contract
- All CLI executions print a single JSON envelope to STDOUT:
  { "status": "ok" | "error", "data"?: {...}, "error"?: {"code": "...", "message": "...", "details"?: {...}} }
"""  # noqa: E501

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import yaml


# ---------------------------
# Envelope helpers (SSOT rule)
# ---------------------------


def ok(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "ok", "data": data}


def err(
    code: str, message: str, details: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    e = {"status": "error", "error": {"code": code, "message": message}}
    if details:
        e["error"]["details"] = details
    return e


# ---------------------------
# Config
# ---------------------------


@dataclass
class AgentConfig:
    model: str = "llama-3.2-3b-instruct"
    bridge_url: str = "http://127.0.0.1:8756"
    tools: tuple[str, ...] = ("verify_ssot", "read_ssot_report", "draft_patches")

    @classmethod
    def from_file(cls, path: Path) -> "AgentConfig":
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            model=str(raw.get("model", cls.model)),
            bridge_url=str(raw.get("bridge_url", cls.bridge_url)),
            tools=tuple(raw.get("tools", cls.tools)),
        )


# ---------------------------
# Bridge client (HTTP)
# ---------------------------


class SSOTBridgeClient:
    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(
        self, path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        try:
            r = requests.post(url, json=payload or {}, timeout=self.timeout)
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"bridge_request_failed: {e}") from e
        except ValueError as e:
            raise RuntimeError(f"bridge_invalid_json: {e}") from e

    def verify_ssot(self) -> Dict[str, Any]:
        return self._post("/tools/verify_ssot")

    def read_ssot_report(self) -> Dict[str, Any]:
        return self._post("/tools/read_ssot_report")

    def draft_patches(self) -> Dict[str, Any]:
        return self._post("/tools/draft_patches")

    def run_repo_inventory(self) -> Dict[str, Any]:
        return self._post("/tools/run_repo_inventory")


# ------------------------------------------------------
# Deterministic, no‑LLM execution (default & CI-friendly)
# ------------------------------------------------------


class DeterministicSSOTAgent:
    def __init__(self, client: SSOTBridgeClient):
        self.client = client

    def run(self) -> Dict[str, Any]:
        # Step 1: verify
        verify = self.client.verify_ssot()

        # Step 2: read report
        report = self.client.read_ssot_report()

        # Step 3: draft patches (suggestions only)
        patches = self.client.draft_patches()

        return ok(
            {
                "phase": "9.5.7.4.7",
                "sequence": ["verify_ssot", "read_ssot_report", "draft_patches"],
                "verify": verify,
                "report": report,
                "patches": patches,
                "note": "Agent is read-only. Apply patches in Cursor and gate with SSOT verification.",  # noqa: E501
            }
        )


# ------------------------------------------------------
# Optional: LangChain Agent (only if --langchain is set)
# ------------------------------------------------------


def build_langchain_agent(client: SSOTBridgeClient):
    """
    Build a minimal LangChain agent that calls the same HTTP tools.
    Import is deferred so the module can be imported without LangChain installed.
    """
    try:
        from langchain.tools import BaseTool  # type: ignore
        from langchain_core.prompts import ChatPromptTemplate  # type: ignore
        from langchain_core.runnables import RunnableLambda, RunnableSequence  # type: ignore
    except Exception as e:  # Do not allow bare except; be explicit
        raise RuntimeError("langchain_not_available") from e

    class VerifyTool(BaseTool):
        name = "verify_ssot"
        description = "Run deterministic SSOT verification."

        def _run(self, *args, **kwargs) -> Any:
            return client.verify_ssot()

        async def _arun(self, *args, **kwargs) -> Any:  # pragma: no cover
            return self._run(*args, **kwargs)

    class ReadReportTool(BaseTool):
        name = "read_ssot_report"
        description = "Read the SSOT JSON report."

        def _run(self, *args, **kwargs) -> Any:
            return client.read_ssot_report()

        async def _arun(self, *args, **kwargs) -> Any:  # pragma: no cover
            return self._run(*args, **kwargs)

    class DraftPatchesTool(BaseTool):
        name = "draft_patches"
        description = "Draft minimal patch specs (no writes)."

        def _run(self, *args, **kwargs) -> Any:
            return client.draft_patches()

        async def _arun(self, *args, **kwargs) -> Any:  # pragma: no cover
            return self._run(*args, **kwargs)

    # A simple RunnableSequence to keep behavior deterministic
    seq = RunnableSequence(
        RunnableLambda(lambda _: {"verify": VerifyTool()()})
        | RunnableLambda(lambda state: {**state, "report": ReadReportTool()()})
        | RunnableLambda(lambda state: {**state, "patches": DraftPatchesTool()()})
        | RunnableLambda(
            lambda state: ok(
                {
                    "phase": "9.5.7.4.7",
                    "sequence": ["verify_ssot", "read_ssot_report", "draft_patches"],
                    **state,
                    "note": "LangChain path; still read-only. Apply patches in Cursor and gate with SSOT verification.",  # noqa: E501
                }
            )
        )
    )
    return seq


# ---------------------------
# CLI
# ---------------------------


def _save_report(payload: Dict[str, Any], out_path: Optional[Path]) -> None:
    if out_path is None:
        # default reports/ with timestamp
        reports_dir = Path("reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        ts = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        out_path = reports_dir / f"ssot_agent_output_{ts}.json"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="SSOT LangChain Agent (deterministic, read-only)"
    )
    parser.add_argument(
        "--config",
        default="config/agents/ssot_agent.yaml",
        help="Path to agent config YAML",
    )
    parser.add_argument(
        "--langchain",
        action="store_true",
        help="Use LangChain sequence instead of deterministic Python",
    )
    parser.add_argument(
        "--timeout", type=float, default=30.0, help="HTTP timeout seconds"
    )
    parser.add_argument(
        "--out", type=str, default="", help="Write JSON output to this path (optional)"
    )
    args = parser.parse_args()

    cfg = AgentConfig.from_file(Path(args.config))
    client = SSOTBridgeClient(cfg.bridge_url, timeout=args.timeout)

    try:
        if args.langchain:
            seq = build_langchain_agent(client)
            result = seq.invoke({})
        else:
            agent = DeterministicSSOTAgent(client)
            result = agent.run()

        # Persist & emit envelope
        out_path = Path(args.out) if args.out else None
        _save_report(result, out_path)
        print(json.dumps(result, separators=(",", ":")))
    except RuntimeError as e:
        print(json.dumps(err("agent_runtime_error", str(e))), flush=True)
    except Exception as e:
        # Explicit error path (no silent fallbacks)
        print(json.dumps(err("agent_unhandled_exception", repr(e))), flush=True)


if __name__ == "__main__":
    main()
