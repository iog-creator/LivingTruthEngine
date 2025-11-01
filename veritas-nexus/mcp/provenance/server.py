from modelcontextprotocol.server import Server
import hashlib

srv = Server("mcp-provenance")

def sha256(s:str)->str: return hashlib.sha256(s.encode()).hexdigest()

def merkle_root(hashes:list[str])->str:
    layer = hashes[:]
    if not layer: return sha256("")
    while len(layer) > 1:
        if len(layer) % 2 == 1: layer.append(layer[-1])
        layer = [sha256(layer[i]+layer[i+1]) for i in range(0,len(layer),2)]
    return layer[0]

@srv.tool()
def hash_sentences(sentences: list[str]):
    hs = [sha256(s) for s in sentences]
    root = merkle_root(hs)
    return {"hashes": hs, "merkle_root": root}

if __name__ == "__main__":
    srv.run()
