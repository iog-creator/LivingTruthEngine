# LM Studio MCP Tools Plugin

This plugin provides LM Studio with access to Living Truth Engine MCP tools, enabling headless operation with visible inference in developer logs.

## Features

- **validate_cursor_rules**: Validate all cursor rules (.mdc files)
- **validate_ssot_bundle**: Validate SSOT (Single Source of Truth) bundle files  
- **run_health_checks**: Run comprehensive system health checks

## Installation

1. Build the plugin:
```bash
cd lmstudio-mcp-tools
npm install
npm run build
```

2. Copy the plugin to LM Studio's plugins directory:
```bash
cp -r lmstudio-mcp-tools /path/to/lmstudio/plugins/
```

3. Restart LM Studio

## Usage

Once installed, you can ask LM Studio:
- "Can you validate the cursor rules?"
- "Can you validate the SSOT bundle?"
- "Can you run health checks?"

You'll see inference happening in the LM Studio developer logs!

## Development

```bash
npm run dev  # Watch mode for development
npm run build  # Build for production
```
