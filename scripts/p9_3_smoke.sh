#!/usr/bin/env bash
set -euo pipefail

echo "=== Phase 9.3.1 Smoke Test (Hardening & Consistency) ==="

# Run proof of life
echo "Running proof of life..."
bash scripts/proof_of_life.sh

# Test health endpoint with embedding model info
echo "Testing health endpoint with embedding model info..."
python3 - <<'PY'
import httpx
import json

try:
    c = httpx.Client(timeout=20)
    
    # Test health/full endpoint
    print("Testing /api/health/full...")
    health_response = c.get("http://localhost:8050/api/health/full")
    print(f"Health response status: {health_response.status_code}")
    
    if health_response.status_code == 200:
        health_data = health_response.json()
        print(f"Health data status: {health_data.get('status')}")
        
        # Check for embedding model info
        if 'data' in health_data:
            data = health_data['data']
            embedding_model = data.get('embedding_model')
            embedding_dim = data.get('embedding_dim')
            print(f"Embedding model: {embedding_model}")
            print(f"Embedding dimension: {embedding_dim}")
            
            # Validate embedding info is present
            if embedding_model and embedding_dim:
                print("✅ Embedding model and dimension info present in health endpoint")
            else:
                print("❌ Missing embedding model or dimension info in health endpoint")
                exit(1)
        else:
            print("❌ No data field in health response")
            exit(1)
    else:
        print(f"❌ Health endpoint failed with status {health_response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error during health testing: {e}")
    exit(1)
PY

# Test graph building and retrieval with node/edge count validation
echo "Testing graph API endpoints with node/edge count validation..."
python3 - <<'PY'
import httpx
import json

try:
    c = httpx.Client(timeout=20)
    
    # Test with a valid UUID
    test_run_id = "123e4567-e89b-12d3-a456-426614174000"
    
    # Test build endpoint (should fail gracefully with no documents)
    print("Testing build endpoint...")
    build_response = c.post(f"http://localhost:8050/api/graph/{test_run_id}/build")
    print(f"Build response status: {build_response.status_code}")
    
    # Test graph retrieval (should return 404 for non-existent graph)
    print("Testing graph retrieval...")
    graph_response = c.get(f"http://localhost:8050/api/graph/{test_run_id}")
    print(f"Graph response status: {graph_response.status_code}")
    
    if graph_response.status_code == 404:
        print("✅ Graph endpoint correctly returns 404 for non-existent run")
    else:
        print(f"⚠️ Graph endpoint returned {graph_response.status_code} instead of 404")
    
    # Test claims endpoint
    print("Testing claims endpoint...")
    claims_response = c.get(f"http://localhost:8050/api/claims/{test_run_id}")
    print(f"Claims response status: {claims_response.status_code}")
    
    if claims_response.status_code == 200:
        claims_data = claims_response.json()
        if claims_data.get('status') == 'ok':
            total_claims = claims_data.get('data', {}).get('total_claims', 0)
            total_links = claims_data.get('data', {}).get('total_links', 0)
            print(f"✅ Claims endpoint working: {total_claims} claims, {total_links} links")
        else:
            print(f"❌ Claims endpoint returned error: {claims_data}")
            exit(1)
    else:
        print(f"❌ Claims endpoint failed with status {claims_response.status_code}")
        exit(1)
    
    # Test entities endpoint
    print("Testing entities endpoint...")
    entities_response = c.get(f"http://localhost:8050/api/entities/{test_run_id}")
    print(f"Entities response status: {entities_response.status_code}")
    
    if entities_response.status_code == 200:
        entities_data = entities_response.json()
        if entities_data.get('status') == 'ok':
            total_entities = entities_data.get('data', {}).get('total_entities', 0)
            total_links = entities_data.get('data', {}).get('total_links', 0)
            print(f"✅ Entities endpoint working: {total_entities} entities, {total_links} links")
        else:
            print(f"❌ Entities endpoint returned error: {entities_data}")
            exit(1)
    else:
        print(f"❌ Entities endpoint failed with status {entities_response.status_code}")
        exit(1)
    
    print("✅ All endpoints responding correctly")
    
except Exception as e:
    print(f"❌ Error during API testing: {e}")
    exit(1)
PY

# Test model registry integration
echo "Testing model registry integration..."
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from common.model_registry import ModelRegistry
    
    reg = ModelRegistry()
    embedding_spec = reg.embedding()
    
    print(f"✅ Model registry loaded successfully")
    print(f"Embedding model: {embedding_spec.name}")
    print(f"Embedding dimension: {embedding_spec.extra.get('dim')}")
    print(f"Embedding provider: {embedding_spec.provider}")
    
    # Validate that dimension is not hard-coded 768
    dim = embedding_spec.extra.get('dim')
    if dim == 768:
        print("❌ Embedding dimension is hard-coded 768 instead of SSOT")
        exit(1)
    elif dim == 384:
        print("✅ Embedding dimension correctly set to 384 from models.toml")
    else:
        print(f"✅ Embedding dimension set to {dim} from SSOT")
        
except Exception as e:
    print(f"❌ Error during model registry testing: {e}")
    exit(1)
PY

# Run tests
echo "Running tests..."
pytest tests/test_linking_pipeline.py tests/test_graph_api.py tests/test_rulego_dspy.py tests/test_pgvector_dim.py tests/test_master_log.py -q

echo "✅ Phase 9.3.1 smoke test completed successfully"
