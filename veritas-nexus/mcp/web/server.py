from modelcontextprotocol.server import Server
import requests
from trafilatura import extract

srv = Server("mcp-web")

@srv.tool()
def fetch(url: str):
    r = requests.get(url, timeout=20, headers={"User-Agent":"veritas/0.1"})
    r.raise_for_status()
    text = extract(r.text) or ""
    return {"url": url, "html": r.text[:0], "text": text}

if __name__ == "__main__":
    srv.run()
