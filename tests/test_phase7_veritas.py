"""
Phase 7 Veritas Tests

Tests for the Generalist Ingestion Runner and bundle creation.
"""

import json
import time
from pathlib import Path
import pytest

def test_phase7_smoke_run():
    """Test basic Veritas run creation and bundle structure."""
    # Late import to avoid heavy startup in collection
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Start a Veritas run
    result = engine.start_veritas_run(
        topic="imagination podcast smoke",
        max_videos=3,
        sources=["youtube"]
    )
    
    # Parse the result
    run_data = json.loads(result)
    run_id = run_data["run_id"]
    
    # Check output directory
    out_dir = Path("/home/mccoy/Projects/NotebookLM/data/outputs/runs")
    assert out_dir.exists(), "Output directory should exist"
    
    # Wait up to 5s for writers
    time.sleep(2)
    
    # Find the bundle
    bundle_dirs = list(out_dir.glob(f"*{run_id}*.veritasrun"))
    assert bundle_dirs, "Bundle directory should be created"
    
    bundle_dir = bundle_dirs[0]
    assert bundle_dir.is_dir(), "Bundle should be a directory"
    
    # Check required files exist
    assert (bundle_dir / "manifest.json").exists(), "manifest.json should exist"
    assert (bundle_dir / "corpus.jsonl").exists(), "corpus.jsonl should exist"
    assert (bundle_dir / "merkle.json").exists(), "merkle.json should exist"
    assert (bundle_dir / "metrics.json").exists(), "metrics.json should exist"
    
    # Check proofs directory
    proofs_dir = bundle_dir / "proofs"
    assert proofs_dir.exists(), "proofs directory should exist"
    assert list(proofs_dir.glob("*.json")), "Should have JSON proof files"
    
    # Check manifest flags
    with open(bundle_dir / "manifest.json") as f:
        manifest = json.load(f)
    
    assert "flags" in manifest, "Manifest should have flags"
    assert manifest["flags"]["OCR_REQUIRED"] == "false", "OCR should be disabled by default"
    
    # Check merkle structure
    with open(bundle_dir / "merkle.json") as f:
        merkle = json.load(f)
    
    assert "root" in merkle, "Merkle should have root"
    assert "tree" in merkle, "Merkle should have tree"
    assert "leaf_count" in merkle, "Merkle should have leaf_count"
    assert merkle["leaf_count"] > 0, "Should have at least one document"
    
    # Check metrics
    with open(bundle_dir / "metrics.json") as f:
        metrics = json.load(f)
    
    assert "run_summary" in metrics, "Metrics should have run_summary"
    assert "source_distribution" in metrics, "Metrics should have source_distribution"
    assert "extraction_methods" in metrics, "Metrics should have extraction_methods"

def test_veritas_mcp_tools():
    """Test MCP tools for Veritas operations."""
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Test list_veritas_runs
    runs_result = engine.list_veritas_runs(limit=5)
    runs_data = json.loads(runs_result)
    assert "runs" in runs_data, "Should return runs list"
    
    # Test start_veritas_run
    start_result = engine.start_veritas_run(
        topic="test run",
        max_videos=2,
        sources=["web"]
    )
    start_data = json.loads(start_result)
    run_id = start_data["run_id"]
    
    # Test get_veritas_run_status
    status_result = engine.get_veritas_run_status(run_id)
    status_data = json.loads(status_result)
    assert status_data["run_id"] == run_id, "Should return correct run ID"
    assert status_data["status"] == "completed", "Run should be completed"
    
    # Test open_veritas_bundle
    bundle_result = engine.open_veritas_bundle(run_id)
    bundle_data = json.loads(bundle_result)
    assert "manifest" in bundle_data, "Should return manifest"
    assert "metrics" in bundle_data, "Should return metrics"
    assert "merkle" in bundle_data, "Should return merkle data"

def test_bundle_structure():
    """Test that bundle structure matches Phase 7 requirements."""
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Create a test run
    result = engine.start_veritas_run(
        topic="bundle structure test",
        max_videos=1,
        sources=["pdf"]
    )
    
    run_data = json.loads(result)
    run_id = run_data["run_id"]
    
    # Wait for completion
    time.sleep(1)
    
    # Get bundle
    bundle_result = engine.open_veritas_bundle(run_id)
    bundle_data = json.loads(bundle_result)
    
    # Check manifest structure
    manifest = bundle_data["manifest"]
    required_manifest_fields = ["topic", "started_at", "document_count", "flags", "documents"]
    for field in required_manifest_fields:
        assert field in manifest, f"Manifest should have {field}"
    
    # Check metrics structure
    metrics = bundle_data["metrics"]
    required_metrics_fields = ["run_summary", "source_distribution", "extraction_methods"]
    for field in required_metrics_fields:
        assert field in metrics, f"Metrics should have {field}"
    
            # Check merkle structure
        merkle = bundle_data["merkle"]
        required_merkle_fields = ["root", "tree", "leaf_count"]
        for field in required_merkle_fields:
            assert field in merkle, f"Merkle should have {field}"
    
    # Verify flags are loaded from config
    assert manifest["flags"]["HF_BURST"] == "off", "HF_BURST should be off"
    assert manifest["flags"]["OCR_REQUIRED"] == "false", "OCR_REQUIRED should be false"
    assert manifest["flags"]["PII_SCRUB"] == "standard", "PII_SCRUB should be standard"
    assert manifest["flags"]["MAX_DOCS_DEFAULT"] == 10, "MAX_DOCS_DEFAULT should be 10"

if __name__ == "__main__":
    # Run tests
    test_phase7_smoke_run()
    test_veritas_mcp_tools()
    test_bundle_structure()
    print("✅ All Phase 7 Veritas tests passed!")
