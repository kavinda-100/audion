#!/usr/bin/env python3
"""
Audion - A simple music player
"""

import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import os

class Audion:
    def __init__(self, root):
        self.root = root
        self.root.title("Audion Music Player")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Variables
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5
        
        self.setup_ui()
        
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
        
        tk.Label(self.file_frame, text="Current file:", font=("Arial", 10)).pack(side=tk.LEFT)
        self.file_label = tk.Label(
            self.file_frame, 
            text="No file loaded", 
            font=("Arial", 10, "italic"),
            fg="gray"
        )
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        # Open file button
        self.open_button = tk.Button(
            self.root,
            text="📂 Open Audio File",
            command=self.open_file,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.open_button.pack(pady=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=15)
        
        self.play_button = tk.Button(
            control_frame,
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
        self.play_button.pack(side=tk.LEFT, padx=5)
        
        self.pause_button = tk.Button(
            control_frame,
            text="⏸ Pause",
            command=self.pause,
            font=("Arial", 11),
            bg="#FF9800",
            fg="white",
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
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
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=15)
        
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
            self.load_file(file_path)
            
    def load_file(self, file_path):
        try:
            # Stop current playback
            pygame.mixer.music.stop()
            
            # Load new file
            pygame.mixer.music.load(file_path)
            self.current_file = file_path
            
            # Update UI
            filename = os.path.basename(file_path)
            self.file_label.config(text=filename, fg="black")
            
            # Enable buttons
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            
            # Auto-play
            self.play()
            
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
            self.status_label.config(text="Playing", fg="green")
            self.play_button.config(text="▶ Play")
            
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
        
    def set_volume(self, value):
        volume = float(value) / 100
        pygame.mixer.music.set_volume(volume)
        

def main():
    root = tk.Tk()
    app = Audion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
