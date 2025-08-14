import { test, expect } from '@playwright/test';

test.describe('Ingestion Tests', () => {
  test('should load runs page and display runs list', async ({ page }) => {
    await page.goto('/runs');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that the page title is displayed
    await expect(page.getByRole('heading', { name: 'Runs' })).toBeVisible();
    
    // Check that runs table is present
    await expect(page.getByText('Recent Runs')).toBeVisible();
    
    // Check that the table headers are present
    await expect(page.getByText('ID')).toBeVisible();
    await expect(page.getByText('Status')).toBeVisible();
    await expect(page.getByText('Created')).toBeVisible();
  });

  test('should display run details when clicking on a run', async ({ page }) => {
    await page.goto('/runs');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Click on the first run in the table
    const firstRun = page.locator('table tbody tr').first();
    await firstRun.click();
    
    // Check that we're on the run detail page
    await expect(page.getByText('Run Details')).toBeVisible();
    
    // Check that run information is displayed
    await expect(page.getByText('Documents')).toBeVisible();
    await expect(page.getByText('Manifest')).toBeVisible();
  });

  test('should handle empty runs list', async ({ page }) => {
    // Mock empty runs response
    await page.route('**/api/runs', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            runs: [],
            total: 0
          }
        })
      });
    });

    await page.goto('/runs');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that empty state is displayed
    await expect(page.getByText('No runs found')).toBeVisible();
  });

  test('should display run status badges correctly', async ({ page }) => {
    await page.goto('/runs');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that status badges are present
    const statusBadges = page.locator('[data-testid="status-badge"]');
    await expect(statusBadges.first()).toBeVisible();
  });
});
