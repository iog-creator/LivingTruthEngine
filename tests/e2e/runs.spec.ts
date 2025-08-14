import { test, expect } from '@playwright/test';

test.describe('Runs Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the runs page
    await page.goto('/runs');
  });

  test('should display runs page with start form and run list', async ({ page }) => {
    // Check page title
    await expect(page.getByRole('heading', { name: 'Runs' })).toBeVisible();
    
    // Check description
    await expect(page.getByText('Manage and monitor analysis runs')).toBeVisible();
    
    // Check start form section
    await expect(page.getByRole('heading', { name: 'Start New Run' })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Start Analysis Run' })).toBeVisible();
    
    // Check recent runs section
    await expect(page.getByRole('heading', { name: 'Recent Runs' })).toBeVisible();
  });

  test('should have start run form with required fields', async ({ page }) => {
    // Check form fields
    await expect(page.getByLabel('YouTube Channel URL')).toBeVisible();
    await expect(page.getByLabel('Video Limit')).toBeVisible();
    await expect(page.getByLabel('Max Depth')).toBeVisible();
    await expect(page.getByLabel('Sort Order')).toBeVisible();
    
    // Check advanced options toggle
    await expect(page.getByText('Advanced Options')).toBeVisible();
    
    // Check submit button
    await expect(page.getByRole('button', { name: 'Start Analysis Run' })).toBeVisible();
  });

  test('should show advanced options when toggled', async ({ page }) => {
    // Toggle advanced options
    await page.getByRole('switch', { name: 'Advanced Options' }).click();
    
    // Check advanced fields are visible
    await expect(page.getByLabel('OCR Required')).toBeVisible();
    await expect(page.getByLabel('JavaScript Render')).toBeVisible();
    await expect(page.getByLabel('Hugging Face Burst')).toBeVisible();
    await expect(page.getByLabel('Run Label (Optional)')).toBeVisible();
    await expect(page.getByLabel('Save To Directory (Optional)')).toBeVisible();
  });

  test('should display run list with refresh functionality', async ({ page }) => {
    // Check refresh button
    await expect(page.getByRole('button', { name: 'Refresh' })).toBeVisible();
    
    // Check if runs are displayed (may be empty initially)
    const runList = page.locator('[data-testid="run-list"]').or(page.locator('text=No Runs Found'));
    await expect(runList).toBeVisible();
  });

  test('should navigate to run detail page', async ({ page }) => {
    // Mock API response for runs
    await page.route('/api/runs', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            runs: [
              {
                id: 'test-run-123',
                human_name: 'Test Run',
                created_at: new Date().toISOString(),
                status: 'completed',
                document_count: 5,
                source_type: 'youtube'
              }
            ]
          }
        })
      });
    });

    // Refresh the page to get the mocked data
    await page.reload();
    
    // Wait for run card to appear
    await expect(page.getByText('Test Run')).toBeVisible();
    
    // Click on run card to navigate to detail page
    await page.getByText('Test Run').click();
    
    // Should navigate to run detail page
    await expect(page).toHaveURL(/\/runs\/test-run-123/);
  });

  test('should display run detail page with tabs', async ({ page }) => {
    // Mock API responses
    await page.route('/api/runs/test-run-123', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            id: 'test-run-123',
            human_name: 'Test Run',
            created_at: new Date().toISOString(),
            status: 'completed',
            manifest: { test: 'manifest' },
            metrics: { test: 'metrics' },
            merkle: { root_hash: 'abc123', leaf_hashes: ['hash1', 'hash2'] }
          }
        })
      });
    });

    await page.route('/api/runs/test-run-123/corpus', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            documents: [
              {
                title: 'Test Document',
                content: 'Test content',
                source_type: 'youtube',
                url: 'https://example.com'
              }
            ]
          }
        })
      });
    });

    // Navigate to run detail page
    await page.goto('/runs/test-run-123');
    
    // Check page title
    await expect(page.getByRole('heading', { name: 'Run Details' })).toBeVisible();
    
    // Check run header
    await expect(page.getByText('Test Run')).toBeVisible();
    await expect(page.getByText('completed')).toBeVisible();
    
    // Check tabs
    await expect(page.getByRole('tab', { name: 'Manifest' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Metrics' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Merkle' })).toBeVisible();
    await expect(page.getByRole('tab', { name: 'Corpus' })).toBeVisible();
    
    // Check manifest tab content
    await page.getByRole('tab', { name: 'Manifest' }).click();
    await expect(page.getByText('"test": "manifest"')).toBeVisible();
    
    // Check metrics tab content
    await page.getByRole('tab', { name: 'Metrics' }).click();
    await expect(page.getByText('"test": "metrics"')).toBeVisible();
    
    // Check merkle tab content
    await page.getByRole('tab', { name: 'Merkle' }).click();
    await expect(page.getByText('abc123')).toBeVisible();
    await expect(page.getByText('2')).toBeVisible(); // leaf count
    
    // Check corpus tab content
    await page.getByRole('tab', { name: 'Corpus' }).click();
    await expect(page.getByText('Test Document')).toBeVisible();
    await expect(page.getByText('Test content')).toBeVisible();
  });

  test('should handle form submission with loading states', async ({ page }) => {
    // Mock API response for successful run start
    await page.route('/api/runs/youtube/start', async route => {
      // Simulate delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            run_id: 'new-run-456',
            status: 'started',
            message: 'Run started successfully'
          }
        })
      });
    });

    // Fill form
    await page.getByLabel('YouTube Channel URL').fill('https://www.youtube.com/@testchannel');
    await page.getByLabel('Video Limit').fill('5');
    await page.getByLabel('Max Depth').fill('2');
    
    // Submit form
    await page.getByRole('button', { name: 'Start Analysis Run' }).click();
    
    // Check loading state
    await expect(page.getByText('Starting Run...')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Starting Run...' })).toBeDisabled();
    
    // Wait for completion
    await expect(page.getByText('Starting Run...')).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Start Analysis Run' })).toBeVisible();
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock API error response
    await page.route('/api/runs', async route => {
      await route.fulfill({
        status: 503,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'error',
          error: 'Service temporarily unavailable'
        })
      });
    });

    // Refresh page to trigger error
    await page.reload();
    
    // Check error state
    await expect(page.getByText('Error Loading Runs')).toBeVisible();
    await expect(page.getByText('Service temporarily unavailable')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Retry' })).toBeVisible();
  });

  test('should show empty state when no runs exist', async ({ page }) => {
    // Mock empty runs response
    await page.route('/api/runs', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          status: 'ok',
          data: {
            runs: []
          }
        })
      });
    });

    // Refresh page
    await page.reload();
    
    // Check empty state
    await expect(page.getByText('No Runs Found')).toBeVisible();
    await expect(page.getByText('Start your first analysis run')).toBeVisible();
  });
});
