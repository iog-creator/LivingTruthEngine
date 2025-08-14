'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, Bug, Info, RefreshCw } from 'lucide-react';
import React from 'react';

interface ErrorBoundaryState {
    hasError: boolean;
    error?: Error;
    errorInfo?: React.ErrorInfo;
    errorId?: string;
}

interface ErrorBoundaryProps {
    children: React.ReactNode;
    fallback?: React.ComponentType<{ error: Error; errorInfo?: React.ErrorInfo; errorId?: string; resetError: () => void }>;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
    constructor(props: ErrorBoundaryProps) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): ErrorBoundaryState {
        // Generate a unique error ID for tracking
        const errorId = `error_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

        // Log error to console for development
        console.error('ErrorBoundary caught an error:', error);

        return {
            hasError: true,
            error,
            errorId
        };
    }

    componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
        // Log error details
        console.error('ErrorBoundary error details:', {
            error: error.message,
            stack: error.stack,
            componentStack: errorInfo.componentStack,
            errorId: this.state.errorId
        });

        // Update state with error info
        this.setState({
            errorInfo,
            errorId: this.state.errorId
        });

        // In a real app, you would send this to your error reporting service
        // Example: Sentry.captureException(error, { extra: errorInfo });
    }

    resetError = () => {
        this.setState({ hasError: false, error: undefined, errorInfo: undefined, errorId: undefined });
    };

    render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                const FallbackComponent = this.props.fallback;
                return (
                    <FallbackComponent
                        error={this.state.error!}
                        errorInfo={this.state.errorInfo}
                        errorId={this.state.errorId}
                        resetError={this.resetError}
                    />
                );
            }

            return (
                <DefaultErrorFallback
                    error={this.state.error!}
                    errorInfo={this.state.errorInfo}
                    errorId={this.state.errorId}
                    resetError={this.resetError}
                />
            );
        }

        return this.props.children;
    }
}

interface ErrorFallbackProps {
    error: Error;
    errorInfo?: React.ErrorInfo;
    errorId?: string;
    resetError: () => void;
}

function DefaultErrorFallback({ error, errorInfo, errorId, resetError }: ErrorFallbackProps) {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
            <Card className="w-full max-w-2xl">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-red-600">
                        <AlertTriangle className="h-5 w-5" />
                        Something went wrong
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="bg-red-50 border border-red-200 rounded-md p-4">
                        <div className="flex items-start gap-3">
                            <Bug className="h-5 w-5 text-red-500 mt-0.5" />
                            <div className="flex-1">
                                <h3 className="font-medium text-red-800">Error Details</h3>
                                <p className="text-sm text-red-700 mt-1">{error.message}</p>
                                {errorId && (
                                    <p className="text-xs text-red-600 mt-2 font-mono">
                                        Error ID: {errorId}
                                    </p>
                                )}
                            </div>
                        </div>
                    </div>

                    {errorInfo && (
                        <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
                            <div className="flex items-start gap-3">
                                <Info className="h-5 w-5 text-gray-500 mt-0.5" />
                                <div className="flex-1">
                                    <h3 className="font-medium text-gray-800">Component Stack</h3>
                                    <pre className="text-xs text-gray-600 mt-2 whitespace-pre-wrap overflow-auto max-h-32">
                                        {errorInfo.componentStack}
                                    </pre>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="flex gap-3">
                        <Button onClick={resetError} className="flex items-center gap-2">
                            <RefreshCw className="h-4 w-4" />
                            Try Again
                        </Button>
                        <Button
                            variant="outline"
                            onClick={() => window.location.reload()}
                            className="flex items-center gap-2"
                        >
                            <RefreshCw className="h-4 w-4" />
                            Reload Page
                        </Button>
                    </div>

                    <div className="text-xs text-gray-500 text-center">
                        If this problem persists, please contact support with the Error ID above.
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default ErrorBoundary;
