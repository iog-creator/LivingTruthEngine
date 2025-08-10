"""
Living Truth Engine - Hybrid Retrieval and Reranking System
Biblical Forensic System for Evidence-Based Information Retrieval
Migrated from living_truth_agent to LivingTruthEngine architecture
"""

import os
import logging
import json
import re
import numpy as np
import requests
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import psycopg2
from psycopg2.extras import RealDictCursor
import redis

# LangChain imports
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.vectorstores.pgvector import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.base import Embeddings

# LivingTruthEngine configuration
from src.config import get_config

# Setup logging
config = get_config()
logging.basicConfig(
    level=getattr(logging, config.monitoring.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOGS_DIR / "retrieval.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Reranking imports
try:
    from cohere import Client as CohereClient
    COHERE_AVAILABLE = True
except ImportError:
    COHERE_AVAILABLE = False
    logger.warning("Cohere not available for reranking")

class LMStudioEmbeddings(Embeddings):
    """Custom embeddings class for LM Studio embedding models."""
    
    def __init__(self, model_name: str, api_url: str = None):
        self.model_name = model_name
        self.api_url = api_url or config.model.LMSTUDIO_EMBEDDING_URL
        self.dimension = 1536  # Qwen3 embedding dimension
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using LM Studio."""
        logger.info(f"Using LM Studio embeddings with model: {self.model_name}")
        embeddings = []
        for i, text in enumerate(texts):
            logger.info(f"Embedding document {i+1}/{len(texts)} using LM Studio")
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "input": text,
                    "encoding_format": "float"
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            embedding = result["data"][0]["embedding"]
            embeddings.append(embedding)
            logger.info(f"Successfully embedded document {i+1} with {len(embedding)} dimensions")
        
        return embeddings
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query using LM Studio."""
        logger.info(f"Embedding query using LM Studio: {text[:50]}...")
        response = requests.post(
            self.api_url,
            json={
                "model": self.model_name,
                "input": text,
                "encoding_format": "float"
            },
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        embedding = result["data"][0]["embedding"]
        logger.info(f"Successfully embedded query with {len(embedding)} dimensions")
        return embedding

class BiblicalReranker:
    """Biblical evidence reranker for survivor testimony analysis."""
    
    def __init__(self):
        # Enhanced boost patterns based on Grok's suggestions
        self.biblical_boost_patterns = {
            "survivor_testimony": {
                "patterns": [
                    r"survivor", r"testimony", r"witness", r"victim", r"abuse",
                    r"trauma", r"healing", r"recovery", r"justice", r"truth"
                ],
                "boost": 0.4
            },
            "biblical_evidence": {
                "patterns": [
                    r"bible", r"scripture", r"gospel", r"psalm", r"proverb",
                    r"leviticus", r"kings", r"jeremiah", r"ezekiel", r"revelation"
                ],
                "boost": 0.3
            },
            "elite_networks": {
                "patterns": [
                    r"elite", r"network", r"organization", r"institution",
                    r"government", r"corporate", r"financial", r"political"
                ],
                "boost": 0.2
            },
            "historical_corroboration": {
                "patterns": [
                    r"historical", r"evidence", r"document", r"record",
                    r"archive", r"investigation", r"forensic", r"analysis"
                ],
                "boost": 0.2
            }
        }
    
    def rerank_documents(self, documents: List[Document], query: str) -> List[Tuple[Document, float]]:
        """Rerank documents based on Biblical forensic relevance."""
        scored_documents = []
        
        for doc in documents:
            score = self._calculate_biblical_score(doc, query)
            scored_documents.append((doc, score))
        
        # Sort by score (highest first)
        scored_documents.sort(key=lambda x: x[1], reverse=True)
        return scored_documents
    
    def _calculate_biblical_score(self, document: Document, query: str) -> float:
        """Calculate Biblical forensic relevance score."""
        content = document.page_content.lower()
        query_lower = query.lower()
        
        # Base score from original ranking
        base_score = getattr(document, 'metadata', {}).get('score', 0.5)
        
        # Calculate pattern boosts
        pattern_score = 0.0
        for category, config in self.biblical_boost_patterns.items():
            category_score = self._calculate_pattern_boost(content, category)
            pattern_score += category_score
        
        # Calculate query relevance
        query_relevance = self._calculate_query_relevance(content, query_lower)
        
        # Combine scores with weights
        final_score = (
            base_score * 0.4 +
            pattern_score * 0.4 +
            query_relevance * 0.2
        )
        
        return min(final_score, 1.0)  # Cap at 1.0
    
    def _calculate_pattern_boost(self, content: str, pattern_category: str) -> float:
        """Calculate boost based on pattern category."""
        if pattern_category not in self.biblical_boost_patterns:
            return 0.0
        
        config = self.biblical_boost_patterns[pattern_category]
        patterns = config["patterns"]
        boost = config["boost"]
        
        matches = 0
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                matches += 1
        
        return (matches / len(patterns)) * boost
    
    def _calculate_query_relevance(self, content: str, query: str) -> float:
        """Calculate relevance between content and query."""
        query_words = set(query.split())
        content_words = set(content.split())
        
        if not query_words:
            return 0.0
        
        intersection = query_words.intersection(content_words)
        return len(intersection) / len(query_words)

class HybridRetriever:
    """Hybrid retriever combining vector search, keyword search, and Biblical reranking."""
    
    def __init__(self, task_type: str = "notebook_agent"):
        # Use dynamic embedding selector
        self.task_type = task_type
        self.config = get_config()
        
        # Initialize embeddings
        self.qwen3_embeddings = LMStudioEmbeddings(
            config.model.LMSTUDIO_EMBEDDING_MODEL_QWEN3
        )
        self.minilm_embeddings = LMStudioEmbeddings(
            config.model.LMSTUDIO_EMBEDDING_MODEL_MINILM
        )
        
        # Initialize reranker
        self.biblical_reranker = BiblicalReranker()
        
        # Setup database connections
        self._setup_database()
        
        # Initialize retrievers
        self.vector_retriever = None
        self.keyword_retriever = None
        self.ensemble_retriever = None
        
        logger.info("✅ HybridRetriever initialized successfully")
    
    def _setup_database(self):
        """Setup database connections."""
        try:
            # PostgreSQL connection for vector store
            self.pg_connection_string = self.config.database.postgres_connection_string
            
            # Redis connection for caching
            self.redis_client = redis.Redis(
                host=self.config.database.REDIS_HOST,
                port=self.config.database.REDIS_PORT,
                db=self.config.database.REDIS_DB,
                decode_responses=True
            )
            
            logger.info("✅ Database connections established")
            
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            raise
    
    def retrieve_documents(self, query: str, top_k: int = None) -> List[Document]:
        """Retrieve documents using hybrid search with Biblical reranking."""
        if top_k is None:
            top_k = self.config.retrieval.TOP_K_RETRIEVAL
        
        try:
            # Perform hybrid search
            documents = self._hybrid_search(query, top_k)
            
            # Apply Biblical reranking
            reranked_documents = self.biblical_reranker.rerank_documents(documents, query)
            
            # Return top documents
            return [doc for doc, score in reranked_documents[:top_k]]
            
        except Exception as e:
            logger.error(f"❌ Document retrieval failed: {e}")
            return []
    
    def _hybrid_search(self, query: str, top_k: int) -> List[Document]:
        """Perform hybrid search combining vector and keyword search."""
        documents = []
        
        # Vector search
        try:
            vector_docs = self._vector_search(query, top_k)
            documents.extend(vector_docs)
        except Exception as e:
            logger.warning(f"Vector search failed: {e}")
        
        # Keyword search
        try:
            keyword_docs = self._keyword_search(query, top_k)
            documents.extend(keyword_docs)
        except Exception as e:
            logger.warning(f"Keyword search failed: {e}")
        
        # Deduplicate documents
        documents = self._deduplicate_documents(documents)
        
        return documents
    
    def _vector_search(self, query: str, top_k: int) -> List[Document]:
        """Perform vector search using LM Studio embeddings."""
        try:
            # Use Qwen3 embeddings for vector search
            embeddings = self.qwen3_embeddings
            
            # Create vector store if not exists
            if not hasattr(self, 'vector_store'):
                self.vector_store = PGVector(
                    connection_string=self.pg_connection_string,
                    embedding_function=embeddings,
                    collection_name="living_truth_documents"
                )
            
            # Search documents
            docs = self.vector_store.similarity_search(query, k=top_k)
            return docs
            
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []
    
    def _keyword_search(self, query: str, top_k: int) -> List[Document]:
        """Perform keyword search using BM25."""
        try:
            # Load documents from sources directory
            documents = self._load_documents_from_sources()
            
            if not documents:
                return []
            
            # Create BM25 retriever
            bm25_retriever = BM25Retriever.from_documents(documents)
            
            # Search documents
            docs = bm25_retriever.get_relevant_documents(query)
            return docs[:top_k]
            
        except Exception as e:
            logger.error(f"Keyword search error: {e}")
            return []
    
    def _load_documents_from_sources(self) -> List[Document]:
        """Load documents from sources directory."""
        documents = []
        sources_dir = self.config.SOURCES_DIR
        
        try:
            for file_path in sources_dir.rglob("*"):
                if file_path.is_file() and file_path.suffix in self.config.processing.SUPPORTED_EXTENSIONS:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": str(file_path),
                                "filename": file_path.name,
                                "file_type": file_path.suffix,
                                "created_at": datetime.now().isoformat()
                            }
                        )
                        documents.append(doc)
                        
                    except Exception as e:
                        logger.warning(f"Failed to load {file_path}: {e}")
            
            logger.info(f"Loaded {len(documents)} documents from sources")
            return documents
            
        except Exception as e:
            logger.error(f"Failed to load documents: {e}")
            return []
    
    def _deduplicate_documents(self, documents: List[Document]) -> List[Document]:
        """Remove duplicate documents based on content similarity."""
        if not documents:
            return []
        
        unique_docs = []
        seen_contents = set()
        
        for doc in documents:
            # Create a hash of the content for deduplication
            content_hash = hash(doc.page_content[:1000])  # Use first 1000 chars
            
            if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                unique_docs.append(doc)
        
        return unique_docs
    
    def search_biblical_evidence(self, query: str) -> List[Dict[str, Any]]:
        """Search for Biblical evidence related to the query."""
        try:
            # Enhance query with Biblical terms
            enhanced_query = self._enhance_query_with_biblical_terms(query)
            
            # Retrieve documents
            documents = self.retrieve_documents(enhanced_query)
            
            # Extract Biblical evidence
            evidence_list = []
            for doc in documents:
                evidence = self._extract_biblical_evidence_from_document(doc, query)
                if evidence:
                    evidence_list.append(evidence)
            
            return evidence_list
            
        except Exception as e:
            logger.error(f"Biblical evidence search failed: {e}")
            return []
    
    def _enhance_query_with_biblical_terms(self, query: str) -> str:
        """Enhance query with Biblical forensic terms."""
        biblical_terms = [
            "biblical evidence", "scriptural reference", "survivor testimony",
            "forensic analysis", "evidence verification", "truth seeking"
        ]
        
        enhanced_query = query
        for term in biblical_terms:
            if term.lower() not in query.lower():
                enhanced_query += f" {term}"
        
        return enhanced_query
    
    def _extract_biblical_evidence_from_document(self, document: Document, query: str) -> Optional[Dict[str, Any]]:
        """Extract Biblical evidence from a document."""
        content = document.page_content
        
        # Look for Biblical references
        biblical_refs = []
        for ref in self.config.biblical_forensic.BIBLICAL_ABUSE_REFERENCES:
            if ref.lower() in content.lower():
                biblical_refs.append(ref)
        
        # Look for historical references
        historical_refs = []
        for ref in self.config.biblical_forensic.HISTORICAL_ABUSE_REFERENCES:
            if ref.lower() in content.lower():
                historical_refs.append(ref)
        
        # Calculate relevance score
        relevance_score = self._calculate_query_relevance(content.lower(), query.lower())
        
        if biblical_refs or historical_refs or relevance_score > 0.3:
            return {
                "document_source": document.metadata.get("source", "unknown"),
                "content_preview": content[:500] + "..." if len(content) > 500 else content,
                "biblical_references": biblical_refs,
                "historical_references": historical_refs,
                "relevance_score": relevance_score,
                "extracted_at": datetime.now().isoformat()
            }
        
        return None
    
    def search_survivor_testimonies(self, query: str = "") -> List[Dict[str, Any]]:
        """Search for survivor testimonies."""
        try:
            # Enhance query for survivor testimony search
            enhanced_query = f"survivor testimony {query}".strip()
            
            # Retrieve documents
            documents = self.retrieve_documents(enhanced_query)
            
            # Extract survivor testimonies
            testimonies = []
            for doc in documents:
                testimony = self._extract_survivor_testimony(doc, query)
                if testimony:
                    testimonies.append(testimony)
            
            return testimonies
            
        except Exception as e:
            logger.error(f"Survivor testimony search failed: {e}")
            return []
    
    def _extract_survivor_testimony(self, document: Document, query: str) -> Optional[Dict[str, Any]]:
        """Extract survivor testimony from a document."""
        content = document.page_content
        
        # Calculate survivor score
        survivor_score = self._calculate_survivor_score(document)
        
        # Extract testimony indicators
        indicators = self._extract_testimony_indicators(document)
        
        if survivor_score > 0.3 or indicators:
            return {
                "document_source": document.metadata.get("source", "unknown"),
                "content_preview": content[:500] + "..." if len(content) > 500 else content,
                "survivor_score": survivor_score,
                "testimony_indicators": indicators,
                "extracted_at": datetime.now().isoformat()
            }
        
        return None
    
    def _calculate_survivor_score(self, document: Document) -> float:
        """Calculate survivor testimony relevance score."""
        content = document.page_content.lower()
        
        survivor_terms = [
            "survivor", "testimony", "witness", "victim", "abuse",
            "trauma", "healing", "recovery", "justice", "truth",
            "experience", "story", "account", "narrative"
        ]
        
        matches = 0
        for term in survivor_terms:
            if term in content:
                matches += 1
        
        return matches / len(survivor_terms)
    
    def _extract_testimony_indicators(self, document: Document) -> List[str]:
        """Extract indicators of survivor testimony."""
        content = document.page_content.lower()
        indicators = []
        
        testimony_patterns = [
            r"i experienced", r"i witnessed", r"i survived",
            r"my story", r"my experience", r"what happened to me",
            r"i was", r"i had", r"i went through"
        ]
        
        for pattern in testimony_patterns:
            if re.search(pattern, content):
                indicators.append(pattern)
        
        return indicators
    
    def close(self):
        """Close database connections."""
        try:
            if hasattr(self, 'redis_client'):
                self.redis_client.close()
            logger.info("✅ Database connections closed")
        except Exception as e:
            logger.error(f"❌ Error closing connections: {e}")

class AdvancedSearchEngine:
    """Advanced search engine with specialized search capabilities."""
    
    def __init__(self):
        self.config = get_config()
        self.hybrid_retriever = HybridRetriever()
        self.search_stats = defaultdict(int)
        
        logger.info("✅ AdvancedSearchEngine initialized")
    
    def search(self, query: str, search_type: str = "hybrid", top_k: int = None) -> Dict[str, Any]:
        """Perform advanced search with multiple search types."""
        if top_k is None:
            top_k = self.config.retrieval.TOP_K_RETRIEVAL
        
        try:
            results = {
                "query": query,
                "search_type": search_type,
                "top_k": top_k,
                "timestamp": datetime.now().isoformat(),
                "results": [],
                "statistics": {}
            }
            
            if search_type == "hybrid":
                documents = self.hybrid_retriever.retrieve_documents(query, top_k)
                results["results"] = [self._document_to_dict(doc) for doc in documents]
            
            elif search_type == "biblical":
                evidence = self.hybrid_retriever.search_biblical_evidence(query)
                results["results"] = evidence
            
            elif search_type == "survivor":
                testimonies = self.hybrid_retriever.search_survivor_testimonies(query)
                results["results"] = testimonies
            
            elif search_type == "elite_networks":
                elite_results = self._search_elite_networks(query, top_k)
                results["results"] = elite_results
            
            elif search_type == "temporal":
                temporal_results = self._search_temporal_patterns(query, top_k)
                results["results"] = temporal_results
            
            # Update statistics
            self.search_stats[search_type] += 1
            results["statistics"] = self.get_search_statistics()
            
            return results
            
        except Exception as e:
            logger.error(f"Advanced search failed: {e}")
            return {
                "query": query,
                "search_type": search_type,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _search_elite_networks(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Search for elite network patterns."""
        try:
            documents = self.hybrid_retriever.retrieve_documents(query, top_k)
            
            elite_results = []
            for doc in documents:
                elite_score = self._calculate_elite_score(doc)
                elite_mentions = self._extract_elite_mentions(doc)
                
                if elite_score > 0.2 or elite_mentions:
                    elite_results.append({
                        "document_source": doc.metadata.get("source", "unknown"),
                        "content_preview": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        "elite_score": elite_score,
                        "elite_mentions": elite_mentions,
                        "extracted_at": datetime.now().isoformat()
                    })
            
            return elite_results
            
        except Exception as e:
            logger.error(f"Elite network search failed: {e}")
            return []
    
    def _search_temporal_patterns(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        """Search for temporal patterns and timelines."""
        try:
            documents = self.hybrid_retriever.retrieve_documents(query, top_k)
            
            temporal_results = []
            for doc in documents:
                temporal_score = self._calculate_temporal_score(doc)
                temporal_indicators = self._extract_temporal_indicators(doc)
                
                if temporal_score > 0.2 or temporal_indicators:
                    temporal_results.append({
                        "document_source": doc.metadata.get("source", "unknown"),
                        "content_preview": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        "temporal_score": temporal_score,
                        "temporal_indicators": temporal_indicators,
                        "extracted_at": datetime.now().isoformat()
                    })
            
            return temporal_results
            
        except Exception as e:
            logger.error(f"Temporal pattern search failed: {e}")
            return []
    
    def _calculate_elite_score(self, document: Document) -> float:
        """Calculate elite network relevance score."""
        content = document.page_content.lower()
        
        elite_terms = [
            "elite", "network", "organization", "institution",
            "government", "corporate", "financial", "political",
            "power", "influence", "control", "authority"
        ]
        
        matches = 0
        for term in elite_terms:
            if term in content:
                matches += 1
        
        return matches / len(elite_terms)
    
    def _calculate_temporal_score(self, document: Document) -> float:
        """Calculate temporal pattern relevance score."""
        content = document.page_content.lower()
        
        temporal_terms = [
            "timeline", "chronology", "sequence", "order",
            "before", "after", "during", "when", "time",
            "date", "year", "month", "day", "period"
        ]
        
        matches = 0
        for term in temporal_terms:
            if term in content:
                matches += 1
        
        return matches / len(temporal_terms)
    
    def _extract_elite_mentions(self, document: Document) -> List[str]:
        """Extract elite network mentions."""
        content = document.page_content.lower()
        mentions = []
        
        elite_patterns = [
            r"elite\s+\w+", r"powerful\s+\w+", r"influential\s+\w+",
            r"government\s+\w+", r"corporate\s+\w+", r"political\s+\w+"
        ]
        
        for pattern in elite_patterns:
            matches = re.findall(pattern, content)
            mentions.extend(matches)
        
        return list(set(mentions))
    
    def _extract_temporal_indicators(self, document: Document) -> List[str]:
        """Extract temporal indicators."""
        content = document.page_content.lower()
        indicators = []
        
        temporal_patterns = [
            r"\d{4}", r"\d{2}/\d{2}/\d{4}", r"\d{2}-\d{2}-\d{4}",
            r"before", r"after", r"during", r"when", r"then"
        ]
        
        for pattern in temporal_patterns:
            matches = re.findall(pattern, content)
            indicators.extend(matches)
        
        return list(set(indicators))
    
    def _document_to_dict(self, document: Document) -> Dict[str, Any]:
        """Convert document to dictionary format."""
        return {
            "content": document.page_content,
            "metadata": document.metadata,
            "score": document.metadata.get("score", 0.0)
        }
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        total_searches = sum(self.search_stats.values())
        
        return {
            "total_searches": total_searches,
            "search_type_counts": dict(self.search_stats),
            "most_used_search_type": max(self.search_stats.items(), key=lambda x: x[1])[0] if self.search_stats else None
        }
    
    def close(self):
        """Close the search engine."""
        try:
            self.hybrid_retriever.close()
            logger.info("✅ AdvancedSearchEngine closed")
        except Exception as e:
            logger.error(f"❌ Error closing AdvancedSearchEngine: {e}")

def main():
    """Test the hybrid retrieval system."""
    try:
        # Initialize search engine
        search_engine = AdvancedSearchEngine()
        
        # Test search
        query = "survivor testimony biblical evidence"
        results = search_engine.search(query, search_type="hybrid", top_k=5)
        
        print(f"Search results for '{query}':")
        print(json.dumps(results, indent=2))
        
        # Close
        search_engine.close()
        
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    main() 