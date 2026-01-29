#!/usr/bin/env python3
"""
Audion - A simple music player
"""

import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os
import random
from mutagen import File as MutagenFile

class Audion:
    def __init__(self, root):
        self.root = root
        self.root.title("Audion Music Player")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        
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
        self.song_length = 0
        self.current_position = 0
        self.seeking = False
        
        self.setup_ui()
        self.check_music_end()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎵 Audion", 
            font=("Arial", 20, "bold"),
            pady=10
        )
        title_label.pack()
        
        # Current file display
        self.file_frame = tk.Frame(self.root)
        self.file_frame.pack(pady=10)
        
        tk.Label(self.file_frame, text="Now Playing:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.file_label = tk.Label(
            self.file_frame, 
            text="No file loaded", 
            font=("Arial", 10, "italic"),
            fg="gray"
        )
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar and time display
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.time_elapsed_label = tk.Label(
            progress_frame,
            text="0:00",
            font=("Arial", 9)
        )
        self.time_elapsed_label.pack(side=tk.LEFT, padx=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_slider = tk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.progress_var,
            showvalue=False,
            length=400,
            command=self.on_progress_drag
        )
        self.progress_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_progress_release)
        
        self.time_remaining_label = tk.Label(
            progress_frame,
            text="0:00",
            font=("Arial", 9)
        )
        self.time_remaining_label.pack(side=tk.LEFT, padx=5)
        
        # Progress bar and time display
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Time labels
        time_frame = tk.Frame(progress_frame)
        time_frame.pack(fill=tk.X)
        
        self.current_time_label = tk.Label(
            time_frame,
            text="0:00",
            font=("Arial", 9),
            fg="gray"
        )
        self.current_time_label.pack(side=tk.LEFT)
        
        self.total_time_label = tk.Label(
            time_frame,
            text="0:00",
            font=("Arial", 9),
            fg="gray"
        )
        self.total_time_label.pack(side=tk.RIGHT)
        
        # Progress bar (slider)
        self.progress_slider = tk.Scale(
            progress_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            showvalue=False,
            length=400,
            sliderlength=20,
            command=self.on_progress_drag
        )
        self.progress_slider.pack(fill=tk.X, pady=5)
        self.progress_slider.bind("<ButtonPress-1>", self.on_progress_press)
        self.progress_slider.bind("<ButtonRelease-1>", self.on_progress_release)
        
        # File/Folder buttons
        file_button_frame = tk.Frame(self.root)
        file_button_frame.pack(pady=5)
        
        self.open_file_button = tk.Button(
            file_button_frame,
            text="📂 Open File",
            command=self.open_file,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.open_file_button.pack(side=tk.LEFT, padx=5)
        
        self.open_folder_button = tk.Button(
            file_button_frame,
            text="📁 Open Folder",
            command=self.open_folder,
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2"
        )
        self.open_folder_button.pack(side=tk.LEFT, padx=5)
        
        # Navigation control buttons
        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=15)
        
        self.prev_button = tk.Button(
            nav_frame,
            text="⏮ Previous",
            command=self.play_previous,
            font=("Arial", 11),
            bg="#9C27B0",
            fg="white",
            padx=12,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT, padx=3)
        
        self.play_button = tk.Button(
            nav_frame,
            text="▶ Play",
            command=self.play,
            font=("Arial", 11),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=3)
        
        self.pause_button = tk.Button(
            nav_frame,
            text="⏸ Pause",
            command=self.pause,
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            padx=12,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=3)
        
        self.stop_button = tk.Button(
            nav_frame,
            text="⏹ Stop",
            command=self.stop,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=3)
        
        self.next_button = tk.Button(
            nav_frame,
            text="⏭ Next",
            command=self.play_next,
            font=("Arial", 11),
            bg="#9C27B0",
            fg="white",
            padx=12,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.next_button.pack(side=tk.LEFT, padx=3)
        
        # Shuffle and Repeat buttons
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=5)
        
        self.shuffle_button = tk.Button(
            mode_frame,
            text="🔀 Shuffle: OFF",
            command=self.toggle_shuffle,
            font=("Arial", 9),
            bg="#607D8B",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.shuffle_button.pack(side=tk.LEFT, padx=5)
        
        self.repeat_button = tk.Button(
            mode_frame,
            text="🔁 Repeat: OFF",
            command=self.toggle_repeat,
            font=("Arial", 9),
            bg="#607D8B",
            fg="white",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.repeat_button.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=10)
        
        tk.Label(volume_frame, text="🔊 Volume:", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.volume_slider = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            command=self.set_volume,
            length=200,
            showvalue=True
        )
        self.volume_slider.set(50)
        self.volume_slider.pack(side=tk.LEFT, padx=10)
        
        # Playlist display
        playlist_label = tk.Label(
            self.root,
            text="Playlist:",
            font=("Arial", 10, "bold")
        )
        playlist_label.pack(pady=(10, 5))
        
        # Playlist frame with scrollbar
        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(playlist_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_box = tk.Listbox(
            playlist_frame,
            yscrollcommand=scrollbar.set,
            font=("Arial", 9),
            selectmode=tk.SINGLE,
            height=8
        )
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.playlist_box.bind('<Double-Button-1>', self.on_playlist_double_click)
        
        scrollbar.config(command=self.playlist_box.yview)
        
        # Status
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)
        
        tk.Label(status_frame, text="Status:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.status_label = tk.Label(
            status_frame,
            text="Stopped",
            font=("Arial", 10, "bold"),
            fg="gray"
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
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
    
    def on_progress_press(self, event):
        """Called when user clicks on the progress bar"""
        self.seeking = True
    
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
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
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
            self.playlist = [file_path]
            self.current_index = 0
            self.update_playlist_display()
            self.load_and_play(0)
    
    def open_folder(self):
        folder_path = filedialog.askdirectory(title="Select Music Folder")
        
        if folder_path:
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
                self.update_playlist_display()
                self.load_and_play(0)
                self.status_label.config(text=f"Loaded {len(audio_files)} tracks", fg="green")
            else:
                self.status_label.config(text="No audio files found", fg="red")
    
    def update_playlist_display(self):
        self.playlist_box.delete(0, tk.END)
        for i, file_path in enumerate(self.playlist):
            filename = os.path.basename(file_path)
            prefix = "▶ " if i == self.current_index else "   "
            self.playlist_box.insert(tk.END, f"{prefix}{filename}")
        
        if self.current_index >= 0:
            self.playlist_box.selection_clear(0, tk.END)
            self.playlist_box.selection_set(self.current_index)
            self.playlist_box.see(self.current_index)
    
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
                self.file_label.config(text=filename, fg="black")
                
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
                self.status_label.config(text=f"Playing ({index + 1}/{len(self.playlist)})", fg="green")
                
            except Exception as e:
                self.status_label.config(text=f"Error: {str(e)}", fg="red")
            
    def play(self):
        if self.current_file:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
            
            self.is_playing = True
            self.status_label.config(text=f"Playing ({self.current_index + 1}/{len(self.playlist)})", fg="green")
            
    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            self.status_label.config(text="Paused", fg="orange")
            
    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.status_label.config(text="Stopped", fg="gray")
    
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
                    self.status_label.config(text="End of playlist", fg="gray")
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
            self.shuffle_button.config(text="🔀 Shuffle: ON", bg="#00BCD4")
        else:
            self.shuffle_button.config(text="🔀 Shuffle: OFF", bg="#607D8B")
    
    def toggle_repeat(self):
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            self.repeat_button.config(text="🔁 Repeat: ON", bg="#00BCD4")
        else:
            self.repeat_button.config(text="🔁 Repeat: OFF", bg="#607D8B")
        
    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)
    
    def check_music_end(self):
        # Update progress bar and time if playing
        if self.is_playing and not self.seeking and self.song_length > 0:
            # Get current position (pygame.mixer.music.get_pos() returns milliseconds played)
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms >= 0:
                self.current_position += 0.1  # Approximate increment
                
                # Update progress slider
                if self.current_position <= self.song_length:
                    self.progress_var.set(self.current_position)
                    
                    # Update time labels
                    remaining = self.song_length - self.current_position
                    self.time_elapsed_label.config(text=self.format_time(self.current_position))
                    self.time_remaining_label.config(text=self.format_time(remaining))
        
        # Check if music has ended by checking if it's busy playing
        if self.is_playing and not pygame.mixer.music.get_busy():
            # Music ended, play next
            self.play_next()
        
        # Schedule next check
        self.root.after(100, self.check_music_end)
        

def main():
    root = tk.Tk()
    app = Audion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
