#!/bin/bash

# Cursor Performance Fix Script
# Based on official Cursor documentation and community solutions

set -e

echo "🔧 Cursor Performance Fix Script"
echo "================================="
echo "This script follows official Cursor recommendations"
echo ""

# Stop Cursor processes
echo "🛑 Stopping Cursor processes..."
pkill -f "cursor.AppImage" || true
sleep 3

# Create backup of current configuration
BACKUP_DIR="$HOME/.config/Cursor_backup_$(date +%Y%m%d_%H%M%S)"
echo "📦 Creating backup at: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

# Backup important files
cp -r ~/.config/Cursor/User "$BACKUP_DIR/" 2>/dev/null || true
cp -r ~/.config/Cursor/Workspaces "$BACKUP_DIR/" 2>/dev/null || true

# Clear problematic cache (official solution)
echo "🧹 Clearing problematic cache directories..."

# Clear workspace storage (causes most issues)
echo "  Clearing workspace storage..."
rm -rf ~/.config/Cursor/User/workspaceStorage/* 2>/dev/null || true

# Clear global storage
echo "  Clearing global storage..."
rm -rf ~/.config/Cursor/User/globalStorage/* 2>/dev/null || true

# Clear cached data (large cache causing I/O issues)
echo "  Clearing cached data..."
rm -rf ~/.config/Cursor/CachedData/* 2>/dev/null || true

# Clear GPU cache
echo "  Clearing GPU cache..."
rm -rf ~/.config/Cursor/GPUCache/* 2>/dev/null || true

# Clear code cache
echo "  Clearing code cache..."
rm -rf ~/.config/Cursor/'Code Cache'/* 2>/dev/null || true

# Clear blob storage (large files)
echo "  Clearing blob storage..."
rm -rf ~/.config/Cursor/blob_storage/* 2>/dev/null || true

# Clear dawn caches
echo "  Clearing dawn caches..."
rm -rf ~/.config/Cursor/DawnGraphiteCache/* 2>/dev/null || true
rm -rf ~/.config/Cursor/DawnWebGPUCache/* 2>/dev/null || true

# Reset Cursor settings to defaults (optional)
echo "⚙️ Resetting Cursor settings..."
cat > ~/.config/Cursor/User/settings.json << 'EOF'
{
    "window.commandCenter": true,
    "cursor.composer.shouldChimeAfterChatFinishes": true,
    "cursor.composer.shouldAllowCustomModes": true,
    "cursor.composer.backspaceRemoveContext": false,
    "diffEditor.maxComputationTime": 0,
    "containers.containerClient": "com.microsoft.visualstudio.containers.docker",
    "containers.orchestratorClient": "com.microsoft.visualstudio.orchestrators.dockercompose"
}
EOF

# Create external cache directory on different disk
EXTERNAL_CACHE="/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02/cursor_cache"
if [ -d "/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02" ]; then
    echo "📁 Setting up external cache directory..."
    mkdir -p "$EXTERNAL_CACHE"
    
    # Create a script to launch Cursor with external cache
    cat > ~/.local/bin/cursor-external << 'EOF'
#!/bin/bash
# Launch Cursor with external cache directory
export TMPDIR="/media/mccoy/ebc29cc3-d43e-4e5e-afaa-47fc1ac75c02/cursor_cache/tmp"
mkdir -p "$TMPDIR"
/home/mccoy/Applications/cursor.AppImage --no-sandbox "$@"
EOF
    
    chmod +x ~/.local/bin/cursor-external
    
    echo "  ✅ External cache script created: ~/.local/bin/cursor-external"
else
    echo "  ⚠️  External disk not available, using local cache"
fi

echo ""
echo "✅ Cursor performance fix completed!"
echo ""
echo "📋 What was done:"
echo "  ✅ Cleared problematic cache directories"
echo "  ✅ Reset Cursor settings to defaults"
echo "  ✅ Created backup at: $BACKUP_DIR"
echo "  ✅ Set up external cache directory"
echo ""
echo "🚀 Next steps:"
echo "  1. Wait 10 seconds for processes to fully stop"
echo "  2. Start Cursor normally: /home/mccoy/Applications/cursor.AppImage"
echo "  3. Or use external cache: ~/.local/bin/cursor-external"
echo ""
echo "💡 If issues persist:"
echo "  - Restart your computer"
echo "  - Check disk space and I/O usage"
echo "  - Consider disabling extensions"
echo ""
echo "🔄 To restore backup:"
echo "  cp -r $BACKUP_DIR/* ~/.config/Cursor/" 