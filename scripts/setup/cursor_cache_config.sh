#!/bin/bash

# Cursor Cache Configuration Script
# Sets up environment variables for external cache location

# Cache location on external disk
CACHE_DEST="/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02/cursor_cache"

# Environment variables to set
export CURSOR_CACHE_DIR="$CACHE_DEST"
export CURSOR_BLOB_STORAGE_DIR="$CACHE_DEST/blob_storage"
export CURSOR_GPUCACHE_DIR="$CACHE_DEST/GPUCache"
export CURSOR_CODECACHE_DIR="$CACHE_DEST/Code Cache"

# Create desktop entry with cache environment
DESKTOP_ENTRY="$HOME/.local/share/applications/cursor-external-cache.desktop"

cat > "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Name=Cursor (External Cache)
Exec=env CURSOR_CACHE_DIR="$CACHE_DEST" CURSOR_BLOB_STORAGE_DIR="$CACHE_DEST/blob_storage" CURSOR_GPUCACHE_DIR="$CACHE_DEST/GPUCache" CURSOR_CODECACHE_DIR="$CACHE_DEST/Code Cache" /home/mccoy/Applications/cursor.AppImage --no-sandbox
Icon=/home/mccoy/.local/share/cursor/cursor.png
Type=Application
Categories=Development;
Comment=AI-first code editor with external cache
EOF

chmod +x "$DESKTOP_ENTRY"

echo "✅ Cursor cache configuration created"
echo "📁 Desktop entry: $DESKTOP_ENTRY"
echo "🔗 Cache location: $CACHE_DEST"
echo ""
echo "💡 Use 'Cursor (External Cache)' from applications menu to launch with external cache" 