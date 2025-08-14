'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useClientMetrics } from '@/hooks/useClientMetrics';
import {
    Activity,
    AlertTriangle,
    Clock,
    Eye,
    EyeOff,
    HardDrive,
    MousePointer,
    RefreshCw
} from 'lucide-react';
import { useEffect, useState } from 'react';

export default function MetricsDisplay() {
    const { getMetrics, logMetrics } = useClientMetrics();
    const [metrics, setMetrics] = useState(getMetrics());
    const [isVisible, setIsVisible] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics(getMetrics());
        }, 1000);

        return () => clearInterval(interval);
    }, [getMetrics]);

    const formatTime = (ms: number) => {
        if (ms < 1000) return `${ms.toFixed(0)}ms`;
        return `${(ms / 1000).toFixed(2)}s`;
    };

    const formatMemory = (bytes?: number) => {
        if (!bytes) return 'N/A';
        return `${(bytes / 1024 / 1024).toFixed(2)}MB`;
    };

    const getApiPerformance = () => {
        const apiTimes = metrics.apiResponseTimes;
        const endpoints = Object.keys(apiTimes);

        if (endpoints.length === 0) return null;

        return endpoints.map(endpoint => {
            const times = apiTimes[endpoint];
            const avg = times.reduce((a, b) => a + b, 0) / times.length;
            const min = Math.min(...times);
            const max = Math.max(...times);

            return {
                endpoint,
                avg,
                min,
                max,
                count: times.length
            };
        });
    };

    if (!isVisible) {
        return (
            <div className="fixed bottom-4 right-4 z-50">
                <Button
                    onClick={() => setIsVisible(true)}
                    size="sm"
                    variant="outline"
                    className="flex items-center gap-2 bg-white/90 backdrop-blur-sm"
                >
                    <Activity className="h-4 w-4" />
                    Show Metrics
                </Button>
            </div>
        );
    }

    return (
        <div className="fixed bottom-4 right-4 z-50 w-80">
            <Card className="bg-white/95 backdrop-blur-sm border-gray-200 shadow-lg">
                <CardHeader className="pb-3">
                    <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center gap-2 text-sm">
                            <Activity className="h-4 w-4" />
                            Client Metrics
                        </CardTitle>
                        <div className="flex items-center gap-1">
                            <Button
                                onClick={() => setIsExpanded(!isExpanded)}
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0"
                            >
                                {isExpanded ? <EyeOff className="h-3 w-3" /> : <Eye className="h-3 w-3" />}
                            </Button>
                            <Button
                                onClick={logMetrics}
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0"
                            >
                                <RefreshCw className="h-3 w-3" />
                            </Button>
                            <Button
                                onClick={() => setIsVisible(false)}
                                size="sm"
                                variant="ghost"
                                className="h-6 w-6 p-0"
                            >
                                ×
                            </Button>
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="space-y-3">
                    {/* Basic Metrics */}
                    <div className="grid grid-cols-2 gap-2 text-xs">
                        <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3 text-blue-500" />
                            <span>Load:</span>
                            <Badge variant="outline" className="text-xs">
                                {formatTime(metrics.pageLoadTime)}
                            </Badge>
                        </div>

                        <div className="flex items-center gap-1">
                            <MousePointer className="h-3 w-3 text-green-500" />
                            <span>Interactions:</span>
                            <Badge variant="outline" className="text-xs">
                                {metrics.userInteractions}
                            </Badge>
                        </div>

                        <div className="flex items-center gap-1">
                            <AlertTriangle className="h-3 w-3 text-red-500" />
                            <span>Errors:</span>
                            <Badge variant="outline" className="text-xs">
                                {metrics.errorCount}
                            </Badge>
                        </div>

                        <div className="flex items-center gap-1">
                            <HardDrive className="h-3 w-3 text-purple-500" />
                            <span>Memory:</span>
                            <Badge variant="outline" className="text-xs">
                                {formatMemory(metrics.memoryUsage)}
                            </Badge>
                        </div>
                    </div>

                    {/* API Performance (expanded view) */}
                    {isExpanded && (
                        <div className="space-y-2">
                            <div className="text-xs font-medium text-gray-600">API Performance</div>
                            {getApiPerformance() ? (
                                <div className="space-y-1">
                                    {getApiPerformance()!.map((api) => (
                                        <div key={api.endpoint} className="text-xs space-y-1">
                                            <div className="font-mono text-gray-700 truncate">
                                                {api.endpoint}
                                            </div>
                                            <div className="grid grid-cols-3 gap-1 text-xs">
                                                <div>avg: {formatTime(api.avg)}</div>
                                                <div>min: {formatTime(api.min)}</div>
                                                <div>max: {formatTime(api.max)}</div>
                                            </div>
                                            <div className="text-gray-500">
                                                {api.count} calls
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-xs text-gray-500">No API calls recorded</div>
                            )}
                        </div>
                    )}

                    {/* Session Info */}
                    <div className="text-xs text-gray-500 border-t pt-2">
                        Session: {metrics.timestamp}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
