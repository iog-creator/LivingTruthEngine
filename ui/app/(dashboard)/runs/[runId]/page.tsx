import { RunDetail } from '@/components/runs/RunDetail';

interface RunDetailPageProps {
  params: Promise<{
    runId: string;
  }>;
}

export default async function RunDetailPage({ params }: RunDetailPageProps) {
  const { runId } = await params;
  
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Run Details</h1>
        <p className="text-muted-foreground">
          Detailed information about run {runId}
        </p>
      </div>
      
      <RunDetail runId={runId} />
    </div>
  );
}
