#!/usr/bin/env python3
"""
Dash Dashboard for Living Truth Engine Visualizations
Enhanced interactive dashboard for survivor testimony analysis
"""

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import logging
import networkx as nx

# Import advanced visualization components
from src.visualization.advanced_viz import AdvancedVisualizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Living Truth Engine - Enhanced Dashboard"

# Initialize advanced visualizer
visualizer = AdvancedVisualizer()

# Add health check endpoint to Dash app
@app.server.route('/health')
def health_check():
    return {"status": "healthy", "service": "dashboard"}

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

def create_enhanced_network_graph(data):
    """Create enhanced network graph using advanced visualizer."""
    if not data:
        return go.Figure()
    
    # Convert data format for advanced visualizer
    graph_data = {
        'nodes': {},
        'edges': []
    }
    
    # Process nodes
    for i, node in enumerate(data.get("nodes", [])):
        node_id = f"node_{i}"
        graph_data['nodes'][node_id] = {
            'label': node.get("label", f"Node {i}"),
            'type': node.get("type", "unknown"),
            'confidence': node.get("confidence", 0.5),
            'description': node.get("description", "")
        }
    
    # Process edges
    for edge in data.get("edges", []):
        graph_data['edges'].append({
            'source': f"node_{edge.get('source', 0)}",
            'target': f"node_{edge.get('target', 0)}",
            'type': edge.get("type", "unknown"),
            'attributes': edge.get("attributes", {})
        })
    
    # Use advanced visualizer to create 3D network graph
    return visualizer.create_interactive_3d_network_graph(graph_data)

# Enhanced app layout with tabs
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Living Truth Engine - Enhanced Analysis Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    dbc.Tabs([
        dbc.Tab(label="Visualizations", tab_id="tab-visualizations", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Visualization Controls"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Visualization Type:"),
                                    dcc.Dropdown(
                                        id='visualization-type',
                                        options=[
                                            {'label': '3D Network Graph', 'value': 'network_3d'},
                                            {'label': '2D Network Graph', 'value': 'network_2d'},
                                            {'label': 'Timeline Analysis', 'value': 'timeline'},
                                            {'label': 'Centrality Analysis', 'value': 'centrality'},
                                            {'label': 'Claims Verification', 'value': 'claims'},
                                            {'label': 'Statistics Overview', 'value': 'stats'}
                                        ],
                                        value='network_3d'
                                    )
                                ], width=6),
                                dbc.Col([
                                    html.Label("Data File:"),
                                    dcc.Dropdown(id='data-file', placeholder="Select a data file...")
                                ], width=6)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button('Refresh Data', id='refresh-btn', n_clicks=0, color="primary", className="mt-3")
                                ], width=12)
                            ])
                        ])
                    ], className="mb-4")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Primary Visualization"),
                        dbc.CardBody([
                            dcc.Graph(id='visualization-graph', style={'height': '600px'})
                        ])
                    ])
                ], width=8),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Analysis Statistics"),
                        dbc.CardBody(id='data-info')
                    ], className="mb-3"),
                    dbc.Card([
                        dbc.CardHeader("Entity Distribution"),
                        dbc.CardBody([
                            dcc.Graph(id='entity-distribution')
                        ])
                    ])
                ], width=4)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Secondary Analysis"),
                        dbc.CardBody([
                            dcc.Graph(id='secondary-graph')
                        ])
                    ])
                ])
            ], className="mt-4"),
        ]),
        dbc.Tab(label="Job Runs", tab_id="tab-job-runs", children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Veritas Runs"),
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Run:"),
                                    dcc.Dropdown(id='run-selector')
                                ], width=6),
                                dbc.Col([
                                    html.Label("Gates:"),
                                    dcc.Checklist(id='gate-toggles', options=[
                                        {"label": "Enable OCR on demand", "value": "ocr"},
                                        {"label": "Allow HF burst", "value": "hf_burst"}
                                    ], value=[])
                                ], width=6)
                            ]),
                            dbc.Button('Refresh Runs', id='refresh-runs-btn', n_clicks=0, color="secondary", className="mt-3"),
                            dbc.Button('Start Test Run', id='start-test-run-btn', n_clicks=0, color="primary", className="mt-3 ms-2"),
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Run Summary"),
                        dbc.CardBody(id='run-summary')
                    ], className="mb-3"),
                    dbc.Card([
                        dbc.CardHeader("Provenance Status"),
                        dbc.CardBody(id='provenance-status')
                    ])
                ], width=8)
            ])
        ])
    ], id="tabs", active_tab="tab-visualizations"),
    dcc.Interval(id='interval-component', interval=30*1000, n_intervals=0)
], fluid=True)

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
    Output('visualization-graph', 'figure'),
    Input('visualization-type', 'value'),
    Input('data-file', 'value')
)
def update_visualization(viz_type, filename):
    """Update primary visualization figure; other panels update via separate callbacks."""
    if not filename:
        return go.Figure()
    
    data = load_visualization_data()
    
    # Find the selected file
    selected_data = None
    for item in data["network_graphs"]:
        if item["name"] == filename:
            selected_data = item["data"]
            break
    
    if not selected_data:
        return go.Figure()
    
    # Convert data format for advanced visualizer
    graph_data = {
        'nodes': {},
        'edges': []
    }
    
    # Process nodes
    for i, node in enumerate(selected_data.get("nodes", [])):
        node_id = f"node_{i}"
        graph_data['nodes'][node_id] = {
            'label': node.get("label", f"Node {i}"),
            'type': node.get("type", "unknown"),
            'confidence': node.get("confidence", 0.5),
            'description': node.get("description", "")
        }
    
    # Process edges
    for edge in selected_data.get("edges", []):
        graph_data['edges'].append({
            'source': f"node_{edge.get('source', 0)}",
            'target': f"node_{edge.get('target', 0)}",
            'type': edge.get("type", "unknown"),
            'attributes': edge.get("attributes", {})
        })
    
    # Create visualization based on type
    if viz_type == 'network_3d':
        fig = visualizer.create_interactive_3d_network_graph(graph_data)
    elif viz_type == 'network_2d':
        fig = create_enhanced_network_graph(selected_data)
    elif viz_type == 'centrality':
        fig = visualizer.create_centrality_analysis(graph_data)
    elif viz_type == 'timeline':
        # Create timeline data from graph
        timeline_data = []
        for node_id, node_data in graph_data['nodes'].items():
            if 'timestamp' in node_data:
                timeline_data.append({
                    'timestamp': node_data['timestamp'],
                    'event': node_data['label'],
                    'entity': node_data['label'],
                    'confidence': node_data.get('confidence', 0.5),
                    'type': node_data.get('type', 'unknown')
                })
        fig = visualizer.create_timeline_visualization(timeline_data)
    elif viz_type == 'claims':
        # Create claims data from graph
        claims_data = []
        for node_id, node_data in graph_data['nodes'].items():
            claims_data.append({
                'claim': node_data['label'],
                'confidence': node_data.get('confidence', 0.5),
                'category': node_data.get('type', 'unknown'),
                'description': node_data.get('description', '')
            })
        fig = go.Figure()
    elif viz_type == 'stats':
        fig = go.Figure()
    else:
        fig = go.Figure()
        info = "Unknown visualization type"
    
    return fig

