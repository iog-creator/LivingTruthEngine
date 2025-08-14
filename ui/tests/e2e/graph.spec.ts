import { test, expect } from '@playwright/test';

test.describe('Graph Tests', () => {
  test('should load graph page and display graph visualization', async ({ page }) => {
    await page.goto('/graph');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that the page title is displayed
    await expect(page.getByRole('heading', { name: 'Graph' })).toBeVisible();
    
    // Check that graph container is present
    await expect(page.getByTestId('graph-container')).toBeVisible();
    
    // Check that graph controls are present
    await expect(page.getByText('Graph Controls')).toBeVisible();
  });

  test('should display graph statistics', async ({ page }) => {
    await page.goto('/graph');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that graph stats are displayed
    await expect(page.getByText('Graph Statistics')).toBeVisible();
    
    // Check that node and edge counts are present
    await expect(page.getByText('Nodes')).toBeVisible();
    await expect(page.getByText('Edges')).toBeVisible();
  });

  test('should handle graph loading state', async ({ page }) => {
    // Mock slow graph response
    await page.route('**/api/graph/**', route => {
      // Delay the response to simulate loading
      setTimeout(() => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            status: 'ok',
            data: {
              nodes: [],
              edges: [],
              stats: {
                total_nodes: 0,
                total_edges: 0,
                node_types: {},
                edge_types: {}
              }
            }
          })
        });
      }, 2000);
    });

    await page.goto('/graph');
    
    // Check that loading state is displayed
    await expect(page.getByText('Loading graph...')).toBeVisible();
  });

  test('should handle empty graph data', async ({ page }) => {
    // Mock empty graph response
    await page.route('**/api/graph/**', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            nodes: [],
            edges: [],
            stats: {
              total_nodes: 0,
              total_edges: 0,
              node_types: {},
              edge_types: {}
            }
          }
        })
      });
    });

    await page.goto('/graph');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that empty state is displayed
    await expect(page.getByText('No graph data available')).toBeVisible();
  });

  test('should display graph filters', async ({ page }) => {
    await page.goto('/graph');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that filter controls are present
    await expect(page.getByText('Filters')).toBeVisible();
    
    // Check that node type filter is present
    await expect(page.getByText('Node Types')).toBeVisible();
    
    // Check that edge type filter is present
    await expect(page.getByText('Edge Types')).toBeVisible();
  });
});
