# Audion Music Player

A simple, clean music player built with Python.

## Features

- Play audio files (MP3, WAV, OGG, FLAC)
- Play/Pause/Stop controls
- Volume control slider
- Clean, native GUI using Tkinter
- Auto-play when file is loaded

## Installation

### 1. Install system dependencies

First, install tkinter (required for GUI):

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S tk
```

**openSUSE:**
```bash
sudo zypper install python3-tk
```

### 2. Set up virtual environment (recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Python dependencies

```bash
pip install pygame
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### 4. Run the player

```bash
python audion.py
```

Or make it executable:

```bash
chmod +x audion.py
./audion.py
```

### 5. Deactivate virtual environment (when done)

```bash
deactivate
```

## Usage

1. Click "Open Audio File" to select an audio file
2. The file will start playing automatically
3. Use Play/Pause/Stop buttons to control playback
4. Adjust volume with the slider (0-100%)

## Supported Audio Formats

- MP3
- WAV
- OGG/Vorbis
- FLAC

## Requirements

- Python 3.6+
- pygame 2.5.2+
- tkinter (python3-tk package on Linux)

## Quick Start (Full Workflow)

```bash
# 1. Install tkinter (system-wide)
sudo apt-get install python3-tk  # Ubuntu/Debian

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install pygame
pip install pygame

# 4. Run Audion
python audion.py

# 5. When done, deactivate
deactivate
```

## Future Enhancements

- Playlist support
- Seek bar
- Track time display
- Keyboard shortcuts
- Recently played files
- Dark mode

Enjoy your music! 🎵
