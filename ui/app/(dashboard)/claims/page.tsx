'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
    Drawer,
    DrawerContent,
    DrawerDescription,
    DrawerHeader,
    DrawerTitle,
    DrawerTrigger
} from '@/components/ui/drawer';
import { Input } from '@/components/ui/input';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import { AlertCircle, CheckCircle, ExternalLink, FileText, Search, XCircle } from 'lucide-react';
import { useSearchParams } from 'next/navigation';
import { Suspense, useState } from 'react';

interface Claim {
    id: string;
    text: string;
    normalized: string;
    confidence: number;
    corroboration_label: 'corroborated' | 'weak' | 'contradicted';
    corroboration_confidence: number;
    link_count: number;
    source_document: string;
    created_at: string;
}

// Mock data for demonstration
const mockClaims: Claim[] = [
    {
        id: 'claim-1',
        text: 'The speaker discusses the importance of critical thinking in modern society',
        normalized: 'critical thinking importance modern society',
        confidence: 0.95,
        corroboration_label: 'corroborated',
        corroboration_confidence: 0.88,
        link_count: 3,
        source_document: 'Document 1',
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'claim-2',
        text: 'Evidence suggests that media literacy is declining among young people',
        normalized: 'media literacy declining young people',
        confidence: 0.87,
        corroboration_label: 'weak',
        corroboration_confidence: 0.45,
        link_count: 1,
        source_document: 'Document 2',
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'claim-3',
        text: 'The podcast emphasizes the role of education in combating misinformation',
        normalized: 'education role combating misinformation',
        confidence: 0.92,
        corroboration_label: 'corroborated',
        corroboration_confidence: 0.91,
        link_count: 5,
        source_document: 'Document 1',
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'claim-4',
        text: 'There is conflicting evidence about the effectiveness of fact-checking',
        normalized: 'conflicting evidence fact-checking effectiveness',
        confidence: 0.78,
        corroboration_label: 'contradicted',
        corroboration_confidence: 0.67,
        link_count: 2,
        source_document: 'Document 3',
        created_at: '2025-08-13T17:05:33Z'
    }
];

function ClaimsContent() {
    const searchParams = useSearchParams();
    const runId = searchParams.get('run_id');
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    // Filter claims based on search term
    const filteredClaims = mockClaims.filter(claim =>
        claim.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
        claim.normalized.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const getCorroborationIcon = (label: string) => {
        switch (label) {
            case 'corroborated':
                return <CheckCircle className="h-4 w-4 text-green-500" />;
            case 'weak':
                return <AlertCircle className="h-4 w-4 text-yellow-500" />;
            case 'contradicted':
                return <XCircle className="h-4 w-4 text-red-500" />;
            default:
                return <AlertCircle className="h-4 w-4 text-gray-500" />;
        }
    };

    const getCorroborationColor = (label: string) => {
        switch (label) {
            case 'corroborated':
                return 'bg-green-100 text-green-800';
            case 'weak':
                return 'bg-yellow-100 text-yellow-800';
            case 'contradicted':
                return 'bg-red-100 text-red-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Claims</h1>
                    <p className="text-muted-foreground">
                        Analyze and verify claims extracted from documents
                        {runId && ` for run: ${runId}`}
                    </p>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Claims Analysis
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center space-x-2 mb-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search claims..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-8"
                            />
                        </div>
                    </div>

                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Claim</TableHead>
                                    <TableHead>Confidence</TableHead>
                                    <TableHead>Corroboration</TableHead>
                                    <TableHead>Links</TableHead>
                                    <TableHead>Source</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredClaims.map((claim) => (
                                    <TableRow key={claim.id}>
                                        <TableCell className="max-w-md">
                                            <div className="space-y-1">
                                                <p className="font-medium">{claim.text}</p>
                                                <p className="text-sm text-muted-foreground">
                                                    {claim.normalized}
                                                </p>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="secondary">
                                                {(claim.confidence * 100).toFixed(0)}%
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {getCorroborationIcon(claim.corroboration_label)}
                                                <Badge className={getCorroborationColor(claim.corroboration_label)}>
                                                    {claim.corroboration_label}
                                                </Badge>
                                                <span className="text-sm text-muted-foreground">
                                                    ({(claim.corroboration_confidence * 100).toFixed(0)}%)
                                                </span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline">
                                                {claim.link_count} links
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                <FileText className="h-4 w-4 text-muted-foreground" />
                                                <span className="text-sm">{claim.source_document}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Drawer open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
                                                <DrawerTrigger asChild>
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => setSelectedClaim(claim)}
                                                    >
                                                        View Details
                                                    </Button>
                                                </DrawerTrigger>
                                                <DrawerContent>
                                                    <div className="mx-auto w-full max-w-sm">
                                                        <DrawerHeader>
                                                            <DrawerTitle>Claim Details</DrawerTitle>
                                                            <DrawerDescription>
                                                                Detailed information about this claim
                                                            </DrawerDescription>
                                                        </DrawerHeader>
                                                        {selectedClaim && (
                                                            <div className="p-4 space-y-4">
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Claim Text</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        {selectedClaim.text}
                                                                    </p>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Normalized Form</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        {selectedClaim.normalized}
                                                                    </p>
                                                                </div>
                                                                <div className="grid grid-cols-2 gap-4">
                                                                    <div>
                                                                        <h4 className="font-semibold mb-2">Extraction Confidence</h4>
                                                                        <Badge variant="secondary">
                                                                            {(selectedClaim.confidence * 100).toFixed(0)}%
                                                                        </Badge>
                                                                    </div>
                                                                    <div>
                                                                        <h4 className="font-semibold mb-2">Corroboration Confidence</h4>
                                                                        <Badge variant="secondary">
                                                                            {(selectedClaim.corroboration_confidence * 100).toFixed(0)}%
                                                                        </Badge>
                                                                    </div>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Source Document</h4>
                                                                    <div className="flex items-center gap-2">
                                                                        <FileText className="h-4 w-4" />
                                                                        <span className="text-sm">{selectedClaim.source_document}</span>
                                                                        <Button variant="ghost" size="sm">
                                                                            <ExternalLink className="h-4 w-4" />
                                                                        </Button>
                                                                    </div>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Created</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        {new Date(selectedClaim.created_at).toLocaleString()}
                                                                    </p>
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                </DrawerContent>
                                            </Drawer>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>

                    <div className="mt-4 text-sm text-muted-foreground">
                        Showing {filteredClaims.length} of {mockClaims.length} claims
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default function ClaimsPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <ClaimsContent />
        </Suspense>
    );
}
