'use client';

import { Button } from '@/components/ui/button';
import { Menu } from 'lucide-react';
import { useAppActions } from '@/lib/state';

export function Header() {
  const { setSidebarOpen } = useAppActions();

  return (
    <header className="flex h-16 items-center gap-4 border-b bg-background px-6">
      <Button
        variant="ghost"
        size="sm"
        className="lg:hidden"
        onClick={() => setSidebarOpen(true)}
      >
        <Menu className="h-4 w-4" />
        <span className="sr-only">Toggle sidebar</span>
      </Button>
      
      <div className="flex-1" />
      
      <div className="flex items-center gap-2">
        <div className="text-sm text-muted-foreground">
          Living Truth Engine Dashboard
        </div>
      </div>
    </header>
  );
}
