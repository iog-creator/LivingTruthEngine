#!/usr/bin/env python3
"""
MCP Router Diagnostics (safe, read-only)
- Launches your MCP server (stdio) and speaks JSON-RPC:
  1) initialize (version negotiation)
  2) notifications/initialized
  3) tools/list (with pagination)
- Computes router health proxies: count, duplicates, namespace skew, schema sanity, latency stats.
- NO tool invocations by default (no side effects).
- Outputs {status,data?,error?} envelope + writes a markdown+json report in ./reports/.

Usage:
  python scripts/mcp_router_diagnostics.py \
    --cmd "make lm-mcp" \
    --proto 2025-06-18 \
    --timeout 8 \
    --max-seconds 20

References:
- tools/list & tools/call JSON-RPC methods (official): https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- lifecycle initialize + initialized notification: https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle
- stdio transport rules (newline-delimited JSON-RPC): https://modelcontextprotocol.io/docs/concepts/transports
"""
from __future__ import annotations
import argparse, json, os, shlex, subprocess, sys, time, uuid, statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

def envelope_ok(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "ok", "data": data}

def envelope_err(code: str, message: str, details: Optional[Dict[str, Any]]=None) -> Dict[str, Any]:
    e = {"status": "error", "error": {"code": code, "message": message}}
    if details: e["error"]["details"] = details
    return e

class JsonRpcIO:
    def __init__(self, proc: subprocess.Popen, timeout: float):
        self.proc = proc
        self.timeout = timeout
        self.buf: Dict[str, Any] = {}
        self.pending: Dict[str, float] = {}

    def send(self, method: str, params: Optional[Dict[str, Any]]=None, id: Optional[str]=None) -> str:
        rid = id or str(uuid.uuid4())
        msg = {"jsonrpc":"2.0","method":method}
        if params is not None: msg["params"] = params
        if id is not None: msg["id"] = id
        line = json.dumps(msg, separators=(",",":")) + "\n"
        self.proc.stdin.write(line.encode("utf-8"))
        self.proc.stdin.flush()
        self.pending[rid] = time.time()
        return rid

    def request(self, method: str, params: Optional[Dict[str, Any]]=None) -> Tuple[str, Dict[str,Any]]:
        rid = str(uuid.uuid4())
        msg = {"jsonrpc":"2.0","id":rid,"method":method}
        if params is not None: msg["params"] = params
        line = json.dumps(msg, separators=(",",":")) + "\n"
        self.proc.stdin.write(line.encode("utf-8"))
        self.proc.stdin.flush()
        self.pending[rid] = time.time()
        return rid, self._await_response(rid)

    def _await_response(self, rid: str) -> Dict[str,Any]:
        deadline = time.time() + self.timeout
        out = b""
        while time.time() < deadline:
            line = self.proc.stdout.readline()
            if not line:
                # Process may still be alive; keep looping briefly
                time.sleep(0.02)
                continue
            try:
                obj = json.loads(line.decode("utf-8").strip() or "{}")
            except json.JSONDecodeError as e:
                # Log malformed JSON but continue processing
                print(f"Warning: Malformed JSON in MCP response: {e}", file=sys.stderr)
                continue
            if obj.get("id") == rid or "method" in obj:
                # return first matching response; notifications pass through
                if obj.get("id") == rid:
                    return obj
                # ignore notifications unless useful
        raise TimeoutError(f"Timeout waiting for response id={rid}")

def start_server(cmd: str) -> subprocess.Popen:
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    return proc

def list_all_tools(rpc: JsonRpcIO) -> Tuple[List[Dict[str,Any]], Dict[str, float]]:
    tools: List[Dict[str,Any]] = []
    latencies: Dict[str, float] = {"calls":0, "samples_ms":[]}
    cursor = None
    while True:
        params = {}
        if cursor: params["cursor"] = cursor
        t0 = time.time()
        _, resp = rpc.request("tools/list", params)
        dt = (time.time() - t0)*1000
        latencies["calls"] += 1
        latencies["samples_ms"].append(dt)
        if "error" in resp:
            raise RuntimeError(f"tools/list error: {resp['error']}")
        rs = resp.get("result", {})
        page = rs.get("tools", []) or []
        tools.extend(page)
        cursor = rs.get("nextCursor")
        if not cursor:
            break
    return tools, latencies

def sanity_check_tool_schema(tool: Dict[str,Any]) -> List[str]:
    issues = []
    if "name" not in tool or not isinstance(tool["name"], str) or not tool["name"].strip():
        issues.append("missing_or_invalid_name")
    isch = tool.get("inputSchema", {})
    if not isinstance(isch, dict):
        issues.append("inputSchema_not_object")
    else:
        if isch.get("type") not in (None, "object"):
            issues.append("inputSchema_type_not_object")
        props = isch.get("properties", {})
        if props is not None and not isinstance(props, dict):
            issues.append("inputSchema_properties_not_object")
    # outputSchema optional; if present check shape
    osch = tool.get("outputSchema")
    if osch is not None and not isinstance(osch, dict):
        issues.append("outputSchema_not_object")
    return issues

