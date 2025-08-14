'use client';

import React, { forwardRef, useImperativeHandle, useMemo } from 'react';
import { ForceGraph2D } from 'react-force-graph';

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
}

interface ForceGraphWrapperProps {
    data: GraphData;
    onNodeClick: (node: GraphNode) => void;
    getNodeColor: (type: string) => string;
    pinnedNodes?: Set<string>;
}

export interface ForceGraphWrapperRef {
    zoomIn: () => void;
    zoomOut: () => void;
    zoomToFit: () => void;
}

const ForceGraphWrapper = forwardRef<ForceGraphWrapperRef, ForceGraphWrapperProps>(
    ({ data, onNodeClick, getNodeColor, pinnedNodes = new Set() }, ref) => {
        const graphRef = React.useRef<any>(null); // eslint-disable-line @typescript-eslint/no-explicit-any

        useImperativeHandle(ref, () => ({
            zoomIn: () => {
                if (graphRef.current?.zoomIn) {
                    graphRef.current.zoomIn();
                }
            },
            zoomOut: () => {
                if (graphRef.current?.zoomOut) {
                    graphRef.current.zoomOut();
                }
            },
            zoomToFit: () => {
                if (graphRef.current?.zoomToFit) {
                    graphRef.current.zoomToFit();
                }
            },
        }));

        // Memoize graph data for performance
        const graphData = useMemo(() => ({
            nodes: data.nodes,
            links: data.edges
        }), [data.nodes, data.edges]);

        // Enhanced node rendering with pinning support
        const nodeCanvasObject = React.useCallback((node: any, ctx: any, globalScale: any) => {
            const label = node.label;
            const fontSize = Math.max(12 / globalScale, 8); // Minimum font size
            ctx.font = `${fontSize}px Sans-Serif`;
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

            // Draw background
            ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
            ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);

            // Draw border for pinned nodes
            if (pinnedNodes.has(node.id)) {
                ctx.strokeStyle = '#3b82f6';
                ctx.lineWidth = 2;
                ctx.strokeRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2, ...bckgDimensions);
            }

            // Draw text
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#000';
            ctx.fillText(label, node.x, node.y);
        }, [pinnedNodes]);

        // Enhanced node color with pinning indication
        const nodeColor = React.useCallback((node: any) => {
            const baseColor = getNodeColor(node.type);
            if (pinnedNodes.has(node.id)) {
                // Add a subtle glow effect for pinned nodes
                return baseColor;
            }
            return baseColor;
        }, [getNodeColor, pinnedNodes]);

        // Enhanced node size based on connections and pinning
        const nodeRelSize = React.useCallback((node: any) => {
            const baseSize = 6;
            const connectionCount = data.edges.filter((edge: any) =>
                edge.source === node.id || edge.target === node.id
            ).length;
            const sizeMultiplier = Math.min(1 + connectionCount * 0.2, 2); // Cap at 2x
            return pinnedNodes.has(node.id) ? baseSize * sizeMultiplier * 1.2 : baseSize * sizeMultiplier;
        }, [data.edges, pinnedNodes]);

        return (
            <ForceGraph2D
                ref={graphRef}
                graphData={graphData}
                nodeLabel="label"
                nodeColor={nodeColor}
                nodeRelSize={nodeRelSize}
                linkColor={() => '#94a3b8'}
                linkWidth={1}
                linkDirectionalParticles={2}
                linkDirectionalParticleSpeed={0.005}
                onNodeClick={(node: any) => onNodeClick(node)} // eslint-disable-line @typescript-eslint/no-explicit-any
                cooldownTicks={50} // Reduced for better performance
                nodeCanvasObject={nodeCanvasObject}
                enableNodeDrag={true}
                enableZoomInteraction={true}
                enablePanInteraction={true}
                d3AlphaDecay={0.02} // Faster stabilization
                d3VelocityDecay={0.3} // Better performance
                linkDirectionalArrowLength={3}
                linkDirectionalArrowRelPos={1}
                linkCurvature={0.1}
                // Performance optimizations
                enablePointerInteraction={true}
                enableZoomPanInteraction={true}
                // Smooth animations
                d3Force="link"
                d3ForceLinkDistance={30}
                d3ForceLinkStrength={0.5}
                d3ForceChargeStrength={-100}
                d3ForceCenterX={0}
                d3ForceCenterY={0}
            />
        );
    }
);

ForceGraphWrapper.displayName = 'ForceGraphWrapper';

export default ForceGraphWrapper;
