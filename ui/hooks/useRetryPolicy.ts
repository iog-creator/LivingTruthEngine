'use client';

import { useCallback, useState } from 'react';

interface RetryConfig {
    maxRetries: number;
    baseDelay: number;
    maxDelay: number;
    backoffMultiplier: number;
    retryCondition?: (error: any) => boolean;
}

interface RetryState {
    isRetrying: boolean;
    retryCount: number;
    lastError?: any;
}

const defaultConfig: RetryConfig = {
    maxRetries: 3,
    baseDelay: 1000, // 1 second
    maxDelay: 10000, // 10 seconds
    backoffMultiplier: 2,
    retryCondition: (error: any) => {
        // Retry on network errors, 5xx server errors, and rate limiting
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            return true; // Network error
        }
        if (error.status >= 500 && error.status < 600) {
            return true; // Server error
        }
        if (error.status === 429) {
            return true; // Rate limiting
        }
        return false;
    }
};

export function useRetryPolicy(config: Partial<RetryConfig> = {}) {
    const [retryState, setRetryState] = useState<RetryState>({
        isRetrying: false,
        retryCount: 0
    });

    const finalConfig = { ...defaultConfig, ...config };

    const calculateDelay = useCallback((retryCount: number): number => {
        const delay = finalConfig.baseDelay * Math.pow(finalConfig.backoffMultiplier, retryCount);
        return Math.min(delay, finalConfig.maxDelay);
    }, [finalConfig]);

    const shouldRetry = useCallback((error: any, retryCount: number): boolean => {
        if (retryCount >= finalConfig.maxRetries) {
            return false;
        }

        if (finalConfig.retryCondition) {
            return finalConfig.retryCondition(error);
        }

        return false;
    }, [finalConfig]);

    const retryWithBackoff = useCallback(async <T>(
        operation: () => Promise<T>,
        onRetry?: (retryCount: number, error: any, delay: number) => void,
        onSuccess?: (result: T) => void,
        onFinalError?: (error: any, totalRetries: number) => void
    ): Promise<T> => {
        let lastError: any;
        let currentRetryCount = 0;

        while (currentRetryCount <= finalConfig.maxRetries) {
            try {
                setRetryState({
                    isRetrying: false,
                    retryCount: currentRetryCount,
                    lastError: undefined
                });

                const result = await operation();

                if (onSuccess) {
                    onSuccess(result);
                }

                return result;
            } catch (error) {
                lastError = error;

                if (!shouldRetry(error, currentRetryCount)) {
                    setRetryState({
                        isRetrying: false,
                        retryCount: currentRetryCount,
                        lastError: error
                    });

                    if (onFinalError) {
                        onFinalError(error, currentRetryCount);
                    }

                    throw error;
                }

                currentRetryCount++;
                const delay = calculateDelay(currentRetryCount - 1);

                setRetryState({
                    isRetrying: true,
                    retryCount: currentRetryCount,
                    lastError: error
                });

                if (onRetry) {
                    onRetry(currentRetryCount, error, delay);
                }

                // Wait before retrying
                await new Promise(resolve => setTimeout(resolve, delay));
            }
        }

        // This should never be reached, but just in case
        throw lastError;
    }, [finalConfig, shouldRetry, calculateDelay]);

    const resetRetryState = useCallback(() => {
        setRetryState({
            isRetrying: false,
            retryCount: 0,
            lastError: undefined
        });
    }, []);

    return {
        retryWithBackoff,
        resetRetryState,
        retryState,
        config: finalConfig
    };
}

// Specialized hook for API calls with retry
export function useApiRetry() {
    const { retryWithBackoff, retryState, resetRetryState } = useRetryPolicy();

    const apiCallWithRetry = useCallback(async <T>(
        apiCall: () => Promise<T>,
        options?: {
            onRetry?: (retryCount: number, error: any, delay: number) => void;
            onSuccess?: (result: T) => void;
            onFinalError?: (error: any, totalRetries: number) => void;
        }
    ): Promise<T> => {
        return retryWithBackoff(
            apiCall,
            (retryCount, error, delay) => {
                console.warn(`API call failed, retrying (${retryCount}/3) in ${delay}ms:`, error);
                if (options?.onRetry) {
                    options.onRetry(retryCount, error, delay);
                }
            },
            options?.onSuccess,
            (error, totalRetries) => {
                console.error(`API call failed after ${totalRetries} retries:`, error);
                if (options?.onFinalError) {
                    options.onFinalError(error, totalRetries);
                }
            }
        );
    }, [retryWithBackoff]);

    return {
        apiCallWithRetry,
        retryState,
        resetRetryState
    };
}
