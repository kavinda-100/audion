# 🎵 Audion Music Player

A modern, sleek music player built with Python featuring a clean UI inspired by macOS and modern design principles.

![Audion Music Player](assets/audion.png)

## ✨ Features

- 🎨 **Modern UI**: Clean, neutral design inspired by macOS and Windows 11
- 📂 **Playlist Support**: Load entire folders of music or individual files
- 🎮 **Full Playback Controls**: Play, Pause, Stop, Next, Previous with seek functionality
- 🔄 **Smart Modes**: Shuffle and repeat modes for continuous listening
- 🔊 **Volume Control**: Smooth volume adjustment with visual feedback
- 📱 **Visual Playlist**: Beautiful playlist view with current track highlighting
- 💾 **Persistence**: Remembers your playlist and last opened folder
- 🎯 **Quick Navigation**: Double-click any track to jump directly to it
- 📊 **Progress Tracking**: Visual progress bar with time elapsed and remaining
- 🖼️ **Professional Icons**: Integrated app icons for all platforms

## 🚀 Quick Installation

### Linux (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/kavinda-100/audion/main/install_linux.sh | bash
```

### Windows

1. Download [`install_windows.bat`](https://raw.githubusercontent.com/kavinda-100/audion/main/install_windows.bat)
2. Double-click to run
3. Follow the prompts

### What the Installation Does

- ✅ Installs all system dependencies automatically
- ✅ Downloads the latest version from GitHub
- ✅ Sets up Python environment with all required packages
- ✅ Builds a standalone executable
- ✅ Creates desktop shortcuts and Start Menu entries
- ✅ Sets up file associations (optional)
- ✅ Creates an uninstaller

## 🎯 Usage

1. **Load Music**:
    - Click "📂 Open File" for a single track
    - Click "📁 Open Folder" to load an entire music directory

2. **Playback**:
    - Use the modern control buttons for playback
    - Drag the progress bar to seek to any position
    - Adjust volume with the smooth slider

3. **Playlist**:
    - View all tracks in the beautiful playlist
    - Double-click any track to play it immediately
    - Current track is highlighted with a ▶ indicator

4. **Smart Features**:
    - Toggle 🔀 Shuffle for random playback
    - Toggle 🔁 Repeat to loop the playlist
    - Your playlist and preferences are automatically saved

## 🎵 Supported Formats

- **MP3** - Most common format
- **WAV** - Uncompressed audio
- **OGG** - Open source format
- **FLAC** - Lossless compression

## 🛠️ Developer Installation

For development or manual setup:

```bash
# Clone the repository
git clone https://github.com/kavinda-100/audion.git
cd audion

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python audion.py
```

## 🏗️ Building Executables

To create standalone executables:

```bash
# Activate your virtual environment first
source venv/bin/activate

# Build executable
python build_executable.py

# Find your executable in dist/ folder
```

## 📋 System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Storage**: 100 MB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)

### Dependencies (automatically installed)

- `pygame` - Audio playback engine
- `mutagen` - Audio metadata reading
- `tkinter` - GUI framework (included with Python)

## 🗂️ Installation Locations

### Linux

- **App**: `~/.local/share/audion/`
- **Executable**: Available as `audion` command
- **Config**: `~/.audion_config.json`

### Windows

- **App**: `%USERPROFILE%\AppData\Local\Audion\`
- **Shortcuts**: Desktop and Start Menu
- **Config**: `%USERPROFILE%\.audion_config.json`

## 🔧 Troubleshooting

### Audio Issues

- Ensure your system has audio drivers installed
- Check volume mixer settings
- Try different audio formats

### Installation Issues

- **Linux**: Ensure you have `curl` installed
- **Windows**: Run as Administrator if needed
- **Both**: Check internet connection

### Performance

- Large playlists (1000+ tracks) may take time to load
- FLAC files require more processing power

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test
4. Commit: `git commit -am 'Add feature'`
5. Push: `git push origin feature-name`
6. Submit a Pull Request

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

## 🙏 Acknowledgments

- Built with Python's `tkinter` for cross-platform GUI
- Audio playback powered by `pygame`
- Metadata reading via `mutagen`
- UI inspired by modern macOS and Windows design

---

**Enjoy your music!** 🎵✨

For support or questions, please [open an issue](https://github.com/kavinda-100/audion/issues).
