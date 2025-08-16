"""
Research Analysis System for Claims Verification and Relationship Mapping
Specialized system for tracking people, places, events with verification weighting.
Migrated from living_truth_agent to LivingTruthEngine architecture
"""

import json
import re
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import spacy
from collections import defaultdict
import pandas as pd
from dataclasses import dataclass, asdict

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog

    GUI_AVAILABLE = True
except (ImportError, ModuleNotFoundError):  # Missing tk runtime in headless/container
    GUI_AVAILABLE = False
    tk = None

    # Provide minimal placeholders to avoid NameErrors if referenced indirectly
    class _Stub:  # simple no-op stub for ttk/messagebox/filedialogs
        def __getattr__(self, name):
            def _noop(*args, **kwargs):
                return None

            return _noop

    ttk = _Stub()
    messagebox = _Stub()
    filedialog = _Stub()
    simpledialog = _Stub()
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for Docker
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # noqa: F401
except (ImportError, ModuleNotFoundError):
    # In headless environments without Tk, skip the TkAgg backend import
    FigureCanvasTkAgg = None
import webbrowser
import logging

# LivingTruthEngine configuration
from src.config import get_config

# Setup logging
config = get_config()
logging.basicConfig(
    level=getattr(logging, config.monitoring.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOGS_DIR / "research_analysis.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


@dataclass
class Claim:
    """Represents a claim made in the content."""

    id: str
    text: str
    source_video: str
    source_timestamp: Optional[str]
    speaker: Optional[str]
    claim_type: str  # 'person', 'place', 'event', 'organization', 'relationship'
    confidence_score: float  # 0.0 to 1.0
    verification_status: (
        str  # 'unverified', 'verified', 'disputed', 'partially_verified'
    )
    supporting_evidence: List[str]
    contradicting_evidence: List[str]
    created_at: str
    updated_at: str


@dataclass
class Entity:
    """Represents a person, place, organization, or event."""

    id: str
    name: str
    entity_type: str  # 'person', 'place', 'organization', 'event'
    aliases: List[str]
    first_mentioned: str
    last_mentioned: str
    mentions: List[str]
    claims_about: List[str]
    claims_by: List[str]
    relationships: List[str]
    verification_score: float  # 0.0 to 1.0
    risk_level: str  # 'low', 'medium', 'high', 'critical'


@dataclass
class Relationship:
    """Represents a relationship between entities."""

    id: str
    entity1_id: str
    entity2_id: str
    relationship_type: str
    source_claim: str
    confidence_score: float
    verification_status: str
    evidence: List[str]


class ResearchAnalysisSystem:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = config.SOURCES_DIR
        self.data_dir = Path(data_dir)
        self.claims: Dict[str, Claim] = {}
        self.entities: Dict[str, Entity] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.graph = nx.DiGraph()

        # Load NLP model for entity extraction
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.info("Installing spaCy model...")
            import subprocess

            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # Load organized data
        self.load_organized_data()

        logger.info("✅ ResearchAnalysisSystem initialized successfully")

    def load_organized_data(self):
        """Load the organized transcript data."""
        organized_file = self.data_dir / "organized" / "organized_transcripts.json"
        if organized_file.exists():
            with open(organized_file, "r", encoding="utf-8") as f:
                self.transcripts = json.load(f)
            logger.info(f"✅ Loaded {len(self.transcripts)} transcripts")
        else:
            logger.warning("❌ No organized data found")
            self.transcripts = []

    def extract_entities_from_text(self, text: str) -> List[Tuple[str, str]]:
        """Extract named entities from text using spaCy."""
        doc = self.nlp(text)
        entities = []

        for ent in doc.ents:
            entities.append((ent.text, ent.label_))

        return entities

    def extract_claims_from_transcript(
        self, transcript_data: Dict[str, Any]
    ) -> List[Claim]:
        """Extract claims from transcript data."""
        claims = []
        transcript_text = transcript_data.get("text", "")
        video_id = transcript_data.get("video_id", "unknown")

        # Split text into sentences for claim extraction
        sentences = re.split(r"[.!?]+", transcript_text)

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue

            # Extract entities from sentence
            entities = self.extract_entities_from_text(sentence)

            # Classify claim type
            claim_type = self.classify_claim_type(sentence, entities)

            # Calculate confidence score
            confidence = self.calculate_claim_confidence(sentence, entities)

            # Only create claims with sufficient confidence
            if confidence > 0.3:
                claim = Claim(
                    id=f"claim_{video_id}_{i}",
                    text=sentence,
                    source_video=video_id,
                    source_timestamp=None,  # Could be enhanced with timestamp extraction  # noqa: E501
                    speaker=None,  # Could be enhanced with speaker detection
                    claim_type=claim_type,
                    confidence_score=confidence,
                    verification_status="unverified",
                    supporting_evidence=[],
                    contradicting_evidence=[],
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                )
                claims.append(claim)

        return claims

    def classify_claim_type(self, text: str, entities: List[Tuple[str, str]]) -> str:
        """Classify the type of claim based on content and entities."""
        text_lower = text.lower()

        # Check for person-related claims
        person_entities = [ent for ent, label in entities if label in ["PERSON"]]
        if person_entities:
            return "person"

        # Check for place-related claims
        place_entities = [ent for ent, label in entities if label in ["GPE", "LOC"]]
        if place_entities:
            return "place"

        # Check for organization-related claims
        org_entities = [ent for ent, label in entities if label in ["ORG"]]
        if org_entities:
            return "organization"

        # Check for event-related claims
        event_indicators = ["happened", "occurred", "took place", "event", "incident"]
        if any(indicator in text_lower for indicator in event_indicators):
            return "event"

        # Default to relationship if multiple entities found
        if len(entities) > 1:
            return "relationship"

        return "general"

    def calculate_claim_confidence(
        self, text: str, entities: List[Tuple[str, str]]
    ) -> float:
        """Calculate confidence score for a claim."""
        confidence = 0.0

        # Base confidence from entity presence
        if entities:
            confidence += 0.3

        # Boost for specific entity types
        person_entities = [ent for ent, label in entities if label == "PERSON"]
        if person_entities:
            confidence += 0.2

        org_entities = [ent for ent, label in entities if label == "ORG"]
        if org_entities:
            confidence += 0.15

        # Boost for specific keywords
        confidence_keywords = [
            "said",
            "stated",
            "claimed",
            "reported",
            "witnessed",
            "saw",
            "heard",
            "experienced",
            "knew",
            "confirmed",
        ]

        text_lower = text.lower()
        keyword_matches = sum(
            1 for keyword in confidence_keywords if keyword in text_lower
        )
        confidence += min(keyword_matches * 0.1, 0.3)

        # Penalty for uncertainty indicators
        uncertainty_indicators = [
            "maybe",
            "possibly",
            "perhaps",
            "might",
            "could",
            "allegedly",
        ]
        uncertainty_matches = sum(
            1 for indicator in uncertainty_indicators if indicator in text_lower
        )
        confidence -= min(uncertainty_matches * 0.1, 0.2)

        return max(0.0, min(1.0, confidence))

    def build_entity_network(self):
        """Build network of entities from claims."""
        self.graph.clear()

        # Add entities as nodes
        for entity_id, entity in self.entities.items():
            self.graph.add_node(
                entity_id,
                name=entity.name,
                entity_type=entity.entity_type,
                verification_score=entity.verification_score,
                risk_level=entity.risk_level,
            )

        # Add relationships as edges
        for rel_id, relationship in self.relationships.items():
            if (
                relationship.entity1_id in self.entities
                and relationship.entity2_id in self.entities
            ):
                self.graph.add_edge(
                    relationship.entity1_id,
                    relationship.entity2_id,
                    relationship_type=relationship.relationship_type,
                    confidence_score=relationship.confidence_score,
                    verification_status=relationship.verification_status,
                )

        logger.info(
            f"✅ Built entity network with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges"  # noqa: E501
        )

    def build_relationship_graph(self):
        """Build relationship graph from claims."""
        # Extract entities from claims
        for claim in self.claims.values():
            entities = self.extract_entities_from_text(claim.text)

            for entity_text, entity_label in entities:
                entity_id = f"{entity_label}_{entity_text.lower().replace(' ', '_')}"

                if entity_id not in self.entities:
                    entity = Entity(
                        id=entity_id,
                        name=entity_text,
                        entity_type=entity_label,
                        aliases=[],
                        first_mentioned=claim.created_at,
                        last_mentioned=claim.updated_at,
                        mentions=[claim.id],
                        claims_about=[],
                        claims_by=[],
                        relationships=[],
                        verification_score=0.5,
                        risk_level="low",
                    )
                    self.entities[entity_id] = entity
                else:
                    self.entities[entity_id].mentions.append(claim.id)
                    self.entities[entity_id].last_mentioned = claim.updated_at

        # Build relationships between entities mentioned in same claims
        for claim in self.claims.values():
            entities = self.extract_entities_from_text(claim.text)

            for i, (entity1_text, entity1_label) in enumerate(entities):
                for j, (entity2_text, entity2_label) in enumerate(
                    entities[i + 1 :], i + 1
                ):
                    entity1_id = (
                        f"{entity1_label}_{entity1_text.lower().replace(' ', '_')}"
                    )
                    entity2_id = (
                        f"{entity2_label}_{entity2_text.lower().replace(' ', '_')}"
                    )

                    rel_id = f"rel_{entity1_id}_{entity2_id}"

                    if rel_id not in self.relationships:
                        relationship = Relationship(
                            id=rel_id,
                            entity1_id=entity1_id,
                            entity2_id=entity2_id,
                            relationship_type="mentioned_together",
                            source_claim=claim.id,
                            confidence_score=claim.confidence_score,
                            verification_status="unverified",
                            evidence=[claim.text],
                        )
                        self.relationships[rel_id] = relationship

        logger.info(
            f"✅ Built relationship graph with {len(self.entities)} entities and {len(self.relationships)} relationships"  # noqa: E501
        )

    def save_analysis_data(self):
        """Save analysis data to files."""
        try:
            # Create analysis directory
            analysis_dir = config.OUTPUTS_DIR / "analysis"
            analysis_dir.mkdir(parents=True, exist_ok=True)

            # Save claims
            claims_file = analysis_dir / "claims.json"
            claims_data = [asdict(claim) for claim in self.claims.values()]
            with open(claims_file, "w", encoding="utf-8") as f:
                json.dump(claims_data, f, indent=2, ensure_ascii=False)

            # Save entities
            entities_file = analysis_dir / "entities.json"
            entities_data = [asdict(entity) for entity in self.entities.values()]
            with open(entities_file, "w", encoding="utf-8") as f:
                json.dump(entities_data, f, indent=2, ensure_ascii=False)

            # Save relationships
            relationships_file = analysis_dir / "relationships.json"
            relationships_data = [asdict(rel) for rel in self.relationships.values()]
            with open(relationships_file, "w", encoding="utf-8") as f:
                json.dump(relationships_data, f, indent=2, ensure_ascii=False)

            # Save network graph
            graph_file = analysis_dir / "network_graph.json"
            graph_data = nx.node_link_data(self.graph)
            with open(graph_file, "w", encoding="utf-8") as f:
                json.dump(graph_data, f, indent=2, ensure_ascii=False)

            logger.info(f"✅ Analysis data saved to {analysis_dir}")

        except Exception as e:
            logger.error(f"❌ Failed to save analysis data: {e}")

    def generate_visualizations(self):
        """Generate visualizations of the analysis."""
        try:
            # Create visualizations directory
            viz_dir = config.OUTPUTS_DIR / "visualizations"
            viz_dir.mkdir(parents=True, exist_ok=True)

            # Generate network graph visualization
            self._generate_network_viz(viz_dir)

            # Generate claims timeline
            self._generate_claims_timeline(viz_dir)

            # Generate entity statistics
            self._generate_entity_stats(viz_dir)

            logger.info(f"✅ Visualizations generated in {viz_dir}")

        except Exception as e:
            logger.error(f"❌ Failed to generate visualizations: {e}")

    def _generate_network_viz(self, viz_dir: Path):
        """Generate network graph visualization."""
        if not self.graph.nodes():
            return

        plt.figure(figsize=(12, 8))

        # Use spring layout for positioning
        pos = nx.spring_layout(self.graph, k=1, iterations=50)

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_color="lightblue", node_size=1000)

        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, edge_color="gray", arrows=True)

        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_weight="bold")

        plt.title("Entity Relationship Network")
        plt.axis("off")

        # Save plot
        network_file = (
            viz_dir / f"network_graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        plt.savefig(network_file, dpi=300, bbox_inches="tight")
        plt.close()

    def _generate_claims_timeline(self, viz_dir: Path):
        """Generate claims timeline visualization."""
        if not self.claims:
            return

        # Create timeline data
        timeline_data = []
        for claim in self.claims.values():
            timeline_data.append(
                {
                    "date": claim.created_at,
                    "claim_type": claim.claim_type,
                    "confidence": claim.confidence_score,
                    "text": claim.text[:100] + "..."
                    if len(claim.text) > 100
                    else claim.text,
                }
            )

        # Save timeline data
        timeline_file = (
            viz_dir / f"claims_timeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(timeline_file, "w", encoding="utf-8") as f:
            json.dump(timeline_data, f, indent=2, ensure_ascii=False)

    def _generate_entity_stats(self, viz_dir: Path):
        """Generate entity statistics."""
        if not self.entities:
            return

        # Calculate statistics
        entity_types = defaultdict(int)
        risk_levels = defaultdict(int)
        verification_scores = []

        for entity in self.entities.values():
            entity_types[entity.entity_type] += 1
            risk_levels[entity.risk_level] += 1
            verification_scores.append(entity.verification_score)

        stats = {
            "total_entities": len(self.entities),
            "entity_types": dict(entity_types),
            "risk_levels": dict(risk_levels),
            "avg_verification_score": sum(verification_scores)
            / len(verification_scores)
            if verification_scores
            else 0,
            "total_claims": len(self.claims),
            "total_relationships": len(self.relationships),
        }

        # Save statistics
        stats_file = (
            viz_dir / f"entity_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

    def run_full_analysis(self):
        """Run complete analysis pipeline."""
        try:
            logger.info("🚀 Starting full analysis pipeline...")

            # Extract claims from transcripts
            all_claims = []
            for transcript in self.transcripts:
                claims = self.extract_claims_from_transcript(transcript)
                all_claims.extend(claims)

            # Store claims
            for claim in all_claims:
                self.claims[claim.id] = claim

            logger.info(f"✅ Extracted {len(all_claims)} claims")

            # Build relationship graph
            self.build_relationship_graph()

            # Build entity network
            self.build_entity_network()

            # Save analysis data
            self.save_analysis_data()

            # Generate visualizations
            self.generate_visualizations()

            logger.info("✅ Full analysis pipeline completed")

            return {
                "claims_count": len(self.claims),
                "entities_count": len(self.entities),
                "relationships_count": len(self.relationships),
                "network_nodes": self.graph.number_of_nodes(),
                "network_edges": self.graph.number_of_edges(),
            }

        except Exception as e:
            logger.error(f"❌ Full analysis pipeline failed: {e}")
            return None

    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of analysis results."""
        return {
            "claims": {
                "total": len(self.claims),
                "by_type": defaultdict(int),
                "by_status": defaultdict(int),
                "avg_confidence": sum(c.confidence_score for c in self.claims.values())
                / len(self.claims)
                if self.claims
                else 0,
            },
            "entities": {
                "total": len(self.entities),
                "by_type": defaultdict(int),
                "by_risk_level": defaultdict(int),
                "avg_verification_score": sum(
                    e.verification_score for e in self.entities.values()
                )
                / len(self.entities)
                if self.entities
                else 0,
            },
            "relationships": {
                "total": len(self.relationships),
                "by_type": defaultdict(int),
                "by_status": defaultdict(int),
            },
            "network": {
                "nodes": self.graph.number_of_nodes(),
                "edges": self.graph.number_of_edges(),
                "density": nx.density(self.graph) if self.graph.nodes() else 0,
            },
        }


class ResearchAnalysisGUI:
    """GUI for research analysis system."""

    def __init__(self, analysis_system: ResearchAnalysisSystem):
        self.analysis_system = analysis_system
        self.root = tk.Tk()
        self.root.title("Research Analysis System")
        self.root.geometry("1200x800")

        self.setup_gui()

    def setup_gui(self):
        """Setup the GUI components."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create tabs
        self.setup_claims_tab(notebook)
        self.setup_entities_tab(notebook)
        self.setup_relationships_tab(notebook)
        self.setup_network_tab(notebook)
        self.setup_analysis_tab(notebook)

    def setup_claims_tab(self, notebook):
        """Setup claims tab."""
        claims_frame = ttk.Frame(notebook)
        notebook.add(claims_frame, text="Claims")

        # Claims list
        claims_list_frame = ttk.LabelFrame(claims_frame, text="Claims")
        claims_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for claims
        columns = ("ID", "Type", "Confidence", "Status", "Text")
        self.claims_tree = ttk.Treeview(
            claims_list_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.claims_tree.heading(col, text=col)
            self.claims_tree.column(col, width=100)

        self.claims_tree.column("Text", width=300)

        # Scrollbar
        claims_scrollbar = ttk.Scrollbar(
            claims_list_frame, orient="vertical", command=self.claims_tree.yview
        )
        self.claims_tree.configure(yscrollcommand=claims_scrollbar.set)

        self.claims_tree.pack(side="left", fill="both", expand=True)
        claims_scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.claims_tree.bind("<<TreeviewSelect>>", self.on_claim_select)

        # Buttons frame
        buttons_frame = ttk.Frame(claims_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_claims).pack(
            side="left", padx=5
        )
        ttk.Button(buttons_frame, text="Export", command=self.export_claims).pack(
            side="left", padx=5
        )
        ttk.Button(buttons_frame, text="Filter", command=self.filter_claims).pack(
            side="left", padx=5
        )
        ttk.Button(
            buttons_frame, text="Mark Verified", command=self.mark_verified
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame, text="Mark Unverified", command=self.mark_unverified
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame, text="Confidence Stats", command=self.show_confidence_stats
        ).pack(side="left", padx=5)

    def setup_entities_tab(self, notebook):
        """Setup entities tab."""
        entities_frame = ttk.Frame(notebook)
        notebook.add(entities_frame, text="Entities")

        # Entities list
        entities_list_frame = ttk.LabelFrame(entities_frame, text="Entities")
        entities_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for entities
        columns = ("ID", "Name", "Type", "Risk Level", "Verification Score")
        self.entities_tree = ttk.Treeview(
            entities_list_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.entities_tree.heading(col, text=col)
            self.entities_tree.column(col, width=120)

        # Scrollbar
        entities_scrollbar = ttk.Scrollbar(
            entities_list_frame, orient="vertical", command=self.entities_tree.yview
        )
        self.entities_tree.configure(yscrollcommand=entities_scrollbar.set)

        self.entities_tree.pack(side="left", fill="both", expand=True)
        entities_scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.entities_tree.bind("<<TreeviewSelect>>", self.on_entity_select)

        # Buttons frame
        buttons_frame = ttk.Frame(entities_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(buttons_frame, text="Refresh", command=self.refresh_entities).pack(
            side="left", padx=5
        )
        ttk.Button(buttons_frame, text="Export", command=self.export_entities).pack(
            side="left", padx=5
        )
        ttk.Button(buttons_frame, text="Filter", command=self.filter_entities).pack(
            side="left", padx=5
        )
        ttk.Button(
            buttons_frame, text="Risk Assessment", command=self.analyze_risk
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame, text="Entity Stats", command=self.show_entity_stats
        ).pack(side="left", padx=5)

    def setup_relationships_tab(self, notebook):
        """Setup relationships tab."""
        relationships_frame = ttk.Frame(notebook)
        notebook.add(relationships_frame, text="Relationships")

        # Relationships list
        relationships_list_frame = ttk.LabelFrame(
            relationships_frame, text="Relationships"
        )
        relationships_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview for relationships
        columns = ("ID", "Entity 1", "Entity 2", "Type", "Confidence", "Status")
        self.relationships_tree = ttk.Treeview(
            relationships_list_frame, columns=columns, show="headings"
        )

        for col in columns:
            self.relationships_tree.heading(col, text=col)
            self.relationships_tree.column(col, width=120)

        # Scrollbar
        relationships_scrollbar = ttk.Scrollbar(
            relationships_list_frame,
            orient="vertical",
            command=self.relationships_tree.yview,
        )
        self.relationships_tree.configure(yscrollcommand=relationships_scrollbar.set)

        self.relationships_tree.pack(side="left", fill="both", expand=True)
        relationships_scrollbar.pack(side="right", fill="y")

        # Bind selection event
        self.relationships_tree.bind("<<TreeviewSelect>>", self.on_relationship_select)

        # Buttons frame
        buttons_frame = ttk.Frame(relationships_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            buttons_frame, text="Refresh", command=self.refresh_relationships
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame, text="Export", command=self.export_relationships
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame, text="Filter", command=self.filter_relationships
        ).pack(side="left", padx=5)
        ttk.Button(
            buttons_frame,
            text="Relationship Stats",
            command=self.show_relationship_stats,
        ).pack(side="left", padx=5)

    def setup_network_tab(self, notebook):
        """Setup network visualization tab."""
        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="Network")

        # Network controls
        controls_frame = ttk.Frame(network_frame)
        controls_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            controls_frame, text="Generate Network", command=self.generate_network
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Load Visualization", command=self.load_visualization
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Save Visualization", command=self.save_visualization
        ).pack(side="left", padx=5)
        ttk.Button(controls_frame, text="Zoom In", command=self.zoom_in).pack(
            side="left", padx=5
        )
        ttk.Button(controls_frame, text="Zoom Out", command=self.zoom_out).pack(
            side="left", padx=5
        )
        ttk.Button(
            controls_frame, text="Network Stats", command=self.show_network_stats
        ).pack(side="left", padx=5)

        # Network display area
        self.network_canvas = None

    def setup_analysis_tab(self, notebook):
        """Setup analysis tab."""
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Analysis")

        # Analysis controls
        controls_frame = ttk.Frame(analysis_frame)
        controls_frame.pack(fill="x", padx=5, pady=5)

        ttk.Button(
            controls_frame, text="Run Full Analysis", command=self.run_full_analysis
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Generate Report", command=self.generate_report
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Show Statistics", command=self.show_statistics
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Search Claims", command=self.search_claims
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Risk Assessment", command=self.risk_assessment
        ).pack(side="left", padx=5)
        ttk.Button(
            controls_frame, text="Export All Data", command=self.export_all_data
        ).pack(side="left", padx=5)

        # Analysis results area
        results_frame = ttk.LabelFrame(analysis_frame, text="Analysis Results")
        results_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.results_text = tk.Text(results_frame, wrap="word")
        results_scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.results_text.yview
        )
        self.results_text.configure(yscrollcommand=results_scrollbar.set)

        self.results_text.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")

    # Event handlers and utility methods would go here...
    # (Implementation details omitted for brevity)

    def on_claim_select(self, event):
        """Handle claim selection."""
        pass

    def on_entity_select(self, event):
        """Handle entity selection."""
        pass

    def on_relationship_select(self, event):
        """Handle relationship selection."""
        pass

    def refresh_claims(self):
        """Refresh claims display."""
        pass

    def export_claims(self):
        """Export claims data."""
        pass

    def filter_claims(self):
        """Filter claims."""
        pass

    def mark_verified(self):
        """Mark selected claims as verified."""
        pass

    def mark_unverified(self):
        """Mark selected claims as unverified."""
        pass

    def show_confidence_stats(self):
        """Show confidence statistics."""
        pass

    def refresh_entities(self):
        """Refresh entities display."""
        pass

    def export_entities(self):
        """Export entities data."""
        pass

    def filter_entities(self):
        """Filter entities."""
        pass

    def analyze_risk(self):
        """Analyze entity risk levels."""
        pass

    def show_entity_stats(self):
        """Show entity statistics."""
        pass

    def refresh_relationships(self):
        """Refresh relationships display."""
        pass

    def export_relationships(self):
        """Export relationships data."""
        pass

    def filter_relationships(self):
        """Filter relationships."""
        pass

    def show_relationship_stats(self):
        """Show relationship statistics."""
        pass

    def generate_network(self):
        """Generate network visualization."""
        pass

    def load_visualization(self):
        """Load visualization."""
        pass

    def save_visualization(self):
        """Save visualization."""
        pass

    def zoom_in(self):
        """Zoom in on network."""
        pass

    def zoom_out(self):
        """Zoom out on network."""
        pass

    def show_network_stats(self):
        """Show network statistics."""
        pass

    def run_full_analysis(self):
        """Run full analysis."""
        pass

    def generate_report(self):
        """Generate analysis report."""
        pass

    def show_statistics(self):
        """Show analysis statistics."""
        pass

    def search_claims(self):
        """Search claims."""
        pass

    def risk_assessment(self):
        """Perform risk assessment."""
        pass

    def export_all_data(self):
        """Export all analysis data."""
        pass

    def run(self):
        """Run the GUI."""
        self.root.mainloop()


def main():
    """Main function for testing."""
    try:
        # Initialize analysis system
        analysis_system = ResearchAnalysisSystem()

        # Run full analysis
        results = analysis_system.run_full_analysis()

        if results:
            print("✅ Analysis completed successfully:")
            print(json.dumps(results, indent=2))

            # Get summary
            summary = analysis_system.get_analysis_summary()
            print("\n📊 Analysis Summary:")
            print(json.dumps(summary, indent=2))
        else:
            print("❌ Analysis failed")

    except Exception as e:
        logger.error(f"❌ Main function failed: {e}")


if __name__ == "__main__":
    main()