@app.callback(
    Output('data-info', 'children'),
    Input('visualization-type', 'value'),
    Input('data-file', 'value')
)
def update_data_info(viz_type, filename):
    if not filename:
        return "No file selected"
    data = load_visualization_data()
    selected_data = None
    for item in data["network_graphs"]:
        if item["name"] == filename:
            selected_data = item["data"]
            break
    if not selected_data:
        return "File not found"
    node_count = len(selected_data.get("nodes", []))
    edge_count = len(selected_data.get("edges", []))
    return f"{viz_type}: {node_count} nodes, {edge_count} edges"

@app.callback(
    Output('entity-distribution', 'figure'),
    Input('visualization-type', 'value'),
    Input('data-file', 'value')
)
def update_entity_distribution(viz_type, filename):
    if not filename:
        return go.Figure()
    data = load_visualization_data()
    selected_data = None
    for item in data["network_graphs"]:
        if item["name"] == filename:
            selected_data = item["data"]
            break
    if not selected_data:
        return go.Figure()
    entity_counts = {}
    for node in selected_data.get("nodes", []):
        t = node.get('type', 'unknown')
        entity_counts[t] = entity_counts.get(t, 0) + 1
    if entity_counts:
        return px.pie(values=list(entity_counts.values()), names=list(entity_counts.keys()), title="Entity Distribution by Type")
    return go.Figure()

@app.callback(
    Output('secondary-graph', 'figure'),
    Input('visualization-type', 'value'),
    Input('data-file', 'value')
)
def update_secondary_graph(viz_type, filename):
    if not filename:
        return go.Figure()
    data = load_visualization_data()
    selected_data = None
    for item in data["network_graphs"]:
        if item["name"] == filename:
            selected_data = item["data"]
            break
    if not selected_data:
        return go.Figure()
    graph_data = {'nodes': {}, 'edges': []}
    for i, node in enumerate(selected_data.get("nodes", [])):
        graph_data['nodes'][f"node_{i}"] = {
            'label': node.get("label", f"Node {i}"),
            'type': node.get("type", "unknown"),
            'confidence': node.get("confidence", 0.5),
            'description': node.get("description", "")
        }
    if viz_type in ('network_3d', 'network_2d'):
        return visualizer.create_centrality_analysis(graph_data)
    if viz_type == 'centrality':
        return visualizer.create_timeline_visualization([])
    return go.Figure()

