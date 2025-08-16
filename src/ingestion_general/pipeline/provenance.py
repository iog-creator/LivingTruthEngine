"""
Provenance Pipeline for Phase 8: Real-data ingestion
Handles provenance tracking, proof generation, and metrics collection
"""

import logging
import hashlib
import json
import os
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)


class ProvenancePipeline:
    """Provenance tracking and proof generation pipeline"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize provenance pipeline"""
        self.config = config
        self.proof_format = config.get("proof_format", "sha256")
        self.merkle_tree_depth = config.get("merkle_tree_depth", 16)

    def create_provenance_data(
        self, canonicalized_docs: List[Dict[str, Any]], run_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create complete provenance data for a run

        Args:
            canonicalized_docs: List of canonicalized documents
            run_params: Run parameters and configuration

        Returns:
            Dictionary containing all provenance data
        """
        logger.info(f"Creating provenance data for {len(canonicalized_docs)} documents")

        # Generate proofs for each document
        proofs = self._generate_document_proofs(canonicalized_docs)

        # Create merkle tree
        merkle_data = self._create_merkle_tree(proofs)

        # Generate metrics
        metrics = self._generate_metrics(canonicalized_docs, run_params)

        # Create suspects list for manual OCR
        suspects = self._identify_suspect_documents(canonicalized_docs)

        provenance_data = {
            "proofs": proofs,
            "merkle": merkle_data,
            "metrics": metrics,
            "suspects": suspects,
            "generated_at": datetime.now(UTC).isoformat(),
            "run_params": run_params,
        }

        logger.info(
            f"Provenance data created with {len(proofs)} proofs and merkle root: {merkle_data.get('root', 'N/A')}"  # noqa: E501
        )
        return provenance_data

    def _generate_document_proofs(
        self, canonicalized_docs: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Generate proofs for each document"""
        proofs = {}

        for doc in canonicalized_docs:
            doc_id = doc.get("id", "unknown")

            # Create proof data
            proof_data = {
                "document_id": doc_id,
                "source_type": doc.get("source_type", "unknown"),
                "uri": doc.get("uri", ""),
                "title": doc.get("title", ""),
                "text_hash": self._hash_text(doc.get("text", "")),
                "metadata_hash": self._hash_metadata(doc.get("metadata", {})),
                "provenance_hash": self._hash_provenance(doc.get("provenance", {})),
                "generated_at": datetime.now(UTC).isoformat(),
            }

            # Generate overall document hash
            proof_data["document_hash"] = self._hash_proof_data(proof_data)

            proofs[doc_id] = proof_data

        return proofs

    def _create_merkle_tree(self, proofs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Create merkle tree from document proofs"""
        if not proofs:
            return {"root": "", "tree": [], "depth": 0}

        # Extract document hashes
        doc_hashes = [proof["document_hash"] for proof in proofs.values()]

        # Build merkle tree
        tree = self._build_merkle_tree(doc_hashes)

        return {
            "root": tree[-1][0] if tree and tree[-1] else "",
            "tree": tree,
            "depth": len(tree),
            "leaf_count": len(doc_hashes),
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def _build_merkle_tree(self, hashes: List[str]) -> List[List[str]]:
        """Build merkle tree from list of hashes"""
        if not hashes:
            return []

        tree = [hashes]
        current_level = hashes

        while len(current_level) > 1:
            next_level = []

            # Process pairs of hashes
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    # Hash the pair
                    combined = current_level[i] + current_level[i + 1]
                    next_level.append(hashlib.sha256(combined.encode()).hexdigest())
                else:
                    # Single hash (odd number)
                    next_level.append(current_level[i])

            tree.append(next_level)
            current_level = next_level

        return tree

    def _generate_metrics(
        self, canonicalized_docs: List[Dict[str, Any]], run_params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive metrics for the run"""

        # Basic counts
        total_docs = len(canonicalized_docs)
        source_counts = {}
        extraction_method_counts = {}
        total_chars = 0
        total_words = 0

        # YouTube-specific metrics
        youtube_metrics = {
            "videos_processed": 0,
            "transcripts_fetched": 0,
            "total_duration": 0,
            "total_views": 0,
        }

        # Web-specific metrics
        web_metrics = {
            "pages_fetched": 0,
            "domains_visited": set(),
            "total_links": 0,
            "max_crawl_depth": 0,
        }

        # PDF-specific metrics
        pdf_metrics = {
            "pdfs_processed": 0,
            "ocr_attempts": 0,
            "suspect_pdfs": 0,
            "total_pages": 0,
        }

        # Process each document
        for doc in canonicalized_docs:
            source_type = doc.get("source_type", "unknown")
            source_counts[source_type] = source_counts.get(source_type, 0) + 1

            # Text metrics
            text = doc.get("text", "")
            total_chars += len(text)
            total_words += len(text.split())

            # Extraction method
            extraction_method = doc.get("provenance", {}).get(
                "extraction_method", "unknown"
            )
            extraction_method_counts[extraction_method] = (
                extraction_method_counts.get(extraction_method, 0) + 1
            )

            # Source-specific metrics
            if source_type == "youtube":
                youtube_metrics["videos_processed"] += 1
                if doc.get("text") and not doc.get("text", "").startswith(
                    "[No transcript"
                ):
                    youtube_metrics["transcripts_fetched"] += 1

                # YouTube-specific data
                youtube_data = doc.get("youtube", {})
                youtube_metrics["total_duration"] += youtube_data.get("duration", 0)
                youtube_metrics["total_views"] += youtube_data.get("view_count", 0)

            elif source_type == "web":
                web_metrics["pages_fetched"] += 1
                web_metrics["total_links"] += len(doc.get("web", {}).get("links", []))

                # Crawl depth
                crawl_depth = doc.get("provenance", {}).get("crawl_depth", 0)
                web_metrics["max_crawl_depth"] = max(
                    web_metrics["max_crawl_depth"], crawl_depth
                )

                # Domain tracking
                uri = doc.get("uri", "")
                if uri:
                    from urllib.parse import urlparse

                    domain = urlparse(uri).netloc
                    web_metrics["domains_visited"].add(domain)

            elif source_type == "pdf":
                pdf_metrics["pdfs_processed"] += 1
                pdf_metrics["total_pages"] += (
                    doc.get("pdf", {}).get("page_count", 0) or 0
                )
                pdf_metrics["ocr_attempts"] += (
                    doc.get("pdf", {}).get("ocr_attempts", 0) or 0
                )

                if doc.get("pdf", {}).get("needs_ocr", False):
                    pdf_metrics["suspect_pdfs"] += 1

        # Convert sets to lists for JSON serialization
        web_metrics["domains_visited"] = list(web_metrics["domains_visited"])

        return {
            "run_summary": {
                "total_documents": total_docs,
                "total_characters": total_chars,
                "total_words": total_words,
                "average_chars_per_doc": total_chars / total_docs
                if total_docs > 0
                else 0,
                "average_words_per_doc": total_words / total_docs
                if total_docs > 0
                else 0,
            },
            "source_distribution": source_counts,
            "extraction_methods": extraction_method_counts,
            "youtube_metrics": youtube_metrics,
            "web_metrics": web_metrics,
            "pdf_metrics": pdf_metrics,
            "run_parameters": run_params,
            "generated_at": datetime.now(UTC).isoformat(),
        }

    def _identify_suspect_documents(
        self, canonicalized_docs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Identify documents that need manual OCR or attention"""
        suspects = []

        for doc in canonicalized_docs:
            source_type = doc.get("source_type", "unknown")

            # Check for PDFs that need OCR
            if source_type == "pdf":
                pdf_data = doc.get("pdf", {})
                if pdf_data.get("needs_ocr", False):
                    suspects.append(
                        {
                            "document_id": doc.get("id"),
                            "uri": doc.get("uri"),
                            "title": doc.get("title"),
                            "reason": "needs_ocr",
                            "extraction_method": pdf_data.get("extraction_method"),
                            "char_count": pdf_data.get("char_count", 0),
                            "page_count": pdf_data.get("page_count", 0),
                        }
                    )

            # Check for documents with very low text content
            text = doc.get("text", "")
            if len(text.strip()) < 100:  # Very low content
                suspects.append(
                    {
                        "document_id": doc.get("id"),
                        "uri": doc.get("uri"),
                        "title": doc.get("title"),
                        "reason": "low_content",
                        "char_count": len(text),
                        "source_type": source_type,
                    }
                )

            # Check for error documents
            if source_type == "error" or "error" in doc.get("title", "").lower():
                suspects.append(
                    {
                        "document_id": doc.get("id"),
                        "uri": doc.get("uri"),
                        "title": doc.get("title"),
                        "reason": "extraction_error",
                        "source_type": source_type,
                    }
                )

        return suspects

    def _hash_text(self, text: str) -> str:
        """Hash text content"""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _hash_metadata(self, metadata: Dict[str, Any]) -> str:
        """Hash metadata dictionary"""
        metadata_str = json.dumps(metadata, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(metadata_str.encode("utf-8")).hexdigest()

    def _hash_provenance(self, provenance: Dict[str, Any]) -> str:
        """Hash provenance information"""
        provenance_str = json.dumps(provenance, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(provenance_str.encode("utf-8")).hexdigest()

    def _hash_proof_data(self, proof_data: Dict[str, Any]) -> str:
        """Hash proof data (excluding the document_hash field)"""
        # Create a copy without the document_hash field
        data_to_hash = {k: v for k, v in proof_data.items() if k != "document_hash"}
        data_str = json.dumps(data_to_hash, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(data_str.encode("utf-8")).hexdigest()

    def save_provenance_data(
        self, provenance_data: Dict[str, Any], output_dir: Path
    ) -> None:
        """Save provenance data to files"""

        # Create proofs directory
        proofs_dir = output_dir / "proofs"
        proofs_dir.mkdir(exist_ok=True)

        # Save individual proof files
        for doc_id, proof in provenance_data["proofs"].items():
            proof_file = proofs_dir / f"{doc_id}.json"
            with open(proof_file, "w", encoding="utf-8") as f:
                json.dump(proof, f, indent=2, ensure_ascii=False)

        # Save merkle tree
        merkle_file = output_dir / "merkle.json"
        with open(merkle_file, "w", encoding="utf-8") as f:
            json.dump(provenance_data["merkle"], f, indent=2, ensure_ascii=False)

        # Save metrics
        metrics_file = output_dir / "metrics.json"
        with open(metrics_file, "w", encoding="utf-8") as f:
            json.dump(provenance_data["metrics"], f, indent=2, ensure_ascii=False)

        # Save suspects
        suspects_file = output_dir / "suspects.json"
        with open(suspects_file, "w", encoding="utf-8") as f:
            json.dump(provenance_data["suspects"], f, indent=2, ensure_ascii=False)

        logger.info(f"Provenance data saved to {output_dir}")

        # Phase 6 compatibility: also write source_hashes.json and merkle_roots.json
        try:
            # Build a synthetic mapping of doc_id -> text hash if available
            files_map: Dict[str, str] = {}
            for doc_id, proof in provenance_data.get("proofs", {}).items():
                # Prefer included text_hash or similar field; otherwise hash proof json
                text_hash = proof.get("text_hash") if isinstance(proof, dict) else None
                if not text_hash:
                    import hashlib, json as _json

                    text_hash = hashlib.sha256(
                        _json.dumps(proof, sort_keys=True).encode("utf-8")
                    ).hexdigest()
                files_map[f"proofs/{doc_id}.json"] = text_hash

            (proofs_dir / "source_hashes.json").write_text(
                json.dumps({"files": files_map}, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            (proofs_dir / "merkle_roots.json").write_text(
                json.dumps(
                    {
                        "root": provenance_data.get("merkle", {}).get("root"),
                        "count": provenance_data.get("merkle", {}).get(
                            "leaf_count", len(files_map)
                        ),
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        except Exception as e:
            logger.warning(f"Failed to write Phase 6 compatibility proofs: {e}")

    def verify_provenance(self, bundle_path: Path) -> Dict[str, Any]:
        """Verify provenance data in a bundle"""
        verification_results = {"verified": True, "errors": [], "warnings": []}

        try:
            # Load corpus
            corpus_file = bundle_path / "corpus.jsonl"
            if not corpus_file.exists():
                verification_results["verified"] = False
                verification_results["errors"].append("corpus.jsonl not found")
                return verification_results

            # Load proofs
            proofs_dir = bundle_path / "proofs"
            if not proofs_dir.exists():
                verification_results["verified"] = False
                verification_results["errors"].append("proofs directory not found")
                return verification_results

            # Load merkle
            merkle_file = bundle_path / "merkle.json"
            if not merkle_file.exists():
                verification_results["verified"] = False
                verification_results["errors"].append("merkle.json not found")
                return verification_results

            # Verify each document
            with open(corpus_file, "r", encoding="utf-8") as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        doc = json.loads(line.strip())
                        doc_id = doc.get("id")

                        # Check if proof exists
                        proof_file = proofs_dir / f"{doc_id}.json"
                        if not proof_file.exists():
                            verification_results["verified"] = False
                            verification_results["errors"].append(
                                f"Proof missing for document {doc_id}"
                            )
                            continue

                        # Load and verify proof
                        with open(proof_file, "r", encoding="utf-8") as pf:
                            proof = json.load(pf)

                        # Verify text hash
                        expected_hash = self._hash_text(doc.get("text", ""))
                        if proof.get("text_hash") != expected_hash:
                            verification_results["verified"] = False
                            verification_results["errors"].append(
                                f"Text hash mismatch for document {doc_id}"
                            )

                    except json.JSONDecodeError as e:
                        verification_results["verified"] = False
                        verification_results["errors"].append(
                            f"Invalid JSON in corpus.jsonl line {line_num}: {e}"
                        )
                    except Exception as e:
                        verification_results["verified"] = False
                        verification_results["errors"].append(
                            f"Error verifying document at line {line_num}: {e}"
                        )

            # Verify merkle tree
            with open(merkle_file, "r", encoding="utf-8") as f:
                merkle_data = json.load(f)

            # Basic merkle verification
            if not merkle_data.get("root"):
                verification_results["verified"] = False
                verification_results["errors"].append("Merkle root is empty")

        except Exception as e:
            verification_results["verified"] = False
            verification_results["errors"].append(f"Error during verification: {e}")

        return verification_results
