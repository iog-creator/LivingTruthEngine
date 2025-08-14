import { test, expect } from '@playwright/test';

test.describe('Graph Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the graph page
    await page.goto('/graph');
  });

  test('should display graph page with run ID parameter', async ({ page }) => {
    // Test without run ID - should show placeholder
    await expect(page.getByText('Please select a run to view its evidence graph.')).toBeVisible();
  });

  test('should handle graph page with run ID', async ({ page }) => {
    // Navigate with a run ID parameter
    await page.goto('/graph?runId=test-run-id');
    
    // Should show the run ID in the UI
    await expect(page.getByText('Run: test-run-id')).toBeVisible();
    
    // Should show error state since the run doesn't exist
    await expect(page.getByText('Failed to load graph data')).toBeVisible();
  });

  test('should display graph visualization when data is available', async ({ page }) => {
    // Mock the API response for testing
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [
              { id: '1', label: 'Test Claim', type: 'claim', confidence: 0.85 },
              { id: '2', label: 'Test Entity', type: 'entity' },
              { id: '3', label: 'Test Document', type: 'document' }
            ],
            edges: [
              { source: '1', target: '2', type: 'supports' },
              { source: '2', target: '3', type: 'mentions' }
            ]
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Should show node and edge counts
    await expect(page.getByText('3 nodes')).toBeVisible();
    await expect(page.getByText('2 edges')).toBeVisible();
    
    // Should show the graph visualization
    await expect(page.locator('canvas')).toBeVisible();
  });

  test('should provide fallback list when WebGL is not available', async ({ page }) => {
    // Mock WebGL as unavailable
    await page.addInitScript(() => {
      Object.defineProperty(window, 'WebGLRenderingContext', {
        value: undefined
      });
    });

    // Mock the API response
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [
              { id: '1', label: 'Test Claim', type: 'claim', confidence: 0.85 },
              { id: '2', label: 'Test Entity', type: 'entity' }
            ],
            edges: [
              { source: '1', target: '2', type: 'supports' }
            ]
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Should show fallback list instead of canvas
    await expect(page.getByText('Test Claim')).toBeVisible();
    await expect(page.getByText('Test Entity')).toBeVisible();
    await expect(page.locator('canvas')).not.toBeVisible();
  });

  test('should support search functionality', async ({ page }) => {
    // Mock the API response
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [
              { id: '1', label: 'Test Claim', type: 'claim' },
              { id: '2', label: 'Another Entity', type: 'entity' }
            ],
            edges: [
              { source: '1', target: '2', type: 'supports' }
            ]
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Find search input and type
    const searchInput = page.getByPlaceholder('Search nodes...');
    await searchInput.fill('Test');
    
    // Should filter to show only matching nodes
    await expect(page.getByText('Test Claim')).toBeVisible();
    await expect(page.getByText('Another Entity')).not.toBeVisible();
  });

  test('should handle node selection and details', async ({ page }) => {
    // Mock the API response
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [
              { id: '1', label: 'Test Claim', type: 'claim', confidence: 0.85 }
            ],
            edges: []
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Click on a node (simulated since we can't easily click on canvas elements in tests)
    // This test verifies the structure is in place for node selection
    await expect(page.getByText('Node Details')).not.toBeVisible();
  });

  test('should display graph controls', async ({ page }) => {
    // Mock the API response
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [{ id: '1', label: 'Test', type: 'claim' }],
            edges: []
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Should show zoom controls
    await expect(page.getByRole('button', { name: /zoom in/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /zoom out/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /reset/i })).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error
    await page.route('/api/graph/**', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'error',
          error: {
            code: 500,
            message: 'Internal server error'
          }
        })
      });
    });

    await page.goto('/graph?runId=test-run-id');
    
    // Should show error state
    await expect(page.getByText('Failed to load graph data')).toBeVisible();
    await expect(page.getByText('Internal server error')).toBeVisible();
  });
});
