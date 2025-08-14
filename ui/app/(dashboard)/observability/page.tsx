'use client';

import ErrorTestComponent from '@/components/ErrorTestComponent';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useClientMetrics } from '@/hooks/useClientMetrics';
import { useApiRetry } from '@/hooks/useRetryPolicy';
import {
    Activity,
    AlertTriangle,
    Bug,
    Info,
    RefreshCw,
    TestTube,
    Zap
} from 'lucide-react';
import { Suspense } from 'react';

function ObservabilityContent() {
    const { getMetrics, logMetrics, trackError } = useClientMetrics();
    const { apiCallWithRetry, retryState } = useApiRetry();

    const handleTestApiCall = async () => {
        try {
            await apiCallWithRetry(
                async () => {
                    // Simulate a potentially failing API call
                    const response = await fetch('/api/health');
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    return response.json();
                },
                {
                    onRetry: (retryCount, error, delay) => {
                        console.log(`Retry ${retryCount} after ${delay}ms due to:`, error);
                    },
                    onSuccess: (result) => {
                        console.log('API call succeeded:', result);
                    },
                    onFinalError: (error) => {
                        console.error('API call failed after all retries:', error);
                    }
                }
            );
        } catch (error) {
            console.error('API call failed:', error);
        }
    };

    const handleManualError = () => {
        trackError();
        console.error('Manual error triggered for testing');
    };

    const metrics = getMetrics();

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Observability</h1>
                    <p className="text-muted-foreground">
                        Test error boundaries, metrics, and retry policies
                    </p>
                </div>
                <Badge variant="outline" className="flex items-center gap-2">
                    <TestTube className="h-4 w-4" />
                    Development Tools
                </Badge>
            </div>

            <div className="grid gap-6 md:grid-cols-2">
                {/* Error Boundary Test */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Bug className="h-5 w-5" />
                            Error Boundary Test
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <ErrorTestComponent onErrorTriggered={trackError} />
                    </CardContent>
                </Card>

                {/* Metrics Overview */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Activity className="h-5 w-5" />
                            Current Metrics
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div className="text-center">
                                <div className="text-2xl font-bold text-blue-600">
                                    {metrics.userInteractions}
                                </div>
                                <div className="text-sm text-muted-foreground">Interactions</div>
                            </div>
                            <div className="text-center">
                                <div className="text-2xl font-bold text-red-600">
                                    {metrics.errorCount}
                                </div>
                                <div className="text-sm text-muted-foreground">Errors</div>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                                <span>Page Load Time:</span>
                                <span className="font-mono">
                                    {metrics.pageLoadTime > 0 ? `${metrics.pageLoadTime.toFixed(0)}ms` : 'N/A'}
                                </span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span>Memory Usage:</span>
                                <span className="font-mono">
                                    {metrics.memoryUsage ? `${(metrics.memoryUsage / 1024 / 1024).toFixed(2)}MB` : 'N/A'}
                                </span>
                            </div>
                        </div>

                        <Button onClick={logMetrics} variant="outline" className="w-full">
                            <RefreshCw className="h-4 w-4 mr-2" />
                            Log Metrics to Console
                        </Button>
                    </CardContent>
                </Card>

                {/* Retry Policy Test */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Zap className="h-5 w-5" />
                            Retry Policy Test
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <p className="text-sm text-muted-foreground">
                            Test the retry policy with API calls. The system will automatically retry failed requests
                            with exponential backoff.
                        </p>

                        <div className="space-y-2">
                            <Button onClick={handleTestApiCall} className="w-full">
                                Test API Call with Retry
                            </Button>

                            {retryState.isRetrying && (
                                <div className="flex items-center gap-2 text-sm text-yellow-600">
                                    <RefreshCw className="h-4 w-4 animate-spin" />
                                    Retrying... (Attempt {retryState.retryCount}/3)
                                </div>
                            )}

                            {retryState.lastError && (
                                <div className="text-sm text-red-600">
                                    Last error: {retryState.lastError.message}
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>

                {/* Manual Error Test */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <AlertTriangle className="h-5 w-5" />
                            Manual Error Test
                        </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <p className="text-sm text-muted-foreground">
                            Manually trigger error tracking to test the metrics system.
                        </p>

                        <Button
                            onClick={handleManualError}
                            variant="destructive"
                            className="w-full"
                        >
                            Trigger Manual Error
                        </Button>

                        <div className="text-xs text-muted-foreground">
                            This will increment the error counter and log to console.
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* API Performance */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Activity className="h-5 w-5" />
                        API Performance
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {Object.keys(metrics.apiResponseTimes).length > 0 ? (
                        <div className="space-y-2">
                            {Object.entries(metrics.apiResponseTimes).map(([endpoint, times]) => {
                                const avg = times.reduce((a, b) => a + b, 0) / times.length;
                                const min = Math.min(...times);
                                const max = Math.max(...times);

                                return (
                                    <div key={endpoint} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                                        <div className="font-mono text-sm">{endpoint}</div>
                                        <div className="flex gap-4 text-sm">
                                            <span>avg: {avg.toFixed(0)}ms</span>
                                            <span>min: {min.toFixed(0)}ms</span>
                                            <span>max: {max.toFixed(0)}ms</span>
                                            <span>calls: {times.length}</span>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-8 text-muted-foreground">
                            <Info className="h-8 w-8 mx-auto mb-2" />
                            <p>No API calls recorded yet</p>
                            <p className="text-sm">Make some API calls to see performance data</p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Instructions */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Info className="h-5 w-5" />
                        How to Test
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid gap-4 md:grid-cols-2">
                        <div>
                            <h4 className="font-semibold mb-2">Error Boundary</h4>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• Click &quot;Show Buggy Component&quot;</li>
                                <li>• Click &quot;Trigger Error&quot; to test error boundary</li>
                                <li>• Verify error boundary catches and displays error</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">Metrics</h4>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• Interact with the page to see interaction count</li>
                                <li>• Trigger errors to see error count</li>
                                <li>• Check console for detailed metrics</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">Retry Policy</h4>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• Test API calls with retry functionality</li>
                                <li>• Watch retry attempts in real-time</li>
                                <li>• Check console for retry logs</li>
                            </ul>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">Development Tools</h4>
                            <ul className="text-sm text-muted-foreground space-y-1">
                                <li>• Use the floating metrics display</li>
                                <li>• Check browser console for logs</li>
                                <li>• Monitor network tab for API calls</li>
                            </ul>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default function ObservabilityPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <ObservabilityContent />
        </Suspense>
    );
}
