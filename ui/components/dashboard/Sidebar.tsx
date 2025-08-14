'use client';

import { Button } from '@/components/ui/button';
import { useAppStore } from '@/lib/state';
import { cn } from '@/lib/utils';
import {
  Activity,
  BarChart3,
  Database,
  FileText,
  Settings,
  Users,
  X
} from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useCallback, useMemo } from 'react';

const navigation = [
  {
    name: 'Overview',
    href: '/overview',
    icon: Activity,
  },
  {
    name: 'Runs',
    href: '/runs',
    icon: BarChart3,
  },
  {
    name: 'Graph',
    href: '/graph',
    icon: Database,
  },
  {
    name: 'Claims',
    href: '/claims',
    icon: FileText,
  },
  {
    name: 'Entities',
    href: '/entities',
    icon: Users,
  },
  {
    name: 'Models',
    href: '/models',
    icon: Database,
  },
  {
    name: 'Health',
    href: '/health',
    icon: Activity,
  },
  {
    name: 'Settings',
    href: '/settings',
    icon: Settings,
  },
];

export function Sidebar() {
  const pathname = usePathname();
  const sidebarOpen = useAppStore((state) => state.sidebarOpen);
  const setSidebarOpen = useAppStore((state) => state.setSidebarOpen);

  // Memoize the close handler to prevent re-renders
  const handleClose = useCallback(() => {
    setSidebarOpen(false);
  }, [setSidebarOpen]);

  // Memoize the navigation items to prevent re-renders
  const navigationItems = useMemo(() => {
    return navigation.map((item) => {
      const isActive = pathname === item.href;
      return (
        <Link
          key={item.name}
          href={item.href}
          className={cn(
            'flex items-center space-x-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
            isActive
              ? 'bg-primary text-primary-foreground'
              : 'text-muted-foreground hover:bg-muted hover:text-foreground'
          )}
          onClick={handleClose}
        >
          <item.icon className="h-4 w-4" />
          <span>{item.name}</span>
        </Link>
      );
    });
  }, [pathname, handleClose]);

  return (
    <>
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={handleClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={cn(
          'fixed inset-y-0 left-0 z-50 w-64 bg-background border-r lg:static lg:translate-x-0 transition-transform duration-200 ease-in-out',
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <div className="flex h-full flex-col">
          {/* Header */}
          <div className="flex h-16 items-center justify-between px-6 border-b">
            <Link href="/overview" className="flex items-center space-x-2">
              <Activity className="h-6 w-6" />
              <span className="font-semibold">Living Truth Engine</span>
            </Link>
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={handleClose}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation - Replaced ScrollArea with simple div */}
          <div className="flex-1 px-3 py-4 overflow-y-auto">
            <nav className="space-y-1">
              {navigationItems}
            </nav>
          </div>

          {/* Footer */}
          <div className="border-t p-4">
            <div className="text-xs text-muted-foreground">
              Phase 9.4.1 - Next.js UI
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
