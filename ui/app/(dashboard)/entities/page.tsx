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
import { Building, ExternalLink, Globe, MapPin, Search, User, Users } from 'lucide-react';
import { useSearchParams } from 'next/navigation';
import { Suspense, useState } from 'react';

interface Entity {
    id: string;
    value: string;
    type: 'PERSON' | 'ORGANIZATION' | 'LOCATION' | 'CONCEPT' | 'DATE';
    confidence: number;
    link_count: number;
    source_document: string;
    span_start: number;
    span_end: number;
    created_at: string;
}

// Mock data for demonstration
const mockEntities: Entity[] = [
    {
        id: 'entity-1',
        value: 'John Smith',
        type: 'PERSON',
        confidence: 0.98,
        link_count: 5,
        source_document: 'Document 1',
        span_start: 120,
        span_end: 130,
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'entity-2',
        value: 'Stanford University',
        type: 'ORGANIZATION',
        confidence: 0.95,
        link_count: 3,
        source_document: 'Document 2',
        span_start: 45,
        span_end: 62,
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'entity-3',
        value: 'California',
        type: 'LOCATION',
        confidence: 0.92,
        link_count: 2,
        source_document: 'Document 1',
        span_start: 200,
        span_end: 210,
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'entity-4',
        value: 'Artificial Intelligence',
        type: 'CONCEPT',
        confidence: 0.88,
        link_count: 7,
        source_document: 'Document 3',
        span_start: 150,
        span_end: 170,
        created_at: '2025-08-13T17:05:33Z'
    },
    {
        id: 'entity-5',
        value: '2024',
        type: 'DATE',
        confidence: 0.99,
        link_count: 1,
        source_document: 'Document 2',
        span_start: 300,
        span_end: 304,
        created_at: '2025-08-13T17:05:33Z'
    }
];

function EntitiesContent() {
    const searchParams = useSearchParams();
    const runId = searchParams.get('run_id');
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedEntity, setSelectedEntity] = useState<Entity | null>(null);
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);

    // Filter entities based on search term
    const filteredEntities = mockEntities.filter(entity =>
        entity.value.toLowerCase().includes(searchTerm.toLowerCase()) ||
        entity.type.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const getEntityIcon = (type: string) => {
        switch (type) {
            case 'PERSON':
                return <User className="h-4 w-4 text-blue-500" />;
            case 'ORGANIZATION':
                return <Building className="h-4 w-4 text-green-500" />;
            case 'LOCATION':
                return <MapPin className="h-4 w-4 text-red-500" />;
            case 'CONCEPT':
                return <Globe className="h-4 w-4 text-purple-500" />;
            case 'DATE':
                return <Users className="h-4 w-4 text-orange-500" />;
            default:
                return <Users className="h-4 w-4 text-gray-500" />;
        }
    };

    const getEntityColor = (type: string) => {
        switch (type) {
            case 'PERSON':
                return 'bg-blue-100 text-blue-800';
            case 'ORGANIZATION':
                return 'bg-green-100 text-green-800';
            case 'LOCATION':
                return 'bg-red-100 text-red-800';
            case 'CONCEPT':
                return 'bg-purple-100 text-purple-800';
            case 'DATE':
                return 'bg-orange-100 text-orange-800';
            default:
                return 'bg-gray-100 text-gray-800';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Entities</h1>
                    <p className="text-muted-foreground">
                        Named entities extracted from documents
                        {runId && ` for run: ${runId}`}
                    </p>
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Users className="h-5 w-5" />
                        Entity Analysis
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex items-center space-x-2 mb-4">
                        <div className="relative flex-1">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search entities..."
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
                                    <TableHead>Entity</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Confidence</TableHead>
                                    <TableHead>Links</TableHead>
                                    <TableHead>Source</TableHead>
                                    <TableHead>Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredEntities.map((entity) => (
                                    <TableRow key={entity.id}>
                                        <TableCell className="max-w-md">
                                            <div className="space-y-1">
                                                <p className="font-medium">{entity.value}</p>
                                                <p className="text-sm text-muted-foreground">
                                                    Position: {entity.span_start}-{entity.span_end}
                                                </p>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                {getEntityIcon(entity.type)}
                                                <Badge className={getEntityColor(entity.type)}>
                                                    {entity.type}
                                                </Badge>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="secondary">
                                                {(entity.confidence * 100).toFixed(0)}%
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="outline">
                                                {entity.link_count} links
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex items-center gap-2">
                                                <Users className="h-4 w-4 text-muted-foreground" />
                                                <span className="text-sm">{entity.source_document}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Drawer open={isDrawerOpen} onOpenChange={setIsDrawerOpen}>
                                                <DrawerTrigger asChild>
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => setSelectedEntity(entity)}
                                                    >
                                                        View Details
                                                    </Button>
                                                </DrawerTrigger>
                                                <DrawerContent>
                                                    <div className="mx-auto w-full max-w-sm">
                                                        <DrawerHeader>
                                                            <DrawerTitle>Entity Details</DrawerTitle>
                                                            <DrawerDescription>
                                                                Detailed information about this entity
                                                            </DrawerDescription>
                                                        </DrawerHeader>
                                                        {selectedEntity && (
                                                            <div className="p-4 space-y-4">
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Entity Value</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        {selectedEntity.value}
                                                                    </p>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Entity Type</h4>
                                                                    <div className="flex items-center gap-2">
                                                                        {getEntityIcon(selectedEntity.type)}
                                                                        <Badge className={getEntityColor(selectedEntity.type)}>
                                                                            {selectedEntity.type}
                                                                        </Badge>
                                                                    </div>
                                                                </div>
                                                                <div className="grid grid-cols-2 gap-4">
                                                                    <div>
                                                                        <h4 className="font-semibold mb-2">Confidence</h4>
                                                                        <Badge variant="secondary">
                                                                            {(selectedEntity.confidence * 100).toFixed(0)}%
                                                                        </Badge>
                                                                    </div>
                                                                    <div>
                                                                        <h4 className="font-semibold mb-2">Link Count</h4>
                                                                        <Badge variant="outline">
                                                                            {selectedEntity.link_count} links
                                                                        </Badge>
                                                                    </div>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Text Position</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        Characters {selectedEntity.span_start} to {selectedEntity.span_end}
                                                                    </p>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Source Document</h4>
                                                                    <div className="flex items-center gap-2">
                                                                        <Users className="h-4 w-4" />
                                                                        <span className="text-sm">{selectedEntity.source_document}</span>
                                                                        <Button variant="ghost" size="sm">
                                                                            <ExternalLink className="h-4 w-4" />
                                                                        </Button>
                                                                    </div>
                                                                </div>
                                                                <div>
                                                                    <h4 className="font-semibold mb-2">Created</h4>
                                                                    <p className="text-sm text-muted-foreground">
                                                                        {new Date(selectedEntity.created_at).toLocaleString()}
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
                        Showing {filteredEntities.length} of {mockEntities.length} entities
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

export default function EntitiesPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <EntitiesContent />
        </Suspense>
    );
}
