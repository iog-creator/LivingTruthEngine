#!/bin/bash

# Cursor AppArmor Fix Script for Ubuntu
# This script fixes the "Cursor is not responding" issues caused by AppArmor restrictions

set -e

echo "🔧 Cursor AppArmor Fix Script"
echo "=============================="

# Check if running as root for certain operations
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root"
   exit 1
fi

echo "📋 Step 1: Installing required dependencies..."
sudo apt update
sudo apt install libfuse2t64 -y

echo "📋 Step 2: Setting up Cursor AppImage..."
mkdir -p ~/Applications

# Check if Cursor AppImage exists in .local/share/cursor
if [[ -f ~/.local/share/cursor/Cursor-*.AppImage ]]; then
    echo "📁 Found Cursor AppImage, copying to Applications directory..."
    cp ~/.local/share/cursor/Cursor-*.AppImage ~/Applications/cursor.AppImage
    chmod +x ~/Applications/cursor.AppImage
    echo "✅ Cursor AppImage copied to ~/Applications/"
    
    echo "🧹 Cleaning up old Cursor references..."
    # Remove old desktop entry if it exists
    if [[ -f ~/.local/share/applications/cursor.desktop ]]; then
        rm ~/.local/share/applications/cursor.desktop
        echo "✅ Removed old desktop entry"
    fi
    
    # Remove old launch script if it exists
    if [[ -f ~/.local/share/cursor/launch_cursor.sh ]]; then
        rm ~/.local/share/cursor/launch_cursor.sh
        echo "✅ Removed old launch script"
    fi
    
    # Remove old AppImage backup if it exists
    if [[ -f ~/.local/share/cursor/Cursor-*.AppImage.zs-old ]]; then
        rm ~/.local/share/cursor/Cursor-*.AppImage.zs-old
        echo "✅ Removed old AppImage backup"
    fi
    
    # Remove old desktop entry in cursor directory if it exists
    if [[ -f ~/.local/share/cursor/cursor.desktop ]]; then
        rm ~/.local/share/cursor/cursor.desktop
        echo "✅ Removed old cursor.desktop file"
    fi
    
    echo "✅ Cleanup completed!"
else
    echo "⚠️  Cursor AppImage not found in ~/.local/share/cursor/"
    echo "   Please download Cursor from https://cursor.com/downloads"
    echo "   and place it in ~/Applications/cursor.AppImage"
fi

echo "📋 Step 3: Creating AppArmor profile..."
sudo tee /etc/apparmor.d/cursor-appimage > /dev/null << 'EOF'
# This profile allows everything and only exists to give the
# application a name instead of having the label "unconfined"

abi <abi/4.0>,
include <tunables/global>

profile cursor /home/mccoy/Applications/cursor*.AppImage flags=(unconfined) {
  userns,

  # Site-specific additions and overrides. See local/README for details.
  include if exists <local/cursor>
}
EOF

echo "📋 Step 4: Applying AppArmor policy..."
sudo apparmor_parser -r /etc/apparmor.d/cursor-appimage

echo "📋 Step 5: Creating desktop entry..."
sudo tee /usr/share/applications/cursor.desktop > /dev/null << 'EOF'
[Desktop Entry]
Name=Cursor
Exec=/home/mccoy/Applications/cursor.AppImage --no-sandbox
Icon=/home/mccoy/.local/share/cursor/cursor.png
Type=Application
Categories=Development;
Comment=AI-first code editor
EOF

echo "📋 Step 6: Verifying installation..."
if sudo aa-status | grep -q cursor; then
    echo "✅ AppArmor profile loaded successfully"
else
    echo "❌ AppArmor profile not loaded"
fi

if [[ -f ~/Applications/cursor.AppImage ]]; then
    echo "✅ Cursor AppImage found in Applications directory"
else
    echo "❌ Cursor AppImage not found"
fi

echo ""
echo "🎉 Cursor AppArmor fix completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Restart Cursor completely"
echo "   2. If issues persist, try running with --disable-gpu flag"
echo "   3. Check system resources with 'htop' during AI operations"
echo ""
echo "🔧 To launch Cursor manually:"
echo "   ~/Applications/cursor.AppImage --no-sandbox"
echo ""
echo "📊 To monitor system resources:"
echo "   htop"
echo ""
echo "🔄 To restart AppArmor if needed:"
echo "   sudo systemctl restart apparmor" 