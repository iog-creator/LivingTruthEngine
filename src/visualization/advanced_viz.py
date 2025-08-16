#!/usr/bin/env python3
"""
Living Truth Engine - Advanced Visualization System
Enhanced interactive visualization for survivor testimony analysis
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from src.config.living_truth_config import get_config

logger = logging.getLogger(__name__)


class AdvancedVisualizer:
    """Advanced visualization system for Living Truth Engine analysis"""

    def __init__(self):
        self.config = get_config()
        self.output_dir = Path("data/outputs/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Enhanced color schemes for different entity types
        self.color_schemes = {
            "survivor": "#FF6B6B",  # Red for survivors
            "perpetrator": "#4ECDC4",  # Teal for perpetrators
            "elite_network": "#45B7D1",  # Blue for elite networks
            "location": "#96CEB4",  # Green for locations
            "biblical_reference": "#FFEAA7",  # Yellow for Biblical references
            "temporal": "#DDA0DD",  # Plum for temporal patterns
            "covert_operation": "#FF8C42",  # Orange for covert operations
            "trafficking": "#FF69B4",  # Pink for trafficking
            "abuse_relationship": "#FF4757",  # Bright red for abuse
            "legal_control": "#747D8C",  # Gray for legal control
            "spiritual_warfare": "#A55EEA",  # Purple for spiritual warfare
            "mind_control": "#26DE81",  # Bright green for mind control
        }

        # Enhanced node sizes based on importance and confidence
        self.node_sizes = {
            "survivor": 20,
            "perpetrator": 16,
            "elite_network": 25,
            "location": 12,
            "biblical_reference": 10,
            "temporal": 8,
            "covert_operation": 18,
            "trafficking": 22,
            "abuse_relationship": 24,
            "legal_control": 14,
            "spiritual_warfare": 20,
            "mind_control": 18,
        }

    def create_interactive_3d_network_graph(
        self, graph_data: Dict[str, Any], output_file: str = None
    ) -> go.Figure:
        """Create fully interactive 3D network graph visualization with advanced features"""  # noqa: E501
        try:
            # Create NetworkX graph
            G = nx.Graph()

            # Add nodes with enhanced metadata
            for node_id, node_data in graph_data.get("nodes", {}).items():
                G.add_node(node_id, **node_data)

            # Add edges with weights
            for edge in graph_data.get("edges", []):
                G.add_edge(edge["source"], edge["target"], **edge.get("attributes", {}))

            # Calculate enhanced 3D layout with force-directed positioning
            pos_3d = self._calculate_enhanced_3d_layout(G)

            # Create interactive 3D scatter plot
            fig = go.Figure()

            # Group nodes by type for better organization
            node_types = {}
            for node_id, node_data in G.nodes(data=True):
                node_type = node_data.get("type", "unknown")
                if node_type not in node_types:
                    node_types[node_type] = []
                node_types[node_type].append((node_id, node_data))

            # Add nodes by type for better legend and interaction
            for node_type, nodes in node_types.items():
                x_coords, y_coords, z_coords = [], [], []
                labels, confidences, descriptions = [], [], []

                for node_id, node_data in nodes:
                    if node_id in pos_3d:
                        x, y, z = pos_3d[node_id]
                        x_coords.append(x)
                        y_coords.append(y)
                        z_coords.append(z)

                        # Enhanced labels with confidence scores
                        confidence = node_data.get("confidence", 0.0)
                        label = f"{node_data.get('label', node_id)}<br>Confidence: {confidence:.2f}"  # noqa: E501
                        labels.append(label)
                        confidences.append(confidence)
                        descriptions.append(node_data.get("description", ""))

                if x_coords:  # Only add trace if there are nodes
                    fig.add_trace(
                        go.Scatter3d(
                            x=x_coords,
                            y=y_coords,
                            z=z_coords,
                            mode="markers+text",
                            marker=dict(
                                size=[
                                    self.node_sizes.get(node_type, 15) * (1 + conf)
                                    for conf in confidences
                                ],
                                color=self.color_schemes.get(node_type, "#808080"),
                                opacity=0.8,
                                line=dict(width=2, color="white"),
                            ),
                            text=labels,
                            textposition="middle center",
                            name=node_type.replace("_", " ").title(),
                            hovertemplate="<b>%{text}</b><br>Type: "
                            + node_type
                            + "<br>Description: %{customdata}<extra></extra>",
                            customdata=descriptions,
                        )
                    )

            # Add edges with enhanced styling
            edge_x, edge_y, edge_z = [], [], []
            edge_colors = []

            for edge in G.edges(data=True):
                source, target, edge_data = edge
                if source in pos_3d and target in pos_3d:
                    x1, y1, z1 = pos_3d[source]
                    x2, y2, z2 = pos_3d[target]

                    edge_x.extend([x1, x2, None])
                    edge_y.extend([y1, y2, None])
                    edge_z.extend([z1, z2, None])

                    edge_type = edge_data.get("type", "unknown")
                    edge_colors.extend([self._get_edge_color(edge_type)] * 3)

            if edge_x:  # Only add edges if they exist
                fig.add_trace(
                    go.Scatter3d(
                        x=edge_x,
                        y=edge_y,
                        z=edge_z,
                        mode="lines",
                        line=dict(color="#888888", width=2),
                        opacity=0.6,
                        hoverinfo="none",
                        showlegend=False,
                    )
                )

            # Enhanced layout
            fig.update_layout(
                title={
                    "text": "Living Truth Engine - 3D Network Analysis",
                    "x": 0.5,
                    "xanchor": "center",
                    "font": {"size": 20},
                },
                scene=dict(
                    xaxis_title="X Position",
                    yaxis_title="Y Position",
                    zaxis_title="Z Position",
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
                ),
                showlegend=True,
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                margin=dict(l=0, r=0, b=0, t=50),
                height=800,
            )

            # Save if output file specified
            if output_file:
                output_path = self.output_dir / output_file
                fig.write_html(str(output_path))
                logger.info(f"3D network graph saved to {output_path}")

            return fig

        except Exception as e:
            logger.error(f"Error creating 3D network graph: {e}")
            return go.Figure()

    def create_interactive_dashboard(self, graph_data: Dict[str, Any]) -> dash.Dash:
        """Create comprehensive interactive dashboard for analysis"""
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.title = "Living Truth Engine - Advanced Analysis Dashboard"

        # Create main 3D network graph
        network_fig = self.create_interactive_3d_network_graph(graph_data)

        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1(
                                    "Living Truth Engine - Advanced Analysis Dashboard",
                                    className="text-center mb-4",
                                ),
                                html.Hr(),
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("3D Network Visualization"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="3d-network-graph",
                                                    figure=network_fig,
                                                    style={"height": "600px"},
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            width=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Network Statistics"),
                                        dbc.CardBody(id="network-stats"),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Entity Distribution"),
                                        dbc.CardBody(
                                            [dcc.Graph(id="entity-distribution")]
                                        ),
                                    ]
                                ),
                            ],
                            width=4,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Centrality Analysis"),
                                        dbc.CardBody(
                                            [dcc.Graph(id="centrality-chart")]
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Temporal Analysis"),
                                        dbc.CardBody(
                                            [dcc.Graph(id="temporal-analysis")]
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                    ]
                ),
            ],
            fluid=True,
        )

        # Callbacks for interactive features
        @app.callback(
            Output("network-stats", "children"), Input("3d-network-graph", "figure")
        )
        def update_network_stats(figure):
            if not figure or not graph_data:
                return "No data available"

            G = nx.Graph()
            for node_id, node_data in graph_data.get("nodes", {}).items():
                G.add_node(node_id, **node_data)
            for edge in graph_data.get("edges", []):
                G.add_edge(edge["source"], edge["target"], **edge.get("attributes", {}))

            stats = [
                html.H5("Network Statistics"),
                html.P(f"Total Nodes: {G.number_of_nodes()}"),
                html.P(f"Total Edges: {G.number_of_edges()}"),
                html.P(f"Network Density: {nx.density(G):.3f}"),
                html.P(f"Average Clustering: {nx.average_clustering(G):.3f}"),
                html.P(
                    f"Diameter: {nx.diameter(G) if nx.is_connected(G) else 'Disconnected'}"  # noqa: E501
                ),
            ]

            return stats

        @app.callback(
            Output("entity-distribution", "figure"), Input("3d-network-graph", "figure")
        )
        def update_entity_distribution(figure):
            if not graph_data:
                return go.Figure()

            # Count entities by type
            entity_counts = {}
            for node_data in graph_data.get("nodes", {}).values():
                node_type = node_data.get("type", "unknown")
                entity_counts[node_type] = entity_counts.get(node_type, 0) + 1

            fig = px.pie(
                values=list(entity_counts.values()),
                names=list(entity_counts.keys()),
                title="Entity Distribution by Type",
            )

            return fig

        @app.callback(
            Output("centrality-chart", "figure"), Input("3d-network-graph", "figure")
        )
        def update_centrality_chart(figure):
            if not graph_data:
                return go.Figure()

            G = nx.Graph()
            for node_id, node_data in graph_data.get("nodes", {}).items():
                G.add_node(node_id, **node_data)
            for edge in graph_data.get("edges", []):
                G.add_edge(edge["source"], edge["target"], **edge.get("attributes", {}))

            # Calculate centrality measures
            degree_centrality = nx.degree_centrality(G)
            betweenness_centrality = nx.betweenness_centrality(G)
            closeness_centrality = nx.closeness_centrality(G)

            # Get top nodes by centrality
            top_nodes = sorted(
                degree_centrality.items(), key=lambda x: x[1], reverse=True
            )[:10]

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=[node for node, _ in top_nodes],
                    y=[degree_centrality[node] for node, _ in top_nodes],
                    name="Degree Centrality",
                )
            )

            fig.update_layout(
                title="Top Nodes by Centrality",
                xaxis_title="Node",
                yaxis_title="Centrality Score",
            )

            return fig

        @app.callback(
            Output("temporal-analysis", "figure"), Input("3d-network-graph", "figure")
        )
        def update_temporal_analysis(figure):
            if not graph_data:
                return go.Figure()

            # Extract temporal data if available
            temporal_data = []
            for node_data in graph_data.get("nodes", {}).values():
                if "timestamp" in node_data:
                    temporal_data.append(
                        {
                            "node": node_data.get("label", "Unknown"),
                            "timestamp": node_data["timestamp"],
                            "type": node_data.get("type", "unknown"),
                        }
                    )

            if not temporal_data:
                return go.Figure()

            df = pd.DataFrame(temporal_data)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            fig = px.scatter(
                df,
                x="timestamp",
                y="type",
                title="Temporal Distribution of Entities",
                labels={"timestamp": "Time", "type": "Entity Type"},
            )

            return fig

        return app

    def create_centrality_analysis(self, graph_data: Dict[str, Any]) -> go.Figure:
        """Create centrality analysis visualization"""
        try:
            G = nx.Graph()

            # Add nodes and edges
            for node_id, node_data in graph_data.get("nodes", {}).items():
                G.add_node(node_id, **node_data)
            for edge in graph_data.get("edges", []):
                G.add_edge(edge["source"], edge["target"], **edge.get("attributes", {}))

            # Calculate centrality measures
            degree_centrality = nx.degree_centrality(G)
            betweenness_centrality = nx.betweenness_centrality(G)
            closeness_centrality = nx.closeness_centrality(G)

            # Create subplots
            fig = make_subplots(
                rows=1,
                cols=3,
                subplot_titles=(
                    "Degree Centrality",
                    "Betweenness Centrality",
                    "Closeness Centrality",
                ),
            )

            # Add centrality plots
            nodes = list(degree_centrality.keys())

            fig.add_trace(
                go.Bar(x=nodes, y=list(degree_centrality.values()), name="Degree"),
                row=1,
                col=1,
            )

            fig.add_trace(
                go.Bar(
                    x=nodes, y=list(betweenness_centrality.values()), name="Betweenness"
                ),
                row=1,
                col=2,
            )

            fig.add_trace(
                go.Bar(
                    x=nodes, y=list(closeness_centrality.values()), name="Closeness"
                ),
                row=1,
                col=3,
            )

            fig.update_layout(
                title="Network Centrality Analysis", showlegend=False, height=400
            )

            return fig

        except Exception as e:
            logger.error(f"Error creating centrality analysis: {e}")
            return go.Figure()

    def _calculate_enhanced_3d_layout(
        self, G: nx.Graph
    ) -> Dict[str, Tuple[float, float, float]]:
        """Calculate enhanced 3D layout with force-directed positioning"""
        try:
            # Use spring layout for initial positioning
            pos_2d = nx.spring_layout(G, k=1, iterations=50)

            # Convert to 3D with additional dimension
            pos_3d = {}
            for node, (x, y) in pos_2d.items():
                # Add z-coordinate based on node properties
                node_data = G.nodes[node]
                z = node_data.get("confidence", 0.5)  # Use confidence as z-coordinate
                pos_3d[node] = (float(x), float(y), float(z))

            return pos_3d

        except Exception as e:
            logger.error(f"Error calculating 3D layout: {e}")
            # Fallback to simple 3D positioning
            pos_3d = {}
            for i, node in enumerate(G.nodes()):
                pos_3d[node] = (
                    np.random.random(),
                    np.random.random(),
                    np.random.random(),
                )
            return pos_3d

    def _get_edge_color(self, edge_type: str) -> str:
        """Get color for edge type"""
        edge_colors = {
            "relationship": "#FF6B6B",
            "temporal": "#4ECDC4",
            "spatial": "#45B7D1",
            "causal": "#96CEB4",
            "hierarchical": "#FFEAA7",
            "unknown": "#808080",
        }
        return edge_colors.get(edge_type, "#808080")

    def export_visualization_data(
        self, graph_data: Dict[str, Any], output_file: str
    ) -> bool:
        """Export visualization data to JSON format"""
        try:
            output_path = self.output_dir / output_file

            # Add metadata
            export_data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "source": "Living Truth Engine Advanced Visualizer",
                },
                "graph_data": graph_data,
            }

            with open(output_path, "w") as f:
                json.dump(export_data, f, indent=2)

            logger.info(f"Visualization data exported to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Error exporting visualization data: {e}")
            return False

    def create_timeline_visualization(
        self, timeline_data: List[Dict[str, Any]]
    ) -> go.Figure:
        """Create timeline visualization for temporal analysis"""
        try:
            if not timeline_data:
                return go.Figure()

            # Process timeline data
            events = []
            for event in timeline_data:
                events.append(
                    {
                        "timestamp": pd.to_datetime(event.get("timestamp")),
                        "event": event.get("event", "Unknown"),
                        "entity": event.get("entity", "Unknown"),
                        "confidence": event.get("confidence", 0.5),
                        "type": event.get("type", "unknown"),
                    }
                )

            df = pd.DataFrame(events)

            # Create timeline
            fig = px.timeline(
                df,
                x_start="timestamp",
                y="entity",
                color="type",
                title="Temporal Analysis Timeline",
            )

            fig.update_layout(xaxis_title="Time", yaxis_title="Entity", height=400)

            return fig

        except Exception as e:
            logger.error(f"Error creating timeline visualization: {e}")
            return go.Figure()

    def create_claims_verification_dashboard(
        self, claims_data: List[Dict[str, Any]]
    ) -> dash.Dash:
        """Create dashboard for claims verification analysis"""
        app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        app.title = "Living Truth Engine - Claims Verification Dashboard"

        # Process claims data
        df = pd.DataFrame(claims_data)

        app.layout = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H1(
                                    "Claims Verification Analysis",
                                    className="text-center mb-4",
                                )
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Claims by Confidence Level"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    figure=px.histogram(
                                                        df,
                                                        x="confidence",
                                                        title="Distribution of Claim Confidence Scores",  # noqa: E501
                                                    )
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Claims by Category"),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    figure=px.pie(
                                                        df,
                                                        names="category",
                                                        title="Claims Distribution by Category",  # noqa: E501
                                                    )
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ],
                            width=6,
                        ),
                    ]
                ),
            ],
            fluid=True,
        )

        return app

    def create_relationship_visualization(self, data: Dict[str, Any]) -> str:
        """
        Create relationship visualization from data.

        Args:
            data: Dictionary containing relationship data

        Returns:
            Path to generated visualization file
        """
        try:
            logger.info("Creating relationship visualization")

            # Extract nodes and edges from data
            nodes = data.get("nodes", {})
            edges = data.get("edges", [])

            if not nodes:
                logger.warning("No nodes found in data for relationship visualization")
                return ""

            # Create NetworkX graph
            G = nx.Graph()

            # Add nodes
            for node_id, node_data in nodes.items():
                G.add_node(node_id, **node_data)

            # Add edges
            for edge in edges:
                G.add_edge(edge["source"], edge["target"], **edge.get("attributes", {}))

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = (
                self.output_dir / f"relationship_visualization_{timestamp}.html"
            )

            # Create 3D network visualization
            fig = self.create_interactive_3d_network_graph(data, str(output_file))

            # Save the visualization
            fig.write_html(str(output_file))

            logger.info(f"✅ Relationship visualization created: {output_file}")
            return str(output_file)

        except Exception as e:
            logger.error(f"Error creating relationship visualization: {e}")
            return ""


def main():
    """Main function for testing visualization system"""
    visualizer = AdvancedVisualizer()

    # Example graph data
    sample_data = {
        "nodes": {
            "node1": {"label": "Entity A", "type": "survivor", "confidence": 0.8},
            "node2": {"label": "Entity B", "type": "perpetrator", "confidence": 0.9},
            "node3": {"label": "Location C", "type": "location", "confidence": 0.7},
        },
        "edges": [
            {"source": "node1", "target": "node2", "type": "relationship"},
            {"source": "node2", "target": "node3", "type": "spatial"},
        ],
    }

    # Create 3D network graph
    fig = visualizer.create_interactive_3d_network_graph(
        sample_data, "sample_3d_network.html"
    )
    print("3D network graph created successfully")

    # Create dashboard
    app = visualizer.create_interactive_dashboard(sample_data)
    print("Interactive dashboard created successfully")


if __name__ == "__main__":
    main()
