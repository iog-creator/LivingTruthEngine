#!/usr/bin/env python
import json, sys, traceback
try:
    from src.mcp_servers.phase9_mcp_server import Phase9MCPServer
    s = Phase9MCPServer()
    tools = []
    for name in dir(s):
        if name.startswith("_"): continue
        attr = getattr(s, name)
        if callable(attr):
            tools.append(name)
    print(json.dumps({"status":"ok","tools":sorted(tools)}))
except Exception as e:
    traceback.print_exc()
    print(json.dumps({"status":"error","error":str(e)}))
    sys.exit(0)
