'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import {
    Clock,
    Database,
    FileText,
    Globe,
    Info,
    Lock,
    Network,
    Settings,
    Shield,
    ToggleLeft,
    Zap
} from 'lucide-react';
import { Suspense, useState } from 'react';

interface SettingFlag {
    name: string;
    value: string | boolean | number;
    description: string;
    category: string;
    readonly: boolean;
}

// Mock data based on veritas_flags.toml and configuration files
const mockSettings: SettingFlag[] = [
    // Network and External Service Controls
    {
        name: "HF_BURST",
        value: "off",
        description: "Disable Hugging Face network bursts by default",
        category: "Network",
        readonly: true
    },
    {
        name: "OCR_REQUIRED",
        value: "false",
        description: "Disable OCR by default for performance",
        category: "Processing",
        readonly: true
    },
    {
        name: "PII_SCRUB",
        value: "standard",
        description: "Enable standard PII scrubbing",
        category: "Privacy",
        readonly: true
    },

    // Ingestion Limits and Controls
    {
        name: "MAX_DOCS_DEFAULT",
        value: 10,
        description: "Default maximum documents per run",
        category: "Limits",
        readonly: true
    },
    {
        name: "MAX_BYTES_PER_DOC",
        value: 1048576,
        description: "1MB limit per document",
        category: "Limits",
        readonly: true
    },
    {
        name: "MAX_RUN_DURATION",
        value: 300,
        description: "5 minute timeout for ingestion runs",
        category: "Limits",
        readonly: true
    },

    // Bundle and Provenance Settings
    {
        name: "BUNDLE_COMPRESSION",
        value: "false",
        description: "Disable compression for easier inspection",
        category: "Storage",
        readonly: true
    },
    {
        name: "MERKLE_TREE_DEPTH",
        value: 16,
        description: "Maximum depth for merkle tree construction",
        category: "Security",
        readonly: true
    },
    {
        name: "PROOF_FORMAT",
        value: "sha256",
        description: "Use SHA-256 for document proofs",
        category: "Security",
        readonly: true
    },

    // Ingestion Configuration
    {
        name: "default_max_videos",
        value: 10,
        description: "Default maximum videos per run",
        category: "YouTube",
        readonly: true
    },
    {
        name: "default_selection",
        value: "oldest",
        description: "Video selection strategy (oldest|latest|by_date_range|ids)",
        category: "YouTube",
        readonly: true
    },
    {
        name: "crawl_depth",
        value: 1,
        description: "Levels of link following (0..3)",
        category: "Web",
        readonly: true
    },
    {
        name: "transcript_pref",
        value: "yt_api",
        description: "Transcript preference (yt_api|whisper_local|both)",
        category: "YouTube",
        readonly: true
    },
    {
        name: "max_pages_per_run",
        value: 50,
        description: "Cap on total pages fetched",
        category: "Web",
        readonly: true
    },
    {
        name: "max_pages_per_domain",
        value: 10,
        description: "Cap per domain to prevent runaway",
        category: "Web",
        readonly: true
    },

    // OCR Configuration
    {
        name: "ocr_mode",
        value: "off",
        description: "OCR mode (off|auto|manual|auto_retry)",
        category: "OCR",
        readonly: true
    },
    {
        name: "suspect_min_chars",
        value: 800,
        description: "Minimum characters to consider text extraction successful",
        category: "OCR",
        readonly: true
    },
    {
        name: "auto_retry_attempts",
        value: 2,
        description: "Number of OCR attempts for suspect PDFs",
        category: "OCR",
        readonly: true
    },
    {
        name: "tesseract_langs",
        value: "eng",
        description: "Tesseract language codes",
        category: "OCR",
        readonly: true
    },
    {
        name: "manual_queue_limit",
        value: 100,
        description: "Maximum files in manual OCR queue",
        category: "OCR",
        readonly: true
    },

    // YouTube Configuration
    {
        name: "default_channel",
        value: "https://www.youtube.com/@imaginationpodcastofficial",
        description: "Default YouTube channel for processing",
        category: "YouTube",
        readonly: true
    },
    {
        name: "extract_flat_timeout",
        value: 30,
        description: "Timeout for yt-dlp extract_flat operations",
        category: "YouTube",
        readonly: true
    },
    {
        name: "transcript_timeout",
        value: 60,
        description: "Timeout for transcript fetching",
        category: "YouTube",
        readonly: true
    },
    {
        name: "max_video_age_days",
        value: 3650,
        description: "Maximum age of videos to process (10 years)",
        category: "YouTube",
        readonly: true
    },

    // Web Configuration
    {
        name: "user_agent",
        value: "LivingTruthEngine/1.0 (Phase 8)",
        description: "User agent for web requests",
        category: "Web",
        readonly: true
    },
    {
        name: "request_timeout",
        value: 30,
        description: "Timeout for web requests",
        category: "Web",
        readonly: true
    },
    {
        name: "max_redirects",
        value: 5,
        description: "Maximum redirects to follow",
        category: "Web",
        readonly: true
    }
];

