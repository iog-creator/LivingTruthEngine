'use client';

import { QueryProvider } from '@/lib/query';
import { ErrorBoundary } from '@/components/dashboard/ErrorBoundary';
import { Sidebar } from '@/components/dashboard/Sidebar';
import { Header } from '@/components/dashboard/Header';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
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
        </div>
      </QueryProvider>
    </ErrorBoundary>
  );
}
