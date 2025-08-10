"""
Living Truth Engine Configuration
Biblical Forensic System for Exposing Elite Predators
Migrated from living_truth_agent to LivingTruthEngine architecture
"""

import os
import toml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class BiblicalForensicConfig:
    """Configuration for Biblical forensic analysis"""
    
    # Core Biblical Principles
    SURVIVOR_CONFIDENCE_BASELINE: float = 0.8  # Psalm 82:3-4 - defend the weak
    EVIDENCE_VERIFICATION_THRESHOLD: float = 0.7  # Proverbs 18:17 - hear both sides
    FORENSIC_INFERENCE_CONFIDENCE: float = 0.6  # Ezekiel 16:20-21 - expose generational abuse
    
    # Biblical References for Verification
    BIBLICAL_ABUSE_REFERENCES: List[str] = field(default_factory=lambda: [
        "Leviticus 18:21",  # Child sacrifice to Moloch
        "2 Kings 23:10",    # Josiah destroys Topheth
        "Jeremiah 7:31",    # Topheth in Valley of Hinnom
        "Psalm 82:3-4",     # Defend the weak and fatherless
        "Isaiah 1:17",      # Learn to do good, seek justice
        "Ezekiel 16:20-21", # Child sacrifice practices
        "Revelation 18:2-3" # Babylon's merchant child trade
    ])
    
    # Pre-300 AD Historical References
    HISTORICAL_ABUSE_REFERENCES: List[str] = field(default_factory=lambda: [
        "Moloch worship",
        "Baal child sacrifice", 
        "Topheth rituals",
        "Carthaginian child sacrifice",
        "Roman Saturnalia",
        "Greek Dionysian rites"
    ])

@dataclass
class DatabaseConfig:
    """Database configuration for vectors and graphs"""
    
    # PostgreSQL with pgvector - adapted for LivingTruthEngine
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "living_truth_engine")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "pass")
    
    @property
    def postgres_connection_string(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Neo4j Graph Database - adapted for LivingTruthEngine
    NEO4J_URI: str = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER: str = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD", "pass")
    
    # Redis for caching - adapted for LivingTruthEngine
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "0"))

@dataclass
class ModelConfig:
    """AI model configuration for multimodal processing"""
    
    # LM Studio base URL
    LMSTUDIO_URL: str = os.getenv("LMSTUDIO_URL", "http://localhost:1234")
    LMSTUDIO_API_KEY: str = os.getenv("LMSTUDIO_API_KEY", "")
    
    # Text embeddings - LM Studio (Dynamic selection)
    LMSTUDIO_EMBEDDING_URL: str = os.getenv("LMSTUDIO_EMBEDDING_URL", "http://localhost:1234/v1/embeddings")
    LMSTUDIO_EMBEDDING_MODEL_QWEN3: str = os.getenv("LMSTUDIO_EMBEDDING_MODEL_QWEN3", "text-embedding-qwen3-embedding-0.6b")
    LMSTUDIO_EMBEDDING_MODEL_MINILM: str = os.getenv("LMSTUDIO_EMBEDDING_MODEL_MINILM", "text-embedding-all-minilm-l6-v2-embedding")
    
    # Embedding dimensions
    QWEN3_EMBEDDING_DIMENSION: int = 1024  # Qwen3-Embedding-0.6B dimension
    MINILM_EMBEDDING_DIMENSION: int = 384  # MiniLM dimension (corrected)
    
    # Reranker
    LMSTUDIO_RERANKER_MODEL: str = os.getenv("LMSTUDIO_RERANKER_MODEL", "qwen.qwen3-reranker-0.6b")
    
    # Vision model (Google Gemma-3-4B)
    VISION_MODEL: str = "google/gemma-3-4b"
    VISION_MODEL_DIMENSION: int = 512
    
    # Language models
    LLM_MODEL: str = "qwen/qwen3-8b"  # Via LM Studio
    LLM_TEMPERATURE: float = 0.1  # Low for forensic accuracy
    LLM_MAX_TOKENS: int = 4096
    
    # Named Entity Recognition
    NER_MODEL: str = "en_core_web_sm"  # spaCy model
    
    # Reranking models
    RERANKER_MODEL: str = "cohere/rerank-english-v2.0"
    ALTERNATIVE_RERANKER: str = "rankllm/rankllm-v1"

