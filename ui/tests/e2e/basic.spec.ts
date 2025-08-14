import { test, expect } from '@playwright/test';

test.describe('Basic UI Tests', () => {
  test('should load overview page without infinite loops', async ({ page }) => {
    // Navigate to the overview page
    await page.goto('http://localhost:3000/overview');
    
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
    
    // Check that the page loads without errors
    await expect(page.locator('body')).toBeVisible();
    
    // Check that we don't have infinite loop errors
    const errorMessages = await page.locator('text=Maximum update depth exceeded').count();
    expect(errorMessages).toBe(0);
    
    // Check that the sidebar is present
    await expect(page.locator('text=Living Truth Engine')).toBeVisible();
    
    // Check that health cards are present (even if empty)
    await expect(page.locator('text=System Status')).toBeVisible();
  });

  test('should navigate between pages without infinite loops', async ({ page }) => {
    // Start at overview
    await page.goto('http://localhost:3000/overview');
    await page.waitForLoadState('networkidle');
    
    // Navigate to runs page
    await page.click('text=Runs');
    await page.waitForLoadState('networkidle');
    
    // Check that we're on the runs page
    await expect(page.locator('body')).toBeVisible();
    
    // Check for no infinite loop errors
    const errorMessages = await page.locator('text=Maximum update depth exceeded').count();
    expect(errorMessages).toBe(0);
    
    // Navigate back to overview
    await page.click('text=Overview');
    await page.waitForLoadState('networkidle');
    
    // Check that we're back on overview
    await expect(page.locator('text=System Status')).toBeVisible();
  });

  test('should handle sidebar toggle without infinite loops', async ({ page }) => {
    await page.goto('http://localhost:3000/overview');
    await page.waitForLoadState('networkidle');
    
    // Toggle sidebar on mobile
    await page.setViewportSize({ width: 768, height: 600 });
    
    // Look for mobile menu button and click it
    const menuButton = page.locator('button[aria-label="Toggle menu"], button:has-text("Menu")').first();
    if (await menuButton.isVisible()) {
      await menuButton.click();
      await page.waitForTimeout(500);
    }
    
    // Check for no infinite loop errors
    const errorMessages = await page.locator('text=Maximum update depth exceeded').count();
    expect(errorMessages).toBe(0);
  });
});
