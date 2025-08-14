'use client';

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Loader2, Play, Settings } from 'lucide-react';
import { startRun, type StartRunRequest } from '@/lib/api';
import { queryKeys } from '@/lib/query';
import { useToast } from '@/hooks/use-toast';

export function StartRunForm() {
  const [formData, setFormData] = useState<StartRunRequest>({
    channel_url: 'https://www.youtube.com/@imaginationpodcastofficial',
    limit: 10,
    sort: 'oldest',
    max_depth: 3,
    ocr_required: false,
    js_render: false,
    hf_burst: false,
    run_label: '',
    save_to_directory: '',
  });

  const [showAdvanced, setShowAdvanced] = useState(false);
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const startRunMutation = useMutation({
    mutationFn: (data: StartRunRequest) => startRun(data),
    onSuccess: (response) => {
      toast({
        title: 'Run Started',
        description: `Analysis run ${response.data?.run_id} has been started successfully.`,
      });
      
      // Refresh the runs list
      queryClient.invalidateQueries({ queryKey: queryKeys.runs });
      
      // Reset form
      setFormData({
        channel_url: 'https://www.youtube.com/@imaginationpodcastofficial',
        limit: 10,
        sort: 'oldest',
        max_depth: 3,
        ocr_required: false,
        js_render: false,
        hf_burst: false,
        run_label: '',
        save_to_directory: '',
      });
    },
    onError: (error) => {
      toast({
        title: 'Error',
        description: error instanceof Error ? error.message : 'Failed to start run',
        variant: 'destructive',
      });
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    startRunMutation.mutate(formData);
  };

  const handleInputChange = (field: keyof StartRunRequest, value: string | number | boolean) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <Play className="h-5 w-5" />
          <span>Start Analysis Run</span>
        </CardTitle>
        <CardDescription>
          Configure and start a new survivor testimony analysis run
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Basic Configuration */}
          <div className="space-y-3">
            <div>
              <Label htmlFor="channel_url">YouTube Channel URL</Label>
              <Input
                id="channel_url"
                type="url"
                value={formData.channel_url}
                onChange={(e) => handleInputChange('channel_url', e.target.value)}
                placeholder="https://www.youtube.com/@channel"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label htmlFor="limit">Video Limit</Label>
                <Input
                  id="limit"
                  type="number"
                  min="1"
                  max="50"
                  value={formData.limit}
                  onChange={(e) => handleInputChange('limit', parseInt(e.target.value) || 10)}
                />
              </div>
              <div>
                <Label htmlFor="max_depth">Max Depth</Label>
                <Input
                  id="max_depth"
                  type="number"
                  min="1"
                  max="5"
                  value={formData.max_depth}
                  onChange={(e) => handleInputChange('max_depth', parseInt(e.target.value) || 3)}
                />
              </div>
            </div>

            <div>
              <Label htmlFor="sort">Sort Order</Label>
              <select
                id="sort"
                value={formData.sort}
                onChange={(e) => handleInputChange('sort', e.target.value)}
                className="w-full p-2 border border-input rounded-md bg-background"
              >
                <option value="oldest">Oldest First</option>
                <option value="newest">Newest First</option>
                <option value="popular">Most Popular</option>
              </select>
            </div>
          </div>

          {/* Advanced Options Toggle */}
          <div className="flex items-center space-x-2">
            <Switch
              id="show-advanced"
              checked={showAdvanced}
              onCheckedChange={setShowAdvanced}
            />
            <Label htmlFor="show-advanced" className="flex items-center space-x-2">
              <Settings className="h-4 w-4" />
              <span>Advanced Options</span>
            </Label>
          </div>

          {/* Advanced Configuration */}
          {showAdvanced && (
            <div className="space-y-3 p-4 border rounded-md bg-muted/50">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Label htmlFor="ocr_required">OCR Required</Label>
                  <Switch
                    id="ocr_required"
                    checked={formData.ocr_required}
                    onCheckedChange={(checked) => handleInputChange('ocr_required', checked)}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="js_render">JavaScript Render</Label>
                  <Switch
                    id="js_render"
                    checked={formData.js_render}
                    onCheckedChange={(checked) => handleInputChange('js_render', checked)}
                  />
                </div>
                <div className="flex items-center justify-between">
                  <Label htmlFor="hf_burst">Hugging Face Burst</Label>
                  <Switch
                    id="hf_burst"
                    checked={formData.hf_burst}
                    onCheckedChange={(checked) => handleInputChange('hf_burst', checked)}
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="run_label">Run Label (Optional)</Label>
                <Input
                  id="run_label"
                  value={formData.run_label}
                  onChange={(e) => handleInputChange('run_label', e.target.value)}
                  placeholder="Enter a descriptive label"
                />
              </div>

              <div>
                <Label htmlFor="save_to_directory">Save To Directory (Optional)</Label>
                <Input
                  id="save_to_directory"
                  value={formData.save_to_directory}
                  onChange={(e) => handleInputChange('save_to_directory', e.target.value)}
                  placeholder="Custom save directory"
                />
              </div>
            </div>
          )}

          {/* Status and Submit */}
          <div className="space-y-3">
            {startRunMutation.isPending && (
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Starting analysis run...</span>
              </div>
            )}

            <Button
              type="submit"
              disabled={startRunMutation.isPending}
              className="w-full"
            >
              {startRunMutation.isPending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Starting Run...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Start Analysis Run
                </>
              )}
            </Button>

            {/* Configuration Summary */}
            <div className="text-xs text-muted-foreground space-y-1">
              <div className="flex items-center justify-between">
                <span>Videos:</span>
                <Badge variant="outline">{formData.limit}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Depth:</span>
                <Badge variant="outline">{formData.max_depth}</Badge>
              </div>
              <div className="flex items-center justify-between">
                <span>Sort:</span>
                <Badge variant="outline">{formData.sort}</Badge>
              </div>
              {showAdvanced && (
                <>
                  {formData.ocr_required && (
                    <div className="flex items-center justify-between">
                      <span>OCR:</span>
                      <Badge variant="secondary">Required</Badge>
                    </div>
                  )}
                  {formData.js_render && (
                    <div className="flex items-center justify-between">
                      <span>JS Render:</span>
                      <Badge variant="secondary">Enabled</Badge>
                    </div>
                  )}
                  {formData.hf_burst && (
                    <div className="flex items-center justify-between">
                      <span>HF Burst:</span>
                      <Badge variant="secondary">Enabled</Badge>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