@dataclass
class ProcessingConfig:
    """Document and data processing configuration"""
    
    # File processing
    SUPPORTED_EXTENSIONS: List[str] = field(default_factory=lambda: [
        ".txt", ".md", ".pdf", ".docx", ".doc",
        ".jpg", ".jpeg", ".png", ".gif", ".bmp",
        ".mp4", ".avi", ".mov", ".wmv",
        ".mp3", ".wav", ".flac", ".m4a"
    ])
    
    # OCR and image processing
    OCR_LANGUAGE: str = "eng"
    IMAGE_RESOLUTION: tuple = (1920, 1080)
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Text processing
    MAX_TEXT_LENGTH: int = 100000  # 100k characters
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Batch processing
    BATCH_SIZE: int = 32
    MAX_CONCURRENT_PROCESSES: int = 4

@dataclass
class RetrievalConfig:
    """Retrieval and ranking configuration"""
    
    # Hybrid search weights
    VECTOR_SEARCH_WEIGHT: float = 0.6
    KEYWORD_SEARCH_WEIGHT: float = 0.4
    
    # Retrieval parameters
    TOP_K_RETRIEVAL: int = 20
    TOP_K_RERANK: int = 10
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Reranking preferences
    BIBLICAL_EVIDENCE_BOOST: float = 0.3
    SURVIVOR_TESTIMONY_BOOST: float = 0.4
    HISTORICAL_CORROBORATION_BOOST: float = 0.2

@dataclass
class SecurityConfig:
    """Security and privacy configuration"""
    
    # Encryption
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "default-key-change-in-production")
    HASH_ALGORITHM: str = "sha256"
    
    # Access control
    ADMIN_USERS: List[str] = field(default_factory=list)
    READ_ONLY_USERS: List[str] = field(default_factory=list)
    
    # Data retention
    DATA_RETENTION_DAYS: int = 365 * 10  # 10 years
    AUDIT_LOG_RETENTION_DAYS: int = 365 * 20  # 20 years
    
    # Privacy protection
    PII_DETECTION_ENABLED: bool = True
    SURVIVOR_ANONYMIZATION: bool = True
    SENSITIVE_PATTERNS: List[str] = field(default_factory=lambda: [
        r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
        r"\b\d{10}\b",  # Phone numbers
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Email
    ])

@dataclass
class MonitoringConfig:
    """System monitoring and logging configuration"""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "living_truth_engine.log"
    MAX_LOG_SIZE: int = 100 * 1024 * 1024  # 100MB
    LOG_BACKUP_COUNT: int = 5
    
    # Performance monitoring
    METRICS_ENABLED: bool = True
    METRICS_INTERVAL: int = 60  # seconds
    ALERT_THRESHOLD_CPU: float = 0.8
    ALERT_THRESHOLD_MEMORY: float = 0.9
    
    # Health checks
    HEALTH_CHECK_INTERVAL: int = 30  # seconds
    DATABASE_HEALTH_CHECK: bool = True
    MODEL_HEALTH_CHECK: bool = True

@dataclass
class HotswapConfig:
    """Hotswapping and modularity configuration"""
    
    # Module reloading
    AUTO_RELOAD_ENABLED: bool = True
    RELOAD_CHECK_INTERVAL: int = 60  # seconds
    RELOAD_ON_CHANGE: bool = True
    
    # Component swapping
    SWAPPABLE_COMPONENTS: List[str] = field(default_factory=lambda: [
        "retriever",
        "reranker", 
        "embedding_model",
        "llm_model",
        "ner_model"
    ])
    
    # Version control
    VERSION_TRACKING: bool = True
    ROLLBACK_ENABLED: bool = True
    MAX_VERSIONS: int = 10

