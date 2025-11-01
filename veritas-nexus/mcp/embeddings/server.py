from modelcontextprotocol.server import Server
from sentence_transformers import SentenceTransformer
import numpy as np

srv = Server("mcp-embeddings")
_model = SentenceTransformer("intfloat/e5-small-v2")

@srv.tool()
def embed(texts: list[str]):
    vecs = _model.encode(texts, normalize_embeddings=True).tolist()
    return {"vectors": vecs}

if __name__ == "__main__":
    srv.run()
