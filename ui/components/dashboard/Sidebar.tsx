'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Activity, 
  BarChart3, 
  Database, 
  FileText, 
  Settings, 
  Users,
  Menu,
  X
} from 'lucide-react';
import { useSidebarOpen, useAppActions } from '@/lib/state';

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
  const sidebarOpen = useSidebarOpen();
  const { setSidebarOpen } = useAppActions();

  return (
    <>
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm lg:hidden"
          onClick={() => setSidebarOpen(false)}
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
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>

          {/* Navigation */}
          <ScrollArea className="flex-1 px-3 py-4">
            <nav className="space-y-1">
              {navigation.map((item) => {
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
                    onClick={() => setSidebarOpen(false)}
                  >
                    <item.icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </nav>
          </ScrollArea>

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
