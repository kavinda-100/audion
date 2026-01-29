#!/bin/bash

# Audion Music Player - Linux Installation Script
# This script will clone the repository, install dependencies, and set up the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}    🎵 Audion Music Player Installation${NC}"
    echo -e "${BLUE}================================================${NC}"
}

# Check if running as root (not recommended)
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. This is not recommended for security reasons."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 1
        fi
    fi
}

# Detect Linux distribution
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO=$ID
        VERSION=$VERSION_ID
    else
        print_error "Cannot detect Linux distribution"
        exit 1
    fi
    print_info "Detected: $PRETTY_NAME"
}

# Install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."
    
    case $DISTRO in
        ubuntu|debian)
            sudo apt update
            sudo apt install -y \
                python3 \
                python3-pip \
                python3-venv \
                python3-dev \
                git \
                portaudio19-dev \
                python3-tk \
                libsdl2-dev \
                libsdl2-mixer-2.0-0 \
                libsdl2-ttf-2.0-0 \
                libsdl2-image-2.0-0
            ;;
        fedora|centos|rhel)
            sudo dnf install -y \
                python3 \
                python3-pip \
                python3-virtualenv \
                python3-devel \
                git \
                portaudio-devel \
                tkinter \
                python3-tkinter \
                SDL2-devel \
                SDL2_mixer \
                SDL2_ttf \
                SDL2_image
            ;;
        arch|manjaro)
            sudo pacman -S --needed \
                python \
                python-pip \
                python-virtualenv \
                git \
                portaudio \
                tk \
                sdl2 \
                sdl2_mixer \
                sdl2_ttf \
                sdl2_image
            ;;
        *)
            print_warning "Unsupported distribution: $DISTRO"
            print_info "Please install the following manually:"
            print_info "- Python 3.8+ with pip and venv"
            print_info "- Git"
            print_info "- PortAudio development files"
            print_info "- Tkinter (python3-tk)"
            print_info "- SDL2 libraries"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
            ;;
    esac
}

# Clone or update repository
setup_repo() {
    local INSTALL_DIR="$HOME/.local/share/audion"
    local REPO_URL="https://github.com/your-username/audion.git"  # Replace with actual repo URL
    
    print_info "Setting up Audion repository..."
    
    if [[ -d "$INSTALL_DIR" ]]; then
        print_info "Existing installation found. Updating..."
        cd "$INSTALL_DIR"
        git pull origin main
    else
        print_info "Cloning Audion repository..."
        mkdir -p "$(dirname "$INSTALL_DIR")"
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    AUDION_DIR="$INSTALL_DIR"
}

# Setup Python virtual environment
setup_python_env() {
    print_info "Setting up Python virtual environment..."
    
    cd "$AUDION_DIR"
    
    # Create virtual environment if it doesn't exist
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Install additional dependencies for building executables
    pip install pyinstaller
}

# Build the application
build_application() {
    print_info "Building Audion application..."
    
    cd "$AUDION_DIR"
    source venv/bin/activate
    
    # Create executable
    python build_executable.py
    
    if [[ -d "dist/audion" ]]; then
        print_success "Application built successfully!"
    else
        print_error "Failed to build application"
        exit 1
    fi
}

# Create desktop entry
create_desktop_entry() {
    print_info "Creating desktop entry..."
    
    local DESKTOP_FILE="$HOME/.local/share/applications/audion.desktop"
    local ICON_PATH="$AUDION_DIR/assets/audion.png"
    local EXEC_PATH="$AUDION_DIR/dist/audion/audion"
    
    # Create applications directory if it doesn't exist
    mkdir -p "$(dirname "$DESKTOP_FILE")"
    
    # Create desktop entry
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Audion Music Player
Comment=A modern music player built with Python
Exec=$EXEC_PATH
Icon=$ICON_PATH
Terminal=false
StartupNotify=true
Categories=AudioVideo;Audio;Player;
MimeType=audio/mpeg;audio/mp3;audio/wav;audio/ogg;audio/flac;
Keywords=music;audio;player;mp3;wav;ogg;flac;
EOF

    # Make desktop file executable
    chmod +x "$DESKTOP_FILE"
    
    # Update desktop database
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database "$HOME/.local/share/applications"
    fi
}

# Create launcher script
create_launcher() {
    print_info "Creating launcher script..."
    
    local LAUNCHER_PATH="$HOME/.local/bin/audion"
    
    # Create bin directory if it doesn't exist
    mkdir -p "$(dirname "$LAUNCHER_PATH")"
    
    # Create launcher script
    cat > "$LAUNCHER_PATH" << EOF
#!/bin/bash
# Audion Music Player Launcher
exec "$AUDION_DIR/dist/audion/audion" "\$@"
EOF

    # Make launcher executable
    chmod +x "$LAUNCHER_PATH"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        print_info "Adding $HOME/.local/bin to PATH..."
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        print_info "Please run 'source ~/.bashrc' or restart your terminal to use 'audion' command"
    fi
}

# Setup file associations (optional)
setup_file_associations() {
    print_info "Setting up file associations..."
    
    local MIMETYPES_FILE="$HOME/.local/share/applications/mimeapps.list"
    
    # Create mimeapps.list if it doesn't exist
    if [[ ! -f "$MIMETYPES_FILE" ]]; then
        mkdir -p "$(dirname "$MIMETYPES_FILE")"
        cat > "$MIMETYPES_FILE" << EOF
[Default Applications]

[Added Associations]
EOF
    fi
    
    # Add audio file associations
    local AUDIO_TYPES=(
        "audio/mpeg=audion.desktop;"
        "audio/mp3=audion.desktop;"
        "audio/wav=audion.desktop;"
        "audio/ogg=audion.desktop;"
        "audio/flac=audion.desktop;"
    )
    
    for association in "${AUDIO_TYPES[@]}"; do
        if ! grep -q "$association" "$MIMETYPES_FILE"; then
            sed -i "/\[Added Associations\]/a $association" "$MIMETYPES_FILE"
        fi
    done
}

# Cleanup function
cleanup() {
    print_info "Cleaning up temporary files..."
    # Add any cleanup tasks here
}

# Main installation function
main() {
    print_header
    
    # Set up error handling
    trap cleanup EXIT
    
    print_info "Starting Audion Music Player installation..."
    
    # Check environment
    check_root
    detect_distro
    
    # Install dependencies
    install_system_deps
    
    # Setup application
    setup_repo
    setup_python_env
    build_application
    
    # Create shortcuts and launchers
    create_desktop_entry
    create_launcher
    
    # Optional: setup file associations
    read -p "Set up file associations for audio files? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        setup_file_associations
    fi
    
    print_success "Installation completed successfully!"
    echo
    print_info "You can now:"
    print_info "• Launch Audion from your application menu"
    print_info "• Run 'audion' from terminal (after restarting terminal or sourcing ~/.bashrc)"
    print_info "• Double-click audio files to open with Audion (if file associations were set up)"
    echo
    print_info "Installation directory: $AUDION_DIR"
    print_success "Enjoy your music! 🎵"
}

# Run main function
main "$@"