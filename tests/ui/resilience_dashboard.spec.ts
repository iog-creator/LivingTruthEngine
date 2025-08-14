import { test, expect } from '@playwright/test';

test.describe('Resilience Dashboard', () => {
  test('should load and display resilience data', async ({ page }) => {
    await page.goto('/ui/resilience');
    
    // Verify gauge renders
    await expect(page.locator('[data-testid="resilience-gauge"]')).toBeVisible();
    
    // Verify chaos table populates
    await expect(page.locator('[data-testid="chaos-results-table"]')).toBeVisible();
    
    // Verify trend graph shows history
    await expect(page.locator('[data-testid="trends-chart"]')).toBeVisible();
    
    // Verify filter input is present
    await expect(page.locator('[data-testid="chaos-filter-scenario"]')).toBeVisible();
  });

  test('should display correct resilience score', async ({ page }) => {
    await page.goto('/ui/resilience');
    
    const gauge = page.locator('[data-testid="resilience-gauge"]');
    await expect(gauge).toContainText('86.0');
  });

  test('should display chaos test data', async ({ page }) => {
    await page.goto('/ui/resilience');
    
    const table = page.locator('[data-testid="chaos-results-table"]');
    await expect(table).toContainText('cpu_pressure');
  });

  test('should display trends data', async ({ page }) => {
    await page.goto('/ui/resilience');
    
    const trends = page.locator('[data-testid="trends-chart"]');
    await expect(trends).toContainText('series: 24');
  });
});
