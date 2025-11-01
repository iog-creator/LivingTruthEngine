from modelcontextprotocol.server import Server
srv = Server("mcp-graph")

@srv.tool()
def write_claims(claims: list[dict]):
    return {"ok": True}

if __name__ == "__main__":
    srv.run()
