import os, json, urllib.request, pytest
BASE = os.environ.get("DASH_URL","http://127.0.0.1:8050")
def get(p): 
    with urllib.request.urlopen(BASE+p, timeout=5) as r: 
        return json.loads(r.read().decode())
@pytest.mark.skipif(os.environ.get("DASH_URL") is None, reason="DASH_URL not set")
def test_health():
    assert get("/api/health")["status"] == "ok"
@pytest.mark.skipif(os.environ.get("DASH_URL") is None, reason="DASH_URL not set")
def test_ssot_snapshot_has_file():
    j = get("/api/ssot/snapshot/latest")
    assert j["status"] == "ok" and j["data"]["file"]
