'use client';

import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Activity, AlertTriangle, CheckCircle, Database, Settings, XCircle } from 'lucide-react';
import { useEffect, useState } from 'react';

interface HealthData {
  all_gates_passed?: boolean;
  service?: string;
  embedding_model?: string;
  pgvector?: { status: string };
  embedding_dim?: number;
  reverse_proxy?: boolean;
  fallbacks_enabled?: boolean;
  ui_origin?: string;
  gates?: Record<string, boolean>;
  errors?: Record<string, string>;
}

export function HealthCards() {
  const [healthData, setHealthData] = useState<HealthData | null>(null);
  const [modelsData, setModelsData] = useState<Record<string, any> | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Fetch health data
        const healthResponse = await fetch('http://localhost:8050/api/health/full');
        if (healthResponse.ok) {
          const healthResult = await healthResponse.json();
          setHealthData(healthResult.data);
        }

        // Fetch models data
        const modelsResponse = await fetch('http://localhost:8050/api/models');
        if (modelsResponse.ok) {
          const modelsResult = await modelsResponse.json();
          setModelsData(modelsResult.data);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <HealthCardsSkeleton />;
  }

  if (error) {
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
            <p className="text-sm text-destructive">{error}</p>
            <p className="text-sm text-muted-foreground mt-2">
              Please check that the dashboard server is running on http://localhost:8050
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Fallback if no data
  if (!healthData) {
    return (
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Activity className="h-5 w-5" />
              <span>System Status</span>
            </CardTitle>
            <CardDescription>Dashboard is running</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm">Status</span>
                <Badge variant="default">Running</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm">Service</span>
                <span className="text-sm font-mono">unified_dashboard</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

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
              <Badge variant={healthData?.pgvector?.status === 'ok' ? 'default' : 'destructive'}>
                {healthData?.pgvector?.status === 'ok' ? 'Connected' : 'Disconnected'}
              </Badge>
            </div>
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
      {healthData?.errors && Object.keys(healthData.errors).length > 0 && (
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
              {Object.entries(healthData.errors).map(([key, error], index) => (
                <div key={index} className="text-sm text-destructive">
                  {key}: {error}
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
