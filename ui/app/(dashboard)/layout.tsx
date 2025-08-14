'use client';

import { Header } from '@/components/dashboard/Header';
import { Sidebar } from '@/components/dashboard/Sidebar';
import ErrorBoundary from '@/components/ErrorBoundary';
import MetricsDisplay from '@/components/MetricsDisplay';
import { useClientMetrics } from '@/hooks/useClientMetrics';
import { QueryProvider } from '@/lib/query';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // Initialize client metrics
  useClientMetrics();

  return (
    <ErrorBoundary>
      <QueryProvider>
        <div className="min-h-screen bg-background">
          <div className="flex">
            <Sidebar />
            <div className="flex-1 flex flex-col">
              <Header />
              <main className="flex-1 p-6">
                {children}
              </main>
            </div>
          </div>
          {/* Development metrics display */}
          {process.env.NODE_ENV === 'development' && <MetricsDisplay />}
        </div>
      </QueryProvider>
    </ErrorBoundary>
  );
}
