from modelcontextprotocol.server import Server
import requests, tempfile
from pymupdf import open as pdfopen

srv = Server("mcp-pdf")

@srv.tool()
def extract_pdf(url: str):
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(requests.get(url, timeout=30).content)
        f.flush()
        doc = pdfopen(f.name)
        text = "\n".join([page.get_text("text") for page in doc])
        return {"doc_id": url, "text": text, "pages": len(doc)}

if __name__ == "__main__":
    srv.run()
