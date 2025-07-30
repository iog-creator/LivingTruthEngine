#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// Path to our Python script
const pythonScript = path.join(__dirname, 'flowise_mcp_server.py');

// Spawn the Python process
const pythonProcess = spawn('./living_venv/bin/python', [pythonScript], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: {
        ...process.env,
        FLOWISE_API_ENDPOINT: process.env.FLOWISE_API_ENDPOINT || 'http://localhost:3000',
        FLOWISE_API_KEY: process.env.FLOWISE_API_KEY,
        FLOWISE_CHATFLOW_ID: process.env.FLOWISE_CHATFLOW_ID,
        PYTHONPATH: __dirname
    }
});

// Forward stdin to Python process
process.stdin.pipe(pythonProcess.stdin);

// Forward Python stdout to our stdout
pythonProcess.stdout.pipe(process.stdout);

// Forward Python stderr to our stderr
pythonProcess.stderr.pipe(process.stderr);

// Handle process exit
pythonProcess.on('exit', (code) => {
    process.exit(code);
});

// Handle errors
pythonProcess.on('error', (err) => {
    console.error('Failed to start Python process:', err);
    process.exit(1);
}); 