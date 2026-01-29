# Audion Music Player Installation Scripts

This directory contains automated installation scripts for different operating systems.

## Quick Installation

### Linux (Ubuntu, Debian, Fedora, Arch, etc.)

```bash
curl -fsSL https://raw.githubusercontent.com/your-username/audion/main/install_linux.sh | bash
```

### Windows

Download and run: `install_windows.bat`

## Manual Installation

### Linux

1. **Download the installation script:**

    ```bash
    wget https://raw.githubusercontent.com/your-username/audion/main/install_linux.sh
    chmod +x install_linux.sh
    ```

2. **Run the installation:**
    ```bash
    ./install_linux.sh
    ```

### Windows

1. **Download the installation script:** `install_windows.bat`
2. **Right-click and select "Run as Administrator" (optional)**
3. **Follow the on-screen prompts**

## What the Installation Scripts Do

### Linux Script (`install_linux.sh`)

1. **System Detection**: Automatically detects your Linux distribution
2. **Dependencies**: Installs system dependencies:
    - Python 3.8+
    - Git
    - Audio libraries (PortAudio, SDL2)
    - Tkinter
3. **Repository Setup**: Clones the Audion repository to `~/.local/share/audion`
4. **Python Environment**: Creates and configures a virtual environment
5. **Application Build**: Builds the executable using PyInstaller
6. **Integration**:
    - Creates desktop entry
    - Adds launcher to `~/.local/bin/audion`
    - Sets up file associations (optional)

**Supported Distributions:**

- Ubuntu / Debian
- Fedora / CentOS / RHEL
- Arch Linux / Manjaro
- Other distributions (with manual dependency installation)

### Windows Script (`install_windows.bat`)

1. **Environment Check**: Verifies Python and Git installation
2. **Repository Setup**: Clones the repository to `%USERPROFILE%\AppData\Local\Audion`
3. **Dependencies**: Installs Python dependencies via pip
4. **Application Build**: Creates Windows executable
5. **Integration**:
    - Desktop shortcut
    - Start Menu entry
    - File associations (optional)
6. **Uninstaller**: Creates uninstall script

## Installation Locations

### Linux

- **Application**: `~/.local/share/audion/`
- **Executable**: `~/.local/share/audion/dist/audion/audion`
- **Launcher**: `~/.local/bin/audion`
- **Desktop Entry**: `~/.local/share/applications/audion.desktop`

### Windows

- **Application**: `%USERPROFILE%\AppData\Local\Audion\`
- **Executable**: `%USERPROFILE%\AppData\Local\Audion\dist\audion\audion.exe`
- **Desktop Shortcut**: `%USERPROFILE%\Desktop\Audion Music Player.lnk`
- **Start Menu**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Audion\`

## Prerequisites

### Linux

- Bash shell
- Internet connection
- Sudo privileges (for system package installation)

### Windows

- Windows 10 or later (for ANSI color support)
- PowerShell (for shortcut creation)
- Internet connection
- Administrative privileges (optional, for system-wide installation)

## Troubleshooting

### Common Issues

#### Linux

**"Permission denied" when running script:**

```bash
chmod +x install_linux.sh
```

**Missing system dependencies:**
The script will attempt to install them automatically. If it fails:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git portaudio19-dev python3-tk

# Fedora
sudo dnf install python3 python3-pip python3-virtualenv git portaudio-devel python3-tkinter

# Arch
sudo pacman -S python python-pip python-virtualenv git portaudio tk
```

**Build failures:**
Ensure all dependencies are installed and try building manually:

```bash
cd ~/.local/share/audion
source venv/bin/activate
python build_executable.py
```

#### Windows

**Python not found:**

- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation
- Restart command prompt/PowerShell

**Git not found:**

- Install Git from https://git-scm.com/download/win
- Or download source code manually

**Build failures:**

- Ensure Python dependencies are installed
- Try running in Command Prompt as Administrator
- Check antivirus isn't blocking PyInstaller

## Manual Uninstallation

### Linux

```bash
# Remove application
rm -rf ~/.local/share/audion

# Remove launcher
rm -f ~/.local/bin/audion

# Remove desktop entry
rm -f ~/.local/share/applications/audion.desktop

# Remove config files (optional)
rm -f ~/.audion_config.json
rm -f ~/.audion_playlist.json
```

### Windows

Run the uninstaller: `%USERPROFILE%\AppData\Local\Audion\uninstall.bat`

Or manually:

```cmd
rmdir /s "%USERPROFILE%\AppData\Local\Audion"
del "%USERPROFILE%\Desktop\Audion Music Player.lnk"
rmdir /s "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Audion"
```

## Development Setup

For development installations that don't create system integration:

### Linux

```bash
git clone https://github.com/your-username/audion.git
cd audion
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python audion.py
```

### Windows

```cmd
git clone https://github.com/your-username/audion.git
cd audion
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python audion.py
```

## Customization

### Changing Installation Location

#### Linux

Edit the `INSTALL_DIR` variable in `install_linux.sh`:

```bash
INSTALL_DIR="$HOME/Applications/audion"  # Custom location
```

#### Windows

Edit the `INSTALL_DIR` variable in `install_windows.bat`:

```cmd
set INSTALL_DIR=C:\Program Files\Audion  # System-wide installation
```

### Repository URL

Update the `REPO_URL` variable in both scripts to point to your repository.

## Security Notes

- The scripts download and execute code from the internet
- Review the scripts before running them
- The Linux script requires sudo privileges for system package installation
- Windows script may trigger antivirus warnings due to executable creation

## Contributing

To improve the installation scripts:

1. Test on different operating systems
2. Add support for more package managers
3. Improve error handling and user feedback
4. Add more customization options

## License

These installation scripts are part of the Audion Music Player project and follow the same license terms.