@dataclass
class VeritasFlags:
    """Phase 8: Veritas Generalist Ingestion Configuration"""
    
    # Ingestion parameters
    default_max_videos: int = 10
    default_selection: str = "oldest"  # oldest|latest|by_date_range|ids
    crawl_depth: int = 1              # 0..3 levels of link following
    allow_domains: List[str] = field(default_factory=lambda: ["youtube.com", "youtu.be"])
    deny_domains: List[str] = field(default_factory=list)
    transcript_pref: str = "yt_api"   # yt_api|whisper_local|both
    max_pages_per_run: int = 50       # Cap on total pages fetched
    max_pages_per_domain: int = 10    # Cap per domain to prevent runaway
    
    # OCR configuration
    ocr_mode: str = "off"             # off|auto|manual|auto_retry
    suspect_min_chars: int = 800      # Minimum characters to consider text extraction successful
    auto_retry_attempts: int = 2      # Number of OCR attempts for suspect PDFs
    tesseract_langs: str = "eng"      # Tesseract language codes
    manual_queue_limit: int = 100     # Maximum files in manual OCR queue
    
    # YouTube configuration
    default_channel: str = "https://www.youtube.com/@imaginationpodcastofficial"
    extract_flat_timeout: int = 30    # Timeout for yt-dlp extract_flat operations
    transcript_timeout: int = 60      # Timeout for transcript fetching
    max_video_age_days: int = 3650    # Maximum age of videos to process (10 years)
    
    # Web crawling configuration
    user_agent: str = "LivingTruthEngine/1.0 (Phase 8)"
    request_timeout: int = 30         # Timeout for web requests
    max_redirects: int = 5            # Maximum redirects to follow
    content_type_whitelist: List[str] = field(default_factory=lambda: [
        "text/html", "application/pdf", "text/plain"
    ])
    
    @classmethod
    def from_toml(cls, toml_path: str = "config/veritas_flags.toml") -> "VeritasFlags":
        """Load VeritasFlags from TOML configuration file"""
        try:
            config_path = Path(toml_path)
            if config_path.exists():
                config_data = toml.load(config_path)
                
                # Extract ingestion section
                ingestion = config_data.get("ingestion", {})
                ocr = config_data.get("ocr", {})
                youtube = config_data.get("youtube", {})
                web = config_data.get("web", {})
                
                return cls(
                    default_max_videos=ingestion.get("default_max_videos", 10),
                    default_selection=ingestion.get("default_selection", "oldest"),
                    crawl_depth=ingestion.get("crawl_depth", 1),
                    allow_domains=ingestion.get("allow_domains", ["youtube.com", "youtu.be"]),
                    deny_domains=ingestion.get("deny_domains", []),
                    transcript_pref=ingestion.get("transcript_pref", "yt_api"),
                    max_pages_per_run=ingestion.get("max_pages_per_run", 50),
                    max_pages_per_domain=ingestion.get("max_pages_per_domain", 10),
                    
                    ocr_mode=ocr.get("mode", "off"),
                    suspect_min_chars=ocr.get("suspect_min_chars", 800),
                    auto_retry_attempts=ocr.get("auto_retry_attempts", 2),
                    tesseract_langs=ocr.get("tesseract_langs", "eng"),
                    manual_queue_limit=ocr.get("manual_queue_limit", 100),
                    
                    default_channel=youtube.get("default_channel", "https://www.youtube.com/@imaginationpodcastofficial"),
                    extract_flat_timeout=youtube.get("extract_flat_timeout", 30),
                    transcript_timeout=youtube.get("transcript_timeout", 60),
                    max_video_age_days=youtube.get("max_video_age_days", 3650),
                    
                    user_agent=web.get("user_agent", "LivingTruthEngine/1.0 (Phase 8)"),
                    request_timeout=web.get("request_timeout", 30),
                    max_redirects=web.get("max_redirects", 5),
                    content_type_whitelist=web.get("content_type_whitelist", ["text/html", "application/pdf", "text/plain"])
                )
            else:
                print(f"Warning: VeritasFlags TOML file not found at {toml_path}, using defaults")
                return cls()
        except Exception as e:
            print(f"Error loading VeritasFlags from {toml_path}: {e}, using defaults")
            return cls()

