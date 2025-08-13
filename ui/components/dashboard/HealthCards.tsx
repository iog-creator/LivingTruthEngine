'use client';

import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { CheckCircle, XCircle, AlertTriangle, Activity, Database, Settings } from 'lucide-react';
import { useHealthFull, useModels } from '@/lib/query';

export function HealthCards() {
  const healthQuery = useQuery(useHealthFull());
  const modelsQuery = useQuery(useModels());

  if (healthQuery.isLoading || modelsQuery.isLoading) {
    return <HealthCardsSkeleton />;
  }

  if (healthQuery.isError || modelsQuery.isError) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <XCircle className="h-5 w-5 text-destructive" />
              <span>System Status</span>
            </CardTitle>
            <CardDescription>Unable to fetch system status</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-destructive">
              {healthQuery.error?.message || 'Unknown error'}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const healthData = healthQuery.data?.data;
  const modelsData = modelsQuery.data?.data;

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {/* System Status Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>System Status</span>
          </CardTitle>
          <CardDescription>Overall system health</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm">Status</span>
              <Badge variant={healthData?.all_gates_passed ? 'default' : 'destructive'}>
                {healthData?.all_gates_passed ? 'Healthy' : 'Unhealthy'}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Service</span>
              <span className="text-sm font-mono">{healthData?.service}</span>
            </div>
            {healthData?.embedding_model && (
              <div className="flex items-center justify-between">
                <span className="text-sm">Embedding Model</span>
                <span className="text-sm font-mono">{healthData.embedding_model}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Database Status Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Database className="h-5 w-5" />
            <span>Database</span>
          </CardTitle>
          <CardDescription>PostgreSQL and pgvector status</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm">pgvector</span>
              <Badge variant={healthData?.pgvector?.enabled ? 'default' : 'destructive'}>
                {healthData?.pgvector?.enabled ? 'Enabled' : 'Disabled'}
              </Badge>
            </div>
            {healthData?.pgvector?.tables && (
              <div className="flex items-center justify-between">
                <span className="text-sm">Tables</span>
                <span className="text-sm">{healthData.pgvector.tables.length}</span>
              </div>
            )}
            {healthData?.embedding_dim && (
              <div className="flex items-center justify-between">
                <span className="text-sm">Dimensions</span>
                <span className="text-sm font-mono">{healthData.embedding_dim}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Configuration Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Settings className="h-5 w-5" />
            <span>Configuration</span>
          </CardTitle>
          <CardDescription>System configuration</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm">Reverse Proxy</span>
              <Badge variant={healthData?.reverse_proxy ? 'default' : 'secondary'}>
                {healthData?.reverse_proxy ? 'Enabled' : 'Disabled'}
              </Badge>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm">Fallbacks</span>
              <Badge variant={healthData?.fallbacks_enabled ? 'default' : 'secondary'}>
                {healthData?.fallbacks_enabled ? 'Enabled' : 'Disabled'}
              </Badge>
            </div>
            {healthData?.ui_origin && (
              <div className="flex items-center justify-between">
                <span className="text-sm">UI Origin</span>
                <span className="text-sm font-mono truncate max-w-24">{healthData.ui_origin}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Health Gates Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <CheckCircle className="h-5 w-5" />
            <span>Health Gates</span>
          </CardTitle>
          <CardDescription>Individual service checks</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {healthData?.gates && Object.entries(healthData.gates).map(([gate, status]) => (
              <div key={gate} className="flex items-center justify-between">
                <span className="text-sm capitalize">{gate.replace(/_/g, ' ')}</span>
                <Badge variant={status ? 'default' : 'destructive'}>
                  {status ? 'OK' : 'Failed'}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Models Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>Models</span>
          </CardTitle>
          <CardDescription>Available AI models</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {modelsData && Object.keys(modelsData).length > 0 ? (
              Object.entries(modelsData).map(([model, config]) => (
                <div key={model} className="flex items-center justify-between">
                  <span className="text-sm font-mono">{model}</span>
                  <Badge variant="outline">Available</Badge>
                </div>
              ))
            ) : (
              <p className="text-sm text-muted-foreground">No models available</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Errors Card */}
      {healthData?.errors && healthData.errors.length > 0 && (
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <AlertTriangle className="h-5 w-5 text-destructive" />
              <span>Errors</span>
            </CardTitle>
            <CardDescription>Recent system errors</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {healthData.errors.map((error, index) => (
                <div key={index} className="text-sm text-destructive">
                  {error}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function HealthCardsSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {Array.from({ length: 6 }).map((_, i) => (
        <Card key={i}>
          <CardHeader>
            <Skeleton className="h-6 w-32" />
            <Skeleton className="h-4 w-48" />
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, j) => (
                <div key={j} className="flex items-center justify-between">
                  <Skeleton className="h-4 w-20" />
                  <Skeleton className="h-6 w-16" />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
