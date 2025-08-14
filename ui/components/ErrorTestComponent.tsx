'use client';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AlertTriangle, Bug, Zap } from 'lucide-react';
import { useState } from 'react';

interface ErrorTestComponentProps {
    onErrorTriggered?: () => void;
}

// Component that will throw an error when triggered
function BuggyComponent({ onErrorTriggered }: { onErrorTriggered?: () => void }) {
    const [shouldThrow, setShouldThrow] = useState(false);

    if (shouldThrow) {
        onErrorTriggered?.();
        throw new Error('This is a test error to demonstrate the error boundary!');
    }

    return (
        <Card className="border-red-200 bg-red-50">
            <CardHeader>
                <CardTitle className="flex items-center gap-2 text-red-600">
                    <Bug className="h-5 w-5" />
                    Buggy Component
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-sm text-red-700 mb-4">
                    This component will throw an error when the button below is clicked.
                </p>
                <Button
                    onClick={() => setShouldThrow(true)}
                    variant="destructive"
                    className="flex items-center gap-2"
                >
                    <Zap className="h-4 w-4" />
                    Trigger Error
                </Button>
            </CardContent>
        </Card>
    );
}

export default function ErrorTestComponent({ onErrorTriggered }: ErrorTestComponentProps) {
    const [showBuggyComponent, setShowBuggyComponent] = useState(false);

    return (
        <div className="space-y-4">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <AlertTriangle className="h-5 w-5 text-yellow-600" />
                        Error Boundary Test
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center gap-2">
                        <Badge variant="outline">Development Only</Badge>
                        <span className="text-sm text-muted-foreground">
                            This component is for testing the error boundary functionality
                        </span>
                    </div>

                    <p className="text-sm text-muted-foreground">
                        Click the button below to test the error boundary. The error boundary will catch
                        the error and display a user-friendly error message with recovery options.
                    </p>

                    <div className="flex gap-2">
                        <Button
                            onClick={() => setShowBuggyComponent(true)}
                            variant="outline"
                            className="flex items-center gap-2"
                        >
                            <Bug className="h-4 w-4" />
                            Show Buggy Component
                        </Button>

                        <Button
                            onClick={() => setShowBuggyComponent(false)}
                            variant="outline"
                        >
                            Hide Component
                        </Button>
                    </div>

                    {showBuggyComponent && (
                        <BuggyComponent onErrorTriggered={onErrorTriggered} />
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
