'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import {
    Activity,
    AlertCircle,
    CheckCircle,
    Clock,
    Cpu,
    Database,
    Gpu,
    Info,
    RefreshCw,
    Server,
    Settings,
    Wifi,
    XCircle
} from 'lucide-react';
import { Suspense, useState } from 'react';

interface HealthGate {
    name: string;
    status: 'ok' | 'error' | 'warning';
    message?: string;
    last_check?: string;
}

interface FallbackEvent {
    timestamp: string;
    type: string;
    reason: string;
    duration_ms: number;
}

interface HealthData {
    all_gates_passed: boolean;
    service: string;
    gates: Record<string, HealthGate>;
    errors: string[];
    fallbacks_enabled: boolean;
    embedding_model: string;
    embedding_dim: number;
    models_checksum: string;
    pgvector: {
        status: string;
        connection: string;
    };
    rulego: {
        status: string;
        policies: number;
    };
    reverse_proxy: boolean;
    ui_origin: string;
}

// Mock data for demonstration (will be replaced with API call)
const mockHealthData: HealthData = {
    all_gates_passed: true,
    service: "unified_dashboard",
    gates: {
        "lmstudio": {
            name: "LM Studio",
            status: "ok",
            message: "Models available",
            last_check: "2025-08-13T10:30:00Z"
        },
        "langflow": {
            name: "Langflow",
            status: "ok",
            message: "Workflow engine ready",
            last_check: "2025-08-13T10:30:00Z"
        },
        "pgvector": {
            name: "PostgreSQL + pgvector",
            status: "ok",
            message: "Database and vector store operational",
            last_check: "2025-08-13T10:30:00Z"
        },
        "rulego": {
            name: "Rulego",
            status: "ok",
            message: "Policy engine loaded",
            last_check: "2025-08-13T10:30:00Z"
        },
        "mcp_hub": {
            name: "MCP Hub Server",
            status: "ok",
            message: "Tool registry available",
            last_check: "2025-08-13T10:30:00Z"
        }
    },
    errors: [],
    fallbacks_enabled: true,
    embedding_model: "sentence-transformers/all-MiniLM-L6-v2",
    embedding_dim: 384,
    models_checksum: "a1b2c3d4e5f6...",
    pgvector: {
        status: "operational",
        connection: "postgresql://postgres:pass@postgres:5432/living_truth_engine"
    },
    rulego: {
        status: "loaded",
        policies: 3
    },
    reverse_proxy: true,
    ui_origin: "http://localhost:3000"
};

const mockFallbackEvents: FallbackEvent[] = [
    {
        timestamp: "2025-08-13T10:25:00Z",
        type: "reranker_cpu",
        reason: "GPU occupied by LLM",
        duration_ms: 1500
    },
    {
        timestamp: "2025-08-13T10:20:00Z",
        type: "youtube_captions",
        reason: "MCP fetch failed",
        duration_ms: 800
    }
];