class LivingTruthConfig:
    """Main configuration class for Living Truth Engine"""
    
    def __init__(self):
        # Initialize all configuration sections
        self.biblical_forensic = BiblicalForensicConfig()
        self.database = DatabaseConfig()
        self.model = ModelConfig()
        self.processing = ProcessingConfig()
        self.retrieval = RetrievalConfig()
        self.security = SecurityConfig()
        self.monitoring = MonitoringConfig()
        self.hotswap = HotswapConfig()
        self.veritas_flags = VeritasFlags.from_toml()
        
        # LivingTruthEngine specific paths
        self.PROJECT_ROOT = Path(__file__).parent.parent.parent
        self.DATA_DIR = self.PROJECT_ROOT / "data"
        self.SOURCES_DIR = self.DATA_DIR / "sources"
        self.OUTPUTS_DIR = self.DATA_DIR / "outputs"
        self.LOGS_DIR = self.OUTPUTS_DIR / "logs"
        self.MODELS_DIR = self.DATA_DIR / "models"
        
        # Paths dictionary for compatibility
        self.paths = {
            "project_root": self.PROJECT_ROOT,
            "data_dir": self.DATA_DIR,
            "sources_dir": self.SOURCES_DIR,
            "outputs_dir": self.OUTPUTS_DIR,
            "logs_dir": self.LOGS_DIR,
            "models_dir": self.MODELS_DIR,
            "visualizations_dir": self.OUTPUTS_DIR / "visualizations",
            "config_dir": self.PROJECT_ROOT / "config",
            "scripts_dir": self.PROJECT_ROOT / "scripts"
        }
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Load environment variables
        self._load_environment_variables()
        
        # Validate configuration
        if not self.validate_configuration():
            raise ValueError("Configuration validation failed")
    
    def _ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.DATA_DIR,
            self.SOURCES_DIR,
            self.OUTPUTS_DIR,
            self.LOGS_DIR,
            self.MODELS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_environment_variables(self):
        """Load and apply environment variable overrides"""
        # Biblical forensic overrides
        if os.getenv("BIBLICAL_CONFIDENCE_BASELINE"):
            self.biblical_forensic.SURVIVOR_CONFIDENCE_BASELINE = float(os.getenv("BIBLICAL_CONFIDENCE_BASELINE"))
        
        if os.getenv("EVIDENCE_VERIFICATION_THRESHOLD"):
            self.biblical_forensic.EVIDENCE_VERIFICATION_THRESHOLD = float(os.getenv("EVIDENCE_VERIFICATION_THRESHOLD"))
        
        if os.getenv("FORENSIC_INFERENCE_CONFIDENCE"):
            self.biblical_forensic.FORENSIC_INFERENCE_CONFIDENCE = float(os.getenv("FORENSIC_INFERENCE_CONFIDENCE"))
        
        # Feature flags
        self.ENABLE_AGI_INTEGRATION = os.getenv("ENABLE_AGI_INTEGRATION", "true").lower() == "true"
        self.ENABLE_RESEARCH_ANALYSIS = os.getenv("ENABLE_RESEARCH_ANALYSIS", "true").lower() == "true"
        self.ENABLE_CLAIMS_VERIFICATION = os.getenv("ENABLE_CLAIMS_VERIFICATION", "true").lower() == "true"
        self.ENABLE_ADVANCED_VISUALIZATION = os.getenv("ENABLE_ADVANCED_VISUALIZATION", "true").lower() == "true"
        self.GRAPH_DATABASE_ENABLED = os.getenv("GRAPH_DATABASE_ENABLED", "true").lower() == "true"
    
    def get_environment_variables(self) -> Dict[str, str]:
        """Get all environment variables for configuration"""
        return {
            # Biblical forensic
            "BIBLICAL_CONFIDENCE_BASELINE": str(self.biblical_forensic.SURVIVOR_CONFIDENCE_BASELINE),
            "EVIDENCE_VERIFICATION_THRESHOLD": str(self.biblical_forensic.EVIDENCE_VERIFICATION_THRESHOLD),
            "FORENSIC_INFERENCE_CONFIDENCE": str(self.biblical_forensic.FORENSIC_INFERENCE_CONFIDENCE),
            
            # Database
            "POSTGRES_HOST": self.database.POSTGRES_HOST,
            "POSTGRES_PORT": str(self.database.POSTGRES_PORT),
            "POSTGRES_DB": self.database.POSTGRES_DB,
            "POSTGRES_USER": self.database.POSTGRES_USER,
            "POSTGRES_PASSWORD": self.database.POSTGRES_PASSWORD,
            "NEO4J_URI": self.database.NEO4J_URI,
            "NEO4J_USER": self.database.NEO4J_USER,
            "NEO4J_PASSWORD": self.database.NEO4J_PASSWORD,
            "REDIS_HOST": self.database.REDIS_HOST,
            "REDIS_PORT": str(self.database.REDIS_PORT),
            "REDIS_DB": str(self.database.REDIS_DB),
            
            # Models
            "LMSTUDIO_EMBEDDING_URL": self.model.LMSTUDIO_EMBEDDING_URL,
            "LMSTUDIO_EMBEDDING_MODEL_QWEN3": self.model.LMSTUDIO_EMBEDDING_MODEL_QWEN3,
            "LMSTUDIO_EMBEDDING_MODEL_MINILM": self.model.LMSTUDIO_EMBEDDING_MODEL_MINILM,
            "LLM_MODEL": self.model.LLM_MODEL,
            
            # Feature flags
            "ENABLE_AGI_INTEGRATION": str(self.ENABLE_AGI_INTEGRATION).lower(),
            "ENABLE_RESEARCH_ANALYSIS": str(self.ENABLE_RESEARCH_ANALYSIS).lower(),
            "ENABLE_CLAIMS_VERIFICATION": str(self.ENABLE_CLAIMS_VERIFICATION).lower(),
            "ENABLE_ADVANCED_VISUALIZATION": str(self.ENABLE_ADVANCED_VISUALIZATION).lower(),
            "GRAPH_DATABASE_ENABLED": str(self.GRAPH_DATABASE_ENABLED).lower(),
        }
    
    def validate_configuration(self) -> bool:
        """Validate the configuration is correct"""
        try:
            # Validate database configuration
            if not self.database.POSTGRES_HOST:
                raise ValueError("PostgreSQL host not configured")
            
            if not self.database.POSTGRES_DB:
                raise ValueError("PostgreSQL database not configured")
            
            # Validate model configuration
            if not self.model.LMSTUDIO_EMBEDDING_URL:
                raise ValueError("LM Studio embedding URL not configured")
            
            # Validate paths
            if not self.PROJECT_ROOT.exists():
                raise ValueError(f"Project root does not exist: {self.PROJECT_ROOT}")
            
            # Validate Biblical forensic configuration
            if not (0.0 <= self.biblical_forensic.SURVIVOR_CONFIDENCE_BASELINE <= 1.0):
                raise ValueError("SURVIVOR_CONFIDENCE_BASELINE must be between 0.0 and 1.0")
            
            if not (0.0 <= self.biblical_forensic.EVIDENCE_VERIFICATION_THRESHOLD <= 1.0):
                raise ValueError("EVIDENCE_VERIFICATION_THRESHOLD must be between 0.0 and 1.0")
            
            if not (0.0 <= self.biblical_forensic.FORENSIC_INFERENCE_CONFIDENCE <= 1.0):
                raise ValueError("FORENSIC_INFERENCE_CONFIDENCE must be between 0.0 and 1.0")
            
            return True
            
        except Exception as e:
            print(f"Configuration validation failed: {e}")
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of the current configuration"""
        return {
            "biblical_forensic": {
                "survivor_confidence_baseline": self.biblical_forensic.SURVIVOR_CONFIDENCE_BASELINE,
                "evidence_verification_threshold": self.biblical_forensic.EVIDENCE_VERIFICATION_THRESHOLD,
                "forensic_inference_confidence": self.biblical_forensic.FORENSIC_INFERENCE_CONFIDENCE,
                "biblical_references_count": len(self.biblical_forensic.BIBLICAL_ABUSE_REFERENCES),
                "historical_references_count": len(self.biblical_forensic.HISTORICAL_ABUSE_REFERENCES)
            },
            "database": {
                "postgres_host": self.database.POSTGRES_HOST,
                "postgres_port": self.database.POSTGRES_PORT,
                "postgres_db": self.database.POSTGRES_DB,
                "neo4j_uri": self.database.NEO4J_URI,
                "redis_host": self.database.REDIS_HOST,
                "redis_port": self.database.REDIS_PORT
            },
            "model": {
                "llm_model": self.model.LLM_MODEL,
                "embedding_models": [
                    self.model.LMSTUDIO_EMBEDDING_MODEL_QWEN3,
                    self.model.LMSTUDIO_EMBEDDING_MODEL_MINILM
                ],
                "embedding_dimensions": {
                    "qwen3": self.model.QWEN3_EMBEDDING_DIMENSION,
                    "minilm": self.model.MINILM_EMBEDDING_DIMENSION
                }
            },
            "processing": {
                "supported_extensions": len(self.processing.SUPPORTED_EXTENSIONS),
                "chunk_size": self.processing.CHUNK_SIZE,
                "chunk_overlap": self.processing.CHUNK_OVERLAP,
                "batch_size": self.processing.BATCH_SIZE
            },
            "retrieval": {
                "vector_search_weight": self.retrieval.VECTOR_SEARCH_WEIGHT,
                "keyword_search_weight": self.retrieval.KEYWORD_SEARCH_WEIGHT,
                "top_k_retrieval": self.retrieval.TOP_K_RETRIEVAL,
                "top_k_rerank": self.retrieval.TOP_K_RERANK,
                "biblical_evidence_boost": self.retrieval.BIBLICAL_EVIDENCE_BOOST,
                "survivor_testimony_boost": self.retrieval.SURVIVOR_TESTIMONY_BOOST
            },
            "security": {
                "pii_detection_enabled": self.security.PII_DETECTION_ENABLED,
                "survivor_anonymization": self.security.SURVIVOR_ANONYMIZATION,
                "sensitive_patterns_count": len(self.security.SENSITIVE_PATTERNS)
            },
            "monitoring": {
                "log_level": self.monitoring.LOG_LEVEL,
                "metrics_enabled": self.monitoring.METRICS_ENABLED,
                "health_check_interval": self.monitoring.HEALTH_CHECK_INTERVAL
            },
            "feature_flags": {
                "enable_agi_integration": self.ENABLE_AGI_INTEGRATION,
                "enable_research_analysis": self.ENABLE_RESEARCH_ANALYSIS,
                "enable_claims_verification": self.ENABLE_CLAIMS_VERIFICATION,
                "enable_advanced_visualization": self.ENABLE_ADVANCED_VISUALIZATION,
                "graph_database_enabled": self.GRAPH_DATABASE_ENABLED
            },
            "paths": {
                "project_root": str(self.PROJECT_ROOT),
                "data_dir": str(self.DATA_DIR),
                "sources_dir": str(self.SOURCES_DIR),
                "outputs_dir": str(self.OUTPUTS_DIR),
                "logs_dir": str(self.LOGS_DIR),
                "models_dir": str(self.MODELS_DIR)
            }
        }

# Global configuration instance
config = LivingTruthConfig()

def get_config() -> LivingTruthConfig:
    """Get the global configuration instance"""
    return config

def reload_config() -> LivingTruthConfig:
    """Reload the configuration from environment variables"""
    global config
    config = LivingTruthConfig()
    return config 