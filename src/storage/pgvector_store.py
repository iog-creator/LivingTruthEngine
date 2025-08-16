import psycopg2
import psycopg2.extras
import numpy as np
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class PgVectorStore:
    def __init__(self, dsn: str, embedder=None):
        self.db = psycopg2.connect(dsn)
        self.db.autocommit = True
        self.embedder = embedder
        self._embedding_dim = None
        self._model_key = None
        self._load_embedding_config()

    def _load_embedding_config(self):
        """Load embedding configuration from model registry (SSOT)"""
        try:
            from src.common.model_registry import ModelRegistry

            reg = ModelRegistry()
            embedding_spec = reg.embedding()
            self._embedding_dim = embedding_spec.extra.get("dim")
            self._model_key = "default"  # Default model key
            logger.info(
                f"Loaded embedding config: model_key={self._model_key}, dim={self._embedding_dim}"  # noqa: E501
            )
        except Exception as e:
            logger.error(f"Failed to load embedding config from model registry: {e}")
            # Fallback to default dimension (should be avoided in production)
            self._embedding_dim = 384  # Default from models.toml
            self._model_key = "default"
            logger.warning(
                f"Using fallback embedding config: dim={self._embedding_dim}"
            )

    def _validate_embedding_dimension(self, embedding: np.ndarray) -> bool:
        """Validate embedding dimension matches SSOT configuration"""
        if self._embedding_dim is None:
            logger.error("Embedding dimension not configured from model registry")
            return False

        if embedding.shape[0] != self._embedding_dim:
            logger.error(
                f"Embedding dimension mismatch: expected {self._embedding_dim}, got {embedding.shape[0]}"  # noqa: E501
            )
            return False

        return True

    def validate_database_schema(self) -> Dict[str, Any]:
        """Validate database schema matches model registry configuration"""
        try:
            with self.db.cursor() as cur:
                # Check if doc_embeddings table has model-aware columns
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.columns 
                        WHERE table_schema = 'lte' 
                        AND table_name = 'doc_embeddings'
                        AND column_name = 'model_key'
                    )
                """)
                model_key_exists = cur.fetchone()[0]

                if not model_key_exists:
                    return {
                        "valid": False,
                        "error": "model_key column not found in doc_embeddings table",
                        "remediation": "Run migration script: docker/initdb/004_model_aware_embeddings_simple.sql",  # noqa: E501
                    }

                # Check for dimension mismatches in existing embeddings
                cur.execute("""
                    SELECT DISTINCT embedding_dim, model_key, COUNT(*) as count
                    FROM lte.doc_embeddings
                    WHERE embedding_dim IS NOT NULL
                    GROUP BY embedding_dim, model_key
                """)
                existing_dims = cur.fetchall()

                # Check if current model dimension exists in database
                current_dim_exists = any(
                    dim == self._embedding_dim and model == self._model_key
                    for dim, model, count in existing_dims
                )

                return {
                    "valid": True,
                    "model_aware_columns": True,
                    "current_model_key": self._model_key,
                    "current_embedding_dim": self._embedding_dim,
                    "existing_dimensions": [
                        {"dim": dim, "model": model, "count": count}
                        for dim, model, count in existing_dims
                    ],
                    "current_dim_exists": current_dim_exists,
                    "dim_mismatch": not current_dim_exists and len(existing_dims) > 0,
                }

        except Exception as e:
            logger.error(f"Database schema validation failed: {e}")
            return {
                "valid": False,
                "error": str(e),
                "remediation": "Check database connection and schema",
            }

    def upsert_docs(self, run_id: str, docs: List[Dict[str, Any]]):
        """Upsert documents and their embeddings to pgvector store"""
        with self.db.cursor() as cur:
            for d in docs:
                # Insert document using actual schema columns
                cur.execute(
                    "INSERT INTO lte.documents(run_id,source_type,uri,title,text_len,sha256) "  # noqa: E501
                    "VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (run_id,source_type,uri,shard_no) DO UPDATE SET title=EXCLUDED.title,text_len=EXCLUDED.text_len,sha256=EXCLUDED.sha256",  # noqa: E501
                    (
                        run_id,
                        d["source_type"],
                        d.get("uri", ""),
                        d.get("title", ""),
                        len(d.get("text", "")),
                        d.get("id", ""),
                    ),
                )

                # Get the document ID for embedding storage
                cur.execute(
                    "SELECT id FROM lte.documents WHERE run_id = %s AND source_type = %s AND uri = %s",  # noqa: E501
                    (run_id, d["source_type"], d.get("uri", "")),
                )
                doc_id = cur.fetchone()[0]

                # Generate and insert embedding if embedder is available
                if self.embedder:
                    vec = np.array(self.embedder.encode(d["text"]))
                    if not self._validate_embedding_dimension(vec):
                        raise ValueError(
                            f"Embedding dimension validation failed for document {doc_id}"  # noqa: E501
                        )

                    # Use model-aware embedding table (current schema)
                    cur.execute(
                        "INSERT INTO lte.doc_embeddings(doc_id,embedding_text,model,model_key,embedding_dim) "  # noqa: E501
                        "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (doc_id) DO UPDATE SET embedding_text=EXCLUDED.embedding_text,model=EXCLUDED.model,model_key=EXCLUDED.model_key,embedding_dim=EXCLUDED.embedding_dim",  # noqa: E501
                        (
                            doc_id,
                            str(vec.tolist()),
                            "sentence-transformers/all-MiniLM-L6-v2",
                            self._model_key,
                            self._embedding_dim,
                        ),
                    )

    def search(self, run_id: str, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        if not self.embedder:
            raise ValueError("Embedder not available for search")

        qvec = np.array(self.embedder.encode(query))
        if not self._validate_embedding_dimension(qvec):
            raise ValueError("Query embedding dimension validation failed")

        with self.db.cursor() as cur:
            cur.execute(
                "SELECT d.id,d.text,d.meta "
                "FROM lte.doc_embeddings e JOIN lte.documents d ON d.id=e.doc_id "
                "WHERE e.model_key=%s AND e.embedding_dim=%s ORDER BY e.embedding_text <#> %s LIMIT %s",  # noqa: E501
                (self._model_key, self._embedding_dim, str(qvec.tolist()), k),
            )
            return [{"id": i, "text": t, "meta": m} for (i, t, m) in cur.fetchall()]

    def get_documents(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a run"""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, source_type, text, meta FROM lte.documents WHERE run_id = %s",  # noqa: E501
                (run_id,),
            )
            return [
                {"id": i, "source_type": s, "text": t, "meta": m}
                for (i, s, t, m) in cur.fetchall()
            ]

    # Phase 9.3: Graph functionality methods

    def store_document(self, doc: Dict[str, Any]) -> int:
        """Store a document and return its ID. Uses UPSERT to handle duplicates."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.documents (run_id, source_type, uri, title, published_at, shard_no, text_len, sha256) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) "
                "ON CONFLICT (run_id, source_type, uri, shard_no) DO UPDATE SET "
                "title = EXCLUDED.title, "
                "published_at = EXCLUDED.published_at, "
                "text_len = EXCLUDED.text_len, "
                "sha256 = EXCLUDED.sha256 "
                "RETURNING id",
                (
                    doc.get("run_id"),
                    doc.get("source_type"),
                    doc.get("uri"),
                    doc.get("title"),
                    doc.get("published_at"),
                    doc.get("shard_no", 1),
                    doc.get("text_len"),
                    doc.get("sha256"),
                ),
            )
            return cur.fetchone()[0]

    def store_entity(self, doc_id: int, entity: Dict[str, Any]) -> int:
        """Store an entity and return its ID. Uses UPSERT to handle duplicates."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.entities (doc_id, type, value, span_start, span_end, conf) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s, %s) "
                "ON CONFLICT DO NOTHING RETURNING id",
                (
                    doc_id,
                    entity["type"],
                    entity["value"],
                    entity.get("span_start"),
                    entity.get("span_end"),
                    entity.get("conf", 1.0),
                ),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                # If conflict occurred, get the existing ID
                cur.execute(
                    "SELECT id FROM lte.entities WHERE doc_id = %s AND type = %s AND value = %s",  # noqa: E501
                    (doc_id, entity["type"], entity["value"]),
                )
                return cur.fetchone()[0]

    def store_claim(self, doc_id: int, claim: Dict[str, Any]) -> int:
        """Store a claim and return its ID. Uses UPSERT to handle duplicates."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.claims (doc_id, text, normalized, conf) "
                "VALUES (%s, %s, %s, %s) "
                "ON CONFLICT DO NOTHING RETURNING id",
                (
                    doc_id,
                    claim["text"],
                    claim.get("normalized"),
                    claim.get("conf", 1.0),
                ),
            )
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                # If conflict occurred, get the existing ID
                cur.execute(
                    "SELECT id FROM lte.claims WHERE doc_id = %s AND text = %s",
                    (doc_id, claim["text"]),
                )
                return cur.fetchone()[0]

    def store_entity_embedding(self, entity_id: int, embedding: np.ndarray) -> None:
        """Store an entity embedding with SSOT validation. Uses UPSERT to handle duplicates."""  # noqa: E501
        if not self._validate_embedding_dimension(embedding):
            raise ValueError(
                f"Entity embedding dimension validation failed for entity {entity_id}"
            )

        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.claim_embeddings (claim_id, embedding, model, model_key, dim) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (claim_id) DO UPDATE SET "
                "embedding = EXCLUDED.embedding, "
                "model = EXCLUDED.model, "
                "model_key = EXCLUDED.model_key, "
                "dim = EXCLUDED.dim",
                (
                    entity_id,
                    embedding.tolist(),
                    "sentence-transformers/all-MiniLM-L6-v2",
                    self._model_key,
                    self._embedding_dim,
                ),
            )

    def store_claim_embedding(self, claim_id: int, embedding: np.ndarray) -> None:
        """Store a claim embedding with SSOT validation. Uses UPSERT to handle duplicates."""  # noqa: E501
        if not self._validate_embedding_dimension(embedding):
            raise ValueError(
                f"Claim embedding dimension validation failed for claim {claim_id}"
            )

        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.claim_embeddings (claim_id, embedding, model, model_key, dim) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (claim_id) DO UPDATE SET "
                "embedding = EXCLUDED.embedding, "
                "model = EXCLUDED.model, "
                "model_key = EXCLUDED.model_key, "
                "dim = EXCLUDED.dim",
                (
                    claim_id,
                    embedding.tolist(),
                    "sentence-transformers/all-MiniLM-L6-v2",
                    self._model_key,
                    self._embedding_dim,
                ),
            )

    def store_entity_link(self, link: Dict[str, Any]) -> None:
        """Store an entity link. Uses UPSERT to handle duplicates."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.entity_links (left_entity_id, right_entity_id, link_type, score, method) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (left_entity_id, right_entity_id, link_type) DO UPDATE SET "  # noqa: E501
                "score = EXCLUDED.score, "
                "method = EXCLUDED.method",
                (
                    link["left_entity_id"],
                    link["right_entity_id"],
                    link["link_type"],
                    link["score"],
                    link["method"],
                ),
            )

    def store_claim_link(self, link: Dict[str, Any]) -> None:
        """Store a claim link. Uses UPSERT to handle duplicates."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.claim_links (left_claim_id, right_claim_id, link_type, score, method) "  # noqa: E501
                "VALUES (%s, %s, %s, %s, %s) "
                "ON CONFLICT (left_claim_id, right_claim_id, link_type) DO UPDATE SET "
                "score = EXCLUDED.score, "
                "method = EXCLUDED.method",
                (
                    link["left_claim_id"],
                    link["right_claim_id"],
                    link["link_type"],
                    link["score"],
                    link["method"],
                ),
            )

    def get_entities_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all entities for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT e.id, e.type, e.value, e.span_start, e.span_end, e.conf, e.created_at "  # noqa: E501
                "FROM lte.entities e "
                "JOIN lte.documents d ON e.doc_id = d.id "
                "WHERE d.run_id = %s",
                (run_id,),
            )
            return [
                {
                    "id": i,
                    "type": t,
                    "value": v,
                    "span_start": ss,
                    "span_end": se,
                    "conf": c,
                    "created_at": ca,
                }
                for (i, t, v, ss, se, c, ca) in cur.fetchall()
            ]

    def get_claims_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all claims for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT c.id, c.text, c.normalized, c.conf, c.created_at "
                "FROM lte.claims c "
                "JOIN lte.documents d ON c.doc_id = d.id "
                "WHERE d.run_id = %s",
                (run_id,),
            )
            return [
                {"id": i, "text": t, "normalized": n, "conf": c, "created_at": ca}
                for (i, t, n, c, ca) in cur.fetchall()
            ]

    def get_entity_links_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all entity links for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT el.id, el.left_entity_id, el.right_entity_id, el.link_type, el.score, el.method, el.created_at "  # noqa: E501
                "FROM lte.entity_links el "
                "JOIN lte.entities e1 ON el.left_entity_id = e1.id "
                "JOIN lte.entities e2 ON el.right_entity_id = e2.id "
                "JOIN lte.documents d1 ON e1.doc_id = d1.id "
                "JOIN lte.documents d2 ON e2.doc_id = d2.id "
                "WHERE d1.run_id = %s AND d2.run_id = %s",
                (run_id, run_id),
            )
            return [
                {
                    "id": i,
                    "left_entity_id": lei,
                    "right_entity_id": rei,
                    "link_type": lt,
                    "score": s,
                    "method": m,
                    "created_at": ca,
                }
                for (i, lei, rei, lt, s, m, ca) in cur.fetchall()
            ]

    def get_claim_links_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all claim links for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT cl.id, cl.left_claim_id, cl.right_claim_id, cl.link_type, cl.score, cl.method, cl.created_at "  # noqa: E501
                "FROM lte.claim_links cl "
                "JOIN lte.claims c1 ON cl.left_claim_id = c1.id "
                "JOIN lte.claims c2 ON cl.right_claim_id = c2.id "
                "JOIN lte.documents d1 ON c1.doc_id = d1.id "
                "JOIN lte.documents d2 ON c2.doc_id = d2.id "
                "WHERE d1.run_id = %s AND d2.run_id = %s",
                (run_id, run_id),
            )
            return [
                {
                    "id": i,
                    "left_claim_id": lci,
                    "right_claim_id": rci,
                    "link_type": lt,
                    "score": s,
                    "method": m,
                    "created_at": ca,
                }
                for (i, lci, rci, lt, s, m, ca) in cur.fetchall()
            ]

    def get_documents_by_run(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a run with full metadata."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, run_id, source_type, uri, title, published_at, shard_no, text_len, sha256, created_at "  # noqa: E501
                "FROM lte.documents WHERE run_id = %s",
                (run_id,),
            )
            return [
                {
                    "id": i,
                    "run_id": ri,
                    "source_type": st,
                    "uri": u,
                    "title": t,
                    "published_at": pa,
                    "shard_no": sn,
                    "text_len": tl,
                    "sha256": s,
                    "created_at": ca,
                }
                for (i, ri, st, u, t, pa, sn, tl, s, ca) in cur.fetchall()
            ]

    def get_run_details(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get run details including document count and metadata."""
        with self.db.cursor() as cur:
            # Check if run exists by looking for documents
            cur.execute(
                "SELECT COUNT(*) as doc_count, MIN(created_at) as start_time, MAX(created_at) as end_time "  # noqa: E501
                "FROM lte.documents WHERE run_id = %s",
                (run_id,),
            )
            result = cur.fetchone()

            if not result or result[0] == 0:
                return None

            doc_count, start_time, end_time = result

            # Get additional run metadata
            cur.execute(
                "SELECT DISTINCT source_type FROM lte.documents WHERE run_id = %s",
                (run_id,),
            )
            source_types = [row[0] for row in cur.fetchall()]

            return {
                "run_id": run_id,
                "document_count": doc_count,
                "start_time": start_time,
                "end_time": end_time,
                "source_types": source_types,
                "status": "completed" if end_time else "in_progress",
            }

    def store_graph_snapshot(self, run_id: str, graph: Dict[str, Any]) -> None:
        """Store a graph snapshot for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lte.graph_snapshots (run_id, payload_json) VALUES (%s, %s)",  # noqa: E501
                (run_id, psycopg2.extras.Json(graph)),
            )

    def get_graph_snapshot(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get the latest graph snapshot for a run."""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT payload_json FROM lte.graph_snapshots WHERE run_id = %s ORDER BY created_at DESC LIMIT 1",  # noqa: E501
                (run_id,),
            )
            result = cur.fetchone()
            return result[0] if result else None

    def clear_run_data(self, run_id: str) -> None:
        """Clear all data for a specific run (for rebuild functionality)."""
        with self.db.cursor() as cur:
            # Delete in order to respect foreign key constraints
            cur.execute("DELETE FROM lte.graph_snapshots WHERE run_id = %s", (run_id,))
            cur.execute(
                "DELETE FROM lte.claim_links WHERE left_claim_id IN (SELECT c.id FROM lte.claims c JOIN lte.documents d ON c.doc_id = d.id WHERE d.run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.claim_links WHERE right_claim_id IN (SELECT c.id FROM lte.claims c JOIN lte.documents d ON c.doc_id = d.id WHERE d.run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.entity_links WHERE left_entity_id IN (SELECT e.id FROM lte.entities e JOIN lte.documents d ON e.doc_id = d.id WHERE d.run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.entity_links WHERE right_entity_id IN (SELECT e.id FROM lte.entities e JOIN lte.documents d ON e.doc_id = d.id WHERE d.run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.claim_embeddings WHERE claim_id IN (SELECT c.id FROM lte.claims c JOIN lte.documents d ON c.doc_id = d.id WHERE d.run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.entities WHERE doc_id IN (SELECT id FROM lte.documents WHERE run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.claims WHERE doc_id IN (SELECT id FROM lte.documents WHERE run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute(
                "DELETE FROM lte.doc_embeddings WHERE doc_id IN (SELECT id FROM lte.documents WHERE run_id = %s)",  # noqa: E501
                (run_id,),
            )
            cur.execute("DELETE FROM lte.documents WHERE run_id = %s", (run_id,))