# Job Runs callbacks
@app.callback(
    Output('run-selector', 'options'),
    Output('run-selector', 'value'),
    Input('refresh-runs-btn', 'n_clicks')
)
def update_runs(_):
    try:
        from ingestion_general.runners import VeritasRunner
        runs = VeritasRunner().list_runs(limit=50)
        options = [{"label": r, "value": r} for r in runs]
        return options, (options[0]["value"] if options else None)
    except Exception as e:
        logger.error(f"Failed to list runs: {e}")
        return [], None

@app.callback(
    Output('run-summary', 'children'),
    Output('provenance-status', 'children'),
    Input('run-selector', 'value')
)
def update_run_summary(run_id):
    if not run_id:
        return "No run selected", ""
    try:
        from ingestion_general.runners import VeritasRunner
        data = VeritasRunner().open_bundle(run_id)
        manifest = data.get("manifest", {})
        proofs = data.get("proofs", {})
        prov = "present" if proofs.get("merkle_roots") else "missing"
        return (json.dumps(manifest, indent=2), f"Provenance: {prov}")
    except Exception as e:
        logger.error(f"Failed to open bundle: {e}")
        return "Error opening bundle", ""

@app.callback(
    Output('refresh-runs-btn', 'children'),
    Input('refresh-runs-btn', 'n_clicks')
)
def refresh_runs_btn(n):
    return f"Refresh Runs ({n or 0})"

@app.callback(
    Output('start-test-run-btn', 'children'),
    Input('start-test-run-btn', 'n_clicks'),
    State('gate-toggles', 'value')
)
def start_test_run(n, gates):
    if not n:
        return "Start Test Run"
    try:
        from ingestion_general.runners import VeritasRunner
        runner = VeritasRunner()
        topic = "Test Veritas Run"
        runner.start(topic=topic, max_docs=1, sources=["web"])  # minimal scaffold
        return f"Started ({n})"
    except Exception as e:
        logger.error(f"Failed to start test run: {e}")
        return "Start Failed"

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
from fastapi import FastAPI, Request
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse

# Create FastAPI app
fastapi_app = FastAPI(title="Living Truth Engine Dashboard")

# Lightweight metadata endpoint for server-side verification (tests/smoke)
@fastapi_app.get("/meta")
def dashboard_meta():
    return {
        "service": "dashboard",
        "tabs": ["Visualizations", "Job Runs"],
        "title": "Living Truth Engine - Enhanced Dashboard"
    }

# Phase 6 compatibility: expose /health at root path for smoke tests
@fastapi_app.get("/health")
def dashboard_health():
    return {"status": "healthy", "service": "unified_dashboard"}

# Mount Dash app as WSGI middleware at root
fastapi_app.mount("/", WSGIMiddleware(app.server))

# Add health check endpoint (this won't work if mounted at root)
# We'll use a different approach - add it to the Dash app itself

# API additions for Phase 8.2
def _get_hub_server():
    """Lazy-load and cache the MCP Hub Server instance."""
    if not hasattr(_get_hub_server, "_hub"):
        try:
            from src.mcp_servers.mcp_hub_server import MCPHubServer
            _get_hub_server._hub = MCPHubServer()
        except Exception:
            _get_hub_server._hub = None
    return _get_hub_server._hub


@fastapi_app.get("/api/health")
def api_health():
    return {"status": "healthy", "service": "unified_dashboard"}


@fastapi_app.get("/api/runs")
def api_list_runs():
    try:
        hub = _get_hub_server()
        if hub:
            result = hub.execute_tool("list_veritas_runs", {"limit": 20})
            return {"status": "ok", "data": json.loads(result)}
        # Fallback to filesystem listing
        runs_dir = Path("data/outputs/runs")
        runs = []
        if runs_dir.exists():
            runs = [p.name[:-11] for p in runs_dir.glob("*.veritasrun") if p.is_dir()]
        return {"status": "ok", "data": {"runs": runs}}
    except Exception as e:
        return {"status": "error", "error": {"code": "list_failed", "msg": str(e)}}


