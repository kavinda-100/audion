#!/usr/bin/env python3
"""
Build script for creating Audion executable
"""
import os
import sys
import subprocess
import platform

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_spec_file():
    """Create PyInstaller spec file for customization"""
    system = platform.system()
    
    # Determine icon path based on platform
    icon_path = None
    if system == 'Windows' and os.path.exists('assets/audion.ico'):
        icon_path = 'assets/audion.ico'
    elif system == 'Darwin' and os.path.exists('assets/audion.icns'):
        icon_path = 'assets/audion.icns'
    elif system == 'Linux' and os.path.exists('assets/audion.png'):
        icon_path = 'assets/audion.png'
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['audion.py'],
    pathex=[],
    binaries=[],
    datas=[('assets/', 'assets/')],  # Include assets folder
    hiddenimports=['pygame', 'mutagen'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Audion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to False for GUI app
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='{icon_path}' if icon_path else None,
)
'''
    
    with open('audion.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Created audion.spec file")

def build_executable():
    """Build the executable"""
    system = platform.system()
    print(f"🔨 Building executable for {system}...")
    
    # Create spec file first
    create_spec_file()
    
    # Build using spec file
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "audion.spec"]
    
    try:
        subprocess.check_call(cmd)
        print(f"✅ Executable created successfully!")
        
        # Show location
        if system == "Windows":
            exe_path = "dist/Audion.exe"
        else:
            exe_path = "dist/Audion"
            
        if os.path.exists(exe_path):
            print(f"📍 Executable location: {os.path.abspath(exe_path)}")
            
            # Make executable on Unix systems
            if system in ["Linux", "Darwin"]:
                os.chmod(exe_path, 0o755)
                print("✅ Made executable")
                
        else:
            print("❌ Executable not found in expected location")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def main():
    print("🎵 Audion Executable Builder")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not os.path.exists('audion.py'):
        print("❌ audion.py not found! Please run this from the project directory.")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Build executable
    success = build_executable()
    
    if success:
        print("\n🎉 Build completed successfully!")
        print("\n📋 Next steps:")
        print("  • Test the executable in the dist/ folder")
        print("  • Create installer packages (see instructions below)")
        print("  • Distribute to users")
    else:
        print("\n❌ Build failed. Check error messages above.")

if __name__ == "__main__":
    main()