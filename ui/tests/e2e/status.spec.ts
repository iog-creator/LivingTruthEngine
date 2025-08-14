import { test, expect } from '@playwright/test';

test.describe('Status Page Tests', () => {
  test('should load overview page and display health status', async ({ page }) => {
    await page.goto('/overview');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that the page title is displayed
    await expect(page.getByRole('heading', { name: 'Living Truth Engine' })).toBeVisible();
    
    // Check that health status is displayed
    await expect(page.getByText('System Status')).toBeVisible();
    
    // Check that the health card is present
    await expect(page.getByTestId('health-card')).toBeVisible();
  });

  test('should display health gates correctly', async ({ page }) => {
    await page.goto('/health');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that health page title is displayed
    await expect(page.getByRole('heading', { name: 'Health' })).toBeVisible();
    
    // Check that health gates table is present
    await expect(page.getByText('Health Gates')).toBeVisible();
    
    // Check that overall status is displayed
    await expect(page.getByText('Overall Status')).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API failure
    await page.route('**/api/health/full', route => {
      route.fulfill({
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

    await page.goto('/overview');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that error is handled gracefully
    await expect(page.getByText('Error loading health status')).toBeVisible();
  });
});
