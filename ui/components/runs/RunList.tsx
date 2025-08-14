'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useRuns } from '@/lib/query';
import { useQuery } from '@tanstack/react-query';
import { formatDistanceToNow } from 'date-fns';
import { Calendar, ExternalLink, FileText, Hash, RefreshCw } from 'lucide-react';
import { useRouter } from 'next/navigation';

export function RunList() {
    const runsQuery = useQuery(useRuns());

    if (runsQuery.isLoading) {
        return <RunListSkeleton />;
    }

    if (runsQuery.isError) {
        return (
            <Card className="border-destructive">
                <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-destructive" />
                        <span>Error Loading Runs</span>
                    </CardTitle>
                    <CardDescription>Unable to fetch runs</CardDescription>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-destructive mb-4">
                        {runsQuery.error?.message || 'Unknown error'}
                    </p>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => runsQuery.refetch()}
                        disabled={runsQuery.isRefetching}
                    >
                        <RefreshCw className={`mr-2 h-4 w-4 ${runsQuery.isRefetching ? 'animate-spin' : ''}`} />
                        Retry
                    </Button>
                </CardContent>
            </Card>
        );
    }

    const runs = runsQuery.data?.data?.runs || [];

    if (runs.length === 0) {
        return (
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center space-x-2">
                        <FileText className="h-5 w-5" />
                        <span>No Runs Found</span>
                    </CardTitle>
                    <CardDescription>Start your first analysis run to see results here</CardDescription>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-muted-foreground">
                        Use the form on the left to start a new analysis run.
                    </p>
                </CardContent>
            </Card>
        );
    }

    return (
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium">Recent Runs ({runs.length})</h3>
                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => runsQuery.refetch()}
                    disabled={runsQuery.isRefetching}
                >
                    <RefreshCw className={`mr-2 h-4 w-4 ${runsQuery.isRefetching ? 'animate-spin' : ''}`} />
                    Refresh
                </Button>
            </div>

            <div className="space-y-3">
                {runs.map((run) => (
                    <RunCard key={run.id} run={run} />
                ))}
            </div>
        </div>
    );
}

function RunCard({ run }: { run: Record<string, unknown> }) {
    const router = useRouter();

    const handleViewDetails = () => {
        router.push(`/runs/${run.id}`);
    };

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
                return <Badge variant="default">Completed</Badge>;
            case 'running':
                return <Badge variant="secondary">Running</Badge>;
            case 'failed':
                return <Badge variant="destructive">Failed</Badge>;
            default:
                return <Badge variant="outline">{status}</Badge>;
        }
    };

    return (
        <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={handleViewDetails}>
            <CardContent className="p-4">
                <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                            <h4 className="font-medium truncate">
                                {(run.human_name as string) || (run.id as string)}
                            </h4>
                            {getStatusBadge(run.status as string)}
                        </div>

                        <div className="space-y-1 text-sm text-muted-foreground">
                            <div className="flex items-center space-x-2">
                                <Hash className="h-3 w-3" />
                                <span className="font-mono text-xs truncate">{run.id as string}</span>
                            </div>

                            {(run.created_at as string) && (
                                <div className="flex items-center space-x-2">
                                    <Calendar className="h-3 w-3" />
                                    <span>{formatDate(run.created_at as string)}</span>
                                </div>
                            )}

                            {(run.document_count as number) !== undefined && (
                                <div className="flex items-center space-x-2">
                                    <FileText className="h-3 w-3" />
                                    <span>{run.document_count as number} documents</span>
                                </div>
                            )}

                            {(run.source_type as string) && (
                                <div className="flex items-center space-x-2">
                                    <span className="text-xs bg-muted px-2 py-1 rounded">
                                        {run.source_type as string}
                                    </span>
                                </div>
                            )}
                        </div>
                    </div>

                    <Button variant="ghost" size="sm" className="ml-2">
                        <ExternalLink className="h-4 w-4" />
                    </Button>
                </div>
            </CardContent>
        </Card>
    );
}

function RunListSkeleton() {
    return (
        <div className="space-y-3">
            <div className="flex items-center justify-between">
                <Skeleton className="h-4 w-24" />
                <Skeleton className="h-8 w-20" />
            </div>

            <div className="space-y-3">
                {Array.from({ length: 3 }).map((_, i) => (
                    <Card key={i}>
                        <CardContent className="p-4">
                            <div className="space-y-3">
                                <div className="flex items-center space-x-2">
                                    <Skeleton className="h-4 w-32" />
                                    <Skeleton className="h-5 w-16" />
                                </div>
                                <div className="space-y-2">
                                    <Skeleton className="h-3 w-48" />
                                    <Skeleton className="h-3 w-24" />
                                    <Skeleton className="h-3 w-20" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
}
