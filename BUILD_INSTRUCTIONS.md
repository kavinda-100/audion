# Audion - Cross-Platform Build Instructions

## 🚀 Quick Start

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Simple Build (One-liner)

```bash
# For GUI app with icon (recommended)
pyinstaller --onefile --windowed --name="Audion" --icon=assets/audion.png --add-data="assets:assets" --hidden-import=pygame --hidden-import=mutagen audion.py

# For Windows
pyinstaller --onefile --windowed --name="Audion" --icon=assets/audion.ico --add-data="assets;assets" --hidden-import=pygame --hidden-import=mutagen audion.py

# For macOS
pyinstaller --onefile --windowed --name="Audion" --icon=assets/audion.icns --add-data="assets:assets" --hidden-import=pygame --hidden-import=mutagen audion.py

# For debug (shows console)
pyinstaller --onefile --name="Audion" --icon=assets/audion.png --add-data="assets:assets" --hidden-import=pygame --hidden-import=mutagen audion.py
```

### 3. Use the Build Script

```bash
python build_executable.py
```

## 📦 Platform-Specific Instructions

### 🐧 Linux (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3-tk python3-dev

# Install Python packages
pip install pygame mutagen pyinstaller

# Build executable
python build_executable.py

# The executable will be in: dist/Audion
# You can run it directly: ./dist/Audion
```

### 🍎 macOS

```bash
# Install dependencies (with Homebrew)
brew install python-tk

# Install Python packages
pip install pygame mutagen pyinstaller

# Build executable
python build_executable.py

# The app bundle will be in: dist/Audion
# You can run it: open dist/Audion.app (if you create an app bundle)
```

### 🪟 Windows

```bash
# Install Python packages
pip install pygame mutagen pyinstaller

# Build executable
python build_executable.py

# The executable will be in: dist/Audion.exe
```

## 🎯 Advanced Options

### Create App Bundle (macOS)

```bash
pyinstaller --onefile --windowed --name="Audion" \
    --hidden-import=pygame --hidden-import=mutagen \
    --osx-bundle-identifier=com.yourname.audion \
    audion.py
```

### Add Icon

```bash
# Create icon files first:
# - Windows: icon.ico
# - macOS: icon.icns
# - Linux: icon.png

pyinstaller --onefile --windowed --name="Audion" \
    --icon=icon.ico \
    --hidden-import=pygame --hidden-import=mutagen \
    audion.py
```

### Debug Build

```bash
pyinstaller --onefile --name="Audion" \
    --console \
    --hidden-import=pygame --hidden-import=mutagen \
    audion.py
```

## 📋 Creating Installation Packages

### 🐧 Linux - Create .deb Package

```bash
# 1. Create package structure
mkdir -p audion-deb/DEBIAN
mkdir -p audion-deb/usr/bin
mkdir -p audion-deb/usr/share/applications
mkdir -p audion-deb/usr/share/pixmaps

# 2. Copy executable
cp dist/Audion audion-deb/usr/bin/audion

# 3. Create control file
cat > audion-deb/DEBIAN/control << EOF
Package: audion
Version: 1.0.0
Section: multimedia
Priority: optional
Architecture: amd64
Depends: libc6
Maintainer: Your Name <your.email@example.com>
Description: Modern Music Player
 A beautiful, modern music player built with Python and tkinter.
 Supports MP3, WAV, OGG, and FLAC audio formats.
EOF

# 4. Create desktop entry
cat > audion-deb/usr/share/applications/audion.desktop << EOF
[Desktop Entry]
Name=Audion
Comment=Modern Music Player
Exec=/usr/bin/audion
Icon=audion
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Player;
EOF

# 5. Build package
dpkg-deb --build audion-deb
mv audion-deb.deb audion_1.0.0_amd64.deb
```

### 🪟 Windows - Create Installer with Inno Setup

```inno
; Create setup.iss file
[Setup]
AppName=Audion
AppVersion=1.0.0
AppPublisher=Your Name
DefaultDirName={pf}\Audion
DefaultGroupName=Audion
OutputDir=installer
OutputBaseFilename=AudionSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\Audion.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Audion"; Filename: "{app}\Audion.exe"
Name: "{commondesktop}\Audion"; Filename: "{app}\Audion.exe"
```

### 🍎 macOS - Create .dmg

```bash
# Use create-dmg tool
brew install create-dmg

create-dmg \
    --volname "Audion Installer" \
    --window-pos 200 120 \
    --window-size 600 300 \
    --icon-size 100 \
    --app-drop-link 425 120 \
    "Audion-1.0.0.dmg" \
    "dist/"
```

## 🔧 Troubleshooting

### Common Issues:

1. **Missing modules**: Add `--hidden-import=module_name`
2. **tkinter issues**: Install `python3-tk` on Linux
3. **pygame/audio issues**: Install system audio libraries
4. **Large file size**: Use `--exclude-module` for unused modules

### Optimize File Size:

```bash
pyinstaller --onefile --windowed \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module scipy \
    --name="Audion" \
    audion.py
```

## 🌐 Cross-Platform Distribution Strategy

### Build Matrix:

- **Linux**: Build on Ubuntu LTS (most compatible)
- **macOS**: Build on macOS 10.14+ (for compatibility)
- **Windows**: Build on Windows 10+ with Python 3.8+

### Automated Building with GitHub Actions:

Create `.github/workflows/build.yml` for automatic builds on all platforms when you push code.

## 📦 File Sizes (Approximate)

- **Linux**: ~25-35 MB
- **macOS**: ~30-40 MB
- **Windows**: ~20-30 MB

## 🚀 Distribution Platforms

- **Linux**: Package repositories, Snap, Flatpak, AppImage
- **macOS**: Mac App Store, Homebrew, direct download
- **Windows**: Microsoft Store, Chocolatey, direct download
