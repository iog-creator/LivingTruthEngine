from modelcontextprotocol.server import Server
from sentence_transformers import CrossEncoder
import numpy as np

srv = Server("mcp-reranker")
_ce = CrossEncoder("BAAI/bge-reranker-base")

@srv.tool()
def rerank(query: str, docs: list[str]):
    pairs = [(query, d) for d in docs]
    scores = _ce.predict(pairs).tolist()
    order = list(np.argsort(scores)[::-1])
    return {"indices": order}

if __name__ == "__main__":
    srv.run()
