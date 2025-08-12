import psycopg
import numpy as np
from typing import List, Dict, Any

class PgVectorStore:
    def __init__(self, dsn: str, embedder=None):
        self.db = psycopg.connect(dsn, autocommit=True)
        self.embedder = embedder

    def upsert_docs(self, run_id: str, docs: List[Dict[str, Any]]):
        """Upsert documents and their embeddings to pgvector store"""
        with self.db.cursor() as cur:
            for d in docs:
                # Insert document
                cur.execute(
                    "INSERT INTO lte.documents(id,run_id,source_type,text,meta) "
                    "VALUES (%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET text=EXCLUDED.text",
                    (d["id"], run_id, d["source_type"], d["text"], d.get("meta", {}))
                )
                
                # Generate and insert embedding if embedder is available
                if self.embedder:
                    vec = self.embedder.encode(d["text"])
                    cur.execute(
                        "INSERT INTO lte.doc_embeddings(id,doc_id,run_id,embedding) "
                        "VALUES (%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET embedding=EXCLUDED.embedding",
                        (d["id"], d["id"], run_id, np.array(vec))
                    )

    def search(self, run_id: str, query: str, k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        if not self.embedder:
            raise ValueError("Embedder not available for search")
            
        qvec = np.array(self.embedder.encode(query))
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT d.id,d.text,d.meta "
                "FROM lte.doc_embeddings e JOIN lte.documents d ON d.id=e.doc_id "
                "WHERE e.run_id=%s ORDER BY e.embedding <#> %s LIMIT %s",
                (run_id, qvec, k)
            )
            return [{"id": i, "text": t, "meta": m} for (i, t, m) in cur.fetchall()]
    
    def get_documents(self, run_id: str) -> List[Dict[str, Any]]:
        """Get all documents for a run"""
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT id, source_type, text, meta FROM lte.documents WHERE run_id = %s",
                (run_id,)
            )
            return [{"id": i, "source_type": s, "text": t, "meta": m} 
                   for (i, s, t, m) in cur.fetchall()]
