#!/usr/bin/env python3
"""
Audion - A simple music player
"""

import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
import random
import json
from mutagen import File as MutagenFile

class Audion:
    def __init__(self, root):
        self.root = root
        self.root.title("Audion Music Player")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # Set minimum window size
        self.root.minsize(700, 550)
        
        # Configure modern styling
        self.setup_modern_theme()
        
        # Initialize pygame mixer only (not the full pygame which includes video)
        pygame.mixer.init()
        
        # Variables
        self.playlist = []
        self.current_index = -1
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5
        self.shuffle_mode = False
        self.repeat_mode = False
        self.song_length = 0
        self.current_position = 0
        self.seeking = False
        
        # Config file for settings
        self.config_file = os.path.expanduser("~/.audion_config.json")
        self.playlist_file = os.path.expanduser("~/.audion_playlist.json")
        self.last_directory = self.load_last_directory()
        
        self.setup_ui()
        self.load_saved_playlist()
        self.check_music_end()
        
    def setup_modern_theme(self):
        """Configure modern, sleek UI theme"""
        # Modern neutral color palette (inspired by macOS/Windows 11)
        self.colors = {
            'bg_primary': '#f6f6f6',      # Light gray background
            'bg_secondary': '#ffffff',    # White cards
            'bg_tertiary': '#e8e8e8',     # Light tertiary background
            'accent': '#007aff',          # iOS blue accent
            'accent_hover': '#0051d5',    # Darker blue for hover
            'success': '#30d158',         # Green for success
            'warning': '#ff9500',         # Orange for warning
            'error': '#ff3b30',          # Red for error
            'text_primary': '#1d1d1f',    # Dark text
            'text_secondary': '#86868b',  # Gray text
            'text_tertiary': '#c7c7cc',   # Light gray text
            'border': '#d1d1d6',          # Subtle border
            'shadow': '#00000010'         # Subtle shadow
        }
        
        # Set light neutral background for main window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure ttk style
        self.style = ttk.Style()
        
        # Configure modern button styles
        self.style.configure('Modern.TButton',
                           background=self.colors['accent'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           padding=(16, 10),
                           font=('SF Pro Display', 11, 'bold'))
        
        self.style.map('Modern.TButton',
                     background=[('active', self.colors['accent_hover']),
                               ('pressed', self.colors['accent_hover'])],
                     relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Configure secondary button style with subtle styling
        self.style.configure('Secondary.TButton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           bordercolor=self.colors['border'],
                           focuscolor='none',
                           padding=(12, 8),
                           font=('SF Pro Display', 10))
        
        self.style.map('Secondary.TButton',
                     background=[('active', self.colors['bg_tertiary']),
                               ('pressed', self.colors['bg_tertiary'])],
                     relief=[('pressed', 'flat'), ('!pressed', 'flat')])
        
        # Configure modern frame styles with subtle shadows
        self.style.configure('Modern.TFrame',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Card.TFrame',
                           background=self.colors['bg_secondary'],
                           borderwidth=1,
                           bordercolor=self.colors['border'],
                           relief='flat')
        
        # Configure modern scale/slider style
        self.style.configure('Modern.Horizontal.TScale',
                           background=self.colors['bg_secondary'],
                           troughcolor=self.colors['bg_tertiary'],
                           borderwidth=0,
                           sliderthickness=18,
                           gripcount=0)
        
        self.style.map('Modern.Horizontal.TScale',
                     background=[('active', self.colors['accent'])],
                     troughcolor=[('active', self.colors['bg_tertiary'])])
        
        # Configure listbox-like styles
        self.style.configure('Modern.Treeview',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           fieldbackground=self.colors['bg_secondary'],
                           borderwidth=1,
                           relief='flat')
        
        self.style.configure('Modern.Treeview.Heading',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0)
        
    def setup_ui(self):
        # Main container with padding
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title with modern typography
        title_frame = ttk.Frame(main_container, style='Modern.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="🎵 Audion", 
            font=("SF Pro Display", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Modern Music Player",
            font=("SF Pro Display", 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()
        
        # Current file display with card-style design
        current_file_card = ttk.Frame(main_container, style='Card.TFrame', padding=15)
        current_file_card.pack(fill=tk.X, pady=(0, 20))
        
        file_info_frame = ttk.Frame(current_file_card, style='Card.TFrame')
        file_info_frame.pack(fill=tk.X)
        
        now_playing_label = tk.Label(
            file_info_frame, 
            text="NOW PLAYING", 
            font=("SF Pro Display", 9, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        now_playing_label.pack(anchor=tk.W)
        
        self.file_label = tk.Label(
            file_info_frame, 
            text="No track selected", 
            font=("SF Pro Display", 14, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            wraplength=600
        )
        self.file_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Progress bar and time display with modern design
        progress_card = ttk.Frame(main_container, style='Card.TFrame', padding=15)
        progress_card.pack(fill=tk.X, pady=(0, 20))
        
        # Time labels with modern styling
        time_frame = ttk.Frame(progress_card, style='Card.TFrame')
        time_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.time_elapsed_label = tk.Label(
            time_frame,
            text="0:00",
            font=("SF Pro Display", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.time_elapsed_label.pack(side=tk.LEFT)
        
        self.time_remaining_label = tk.Label(
            time_frame,
            text="0:00",
            font=("SF Pro Display", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.time_remaining_label.pack(side=tk.RIGHT)
        
        # Modern progress slider
        self.progress_var = tk.DoubleVar()
        self.progress_slider = ttk.Scale(
            progress_card,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.progress_var,
            style='Modern.Horizontal.TScale',
            command=self.on_progress_drag
        )
        self.progress_slider.pack(fill=tk.X, pady=(0, 5))
        self.progress_slider.bind("<ButtonRelease-1>", self.on_progress_release)
        
        # File/Folder buttons with modern styling
        file_button_frame = ttk.Frame(main_container, style='Modern.TFrame')
        file_button_frame.pack(fill=tk.X, pady=(0, 20))
        
        buttons_container = ttk.Frame(file_button_frame, style='Modern.TFrame')
        buttons_container.pack()
        
        self.open_file_button = ttk.Button(
            buttons_container,
            text="📂 Open File",
            command=self.open_file,
            style='Modern.TButton'
        )
        self.open_file_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_folder_button = ttk.Button(
            buttons_container,
            text="📁 Open Folder",
            command=self.open_folder,
            style='Modern.TButton'
        )
        self.open_folder_button.pack(side=tk.LEFT)
        
        # Navigation control buttons with modern design
        nav_card = ttk.Frame(main_container, style='Card.TFrame', padding=20)
        nav_card.pack(fill=tk.X, pady=(0, 20))
        
        nav_container = ttk.Frame(nav_card, style='Card.TFrame')
        nav_container.pack()
        
        # Control buttons with modern styling
        self.prev_button = ttk.Button(
            nav_container,
            text="⏮ Previous",
            command=self.play_previous,
            style='Secondary.TButton',
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.play_button = ttk.Button(
            nav_container,
            text="▶ Play",
            command=self.play,
            style='Modern.TButton',
            state=tk.DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = ttk.Button(
            nav_container,
            text="⏸ Pause",
            command=self.pause,
            style='Secondary.TButton',
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            nav_container,
            text="⏹ Stop",
            command=self.stop,
            style='Secondary.TButton',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = ttk.Button(
            nav_container,
            text="⏭ Next",
            command=self.play_next,
            style='Secondary.TButton',
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Mode controls (Shuffle and Repeat) with modern styling
        mode_frame = ttk.Frame(nav_card, style='Card.TFrame')
        mode_frame.pack(pady=(15, 0))
        
        self.shuffle_button = ttk.Button(
            mode_frame,
            text="🔀 Shuffle: OFF",
            command=self.toggle_shuffle,
            style='Secondary.TButton'
        )
        self.shuffle_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.repeat_button = ttk.Button(
            mode_frame,
            text="🔁 Repeat: OFF",
            command=self.toggle_repeat,
            style='Secondary.TButton'
        )
        self.repeat_button.pack(side=tk.LEFT)
        
        # Volume control with modern design
        volume_card = ttk.Frame(main_container, style='Card.TFrame', padding=15)
        volume_card.pack(fill=tk.X, pady=(0, 20))
        
        volume_label = tk.Label(
            volume_card, 
            text="🔊 Volume", 
            font=("SF Pro Display", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        volume_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.volume_slider = ttk.Scale(
            volume_card,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            style='Modern.Horizontal.TScale',
            command=self.set_volume
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(fill=tk.X)
        
        # Modern Playlist display - moved below buttons for better visibility
        playlist_card = ttk.Frame(main_container, style='Card.TFrame', padding=20)
        playlist_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Playlist header with clear title
        playlist_header_frame = tk.Frame(playlist_card, bg=self.colors['bg_secondary'])
        playlist_header_frame.pack(fill=tk.X, pady=(0, 15))
        
        playlist_header = tk.Label(
            playlist_header_frame,
            text="🎶 Music Library",
            font=("SF Pro Display", 16, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        playlist_header.pack(anchor=tk.W)
        
        # Playlist container with distinct background
        playlist_container = tk.Frame(
            playlist_card, 
            bg=self.colors['bg_tertiary'],
            relief='flat',
            bd=2
        )
        playlist_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create listbox with contrasting background for visibility
        self.playlist_box = tk.Listbox(
            playlist_container,
            font=("SF Pro Display", 12),
            selectmode=tk.SINGLE,
            height=12,
            bg=self.colors['bg_tertiary'],      # Light gray background
            fg=self.colors['text_primary'],      # Dark text
            selectbackground=self.colors['accent'], # Blue selection
            selectforeground='white',
            borderwidth=0,
            relief='flat',
            highlightthickness=1,
            highlightcolor=self.colors['border'],
            highlightbackground=self.colors['border'],
            activestyle='dotbox'
        )
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.playlist_box.bind('<Double-Button-1>', self.on_playlist_double_click)
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(playlist_container, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 8), pady=8)
        scrollbar.config(command=self.playlist_box.yview)
        self.playlist_box.config(yscrollcommand=scrollbar.set)
        
        # Modern status bar
        status_card = ttk.Frame(main_container, style='Card.TFrame', padding=10)
        status_card.pack(fill=tk.X)
        
        status_frame = ttk.Frame(status_card, style='Card.TFrame')
        status_frame.pack()
        
        status_icon = tk.Label(
            status_frame, 
            text="●", 
            font=("SF Pro Display", 14),
            bg=self.colors['bg_secondary'],
            fg=self.colors['success']
        )
        status_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=("SF Pro Display", 11),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        self.status_label.pack(side=tk.LEFT)
        
    def get_song_length(self, file_path):
        """Get the length of the audio file in seconds"""
        try:
            audio = MutagenFile(file_path)
            if audio and audio.info:
                return audio.info.length
        except:
            pass
        return 0
    
    def format_time(self, seconds):
        """Format seconds to MM:SS"""
        if seconds < 0:
            seconds = 0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def on_progress_release(self, event):
        """Called when user releases the progress bar - seek to that position"""
        if self.current_file and self.song_length > 0:
            seek_time = self.progress_var.get()
            
            try:
                # Restart the song from the desired position
                pygame.mixer.music.play(start=seek_time)
                self.current_position = seek_time
                
                # If we were paused, pause again after seeking
                if self.is_paused:
                    pygame.mixer.music.pause()
                elif not self.is_playing:
                    pygame.mixer.music.pause()
            except Exception as e:
                # Some formats don't support seeking well
                print(f"Seek error: {e}")
        
        self.seeking = False
    
    def on_progress_drag(self, value):
        """Update time label while dragging"""
        if self.song_length > 0:
            current_time = float(value)
            remaining_time = self.song_length - current_time
            self.time_elapsed_label.config(text=self.format_time(current_time))
            self.time_remaining_label.config(text=self.format_time(remaining_time))
            self.seeking = True
    
    def update_progress(self):
        """Update the progress bar and time labels"""
        if self.is_playing and not self.seeking and self.song_length > 0:
            # Get current position
            pos = pygame.mixer.music.get_pos() / 1000.0  # Convert ms to seconds
            
            # pygame.mixer.music.get_pos() returns time since start of current play
            # We need to track the actual position
            if pos >= 0:
                self.current_position = pos
                
                # Update progress bar
                progress_percent = (self.current_position / self.song_length) * 100
                if progress_percent <= 100:
                    self.progress_slider.set(progress_percent)
                
                # Update time labels
                self.current_time_label.config(text=self.format_time(self.current_position))
                remaining = self.song_length - self.current_position
                self.total_time_label.config(text=self.format_time(self.song_length))
    
    def open_file(self):
        initial_dir = self.last_directory if self.last_directory and os.path.exists(self.last_directory) else os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            initialdir=initial_dir,
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg *.flac"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("OGG Files", "*.ogg"),
                ("FLAC Files", "*.flac"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            # Save the directory for next time
            self.last_directory = os.path.dirname(file_path)
            self.save_last_directory()
            
            self.playlist = [file_path]
            self.current_index = 0
            self.update_playlist_display()
            self.load_and_play(0)
    
    def open_folder(self):
        initial_dir = self.last_directory if self.last_directory and os.path.exists(self.last_directory) else os.path.expanduser("~")
        
        folder_path = filedialog.askdirectory(title="Select Music Folder", initialdir=initial_dir)
        
        if folder_path:
            # Save the directory for next time
            self.last_directory = folder_path
            self.save_last_directory()
            
            # Get all audio files from the folder
            audio_extensions = ('.mp3', '.wav', '.ogg', '.flac')
            audio_files = []
            
            for file in os.listdir(folder_path):
                if file.lower().endswith(audio_extensions):
                    audio_files.append(os.path.join(folder_path, file))
            
            if audio_files:
                audio_files.sort()  # Sort alphabetically
                self.playlist = audio_files
                self.current_index = 0
                self.save_playlist()
                self.update_playlist_display()
                # Force refresh the listbox display
                self.root.update_idletasks()
                self.load_and_play(0)
                self.status_label.config(text=f"Loaded {len(audio_files)} tracks", fg=self.colors['success'])
            else:
                self.status_label.config(text="No audio files found", fg=self.colors['error'])
    
    def update_playlist_display(self):
        # Clear and repopulate the listbox
        self.playlist_box.delete(0, tk.END)
        
        if not self.playlist:
            return
            
        for i, file_path in enumerate(self.playlist):
            filename = os.path.basename(file_path)
            prefix = "▶ " if i == self.current_index else "   "
            self.playlist_box.insert(tk.END, f"{prefix}{filename}")
        
        # Update selection and scroll to current song
        if self.current_index >= 0 and self.current_index < len(self.playlist):
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
            self.playlist_box.see(self.current_index)
            
        # Force GUI update
        self.playlist_box.update_idletasks()
        self.root.update_idletasks()
    
    def on_playlist_double_click(self, event):
        selection = self.playlist_box.curselection()
        if selection:
            index = selection[0]
            self.load_and_play(index)
            
    def load_and_play(self, index):
        if 0 <= index < len(self.playlist):
            file_path = self.playlist[index]
            try:
                # Stop current playback
                pygame.mixer.music.stop()
                
                # Get song length
                self.song_length = self.get_song_length(file_path)
                self.current_position = 0
                
                # Update progress bar and time
                self.progress_slider.config(to=self.song_length if self.song_length > 0 else 100)
                self.progress_var.set(0)
                self.time_elapsed_label.config(text="0:00")
                self.time_remaining_label.config(text=self.format_time(self.song_length))
                
                # Load new file
                pygame.mixer.music.load(file_path)
                self.current_file = file_path
                self.current_index = index
                
                # Update UI
                filename = os.path.basename(file_path)
                self.file_label.config(text=filename, fg=self.colors['text_primary'])
                
                # Enable buttons
                self.play_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                self.prev_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL)
                
                # Update playlist display
                self.update_playlist_display()
                
                # Auto-play
                pygame.mixer.music.play()
                self.is_playing = True
                self.is_paused = False
                self.status_label.config(text=f"Playing ({index + 1}/{len(self.playlist)})", fg=self.colors['success'])
                
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}", fg=self.colors['error'])
    
    def load_song(self, index):
        """Load a song but don't play it automatically (for restoring saved state)"""
        if 0 <= index < len(self.playlist):
            file_path = self.playlist[index]
            try:
                # Stop current playback
                pygame.mixer.music.stop()
                
                # Get song length
                self.song_length = self.get_song_length(file_path)
                self.current_position = 0
                
                # Update progress bar and time
                self.progress_slider.config(to=self.song_length if self.song_length > 0 else 100)
                self.progress_var.set(0)
                self.time_elapsed_label.config(text="0:00")
                self.time_remaining_label.config(text=self.format_time(self.song_length))
                
                # Load new file
                pygame.mixer.music.load(file_path)
                self.current_file = file_path
                self.current_index = index
                
                # Update UI
                filename = os.path.basename(file_path)
                self.file_label.config(text=filename, fg=self.colors['text_primary'])
                
                # Enable buttons
                self.play_button.config(state=tk.NORMAL)
                self.pause_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                self.prev_button.config(state=tk.NORMAL)
                self.next_button.config(state=tk.NORMAL)
                
                # Update playlist display
                self.update_playlist_display()
                
                # Don't auto-play, just set status as ready
                self.is_playing = False
                self.is_paused = False
                self.status_label.config(text=f"Ready to play ({index + 1}/{len(self.playlist)})", fg=self.colors['accent'])
                
            except Exception as e:
                self.status_label.config(text=f"Error loading song: {str(e)}", fg=self.colors['error'])
            
    def play(self):
        if self.current_file:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
            
            self.is_playing = True
            self.status_label.config(text=f"Playing ({self.current_index + 1}/{len(self.playlist)})", fg=self.colors['success'])
            
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            self.status_label.config(text="Paused", fg=self.colors['warning'])
            
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.status_label.config(text="Stopped", fg=self.colors['text_secondary'])
    
    def play_next(self):
        if not self.playlist:
            return
        
        if self.shuffle_mode:
            # Pick a random track (but not the current one if possible)
            if len(self.playlist) > 1:
                next_index = random.choice([i for i in range(len(self.playlist)) if i != self.current_index])
            else:
                next_index = 0
        else:
            next_index = self.current_index + 1
            if next_index >= len(self.playlist):
                if self.repeat_mode:
                    next_index = 0
                else:
                    self.stop()
                    self.status_label.config(text="End of playlist", fg=self.colors['text_secondary'])
                    return
        
        self.load_and_play(next_index)
    
    def play_previous(self):
        if not self.playlist:
            return
        
        prev_index = self.current_index - 1
        if prev_index < 0:
            if self.repeat_mode:
                prev_index = len(self.playlist) - 1
            else:
                prev_index = 0
        
        self.load_and_play(prev_index)
    
    def toggle_shuffle(self):
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            self.shuffle_button.config(text="🔀 Shuffle: ON")
            # Create active style for shuffle
            self.style.configure('Shuffle.Active.TButton',
                               background=self.colors['success'],
                               foreground=self.colors['text_primary'])
            self.shuffle_button.config(style='Shuffle.Active.TButton')
        else:
            self.shuffle_button.config(text="🔀 Shuffle: OFF", style='Secondary.TButton')
    
    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            self.repeat_button.config(text="🔁 Repeat: ON")
            # Create active style for repeat
            self.style.configure('Repeat.Active.TButton',
                               background=self.colors['success'],
                               foreground=self.colors['text_primary'])
            self.repeat_button.config(style='Repeat.Active.TButton')
        else:
            self.repeat_button.config(text="🔁 Repeat: OFF", style='Secondary.TButton')
        
    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)
    
    def check_music_end(self):
        # Update progress bar and time if playing
        if self.is_playing and not self.seeking and self.song_length > 0:
            # Get current position in milliseconds since the song started
            pos_ms = pygame.mixer.music.get_pos()
            
            # get_pos() returns time since music.play() was called
            # Convert to seconds and add to our tracked position from seeks
            if pos_ms >= 0:
                current_time = self.current_position + (pos_ms / 1000.0)
                
                # Make sure we don't exceed song length
                if current_time <= self.song_length:
                    self.progress_var.set(current_time)
                    
                    # Update time labels
                    remaining = max(0, self.song_length - current_time)
                    self.time_elapsed_label.config(text=self.format_time(current_time))
                    self.time_remaining_label.config(text=self.format_time(remaining))
        
        # Check if music has ended by checking if it's busy playing
        if self.is_playing and not pygame.mixer.music.get_busy():
            # Music ended, play next
            self.play_next()
        
        # Schedule next check
        self.root.after(100, self.check_music_end)
        
    def load_last_directory(self):
        """Load the last opened directory from config file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('last_directory', None)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return None
    
    def save_last_directory(self):
        """Save the last opened directory to config file"""
        try:
            config = {}
            if os.path.exists(self.config_file):
                try:
                    with open(self.config_file, 'r') as f:
                        config = json.load(f)
                except json.JSONDecodeError:
                    config = {}
            
            config['last_directory'] = self.last_directory
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")
    
    def save_playlist(self):
        """Save current playlist to file"""
        try:
            playlist_data = {
                'playlist': self.playlist,
                'current_index': self.current_index,
                'last_saved': os.path.getctime(self.playlist[0]) if self.playlist else 0
            }
            
            with open(self.playlist_file, 'w') as f:
                json.dump(playlist_data, f, indent=2)
        except Exception as e:
            print(f"Could not save playlist: {e}")
    
    def load_saved_playlist(self):
        """Load saved playlist and remove deleted files"""
        try:
            if not os.path.exists(self.playlist_file):
                return
                
            with open(self.playlist_file, 'r') as f:
                playlist_data = json.load(f)
            
            saved_playlist = playlist_data.get('playlist', [])
            if not saved_playlist:
                return
            
            # Filter out deleted files
            existing_files = []
            for file_path in saved_playlist:
                if os.path.exists(file_path):
                    existing_files.append(file_path)
            
            if existing_files:
                self.playlist = existing_files
                self.current_index = min(playlist_data.get('current_index', 0), len(existing_files) - 1)
                self.update_playlist_display()
                
                # Load the current song so buttons are enabled
                self.load_song(self.current_index)
                
                # Update status
                removed_count = len(saved_playlist) - len(existing_files)
                if removed_count > 0:
                    self.status_label.config(
                        text=f"Loaded {len(existing_files)} tracks ({removed_count} deleted files removed)",
                        fg=self.colors['warning']
                    )
                else:
                    self.status_label.config(
                        text=f"Loaded {len(existing_files)} saved tracks",
                        fg=self.colors['success']
                    )
                
                # Save updated playlist (without deleted files)
                self.save_playlist()
            
        except (json.JSONDecodeError, FileNotFoundError, Exception) as e:
            print(f"Could not load saved playlist: {e}")


def main():
    root = tk.Tk()
    app = Audion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
