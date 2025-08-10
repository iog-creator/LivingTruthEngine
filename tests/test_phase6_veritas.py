from __future__ import annotations

import json
from pathlib import Path

from src.ingestion_general.provenance import compute_sha256_bytes, build_merkle_root, verify_merkle_root
from src.ingestion_general.runners import VeritasRunner


def test_merkle_roundtrip() -> None:
    leaves = [b"a", b"b", b"c"]
    hashes = [compute_sha256_bytes(x) for x in leaves]
    root = build_merkle_root(hashes)
    assert root and isinstance(root, str)
    assert verify_merkle_root(hashes, root)


def test_bundle_manifest_and_proofs(tmp_path: Path) -> None:
    runner = VeritasRunner(project_root=tmp_path)
    status = runner.start(topic="Phase6 test", max_docs=1, sources=["web"])  # creates bundle + proofs
    bundle = Path(status.bundle_dir)
    assert (bundle / "manifest.json").exists()
    assert (bundle / "metrics.json").exists()
    assert (bundle / "proofs" / "source_hashes.json").exists()
    assert (bundle / "proofs" / "merkle_roots.json").exists()

    proofs = json.loads((bundle / "proofs" / "merkle_roots.json").read_text(encoding="utf-8"))
    assert proofs.get("root")
    assert proofs.get("count", 0) >= 1


def test_engine_list_and_open_bundle(tmp_path: Path) -> None:
    runner = VeritasRunner(project_root=tmp_path)
    status = runner.start(topic="Open bundle", max_docs=1, sources=["web"])  # creates bundle
    runs = runner.list_runs(limit=10)
    assert status.run_id in runs
    opened = runner.open_bundle(status.run_id)
    assert opened["manifest"]["run_id"] == status.run_id


def test_dashboard_job_runs_tab_imports() -> None:
    # Importing the dashboard should succeed and expose fastapi_app
    from src.analysis.dash_app import fastapi_app  # noqa: F401
    assert fastapi_app is not None


