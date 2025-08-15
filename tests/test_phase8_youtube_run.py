"""
Phase 8 YouTube Channel Ingestion Tests

Tests for real data ingestion from YouTube channels with depth-limited expansion,
OCR/JS toggles, and dashboard controls.
"""

import json
import time
from pathlib import Path
import pytest

def test_phase8_youtube_channel_run():
    """Test YouTube channel ingestion with real data and depth-limited expansion."""
    # Late import to avoid heavy startup in collection
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Start a YouTube channel run with Phase 8 parameters
    result = engine.start_veritas_run(
        topic="imagination podcast phase8 test",
        channel_url="https://www.youtube.com/@imaginationpodcastofficial",
        selection="oldest",
        max_videos=2,
        crawl_depth=1,
        allow_domains=["youtube.com", "youtu.be", "www.youtube.com"],
        transcript_pref="yt_api",
        ocr_mode="off",
        auto_retry_attempts=2,
        sources=["youtube"]
    )
    
    # Parse the result
    run_data = json.loads(result)
    run_id = run_data["run_id"]
    
    print(f"Started Phase 8 run: {run_id}")
    
    # Check output directory
    out_dir = Path(__file__).parent.parent / "data/outputs/runs"
    assert out_dir.exists(), "Output directory should exist"
    
    # Wait up to 10s for writers (longer for real data)
    time.sleep(5)
    
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
    
    # Check manifest flags for Phase 8 features
    with open(bundle_dir / "manifest.json") as f:
        manifest = json.load(f)
    
    assert "flags" in manifest, "Manifest should have flags"
    assert "channel_url" in manifest, "Manifest should have channel_url"
    assert "selection" in manifest, "Manifest should have selection"
    assert "crawl_depth" in manifest, "Manifest should have crawl_depth"
    assert "ocr_mode" in manifest, "Manifest should have ocr_mode"
    
    # Verify Phase 8 specific flags
    assert manifest["channel_url"] == "https://www.youtube.com/@imaginationpodcastofficial"
    assert manifest["selection"] == "oldest"
    assert manifest["crawl_depth"] == 1
    assert manifest["ocr_mode"] == "off"
    
    # Check merkle structure
    with open(bundle_dir / "merkle.json") as f:
        merkle = json.load(f)
    
    assert "root" in merkle, "Merkle should have root"
    assert "tree" in merkle, "Merkle should have tree"
    assert "leaf_count" in merkle, "Merkle should have leaf_count"
    assert merkle["leaf_count"] > 0, "Should have at least one document"
    assert merkle["root"] != "", "Merkle root should not be empty"
    
    # Check metrics
    with open(bundle_dir / "metrics.json") as f:
        metrics = json.load(f)
    
    assert "run_summary" in metrics, "Metrics should have run_summary"
    assert "source_distribution" in metrics, "Metrics should have source_distribution"
    assert "extraction_methods" in metrics, "Metrics should have extraction_methods"
    assert "youtube_metrics" in metrics, "Metrics should have youtube_metrics"
    assert "run_parameters" in metrics, "Metrics should have run_parameters"
    
    # Check corpus for real content
    with open(bundle_dir / "corpus.jsonl") as f:
        corpus_lines = f.readlines()
    
    assert len(corpus_lines) >= 2, "Should have at least 2 documents (transcripts)"
    
    # Parse corpus and check for real content
    youtube_docs = 0
    web_docs = 0
    
    for line in corpus_lines:
        doc = json.loads(line.strip())
        assert "id" in doc, "Document should have id"
        assert "source_type" in doc, "Document should have source_type"
        assert "text" in doc, "Document should have text"
        assert len(doc["text"]) > 10, "Document should have some content"
        
        if doc["source_type"] == "youtube":
            youtube_docs += 1
        elif doc["source_type"] == "web":
            web_docs += 1
    
    assert youtube_docs >= 2, "Should have at least 2 YouTube transcripts"
    # May have web docs from depth expansion, but not required for this test
    
    print(f"✅ Phase 8 test passed: {youtube_docs} YouTube docs, {web_docs} web docs")

def test_phase8_mcp_tools():
    """Test MCP tools for Phase 8 YouTube operations."""
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Test list_veritas_runs
    runs_result = engine.list_veritas_runs(limit=5)
    runs_data = json.loads(runs_result)
    assert "runs" in runs_data, "Should return runs list"
    
    # Test start_veritas_run with Phase 8 parameters
    start_result = engine.start_veritas_run(
        topic="phase8 mcp test",
        channel_url="https://www.youtube.com/@imaginationpodcastofficial",
        selection="newest",
        max_videos=1,
        crawl_depth=0,  # No expansion
        ocr_mode="off",
        sources=["youtube"]
    )
    start_data = json.loads(start_result)
    run_id = start_data["run_id"]
    
    # Test get_veritas_run_status
    time.sleep(2)  # Wait for processing
    status_result = engine.get_veritas_run_status(run_id)
    status_data = json.loads(status_result)
    assert "status" in status_data, "Should return status"
    
    # Test open_veritas_bundle
    bundle_result = engine.open_veritas_bundle(run_id)
    bundle_data = json.loads(bundle_result)
    assert "manifest" in bundle_data, "Should return manifest"
    assert "metrics" in bundle_data, "Should return metrics"
    assert "merkle" in bundle_data, "Should return merkle"

def test_phase8_bundle_structure():
    """Test complete bundle structure for Phase 8 features."""
    from src.mcp_servers.living_truth_fastmcp_server import LivingTruthEngine
    
    engine = LivingTruthEngine()
    
    # Start a run to test bundle structure
    result = engine.start_veritas_run(
        topic="phase8 bundle test",
        channel_url="https://www.youtube.com/@imaginationpodcastofficial",
        selection="oldest",
        max_videos=1,
        crawl_depth=1,
        ocr_mode="off",
        sources=["youtube"]
    )
    
    run_data = json.loads(result)
    run_id = run_data["run_id"]
    
    time.sleep(3)  # Wait for processing
    
    # Open the bundle
    bundle_result = engine.open_veritas_bundle(run_id)
    bundle_data = json.loads(bundle_result)
    
    # Check manifest structure
    manifest = bundle_data["manifest"]
    required_fields = [
        "run_id", "topic", "channel_url", "selection", "max_videos",
        "crawl_depth", "ocr_mode", "flags", "documents", "started_at"
    ]
    
    for field in required_fields:
        assert field in manifest, f"Manifest should have {field}"
    
    # Check metrics structure
    metrics = bundle_data["metrics"]
    required_metrics = [
        "run_summary", "source_distribution", "extraction_methods", 
        "youtube_metrics", "run_parameters"
    ]
    
    for metric in required_metrics:
        assert metric in metrics, f"Metrics should have {metric}"
    
    # Check merkle structure
    merkle = bundle_data["merkle"]
    assert "root" in merkle, "Merkle should have root"
    assert "tree" in merkle, "Merkle should have tree"
    assert "leaf_count" in merkle, "Merkle should have leaf_count"
    assert merkle["root"] != "", "Merkle root should not be empty"
    
    print(f"✅ Phase 8 bundle structure test passed for run: {run_id}")

if __name__ == "__main__":
    # Run tests directly
    test_phase8_youtube_channel_run()
    test_phase8_mcp_tools()
    test_phase8_bundle_structure()
    print("✅ All Phase 8 tests passed!")
