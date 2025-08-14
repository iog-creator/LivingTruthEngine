import { RunList } from '@/components/runs/RunList';
import { StartRunForm } from '@/components/runs/StartRunForm';

export default function RunsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Runs</h1>
        <p className="text-muted-foreground">
          Manage and monitor analysis runs for survivor testimony corroboration.
        </p>
      </div>
      
      <div className="grid gap-6 lg:grid-cols-2">
        <div>
          <h2 className="text-xl font-semibold mb-4">Start New Run</h2>
          <StartRunForm />
        </div>
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Recent Runs</h2>
          <RunList />
        </div>
      </div>
    </div>
  );
}
