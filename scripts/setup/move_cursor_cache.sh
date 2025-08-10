#!/bin/bash

# Cursor Cache Migration Script
# Moves Cursor cache to a different disk to prevent I/O conflicts

set -e  # Exit on any error

# Configuration
CACHE_SOURCE="$HOME/.config/Cursor"
CACHE_DEST="/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02/cursor_cache"
BACKUP_DIR="$HOME/.config/Cursor_cache_backup_$(date +%Y%m%d_%H%M%S)"

# Cache directories to move
CACHE_DIRS=(
    "CachedData"
    "Cache" 
    "GPUCache"
    "Code Cache"
    "blob_storage"
    "DawnGraphiteCache"
    "DawnWebGPUCache"
)

echo "🔄 Cursor Cache Migration Script"
echo "=================================="
echo "Source: $CACHE_SOURCE"
echo "Destination: $CACHE_DEST"
echo "Backup: $BACKUP_DIR"
echo ""

# Check if destination disk is mounted
if [ ! -d "/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02" ]; then
    echo "❌ Error: Destination disk not mounted"
    echo "Please ensure the disk is mounted at /media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02"
    exit 1
fi

# Check available space
SOURCE_SIZE=$(du -sb "$CACHE_SOURCE" 2>/dev/null | cut -f1 || echo "0")
DEST_AVAIL=$(df -B1 "/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02" | tail -1 | awk '{print $4}')

echo "📊 Space Analysis:"
echo "  Source cache size: $(numfmt --to=iec $SOURCE_SIZE)"
echo "  Destination available: $(numfmt --to=iec $DEST_AVAIL)"
echo ""

if [ "$SOURCE_SIZE" -gt "$DEST_AVAIL" ]; then
    echo "❌ Error: Not enough space on destination disk"
    exit 1
fi

# Create backup directory
echo "📦 Creating backup..."
mkdir -p "$BACKUP_DIR"

# Create destination directory
echo "📁 Creating destination directory..."
mkdir -p "$CACHE_DEST"

# Stop Cursor if running
echo "🛑 Stopping Cursor processes..."
pkill -f "cursor.AppImage" || true
sleep 2

# Move cache directories
for dir in "${CACHE_DIRS[@]}"; do
    if [ -d "$CACHE_SOURCE/$dir" ]; then
        echo "🔄 Moving $dir..."
        
        # Create backup
        cp -r "$CACHE_SOURCE/$dir" "$BACKUP_DIR/"
        
        # Move to destination
        mv "$CACHE_SOURCE/$dir" "$CACHE_DEST/"
        
        # Create symlink
        ln -sf "$CACHE_DEST/$dir" "$CACHE_SOURCE/$dir"
        
        echo "  ✅ $dir moved and symlinked"
    else
        echo "  ⚠️  $dir not found, skipping"
    fi
done

# Create a symlink for the entire cache directory (fallback)
echo "🔗 Creating main cache symlink..."
if [ ! -L "$CACHE_SOURCE/Cache" ]; then
    ln -sf "$CACHE_DEST" "$CACHE_SOURCE/Cache_External"
fi

echo ""
echo "✅ Cache migration completed successfully!"
echo ""
echo "📋 Summary:"
echo "  Cache moved to: $CACHE_DEST"
echo "  Backup created at: $BACKUP_DIR"
echo "  Symlinks created in: $CACHE_SOURCE"
echo ""
echo "🚀 You can now restart Cursor. The cache will be stored on a different disk."
echo "💡 To revert, run: rm -rf $CACHE_SOURCE/* && cp -r $BACKUP_DIR/* $CACHE_SOURCE/" 