function SettingsContent() {
    const [selectedCategory, setSelectedCategory] = useState<string>('all');

    const categories = ['all', ...Array.from(new Set(mockSettings.map(s => s.category)))];

    const filteredSettings = selectedCategory === 'all'
        ? mockSettings
        : mockSettings.filter(s => s.category === selectedCategory);

    const getCategoryIcon = (category: string) => {
        switch (category.toLowerCase()) {
            case 'network':
                return <Network className="h-4 w-4" />;
            case 'processing':
                return <Zap className="h-4 w-4" />;
            case 'privacy':
                return <Shield className="h-4 w-4" />;
            case 'limits':
                return <Clock className="h-4 w-4" />;
            case 'storage':
                return <Database className="h-4 w-4" />;
            case 'security':
                return <Shield className="h-4 w-4" />;
            case 'youtube':
                return <Globe className="h-4 w-4" />;
            case 'web':
                return <Network className="h-4 w-4" />;
            case 'ocr':
                return <FileText className="h-4 w-4" />;
            default:
                return <Settings className="h-4 w-4" />;
        }
    };

    const getValueDisplay = (value: string | boolean | number) => {
        if (typeof value === 'boolean') {
            return value ? 'true' : 'false';
        }
        if (typeof value === 'number') {
            return value.toString();
        }
        return String(value);
    };

    const getValueColor = (value: string | boolean | number) => {
        if (typeof value === 'boolean') {
            return value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800';
        }
        if (typeof value === 'number') {
            return 'bg-blue-100 text-blue-800';
        }
        return 'bg-gray-100 text-gray-800';
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
                    <p className="text-muted-foreground">
                        System configuration flags and parameters
                    </p>
                </div>
            </div>

            {/* Configuration Summary */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Settings className="h-5 w-5" />
                            Total Settings
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{mockSettings.length}</div>
                        <p className="text-xs text-muted-foreground">
                            Configuration flags
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Lock className="h-5 w-5" />
                            Read-Only
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{mockSettings.filter(s => s.readonly).length}</div>
                        <p className="text-xs text-muted-foreground">
                            Immutable settings
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <FileText className="h-5 w-5" />
                            Categories
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{categories.length - 1}</div>
                        <p className="text-xs text-muted-foreground">
                            Configuration groups
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Info className="h-5 w-5" />
                            Source
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-sm font-medium">veritas_flags.toml</div>
                        <p className="text-xs text-muted-foreground">
                            Configuration file
                        </p>
                    </CardContent>
                </Card>
            </div>

            {/* Category Filter */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Settings className="h-5 w-5" />
                        Filter by Category
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-wrap gap-2">
                        {categories.map(category => (
                            <Button
                                key={category}
                                variant={selectedCategory === category ? "default" : "outline"}
                                size="sm"
                                onClick={() => setSelectedCategory(category)}
                                className="flex items-center gap-2"
                            >
                                {getCategoryIcon(category)}
                                {category.charAt(0).toUpperCase() + category.slice(1)}
                            </Button>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Settings Table */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Configuration Flags
                        {selectedCategory !== 'all' && (
                            <Badge variant="secondary">
                                {filteredSettings.length} settings
                            </Badge>
                        )}
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Setting</TableHead>
                                    <TableHead>Value</TableHead>
                                    <TableHead>Category</TableHead>
                                    <TableHead>Description</TableHead>
                                    <TableHead>Status</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredSettings.map((setting, index) => (
                                    <TableRow key={index}>
                                        <TableCell>
                                            <div className="font-mono text-sm font-medium">
                                                {setting.name}
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge className={getValueColor(setting.value)}>
                                                {getValueDisplay(setting.value)}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {getCategoryIcon(setting.category)}
                                                <span className="text-sm">{setting.category}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="max-w-md">
                                            <span className="text-sm text-muted-foreground">
                                                {setting.description}
                                            </span>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {setting.readonly ? (
                                                    <>
                                                        <Lock className="h-4 w-4 text-gray-500" />
                                                        <span className="text-sm text-muted-foreground">Read-only</span>
                                                    </>
                                                ) : (
                                                    <>
                                                        <ToggleLeft className="h-4 w-4 text-blue-500" />
                                                        <span className="text-sm text-muted-foreground">Editable</span>
                                                    </>
                                                )}
                                            </div>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>

            {/* Configuration Info */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Info className="h-5 w-5" />
                        Configuration Information
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div>
                            <h4 className="font-semibold mb-2">Configuration Source</h4>
                            <p className="text-sm text-muted-foreground">
                                These settings are loaded from <code className="bg-gray-100 px-1 rounded">config/veritas_flags.toml</code>
                                and represent the current system configuration. All settings are read-only and cannot be modified
                                through the UI. Changes must be made directly to the configuration file and the system restarted.
                            </p>
                        </div>
                        <div>
                            <h4 className="font-semibold mb-2">Phase 8 Implementation</h4>
                            <p className="text-sm text-muted-foreground">
                                This configuration implements Phase 8 of the Living Truth Engine, providing flexible run parameters,
                                OCR pipeline configuration, YouTube channel processing, and web crawling settings. The system
                                enforces local-only operation by default with conservative limits and timeouts.
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default function SettingsPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <SettingsContent />
        </Suspense>
    );
}
