from modelcontextprotocol.server import Server
import os, requests

LM = os.getenv("LM_STUDIO_HOST","http://host.docker.internal:1234").rstrip("/")
srv = Server("mcp-llm-local")

@srv.tool()
def complete(model: str, prompt: str, temperature: float = 0.0):
    r = requests.post(f"{LM}/v1/completions", json={"model": model, "prompt": prompt, "temperature": temperature}, timeout=60)
    r.raise_for_status()
    txt = r.json()["choices"][0]["text"]
    return {"text": txt}

if __name__ == "__main__":
    srv.run()