function HealthContent() {
    const [isRefreshing, setIsRefreshing] = useState(false);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'ok':
                return <CheckCircle className="h-4 w-4 text-green-500" />;
            case 'error':
                return <XCircle className="h-4 w-4 text-red-500" />;
            case 'warning':
                return <AlertCircle className="h-4 w-4 text-yellow-500" />;
            default:
                return <Info className="h-4 w-4 text-gray-500" />;
        }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'ok':
                return 'bg-green-100 text-green-800';
            case 'error':
                return 'bg-red-100 text-red-800';
            case 'warning':
                return 'bg-yellow-100 text-yellow-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    const getGateIcon = (gateName: string) => {
        switch (gateName.toLowerCase()) {
            case 'lmstudio':
                return <Cpu className="h-4 w-4" />;
            case 'langflow':
                return <Server className="h-4 w-4" />;
            case 'pgvector':
                return <Database className="h-4 w-4" />;
            case 'rulego':
                return <Settings className="h-4 w-4" />;
            case 'mcp_hub':
                return <Wifi className="h-4 w-4" />;
            default:
                return <Activity className="h-4 w-4" />;
        }
    };

    const handleRefresh = () => {
        setIsRefreshing(true);
        // Simulate API call
        setTimeout(() => setIsRefreshing(false), 1000);
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Health</h1>
                    <p className="text-muted-foreground">
                        System health status and fallback events
                    </p>
                </div>
                <Button
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    variant="outline"
                >
                    <RefreshCw className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                    Refresh
                </Button>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                {/* Overall Status */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Activity className="h-5 w-5" />
                            Overall Status
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="flex items-center gap-2">
                                {mockHealthData.all_gates_passed ? (
                                    <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : (
                                    <XCircle className="h-4 w-4 text-red-500" />
                                )}
                                <Badge className={mockHealthData.all_gates_passed ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                                    {mockHealthData.all_gates_passed ? 'Healthy' : 'Unhealthy'}
                                </Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">
                                All health gates passing
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* Service */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Server className="h-5 w-5" />
                            Service
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="text-sm font-medium">{mockHealthData.service}</div>
                            <p className="text-xs text-muted-foreground">
                                Unified Dashboard
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* Embedding Model */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Gpu className="h-5 w-5" />
                            Embedding Model
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="text-sm font-medium">{mockHealthData.embedding_model}</div>
                            <p className="text-xs text-muted-foreground">
                                Dim: {mockHealthData.embedding_dim}
                            </p>
                        </div>
                    </CardContent>
                </Card>

                {/* Models Checksum */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Settings className="h-5 w-5" />
                            Models Checksum
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div className="text-sm font-mono">{mockHealthData.models_checksum}</div>
                            <p className="text-xs text-muted-foreground">
                                SSOT configuration
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Health Gates */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Activity className="h-5 w-5" />
                        Health Gates
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Gate</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Message</TableHead>
                                    <TableHead>Last Check</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {Object.entries(mockHealthData.gates).map(([key, gate]) => (
                                    <TableRow key={key}>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {getGateIcon(gate.name)}
                                                <span className="font-medium">{gate.name}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {getStatusIcon(gate.status)}
                                                <Badge className={getStatusColor(gate.status)}>
                                                    {gate.status.toUpperCase()}
                                                </Badge>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <span className="text-sm text-muted-foreground">
                                                {gate.message || 'No message'}
                                            </span>
                                        </TableCell>
                                        <TableCell>
                                            <span className="text-sm text-muted-foreground">
                                                {gate.last_check ? new Date(gate.last_check).toLocaleTimeString() : 'Never'}
                                            </span>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>

            {/* Fallback Events */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <AlertCircle className="h-5 w-5" />
                        Recent Fallback Events
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {mockFallbackEvents.length > 0 ? (
                        <div className="rounded-md border">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>Timestamp</TableHead>
                                        <TableHead>Type</TableHead>
                                        <TableHead>Reason</TableHead>
                                        <TableHead>Duration</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {mockFallbackEvents.map((event, index) => (
                                        <TableRow key={index}>
                                            <TableCell>
                                                <div className="flex items-center gap-2">
                                                    <Clock className="h-4 w-4 text-muted-foreground" />
                                                    <span className="text-sm">
                                                        {new Date(event.timestamp).toLocaleTimeString()}
                                                    </span>
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant="outline" className="font-mono text-xs">
                                                    {event.type}
                                                </Badge>
                                            </TableCell>
                                            <TableCell>
                                                <span className="text-sm text-muted-foreground">
                                                    {event.reason}
                                                </span>
                                            </TableCell>
                                            <TableCell>
                                                <span className="text-sm font-mono">
                                                    {event.duration_ms}ms
                                                </span>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </div>
                    ) : (
                        <div className="text-center py-8 text-muted-foreground">
                            <CheckCircle className="h-8 w-8 mx-auto mb-2 text-green-500" />
                            <p>No fallback events recorded</p>
                            <p className="text-sm">All systems operating normally</p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* System Information */}
            <div className="grid gap-6 md:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Database className="h-5 w-5" />
                            Database Status
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div><strong>Status:</strong> {mockHealthData.pgvector.status}</div>
                            <div><strong>Connection:</strong>
                                <span className="font-mono text-xs ml-2">
                                    {mockHealthData.pgvector.connection.split('@')[1]}
                                </span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Settings className="h-5 w-5" />
                            Rulego Status
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2">
                            <div><strong>Status:</strong> {mockHealthData.rulego.status}</div>
                            <div><strong>Policies Loaded:</strong> {mockHealthData.rulego.policies}</div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

export default function HealthPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <HealthContent />
        </Suspense>
    );
}
