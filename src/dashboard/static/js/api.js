/**
 * Typed API Helper for Living Truth Engine Dashboard
 * Enforces envelope format: {status, data?, error?}
 */

// Envelope validation
function validateEnvelope(response, path) {
    if (!response || typeof response !== 'object') {
        throw new Error(`Invalid response format for ${path}`);
    }

    // Handle legacy health endpoints
    if ((path === '/api/health' || path === '/api/health/full') && response.status === 'healthy') {
        return response;
    }

    // Envelope format validation
    if (!('status' in response)) {
        throw new Error(`Missing 'status' field in response for ${path}`);
    }

    if (response.status === 'ok' && !('data' in response)) {
        throw new Error(`Missing 'data' field in successful response for ${path}`);
    }

    if (response.status === 'error' && !('error' in response)) {
        throw new Error(`Missing 'error' field in error response for ${path}`);
    }

    return response;
}

// Base URL configuration
const BASE_URL = window.BASE_URL || '';

/**
 * Typed API call function
 * @param {string} path - API endpoint path
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} - Typed response data
 */
async function api(path, options = {}) {
    const url = `${BASE_URL}${path}`;

    // Default headers
    const headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        ...options.headers
    };

    const fetchOptions = {
        ...options,
        headers
    };

    try {
        const response = await fetch(url, fetchOptions);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();
        const validated = validateEnvelope(result, path);

        if (validated.status === 'error') {
            const errorMsg = validated.error?.msg || validated.error?.message || 'API call failed';
            throw new Error(errorMsg);
        }

        return validated.data || validated;

    } catch (error) {
        console.error(`API call failed for ${path}:`, error);
        throw error;
    }
}

/**
 * GET request helper
 * @param {string} path - API endpoint path
 * @returns {Promise<any>} - Response data
 */
async function apiGet(path) {
    return api(path, { method: 'GET' });
}

/**
 * POST request helper
 * @param {string} path - API endpoint path
 * @param {any} data - Request body data
 * @returns {Promise<any>} - Response data
 */
async function apiPost(path, data) {
    return api(path, {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

/**
 * PUT request helper
 * @param {string} path - API endpoint path
 * @param {any} data - Request body data
 * @returns {Promise<any>} - Response data
 */
async function apiPut(path, data) {
    return api(path, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
}

/**
 * DELETE request helper
 * @param {string} path - API endpoint path
 * @returns {Promise<any>} - Response data
 */
async function apiDelete(path) {
    return api(path, { method: 'DELETE' });
}

// Export for use in other scripts
window.LTE_API = {
    api,
    apiGet,
    apiPost,
    apiPut,
    apiDelete,
    validateEnvelope
};
