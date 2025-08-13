import { HealthCards } from '@/components/dashboard/HealthCards';

export default function OverviewPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Overview</h1>
        <p className="text-muted-foreground">
          System health and status overview for the Living Truth Engine.
        </p>
      </div>
      
      <HealthCards />
    </div>
  );
}
