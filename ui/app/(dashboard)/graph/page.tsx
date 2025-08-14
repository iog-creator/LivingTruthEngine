'use client';

import { GraphView } from '@/components/graph/GraphView';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { getGraph } from '@/lib/api';
import { type GraphResponse } from '@/lib/schemas';
import { useQuery } from '@tanstack/react-query';
import { Suspense } from 'react';

function GraphPageContent() {
  // This will be wrapped in Suspense
  // eslint-disable-next-line @typescript-eslint/no-require-imports
  const { useSearchParams } = require('next/navigation');
  const searchParams = useSearchParams();
  const runId = searchParams.get('runId');

  const { data: graphData, isLoading, error } = useQuery<GraphResponse['data']>({
    queryKey: ['graph', runId],
    queryFn: async () => {
      if (!runId) throw new Error('No run ID provided');
      const response = await getGraph(runId);
      return response.data;
    },
    enabled: !!runId,
  });

  if (!runId) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardHeader>
            <CardTitle>Evidence Graph</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">
              Please select a run to view its evidence graph.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardHeader>
            <CardTitle>Evidence Graph</CardTitle>
            <Badge variant="destructive">Error</Badge>
          </CardHeader>
          <CardContent>
            <p className="text-destructive">
              Failed to load graph data: {error.message}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle>Evidence Graph</CardTitle>
          <div className="flex items-center gap-2">
            <Badge variant="outline">Run: {runId}</Badge>
            {graphData && (
              <>
                <Badge variant="secondary">
                  {graphData.nodes.length} nodes
                </Badge>
                <Badge variant="secondary">
                  {graphData.edges.length} edges
                </Badge>
              </>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-4">
              <Skeleton className="h-[400px] w-full" />
              <div className="flex gap-4">
                <Skeleton className="h-6 w-24" />
                <Skeleton className="h-6 w-24" />
              </div>
            </div>
          ) : graphData ? (
            <GraphView data={graphData} />
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}

export default function GraphPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <GraphPageContent />
    </Suspense>
  );
}
