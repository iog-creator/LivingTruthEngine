#!/usr/bin/env python3
"""
Test SSOT metadata index system:
- Collection and validation roundtrip
- Latest copy generation
- Schema validation
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
IDX = REPORTS / "ssot_meta_index.json"

def run(cmd):
    subprocess.check_call(cmd, cwd=str(ROOT))

def test_collect_and_validate_roundtrip():
    """Test that collection and validation work together."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    # generate
    run(["python","scripts/collect_yaml_meta.py","--out", str(IDX)])
    assert IDX.exists(), "index not generated"
    # basic JSON parse
    data = json.loads(IDX.read_text(encoding="utf-8"))
    assert "rules" in data and isinstance(data["rules"], list)
    # validate via script (exit 0 on ok)
    run(["python","scripts/validate_ssot_meta_index.py"])

def test_latest_copy_exists():
    """Test that the latest copy is created."""
    latest = IDX.with_name("ssot_meta_index_latest.json")
    if not latest.exists():
        # regenerate if missing (idempotent)
        run(["python","scripts/collect_yaml_meta.py","--out", str(IDX)])
    assert latest.exists(), "latest index copy not created"
    
    # verify latest copy matches main index
    main_data = json.loads(IDX.read_text(encoding="utf-8"))
    latest_data = json.loads(latest.read_text(encoding="utf-8"))
    assert main_data == latest_data, "latest copy should match main index"

def test_schema_validation():
    """Test that the generated index passes schema validation."""
    REPORTS.mkdir(parents=True, exist_ok=True)
    run(["python","scripts/collect_yaml_meta.py","--out", str(IDX)])
    
    # Load and validate basic structure
    data = json.loads(IDX.read_text(encoding="utf-8"))
    assert "generated_at_utc" in data, "should have generation timestamp"
    assert "rules" in data, "should have rules array"
    assert "docs" in data, "should have docs array"
    assert isinstance(data["rules"], list), "rules should be array"
    assert isinstance(data["docs"], list), "docs should be array"
    
    # Validate rule structure
    for rule in data["rules"]:
        assert isinstance(rule, dict), "each rule should be object"
        assert "file" in rule, "rule should have file path"
        assert isinstance(rule["file"], str), "file should be string"
        if "description" in rule:
            assert isinstance(rule["description"], str), "description should be string"
        if "alwaysApply" in rule:
            assert isinstance(rule["alwaysApply"], bool), "alwaysApply should be boolean"
        if "ssot_meta" in rule:
            assert isinstance(rule["ssot_meta"], list), "ssot_meta should be array"
            for meta in rule["ssot_meta"]:
                assert isinstance(meta, dict), "ssot_meta entries should be objects"

def test_make_targets():
    """Test that make targets work correctly."""
    # Test meta-ci target
    run(["make", "meta-ci"])
    
    # Don't test test-meta target here - that would cause infinite recursion!
    # The test-meta target is what's running this test file

if __name__ == "__main__":
    # Run tests
    test_collect_and_validate_roundtrip()
    test_latest_copy_exists()
    test_schema_validation()
    test_make_targets()
    print("✓ All SSOT metadata tests passed")

