'use client';

import { useCallback, useEffect, useRef } from 'react';

interface ClientMetrics {
    pageLoadTime: number;
    apiResponseTimes: Record<string, number[]>;
    errorCount: number;
    userInteractions: number;
    memoryUsage?: number;
    timestamp: number;
}

interface MetricsData {
    metrics: ClientMetrics;
    sessionId: string;
    userAgent: string;
    timestamp: number;
}

class ClientMetricsManager {
    private static instance: ClientMetricsManager;
    private metrics: ClientMetrics;
    private sessionId: string;
    private isDevelopment: boolean;

    private constructor() {
        this.sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this.isDevelopment = process.env.NODE_ENV === 'development';

        this.metrics = {
            pageLoadTime: 0,
            apiResponseTimes: {},
            errorCount: 0,
            userInteractions: 0,
            memoryUsage: undefined,
            timestamp: Date.now()
        };

        this.initializeMetrics();
    }

    static getInstance(): ClientMetricsManager {
        if (!ClientMetricsManager.instance) {
            ClientMetricsManager.instance = new ClientMetricsManager();
        }
        return ClientMetricsManager.instance;
    }

    private initializeMetrics() {
        // Track page load time
        if (typeof window !== 'undefined') {
            window.addEventListener('load', () => {
                const loadTime = performance.now();
                this.metrics.pageLoadTime = loadTime;

                if (this.isDevelopment) {
                    console.log('📊 Client Metrics - Page Load Time:', `${loadTime.toFixed(2)}ms`);
                }
            });

            // Track memory usage if available
            if ('memory' in performance) {
                const memory = (performance as any).memory;
                this.metrics.memoryUsage = memory.usedJSHeapSize;

                if (this.isDevelopment) {
                    console.log('📊 Client Metrics - Memory Usage:', `${(memory.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB`);
                }
            }
        }
    }

    trackApiCall(endpoint: string, startTime: number, endTime: number) {
        const duration = endTime - startTime;

        if (!this.metrics.apiResponseTimes[endpoint]) {
            this.metrics.apiResponseTimes[endpoint] = [];
        }

        this.metrics.apiResponseTimes[endpoint].push(duration);

        // Keep only last 10 measurements per endpoint
        if (this.metrics.apiResponseTimes[endpoint].length > 10) {
            this.metrics.apiResponseTimes[endpoint] = this.metrics.apiResponseTimes[endpoint].slice(-10);
        }

        if (this.isDevelopment) {
            console.log(`📊 Client Metrics - API Call: ${endpoint} took ${duration.toFixed(2)}ms`);
        }
    }

    trackError() {
        this.metrics.errorCount++;

        if (this.isDevelopment) {
            console.log(`📊 Client Metrics - Error count: ${this.metrics.errorCount}`);
        }
    }

    trackUserInteraction() {
        this.metrics.userInteractions++;

        if (this.isDevelopment && this.metrics.userInteractions % 10 === 0) {
            console.log(`📊 Client Metrics - User interactions: ${this.metrics.userInteractions}`);
        }
    }

    getMetrics(): ClientMetrics {
        return { ...this.metrics };
    }

    getMetricsData(): MetricsData {
        return {
            metrics: this.getMetrics(),
            sessionId: this.sessionId,
            userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'unknown',
            timestamp: Date.now()
        };
    }

    // Development helper to display metrics in console
    logMetrics() {
        if (this.isDevelopment) {
            console.group('📊 Client Metrics Summary');
            console.log('Session ID:', this.sessionId);
            console.log('Page Load Time:', `${this.metrics.pageLoadTime.toFixed(2)}ms`);
            console.log('Error Count:', this.metrics.errorCount);
            console.log('User Interactions:', this.metrics.userInteractions);

            if (this.metrics.memoryUsage) {
                console.log('Memory Usage:', `${(this.metrics.memoryUsage / 1024 / 1024).toFixed(2)}MB`);
            }

            console.log('API Response Times:');
            Object.entries(this.metrics.apiResponseTimes).forEach(([endpoint, times]) => {
                const avg = times.reduce((a, b) => a + b, 0) / times.length;
                const min = Math.min(...times);
                const max = Math.max(...times);
                console.log(`  ${endpoint}: avg=${avg.toFixed(2)}ms, min=${min.toFixed(2)}ms, max=${max.toFixed(2)}ms`);
            });
            console.groupEnd();
        }
    }
}

export function useClientMetrics() {
    const metricsManager = useRef(ClientMetricsManager.getInstance());
    const interactionTimeout = useRef<NodeJS.Timeout | undefined>(undefined);

    const trackApiCall = useCallback((endpoint: string, startTime: number, endTime: number) => {
        metricsManager.current.trackApiCall(endpoint, startTime, endTime);
    }, []);

    const trackError = useCallback(() => {
        metricsManager.current.trackError();
    }, []);

    const trackUserInteraction = useCallback(() => {
        metricsManager.current.trackUserInteraction();

        // Debounce interaction tracking
        if (interactionTimeout.current) {
            clearTimeout(interactionTimeout.current);
        }

        interactionTimeout.current = setTimeout(() => {
            // This will be called after user stops interacting
        }, 1000);
    }, []);

    const getMetrics = useCallback(() => {
        return metricsManager.current.getMetrics();
    }, []);

    const getMetricsData = useCallback(() => {
        return metricsManager.current.getMetricsData();
    }, []);

    const logMetrics = useCallback(() => {
        metricsManager.current.logMetrics();
    }, []);

    useEffect(() => {
        // Set up global error tracking
        const handleError = (event: ErrorEvent) => {
            trackError();
        };

        const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
            trackError();
        };

        // Set up user interaction tracking
        const handleUserInteraction = () => {
            trackUserInteraction();
        };

        if (typeof window !== 'undefined') {
            window.addEventListener('error', handleError);
            window.addEventListener('unhandledrejection', handleUnhandledRejection);

            // Track various user interactions
            window.addEventListener('click', handleUserInteraction);
            window.addEventListener('keydown', handleUserInteraction);
            window.addEventListener('scroll', handleUserInteraction);

            // Log metrics on page unload
            window.addEventListener('beforeunload', () => {
                logMetrics();
            });

            // Log metrics every 30 seconds in development
            if (process.env.NODE_ENV === 'development') {
                const interval = setInterval(() => {
                    logMetrics();
                }, 30000);

                return () => {
                    clearInterval(interval);
                    window.removeEventListener('error', handleError);
                    window.removeEventListener('unhandledrejection', handleUnhandledRejection);
                    window.removeEventListener('click', handleUserInteraction);
                    window.removeEventListener('keydown', handleUserInteraction);
                    window.removeEventListener('scroll', handleUserInteraction);
                };
            }
        }

        return () => {
            if (typeof window !== 'undefined') {
                window.removeEventListener('error', handleError);
                window.removeEventListener('unhandledrejection', handleUnhandledRejection);
                window.removeEventListener('click', handleUserInteraction);
                window.removeEventListener('keydown', handleUserInteraction);
                window.removeEventListener('scroll', handleUserInteraction);
            }
        };
    }, [trackError, trackUserInteraction, logMetrics]);

    return {
        trackApiCall,
        trackError,
        trackUserInteraction,
        getMetrics,
        getMetricsData,
        logMetrics
    };
}
