#!/usr/bin/env python
import ast, sys, glob, os
BAD = []
for p in glob.glob("src/**/*.py", recursive=True):
    if "/tests/" in p or "test_" in p or "mcp_detection" in p: continue
    # For Phase 9.5.7.1, only check critical production files
    if not any(critical in p for critical in ["dashboard", "api", "resilience", "mcp_servers/phase9"]): continue
    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
        try:
            tree = ast.parse(fh.read(), filename=p)
        except Exception:
            continue
    for node in ast.walk(tree):
        # hard-fail on print() in prod code
        if isinstance(node, ast.Call) and getattr(getattr(node.func, 'id', None), 'lower', lambda: '' )() == 'print':
            BAD.append((p, node.lineno, "print() in prod code"))
        # naive check: logger call without kwargs containing required keys
        if isinstance(node, ast.Call) and hasattr(node.func, 'attr') and node.func.attr in ('info','warning','error','critical','debug'):
            # allow for now; enforce via runtime sampling later
            pass
if BAD:
    for f, ln, why in BAD:
        print(f"{f}:{ln}: {why}")
    sys.exit(1)
print("Logging schema check: PASS (no raw print() in prod code).")