@fastapi_app.post("/api/runs/youtube/start")
async def api_start_youtube_run(request: Request):
    """Start a YouTube analysis run via MCP with toggle propagation and human-friendly naming."""
    try:
        data = await request.json()
        channel_url = (data.get("channel_url") or "").strip()
        limit = int(data.get("limit") or 10)
        max_depth = int(data.get("max_depth") or 1)
        ocr = bool(data.get("ocr") or False)
        js_render = bool(data.get("js_render") or False)
        selection = data.get("selection", "oldest")
        transcript_pref = data.get("transcript_pref", "yt_api")

        human_name = f"{channel_url or 'YouTube'} — {limit} videos — depth {max_depth}"
        params = {
            "topic": human_name,
            "channel_url": channel_url,
            "selection": selection,
            "max_videos": limit,
            "crawl_depth": max_depth,
            "transcript_pref": transcript_pref,
            "ocr_mode": ("auto_retry" if ocr else "off"),
            "sources": ["youtube", "web"] if js_render else ["youtube"],
            "human_name": human_name,
        }

        hub = _get_hub_server()
        if not hub:
            return {"status": "error", "error": {"code": "mcp_unavailable", "msg": "MCP server not available"}}

        # Emit activity start
        try:
            from src.api.ai_activity import bus as activity_bus
            import asyncio as _asyncio
            _asyncio.create_task(activity_bus.emit("llm", "working", {"stage": "start_run"}))
        except Exception:
            pass

        result = hub.execute_tool("start_veritas_run", params)
        return {"status": "ok", "data": json.loads(result)}
    except Exception as e:
        try:
            from src.api.ai_activity import bus as activity_bus
            import asyncio as _asyncio
            _asyncio.create_task(activity_bus.emit("llm", "error", {"error": str(e)}))
        except Exception:
            pass
        return {"status": "error", "error": {"code": "start_failed", "msg": str(e)}}


@fastapi_app.post("/api/execute")
async def api_execute_tool(request: Request):
    try:
        data = await request.json()
        tool_name = data.get("tool_name")
        params = data.get("params", {})
        if not tool_name:
            return {"status": "error", "error": {"code": "invalid_request", "msg": "tool_name is required"}}
        hub = _get_hub_server()
        if not hub:
            return {"status": "error", "error": {"code": "mcp_unavailable", "msg": "MCP server not available"}}
        result = hub.execute_tool(tool_name, params)
        # Attempt to parse JSON responses
        try:
            parsed = json.loads(result)
        except Exception:
            parsed = result
        return {"status": "ok", "data": parsed}
    except Exception as e:
        return {"status": "error", "error": {"code": "execute_failed", "msg": str(e)}}


@fastapi_app.post("/api/ai/chat")
async def api_ai_chat(request: Request):
    try:
        data = await request.json()
        message = (data.get("message") or "").strip()
        context_run_id = (data.get("context_run_id") or "").strip()
        if not message:
            return {"status": "error", "error": {"code": "invalid_request", "msg": "message is required"}}

        hub = _get_hub_server()
        if not hub:
            return {"status": "error", "error": {"code": "mcp_unavailable", "msg": "MCP server not available"}}

        try:
            from src.api.ai_activity import bus as activity_bus
            import asyncio as _asyncio
            _asyncio.create_task(activity_bus.emit("llm", "inference", {"context_run_id": context_run_id}))
        except Exception:
            pass

        tool_name = "generate_lm_studio_text"
        params = {"prompt": message}
        result = hub.execute_tool(tool_name, params)

        try:
            from src.api.ai_activity import bus as activity_bus
            import asyncio as _asyncio
            _asyncio.create_task(activity_bus.emit("llm", "done", {"context_run_id": context_run_id}))
        except Exception:
            pass

        # Try parse JSON
        try:
            parsed = json.loads(result)
        except Exception:
            parsed = result
        return {"status": "ok", "data": parsed}
    except Exception as e:
        try:
            from src.api.ai_activity import bus as activity_bus
            import asyncio as _asyncio
            _asyncio.create_task(activity_bus.emit("llm", "error", {"error": str(e)}))
        except Exception:
            pass
        return {"status": "error", "error": {"code": "chat_failed", "msg": str(e)}}


@fastapi_app.websocket("/ws/ai-activity")
async def ai_activity_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        from src.api.ai_activity import bus as activity_bus
        async for event in activity_bus.subscribe():
            await websocket.send_json({"ai_type": event.ai_type, "status": event.status, "meta": event.meta})
    except WebSocketDisconnect:
        return
    except Exception as e:
        try:
            await websocket.send_json({"ai_type": "system", "status": "error", "meta": {"msg": str(e)}})
        except Exception:
            pass
        await websocket.close()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 