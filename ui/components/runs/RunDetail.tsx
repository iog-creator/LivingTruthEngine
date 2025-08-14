'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  FileText, 
  RefreshCw, 
  CheckCircle, 
  AlertTriangle,
  FileJson,
  BarChart3,
  Shield,
  ExternalLink
} from 'lucide-react';
import { useRun, useRunCorpus } from '@/lib/query';
import { formatDistanceToNow } from 'date-fns';
import { useRouter } from 'next/navigation';

interface RunDetailProps {
  runId: string;
}

export function RunDetail({ runId }: RunDetailProps) {
  const router = useRouter();
  const runQuery = useQuery(useRun(runId));
  const corpusQuery = useQuery(useRunCorpus(runId));

  if (runQuery.isLoading) {
    return <RunDetailSkeleton />;
  }

  if (runQuery.isError) {
    return (
      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="h-5 w-5 text-destructive" />
            <span>Error Loading Run</span>
          </CardTitle>
          <CardDescription>Unable to fetch run details</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-destructive mb-4">
            {runQuery.error?.message || 'Unknown error'}
          </p>
          <div className="flex space-x-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => runQuery.refetch()}
              disabled={runQuery.isRefetching}
            >
              <RefreshCw className={`mr-2 h-4 w-4 ${runQuery.isRefetching ? 'animate-spin' : ''}`} />
              Retry
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push('/runs')}
            >
              Back to Runs
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const run = runQuery.data?.data;
  const corpus = corpusQuery.data?.data;

  if (!run) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Run Not Found</CardTitle>
          <CardDescription>The requested run could not be found</CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            variant="outline"
            onClick={() => router.push('/runs')}
          >
            Back to Runs
          </Button>
        </CardContent>
      </Card>
    );
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Unknown';
    try {
      return formatDistanceToNow(new Date(dateString), { addSuffix: true });
    } catch {
      return 'Invalid date';
    }
  };

  const getStatusBadge = (status?: string) => {
    if (!status) return <Badge variant="secondary">Unknown</Badge>;
    
    switch (status.toLowerCase()) {
      case 'completed':
        return <Badge variant="default" className="flex items-center space-x-1">
          <CheckCircle className="h-3 w-3" />
          <span>Completed</span>
        </Badge>;
      case 'running':
        return <Badge variant="secondary">Running</Badge>;
      case 'failed':
        return <Badge variant="destructive" className="flex items-center space-x-1">
          <AlertTriangle className="h-3 w-3" />
          <span>Failed</span>
        </Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Run Header */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <CardTitle className="flex items-center space-x-2 mb-2">
                <FileText className="h-5 w-5" />
                <span>{run.id}</span>
                {getStatusBadge(run.status)}
              </CardTitle>
              <CardDescription>
                Analysis run details and verification information
              </CardDescription>
            </div>
            <Button
              variant="outline"
              size="sm"
              onClick={() => router.push('/runs')}
            >
              <ExternalLink className="mr-2 h-4 w-4" />
              Back to Runs
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-1">
              <p className="text-sm font-medium">Run ID</p>
              <p className="text-sm text-muted-foreground font-mono">{run.id}</p>
            </div>
            <div className="space-y-1">
              <p className="text-sm font-medium">Created</p>
              <p className="text-sm text-muted-foreground">
                {run.created_at ? formatDate(run.created_at) : 'Unknown'}
              </p>
            </div>
                         <div className="space-y-1">
               <p className="text-sm font-medium">Documents</p>
               <p className="text-sm text-muted-foreground">
                 {corpus?.documents?.length || 0}
               </p>
             </div>
                         <div className="space-y-1">
               <p className="text-sm font-medium">Source Type</p>
               <p className="text-sm text-muted-foreground">
                 Unknown
               </p>
             </div>
          </div>
        </CardContent>
      </Card>

      {/* Run Details Tabs */}
      <Tabs defaultValue="manifest" className="space-y-4">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="manifest" className="flex items-center space-x-2">
            <FileJson className="h-4 w-4" />
            <span>Manifest</span>
          </TabsTrigger>
          <TabsTrigger value="metrics" className="flex items-center space-x-2">
            <BarChart3 className="h-4 w-4" />
            <span>Metrics</span>
          </TabsTrigger>
          <TabsTrigger value="merkle" className="flex items-center space-x-2">
            <Shield className="h-4 w-4" />
            <span>Merkle</span>
          </TabsTrigger>
          <TabsTrigger value="corpus" className="flex items-center space-x-2">
            <FileText className="h-4 w-4" />
            <span>Corpus</span>
          </TabsTrigger>
        </TabsList>

        <TabsContent value="manifest" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileJson className="h-5 w-5" />
                <span>Manifest</span>
              </CardTitle>
              <CardDescription>Run configuration and metadata</CardDescription>
            </CardHeader>
            <CardContent>
              {run.manifest ? (
                <pre className="bg-muted p-4 rounded-md text-sm overflow-auto max-h-96">
                  {JSON.stringify(run.manifest, null, 2)}
                </pre>
              ) : (
                <p className="text-muted-foreground">No manifest data available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="metrics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <BarChart3 className="h-5 w-5" />
                <span>Metrics</span>
              </CardTitle>
              <CardDescription>Run performance and statistics</CardDescription>
            </CardHeader>
            <CardContent>
              {run.metrics ? (
                <pre className="bg-muted p-4 rounded-md text-sm overflow-auto max-h-96">
                  {JSON.stringify(run.metrics, null, 2)}
                </pre>
              ) : (
                <p className="text-muted-foreground">No metrics data available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="merkle" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Shield className="h-5 w-5" />
                <span>Merkle Tree</span>
              </CardTitle>
              <CardDescription>Cryptographic verification data</CardDescription>
            </CardHeader>
            <CardContent>
              {run.merkle ? (
                <div className="space-y-4">
                  <div className="grid gap-4 md:grid-cols-2">
                                         <div className="space-y-1">
                       <p className="text-sm font-medium">Root Hash</p>
                       <p className="text-sm font-mono text-muted-foreground break-all">
                         {(run.merkle as Record<string, unknown>)?.root_hash as string || 'N/A'}
                       </p>
                     </div>
                     <div className="space-y-1">
                       <p className="text-sm font-medium">Leaf Count</p>
                       <p className="text-sm text-muted-foreground">
                         {((run.merkle as Record<string, unknown>)?.leaf_hashes as unknown[])?.length || 0}
                       </p>
                     </div>
                  </div>
                  <pre className="bg-muted p-4 rounded-md text-sm overflow-auto max-h-96">
                    {JSON.stringify(run.merkle, null, 2)}
                  </pre>
                </div>
              ) : (
                <p className="text-muted-foreground">No merkle tree data available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="corpus" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <FileText className="h-5 w-5" />
                <span>Corpus</span>
              </CardTitle>
              <CardDescription>Documents and content from this run</CardDescription>
            </CardHeader>
            <CardContent>
              {corpusQuery.isLoading ? (
                <div className="space-y-2">
                  {Array.from({ length: 3 }).map((_, i) => (
                    <Skeleton key={i} className="h-20 w-full" />
                  ))}
                </div>
              ) : corpusQuery.isError ? (
                <p className="text-destructive">
                  Error loading corpus: {corpusQuery.error?.message}
                </p>
              ) : corpus?.documents && corpus.documents.length > 0 ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-muted-foreground">
                      {corpus.documents.length} documents
                    </p>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => corpusQuery.refetch()}
                      disabled={corpusQuery.isRefetching}
                    >
                      <RefreshCw className={`mr-2 h-4 w-4 ${corpusQuery.isRefetching ? 'animate-spin' : ''}`} />
                      Refresh
                    </Button>
                  </div>
                  <div className="space-y-3">
                                         {corpus.documents.map((doc: Record<string, unknown>, index: number) => (
                      <div key={index} className="border rounded-md p-3">
                                                 <div className="flex items-start justify-between mb-2">
                           <h4 className="font-medium text-sm">
                             Document {index + 1}
                           </h4>
                           {(doc.source_type as string) && (
                             <Badge variant="outline" className="text-xs">
                               {doc.source_type as string}
                             </Badge>
                           )}
                         </div>
                                                 {(doc.title as string) && (
                           <p className="text-sm font-medium mb-1">{doc.title as string}</p>
                         )}
                         {(doc.content as string) && (
                           <p className="text-sm text-muted-foreground line-clamp-3">
                             {doc.content as string}
                           </p>
                         )}
                         {(doc.url as string) && (
                           <p className="text-xs text-muted-foreground mt-2 break-all">
                             {doc.url as string}
                           </p>
                         )}
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <p className="text-muted-foreground">No corpus data available</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function RunDetailSkeleton() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <Skeleton className="h-6 w-48 mb-2" />
              <Skeleton className="h-4 w-64" />
            </div>
            <Skeleton className="h-8 w-24" />
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="space-y-1">
                <Skeleton className="h-4 w-16" />
                <Skeleton className="h-4 w-32" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="space-y-4">
        <Skeleton className="h-10 w-full" />
        <Card>
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-64 w-full" />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
