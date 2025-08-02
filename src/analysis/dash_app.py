#!/usr/bin/env python3
"""
Dash Dashboard for Living Truth Engine Visualizations
Interactive dashboard for survivor testimony analysis
"""

import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Living Truth Engine Dashboard"

# Get visualizations directory
visualizations_dir = Path("/app/visualizations")
if not visualizations_dir.exists():
    visualizations_dir = Path("data/outputs/visualizations")

def load_visualization_data():
    """Load visualization data from files."""
    data = {
        "network_graphs": [],
        "timeline_data": [],
        "statistics": {}
    }
    
    try:
        # Load network visualization data
        for file in visualizations_dir.glob("*.json"):
            if "network" in file.name:
                with open(file, 'r') as f:
                    data["network_graphs"].append({
                        "name": file.name,
                        "data": json.load(f),
                        "timestamp": datetime.fromtimestamp(file.stat().st_mtime)
                    })
        
        # Load timeline data
        for file in visualizations_dir.glob("*timeline*.json"):
            with open(file, 'r') as f:
                data["timeline_data"].append({
                    "name": file.name,
                    "data": json.load(f),
                    "timestamp": datetime.fromtimestamp(file.stat().st_mtime)
                })
                
    except Exception as e:
        logger.error(f"Error loading visualization data: {e}")
    
    return data

def create_network_graph(data):
    """Create network graph from data."""
    if not data:
        return go.Figure()
    
    # Extract nodes and edges from data
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    
    # Create node positions
    node_x = [node.get("x", 0) for node in nodes]
    node_y = [node.get("y", 0) for node in nodes]
    node_text = [node.get("label", "") for node in nodes]
    node_colors = [node.get("color", "blue") for node in nodes]
    
    # Create edge positions
    edge_x = []
    edge_y = []
    for edge in edges:
        source = edge.get("source", 0)
        target = edge.get("target", 0)
        if source < len(nodes) and target < len(nodes):
            edge_x.extend([node_x[source], node_x[target], None])
            edge_y.extend([node_y[source], node_y[target], None])
    
    # Create figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=0.5, color='gray'),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="middle center",
        marker=dict(
            size=20,
            color=node_colors,
            line=dict(width=2, color='white')
        ),
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        title="Relationship Network",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
    
    return fig

# App layout
app.layout = html.Div([
    html.H1("Living Truth Engine Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Control panel
    html.Div([
        html.H3("Controls", style={'color': '#34495e'}),
        dcc.Dropdown(
            id='visualization-type',
            options=[
                {'label': 'Network Graph', 'value': 'network'},
                {'label': 'Timeline', 'value': 'timeline'},
                {'label': 'Statistics', 'value': 'stats'}
            ],
            value='network',
            style={'marginBottom': 20}
        ),
        dcc.Dropdown(
            id='data-file',
            options=[],
            placeholder="Select data file...",
            style={'marginBottom': 20}
        ),
        html.Button('Refresh Data', id='refresh-btn', n_clicks=0,
                   style={'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'padding': '10px 20px'})
    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
    
    # Visualization area
    html.Div([
        dcc.Graph(id='visualization-graph', style={'height': '600px'}),
        html.Div(id='data-info', style={'marginTop': 20, 'padding': '10px', 'backgroundColor': '#f8f9fa'})
    ], style={'width': '70%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
    
    # Update interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # 30 seconds
        n_intervals=0
    )
])

@app.callback(
    [Output('data-file', 'options'),
     Output('data-file', 'value')],
    [Input('refresh-btn', 'n_clicks'),
     Input('interval-component', 'n_intervals')]
)
def update_file_options(n_clicks, n_intervals):
    """Update available data files."""
    data = load_visualization_data()
    
    if not data["network_graphs"]:
        return [], None
    
    options = [{'label': f"{item['name']} ({item['timestamp'].strftime('%Y-%m-%d %H:%M')})", 
                'value': item['name']} for item in data["network_graphs"]]
    
    return options, options[0]['value'] if options else None

@app.callback(
    [Output('visualization-graph', 'figure'),
     Output('data-info', 'children')],
    [Input('visualization-type', 'value'),
     Input('data-file', 'value')]
)
def update_visualization(viz_type, filename):
    """Update visualization based on selection."""
    if not filename:
        return go.Figure(), "No data selected"
    
    data = load_visualization_data()
    
    # Find the selected file
    selected_data = None
    for item in data["network_graphs"]:
        if item["name"] == filename:
            selected_data = item["data"]
            break
    
    if not selected_data:
        return go.Figure(), "Data not found"
    
    if viz_type == 'network':
        fig = create_network_graph(selected_data)
        info = f"Network Graph: {len(selected_data.get('nodes', []))} nodes, {len(selected_data.get('edges', []))} edges"
    else:
        fig = go.Figure()
        fig.add_annotation(text="Visualization type not implemented yet", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        info = "Visualization type not implemented yet"
    
    return fig, info

@app.callback(
    Output('refresh-btn', 'children'),
    [Input('refresh-btn', 'n_clicks')]
)
def update_refresh_button(n_clicks):
    """Update refresh button text."""
    if n_clicks:
        return f"Refreshed ({datetime.now().strftime('%H:%M:%S')})"
    return "Refresh Data"

# Create ASGI app for uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Create FastAPI app
fastapi_app = FastAPI(title="Living Truth Engine Dashboard")

# Mount Dash app as WSGI middleware
fastapi_app.mount("/dash", WSGIMiddleware(app.server))

# Add health check endpoint
@fastapi_app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "dashboard"}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 