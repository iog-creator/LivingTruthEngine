'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Filter, Pin, PinOff, RotateCcw, Search, ZoomIn, ZoomOut } from 'lucide-react';
import dynamic from 'next/dynamic';
import { useEffect, useMemo, useRef, useState } from 'react';
import { ForceGraphWrapperRef } from './ForceGraphWrapper';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, unknown>;
}

interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
  properties?: Record<string, unknown>;
}

interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    total_nodes: number;
    total_edges: number;
    node_types: Record<string, number>;
    edge_types: Record<string, number>;
  };
}

interface GraphViewProps {
  data: GraphData;
}

// Create a proper wrapper component for force-graph
const ForceGraphWrapper = dynamic(
  () => import('./ForceGraphWrapper'),
  {
    ssr: false,
    loading: () => <div className="h-[400px] w-full bg-muted animate-pulse flex items-center justify-center">Loading graph visualization...</div>
  }
);

export function GraphView({ data }: GraphViewProps) {
  const [webglSupported, setWebglSupported] = useState<boolean | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [pinnedNodes, setPinnedNodes] = useState<Set<string>>(new Set());
  const [nodeTypeFilters, setNodeTypeFilters] = useState<Set<string>>(new Set(Object.keys(data.stats.node_types)));
  const [showFilters, setShowFilters] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const graphRef = useRef<ForceGraphWrapperRef>(null);

  // Check WebGL support
  useEffect(() => {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    setWebglSupported(!!gl);
  }, []);

  // Memoized filtered data for performance
  const filteredData = useMemo(() => {
    setIsLoading(true);

    // Filter by node type
    const typeFilteredNodes = data.nodes.filter(node =>
      nodeTypeFilters.has(node.type)
    );

    // Filter by search term
    const searchFilteredNodes = typeFilteredNodes.filter(node =>
      node.label.toLowerCase().includes(searchTerm.toLowerCase()) ||
      node.type.toLowerCase().includes(searchTerm.toLowerCase())
    );

    // Filter edges to only include connections between visible nodes
    const visibleNodeIds = new Set(searchFilteredNodes.map(n => n.id));
    const filteredEdges = data.edges.filter(edge =>
      visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target)
    );

    setIsLoading(false);

    return {
      nodes: searchFilteredNodes,
      edges: filteredEdges
    };
  }, [data.nodes, data.edges, searchTerm, nodeTypeFilters]);

  // Node color mapping
  const getNodeColor = (type: string) => {
    switch (type) {
      case 'claim': return '#ef4444'; // red
      case 'entity': return '#3b82f6'; // blue
      case 'document': return '#10b981'; // green
      default: return '#6b7280'; // gray
    }
  };

  // Handle node click
  const handleNodeClick = (node: GraphNode) => {
    setSelectedNode(node);
  };

  // Handle node pinning
  const toggleNodePin = (nodeId: string) => {
    const newPinnedNodes = new Set(pinnedNodes);
    if (newPinnedNodes.has(nodeId)) {
      newPinnedNodes.delete(nodeId);
    } else {
      newPinnedNodes.add(nodeId);
    }
    setPinnedNodes(newPinnedNodes);
  };

  // Handle node type filter toggle
  const toggleNodeTypeFilter = (nodeType: string) => {
    const newFilters = new Set(nodeTypeFilters);
    if (newFilters.has(nodeType)) {
      newFilters.delete(nodeType);
    } else {
      newFilters.add(nodeType);
    }
    setNodeTypeFilters(newFilters);
  };

  // Graph controls
  const zoomIn = () => {
    if (graphRef.current?.zoomIn) {
      graphRef.current.zoomIn();
    }
  };

  const zoomOut = () => {
    if (graphRef.current?.zoomOut) {
      graphRef.current.zoomOut();
    }
  };

  const resetView = () => {
    if (graphRef.current?.zoomToFit) {
      graphRef.current.zoomToFit();
    }
  };

  // Clear all filters
  const clearFilters = () => {
    setSearchTerm('');
    setNodeTypeFilters(new Set(Object.keys(data.stats.node_types)));
    setPinnedNodes(new Set());
  };

  if (webglSupported === false) {
    // Fallback list view when WebGL is not available
    return (
      <div className="space-y-4">
        {/* Enhanced Controls */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 flex-1">
            <Search className="h-4 w-4" />
            <input
              type="text"
              placeholder="Search nodes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-3 py-2 border rounded-md"
            />
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="h-4 w-4" />
            Filters
          </Button>

          <Button variant="outline" size="sm" onClick={clearFilters}>
            Clear
          </Button>
        </div>

        {/* Filters Panel */}
        {showFilters && (
          <Card>
            <CardHeader>
              <CardTitle className="text-sm">Node Type Filters</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {Object.entries(data.stats.node_types).map(([type, count]) => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={type}
                      checked={nodeTypeFilters.has(type)}
                      onCheckedChange={() => toggleNodeTypeFilter(type)}
                    />
                    <label htmlFor={type} className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                      {type} ({count})
                    </label>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Enhanced Node List */}
        <div className="grid gap-2">
          {filteredData.nodes.map((node) => (
            <Card key={node.id} className="cursor-pointer hover:bg-muted/50">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <h4 className="font-medium">{node.label}</h4>
                      {pinnedNodes.has(node.id) && (
                        <Pin className="h-4 w-4 text-blue-500" />
                      )}
                    </div>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge variant="outline">{node.type}</Badge>
                      <span className="text-sm text-muted-foreground">
                        {filteredData.edges.filter(e => e.source === node.id || e.target === node.id).length} connections
                      </span>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      toggleNodePin(node.id);
                    }}
                  >
                    {pinnedNodes.has(node.id) ? (
                      <PinOff className="h-4 w-4" />
                    ) : (
                      <Pin className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Enhanced Controls */}
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 flex-1">
          <Search className="h-4 w-4" />
          <input
            type="text"
            placeholder="Search nodes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-3 py-2 border rounded-md"
          />
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="h-4 w-4" />
            Filters
          </Button>

          <Button variant="outline" size="sm" onClick={clearFilters}>
            Clear
          </Button>

          <Button variant="outline" size="sm" onClick={zoomIn}>
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={zoomOut}>
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={resetView}>
            <RotateCcw className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Node Type Filters</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Object.entries(data.stats.node_types).map(([type, count]) => (
                <div key={type} className="flex items-center space-x-2">
                  <Checkbox
                    id={type}
                    checked={nodeTypeFilters.has(type)}
                    onCheckedChange={() => toggleNodeTypeFilter(type)}
                  />
                  <label htmlFor={type} className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">
                    {type} ({count})
                  </label>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Loading Indicator */}
      {isLoading && (
        <div className="flex items-center justify-center p-4">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-sm text-muted-foreground">Updating graph...</span>
        </div>
      )}

      {/* Graph Visualization */}
      <div className="border rounded-lg overflow-hidden">
        <ForceGraphWrapper
          ref={graphRef}
          data={filteredData}
          onNodeClick={handleNodeClick}
          getNodeColor={getNodeColor}
          pinnedNodes={pinnedNodes}
        />
      </div>

      {/* Enhanced Selected Node Details */}
      {selectedNode && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              Node Details
              <Button
                variant="ghost"
                size="sm"
                onClick={() => toggleNodePin(selectedNode.id)}
              >
                {pinnedNodes.has(selectedNode.id) ? (
                  <PinOff className="h-4 w-4" />
                ) : (
                  <Pin className="h-4 w-4" />
                )}
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div>
                <strong>Label:</strong> {selectedNode.label}
              </div>
              <div>
                <strong>Type:</strong> <Badge variant="outline">{selectedNode.type}</Badge>
              </div>
              <div>
                <strong>Connections:</strong> {
                  filteredData.edges.filter(e => e.source === selectedNode.id || e.target === selectedNode.id).length
                }
              </div>
              {selectedNode.properties && Object.keys(selectedNode.properties).length > 0 && (
                <div>
                  <strong>Properties:</strong>
                  <div className="mt-1 text-sm text-muted-foreground">
                    {Object.entries(selectedNode.properties).map(([key, value]) => (
                      <div key={key}>
                        {key}: {String(value)}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Graph Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="text-sm">Graph Statistics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Visible Nodes:</strong> {filteredData.nodes.length} / {data.stats.total_nodes}
            </div>
            <div>
              <strong>Visible Edges:</strong> {filteredData.edges.length} / {data.stats.total_edges}
            </div>
            <div>
              <strong>Pinned Nodes:</strong> {pinnedNodes.size}
            </div>
            <div>
              <strong>Active Filters:</strong> {nodeTypeFilters.size} / {Object.keys(data.stats.node_types).length}
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
