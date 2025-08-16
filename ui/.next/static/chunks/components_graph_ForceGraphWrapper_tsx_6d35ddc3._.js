(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/components/graph/ForceGraphWrapper.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>__TURBOPACK__default__export__
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$force$2d$graph$2f$dist$2f$react$2d$force$2d$graph$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/react-force-graph/dist/react-force-graph.mjs [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
'use client';
;
;
const ForceGraphWrapper = /*#__PURE__*/ _s((0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["forwardRef"])(_c = _s((param, ref)=>{
    let { data, onNodeClick, getNodeColor, pinnedNodes = new Set() } = param;
    _s();
    const graphRef = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].useRef(null); // eslint-disable-line @typescript-eslint/no-explicit-any
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useImperativeHandle"])(ref, {
        "ForceGraphWrapper.useImperativeHandle": ()=>({
                zoomIn: ({
                    "ForceGraphWrapper.useImperativeHandle": ()=>{
                        var _graphRef_current;
                        if ((_graphRef_current = graphRef.current) === null || _graphRef_current === void 0 ? void 0 : _graphRef_current.zoomIn) {
                            graphRef.current.zoomIn();
                        }
                    }
                })["ForceGraphWrapper.useImperativeHandle"],
                zoomOut: ({
                    "ForceGraphWrapper.useImperativeHandle": ()=>{
                        var _graphRef_current;
                        if ((_graphRef_current = graphRef.current) === null || _graphRef_current === void 0 ? void 0 : _graphRef_current.zoomOut) {
                            graphRef.current.zoomOut();
                        }
                    }
                })["ForceGraphWrapper.useImperativeHandle"],
                zoomToFit: ({
                    "ForceGraphWrapper.useImperativeHandle": ()=>{
                        var _graphRef_current;
                        if ((_graphRef_current = graphRef.current) === null || _graphRef_current === void 0 ? void 0 : _graphRef_current.zoomToFit) {
                            graphRef.current.zoomToFit();
                        }
                    }
                })["ForceGraphWrapper.useImperativeHandle"]
            })
    }["ForceGraphWrapper.useImperativeHandle"]);
    // Memoize graph data for performance
    const graphData = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useMemo"])({
        "ForceGraphWrapper.useMemo[graphData]": ()=>({
                nodes: data.nodes,
                links: data.edges
            })
    }["ForceGraphWrapper.useMemo[graphData]"], [
        data.nodes,
        data.edges
    ]);
    // Enhanced node rendering with pinning support
    const nodeCanvasObject = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].useCallback({
        "ForceGraphWrapper.useCallback[nodeCanvasObject]": (node, ctx, globalScale)=>{
            const label = node.label;
            const fontSize = Math.max(12 / globalScale, 8); // Minimum font size
            ctx.font = "".concat(fontSize, "px Sans-Serif");
            const textWidth = ctx.measureText(label).width;
            const bckgDimensions = [
                textWidth,
                fontSize
            ].map({
                "ForceGraphWrapper.useCallback[nodeCanvasObject].bckgDimensions": (n)=>n + fontSize * 0.2
            }["ForceGraphWrapper.useCallback[nodeCanvasObject].bckgDimensions"]);
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
        }
    }["ForceGraphWrapper.useCallback[nodeCanvasObject]"], [
        pinnedNodes
    ]);
    // Enhanced node color with pinning indication
    const nodeColor = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].useCallback({
        "ForceGraphWrapper.useCallback[nodeColor]": (node)=>{
            const baseColor = getNodeColor(node.type);
            if (pinnedNodes.has(node.id)) {
                // Add a subtle glow effect for pinned nodes
                return baseColor;
            }
            return baseColor;
        }
    }["ForceGraphWrapper.useCallback[nodeColor]"], [
        getNodeColor,
        pinnedNodes
    ]);
    // Enhanced node size based on connections and pinning
    const nodeRelSize = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].useCallback({
        "ForceGraphWrapper.useCallback[nodeRelSize]": (node)=>{
            const baseSize = 6;
            const connectionCount = data.edges.filter({
                "ForceGraphWrapper.useCallback[nodeRelSize]": (edge)=>edge.source === node.id || edge.target === node.id
            }["ForceGraphWrapper.useCallback[nodeRelSize]"]).length;
            const sizeMultiplier = Math.min(1 + connectionCount * 0.2, 2); // Cap at 2x
            return pinnedNodes.has(node.id) ? baseSize * sizeMultiplier * 1.2 : baseSize * sizeMultiplier;
        }
    }["ForceGraphWrapper.useCallback[nodeRelSize]"], [
        data.edges,
        pinnedNodes
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$react$2d$force$2d$graph$2f$dist$2f$react$2d$force$2d$graph$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["ForceGraph2D"], {
        ref: graphRef,
        graphData: graphData,
        nodeLabel: "label",
        nodeColor: nodeColor,
        nodeRelSize: nodeRelSize,
        linkColor: ()=>'#94a3b8',
        linkWidth: 1,
        linkDirectionalParticles: 2,
        linkDirectionalParticleSpeed: 0.005,
        onNodeClick: (node)=>onNodeClick(node),
        cooldownTicks: 50,
        nodeCanvasObject: nodeCanvasObject,
        enableNodeDrag: true,
        enableZoomInteraction: true,
        enablePanInteraction: true,
        d3AlphaDecay: 0.02,
        d3VelocityDecay: 0.3,
        linkDirectionalArrowLength: 3,
        linkDirectionalArrowRelPos: 1,
        linkCurvature: 0.1,
        // Performance optimizations
        enablePointerInteraction: true,
        enableZoomPanInteraction: true,
        // Smooth animations
        d3Force: "link",
        d3ForceLinkDistance: 30,
        d3ForceLinkStrength: 0.5,
        d3ForceChargeStrength: -100,
        d3ForceCenterX: 0,
        d3ForceCenterY: 0
    }, void 0, false, {
        fileName: "[project]/components/graph/ForceGraphWrapper.tsx",
        lineNumber: 114,
        columnNumber: 13
    }, ("TURBOPACK compile-time value", void 0));
}, "Lkwy72KCz4Fgfy1w5kanYtgAyRU=")), "Lkwy72KCz4Fgfy1w5kanYtgAyRU=");
_c1 = ForceGraphWrapper;
ForceGraphWrapper.displayName = 'ForceGraphWrapper';
const __TURBOPACK__default__export__ = ForceGraphWrapper;
var _c, _c1;
__turbopack_context__.k.register(_c, "ForceGraphWrapper$forwardRef");
__turbopack_context__.k.register(_c1, "ForceGraphWrapper");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/components/graph/ForceGraphWrapper.tsx [app-client] (ecmascript, next/dynamic entry)": ((__turbopack_context__) => {

__turbopack_context__.n(__turbopack_context__.i("[project]/components/graph/ForceGraphWrapper.tsx [app-client] (ecmascript)"));
}),
}]);

//# sourceMappingURL=components_graph_ForceGraphWrapper_tsx_6d35ddc3._.js.map