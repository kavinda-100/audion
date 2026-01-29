# Audion Music Player

A simple, clean music player built with Python.

## Features

- **Playlist Support**: Load entire folders of music
- **Play Controls**: Play, Pause, Stop, Next, Previous
- **Progress Bar**: Visual progress with elapsed/remaining time
- **Seek Functionality**: Drag the progress bar to jump to any position in the song
- **Shuffle Mode**: Random playback order
- **Repeat Mode**: Loop through playlist continuously
- **Volume Control**: Adjustable volume slider (0-100%)
- **Auto-advance**: Automatically plays next track when current finishes
- **Visual Playlist**: See all tracks with current track highlighted
- **Double-click**: Jump to any track in the playlist
- Clean, native GUI using Tkinter

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
pip install pygame mutagen
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

1. **Load Music**:
   - Click "Open File" to play a single audio file
   - Click "Open Folder" to load all music from a directory

2. **Playback Controls**:
   - Use Previous/Next buttons to navigate tracks
   - Play/Pause/Stop to control playback
   - Double-click any track in the playlist to jump to it

3. **Modes**:
   - Toggle "Shuffle" for random playback order
   - Toggle "Repeat" to loop the playlist continuously

4. **Volume**: Adjust with the slider (0-100%)

The player will automatically advance to the next track when the current one finishes.

## Supported Audio Formats

- MP3
- WAV
- OGG/Vorbis
- FLAC

## Requirements

- Python 3.6+
- pygame 2.5.2+
- mutagen 1.47.0+ (for reading audio file metadata)
- tkinter (python3-tk package on Linux)

## Quick Start (Full Workflow)

```bash
# 1. Install tkinter (system-wide)
sudo apt-get install python3-tk  # Ubuntu/Debian

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install pygame mutagen

# 4. Run Audion
python audion.py

# 5. When done, deactivate
deactivate
```

## Future Enhancements

- Display track duration and time elapsed
- Keyboard shortcuts
- Recently played folders
- Dark mode
- Search/filter in playlist
- Save/load playlists
- Equalizer

Enjoy your music! 🎵