def compute_metrics(tools: List[Dict[str,Any]], list_latency: Dict[str, float]) -> Dict[str, Any]:
    names = [t.get("name","") for t in tools]
    dups = sorted({n for n in names if names.count(n) > 1})
    prefixes = {}
    for n in names:
        pre = n.split(".",1)[0] if "." in n else n.split("_",1)[0]
        prefixes[pre] = prefixes.get(pre, 0) + 1

    schema_issues = {}
    for t in tools:
        iss = sanity_check_tool_schema(t)
        if iss:
            schema_issues[t.get("name","<unnamed>")] = iss

    samples = list_latency.get("samples_ms", [])
    lat = {
        "calls": list_latency.get("calls", 0),
        "p50_ms": round(statistics.median(samples),2) if samples else None,
        "p95_ms": round(sorted(samples)[int(0.95*len(samples))-1],2) if samples else None,
        "max_ms": round(max(samples),2) if samples else None,
    }

    # "router sanity" signals: surface namespace balance and long descriptions
    long_desc = [t["name"] for t in tools if len((t.get("description") or "")) > 512]

    return {
        "count": len(tools),
        "duplicates": dups,
        "namespaces_top": sorted(prefixes.items(), key=lambda kv: (-kv[1], kv[0]))[:10],
        "schema_issues": schema_issues,
        "list_latency": lat,
        "long_descriptions": long_desc[:10],
    }

def main():
    ap = argparse.ArgumentParser(description="MCP Router Diagnostics (safe)")
    ap.add_argument("--cmd", default=os.environ.get("MCP_CMD","make lm-mcp"),
                    help="Command to launch MCP server (stdio). Default: make lm-mcp")
    ap.add_argument("--proto", default="2025-06-18", help="Requested MCP protocol version")
    ap.add_argument("--timeout", type=float, default=8.0, help="Per-request timeout (seconds)")
    ap.add_argument("--max-seconds", type=float, default=20.0, help="Overall time budget (seconds)")
    ap.add_argument("--out", default="", help="Write JSON report to this path (also writes .md).")
    args = ap.parse_args()

    start = time.time()
    reports_dir = Path("reports"); reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    out_json = Path(args.out) if args.out else reports_dir / f"mcp_router_report_{stamp}.json"
    out_md   = reports_dir / f"mcp_router_report_{stamp}.md"

    try:
        proc = start_server(args.cmd)
    except Exception as e:
        print(json.dumps(envelope_err("server_start_failed", str(e))), flush=True)
        return

    rpc = JsonRpcIO(proc, timeout=args.timeout)
    try:
        # Initialize → negotiate protocol (client proposes latest it supports)
        init_params = {
            "protocolVersion": args.proto,
            "capabilities": {"tools": {"listChanged": True}},
            "clientInfo": {"name":"router-diagnostics","version":"0.1.0"},
        }
        _, init = rpc.request("initialize", init_params)  # spec lifecycle
        if "error" in init:
            raise RuntimeError(f"initialize error: {init['error']}")
        # Send initialized notification
        rpc.send("notifications/initialized", {"ready": True})

        # Enumerate tools with pagination
        tools, list_lat = list_all_tools(rpc)
        metrics = compute_metrics(tools, list_lat)

        budget_ok = (time.time()-start) <= args.max_seconds
        status = "ok" if budget_ok else "error"
        result = envelope_ok({
            "protocol_negotiated": init.get("result",{}).get("protocolVersion"),
            "tools_count": metrics["count"],
            "duplicates": metrics["duplicates"],
            "namespaces_top": metrics["namespaces_top"],
            "schema_issues": metrics["schema_issues"],
            "list_latency": metrics["list_latency"],
            "long_descriptions": metrics["long_descriptions"],
            "time_sec": round(time.time()-start,2),
            "notes": [
                "This is a discovery-only probe; no tools were invoked.",
                "Large toolsets are fine when router discovery & pagination are fast and names are collision-free."
            ]
        }) if status=="ok" else envelope_err("time_budget_exceeded","Router listing exceeded time budget")

        # Persist artifacts
        out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
        out_md.write_text(
            f"# MCP Router Report ({stamp})\n\n"
            f"- Protocol negotiated: `{result.get('data',{}).get('protocol_negotiated')}`\n"
            f"- Tool count: **{metrics['count']}**\n"
            f"- tools/list latency p50/p95/max (ms): {metrics['list_latency']}\n"
            f"- Duplicate names: {metrics['duplicates'] or 'none'}\n"
            f"- Top namespaces: {metrics['namespaces_top']}\n"
            f"- Schema issues (first 10): {list(metrics['schema_issues'].items())[:10] or 'none'}\n"
            f"- Long descriptions (first 10): {metrics['long_descriptions'] or 'none'}\n"
            f"- NOTE: No tools were invoked by this probe.\n",
            encoding="utf-8"
        )

        print(json.dumps(result, separators=(",",":")), flush=True)

    except Exception as e:
        print(json.dumps(envelope_err("diagnostics_failed", repr(e))), flush=True)
    finally:
        try:
            proc.terminate()
        except (OSError, subprocess.SubprocessError) as e:
            print(f"Warning: Failed to terminate MCP server process: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
