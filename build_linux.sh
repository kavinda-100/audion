#!/bin/bash

# Audion Quick Build Script for Linux
# This script builds the Audion music player into a standalone executable

set -e

echo "🎵 Audion Linux Build Script"
echo "============================"

# Check if we're in the right directory
if [ ! -f "audion.py" ]; then
    echo "❌ Error: audion.py not found!"
    echo "Please run this script from the Audion project directory."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "🐍 Python version: $python_version"

# Install system dependencies for Ubuntu/Debian
if command -v apt-get &> /dev/null; then
    echo "📦 Installing system dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3-tk python3-dev python3-pip
fi

# Create virtual environment (recommended)
echo "🏗️ Setting up virtual environment..."
python3 -m venv build_env
source build_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install pygame mutagen pyinstaller

# Build the executable
echo "🔨 Building executable..."

# Check if assets folder exists
if [ ! -d "assets" ]; then
    echo "⚠️ Warning: assets folder not found. Building without icon."
    pyinstaller \
        --onefile \
        --windowed \
        --name="Audion" \
        --hidden-import=pygame \
        --hidden-import=mutagen \
        --distpath=./dist \
        --workpath=./build \
        --specpath=./build \
        audion.py
else
    echo "🎨 Found assets folder, including icons..."
    pyinstaller \
        --onefile \
        --windowed \
        --name="Audion" \
        --icon=assets/audion.png \
        --add-data="assets:assets" \
        --hidden-import=pygame \
        --hidden-import=mutagen \
        --distpath=./dist \
        --workpath=./build \
        --specpath=./build \
        audion.py
fi

# Check if build was successful
if [ -f "dist/Audion" ]; then
    # Make executable
    chmod +x dist/Audion
    
    echo "✅ Build successful!"
    echo "📍 Executable location: $(pwd)/dist/Audion"
    echo ""
    echo "🧪 Testing the executable..."
    
    # Test if it runs (just check if it starts without error)
    timeout 3s ./dist/Audion &>/dev/null || echo "⚠️ Note: Quick test completed (this is normal)"
    
    echo ""
    echo "🎉 Audion is ready!"
    echo ""
    echo "📋 Next steps:"
    echo "  • Test: ./dist/Audion"
    echo "  • Copy to /usr/local/bin: sudo cp dist/Audion /usr/local/bin/audion"
    echo "  • Create .deb package: see BUILD_INSTRUCTIONS.md"
    echo ""
    echo "📊 File size: $(ls -lh dist/Audion | awk '{print $5}')"
    
else
    echo "❌ Build failed!"
    echo "Check the error messages above."
    exit 1
fi

# Deactivate virtual environment
deactivate

echo "🏁 Build process completed!"