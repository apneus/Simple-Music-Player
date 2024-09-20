import customtkinter as ctk
from tkinter import filedialog, Tk, Listbox
import pygame
import os

# Initialize Pygame Mixer for audio playback
pygame.mixer.init()

# Set the starting appearance mode for CustomTkinter
ctk.set_appearance_mode("dark")  # Set to 'dark' mode

class MusicPlayer:
    def __init__(self, root):
        self.current_song_length = 0
        # Initialize the music player application
        self.root = root
        # Set the window title
        self.root.title("CustomTkinter Music Player")  
        # Set the window size
        self.root.geometry("600x700")  
        # Set the window to fixed
        self.root.minsize(600, 700)
        self.root.maxsize(600, 700)

        # List to store the loaded songs
        self.songs_list = []
        # Index to keep track of the currently playing song
        self.current_song_index = 0
        # Boolean to check if a song is currently playing
        self.is_playing = False

        # Create the GUI components
        self.create_widgets()

        # Start checking for song end events
        self.check_for_song_end()

    def create_widgets(self):

        # CREATE AND ARRANGE THE WIDGETS FOR THE MUSIC PLAYER

        # Configure the grid system for proper layout management
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)

        # This row will expand and push everything upward
        self.root.grid_rowconfigure(6, weight=1)  

        # Song Listbox for displaying songs
        self.song_listbox = Listbox(
            self.root, 
            height=10, 
            width=60, 
            bg="#2B2B2B",  
            fg="white",  
            selectbackground="#1C1C1C",  
            selectforeground="white",  
            highlightbackground="#444444",  
            highlightcolor="#444444"  
        )
        # Center the listbox in the window
        self.song_listbox.grid(row=0, column=0, columnspan=4, pady=20, padx=10)  
        # Bind double-click event to the listbox to play song
        self.song_listbox.bind("<Double-Button-1>", self.on_double_click)

        # Load Songs Button (centered)
        self.load_button = ctk.CTkButton(
            self.root, 
            text="Load Songs", 
            command=self.load_songs
        )
        # Center the load button with columnspan
        self.load_button.grid(row=1, column=1, columnspan=2, pady=(10, 20), sticky="ew")

        # Create a frame to hold control buttons (Play, Pause, Stop)
        button_frame = ctk.CTkFrame(self.root)
        # Center the button frame in middle columns
        button_frame.grid(row=2, column=1, columnspan=2, pady=10, sticky="ew")

        # Configure columns in button frame for equal spacing
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        button_frame.grid_columnconfigure(3, weight=1)
        button_frame.grid_columnconfigure(4, weight=1)

        # Play Button
        self.play_button = ctk.CTkButton(
            button_frame, 
            text="Play", 
            command=self.play_song
        )
        # Place play button in button frame
        self.play_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Pause Button
        self.pause_button = ctk.CTkButton(
            button_frame, 
            text="Pause", 
            command=self.pause_song
        )
        # Place pause button in button frame
        self.pause_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Stop Button
        self.stop_button = ctk.CTkButton(
            button_frame, 
            text="Stop", 
            command=self.stop_song
        )
        # Place stop button in button frame
        self.stop_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Next Button
        self.next_button = ctk.CTkButton(
            self.root, 
            text="Next", 
            command=self.next_song
        )
        # Place next button to the left of the volume slider
        self.next_button.grid(row=3, column=3, padx=10, pady=10, sticky="w")

        # Previous Button
        self.previous_button = ctk.CTkButton(
            self.root, 
            text="Previous", 
            command=self.previous_song
        )
        # Place previous button to the right of the volume slider
        self.previous_button.grid(row=3, column=0, padx=10, pady=10, sticky="e")

        # Volume Control Slider (centered with Listbox)
        self.volume_slider = ctk.CTkSlider(
            self.root, 
            from_=0, 
            to=1, 
            command=self.set_volume
        )
        # Center the volume slider with columnspan and sticky
        self.volume_slider.grid(row=6, column=1, columnspan=2, pady=20, sticky="ew")
        # Set the initial volume level to 10%
        self.volume_slider.set(0.1)

        # Set the initial volume in pygame mixer to match the slider
        pygame.mixer.music.set_volume(0.1)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.root, width=350)
        self.progress_bar.grid(row=3, column=0, columnspan=4, pady=10)  
        # Initialize progress to 0    
        self.progress_bar.set(0)  

        # Label to display the current time of the song
        self.current_time_label = ctk.CTkLabel(
        self.root,
        text="00:00",  # Initialize with 0:00
        text_color="white"
        )
        # Position the timer label below the progress bar
        self.current_time_label.grid(row=5, column=0, columnspan=4, pady=(10, 0), sticky="n")

        # Label to display the current song or status
        self.current_song_label = ctk.CTkLabel(
            self.root, 
            text="No song loaded", 
            text_color="white"
        )
        # Position label below the volume slider
        self.current_song_label.grid(row=4, column=0, columnspan=4, pady=10)

        # Add a theme selection dropdown menu at the bottom of the interface window
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.root,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
            width=100
        )
        # Set the initial appearance mode to "Dark"
        self.appearance_mode_menu.set("Dark")
        # Place the dropdown menu at the bottom
        self.appearance_mode_menu.grid(row=8, column=1, columnspan=2, pady=20, padx=10, sticky="s")

        # Add a label for the theme dropdown
        self.theme_label = ctk.CTkLabel(
        self.root,
        text="Select Theme",  # The title of the label
        text_color="white"
        )
        # Position the label above the dropdown (row=7)
        self.theme_label.grid(row=7, column=1, columnspan=2, padx=10, pady=0, sticky="ew")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # Change the appearance mode (theme)
        ctk.set_appearance_mode(new_appearance_mode)

    def check_for_song_end(self):
        # Check if the song has ended and trigger the next song
        if not pygame.mixer.music.get_busy() and self.is_playing:
            self.next_song()
        else:
            # Update progress bar if song is playing
            self.update_progress_bar()  
        self.root.after(100, self.check_for_song_end)

    def load_songs(self):

        # LOAD SONGS FROM A SELECTED DIRECTORY

        # Clear the current song list and listbox
        self.songs_list.clear()  
        self.song_listbox.delete(0, 'end')  

        # Open a directory selection dialog
        directory = filedialog.askdirectory()
        if directory:
            # Change current directory to the selected one
            os.chdir(directory)
            # Iterate over files in the directory
            for file in os.listdir(directory):
                # Only add .mp3 files
                if file.endswith(".mp3"):
                    # Add file to the internal song list
                    self.songs_list.append(file)  
                    # Add file to the listbox UI
                    self.song_listbox.insert("end", file)  
            # Update the song label based on loaded songs
            if self.songs_list:
                self.current_song_label.configure(text=f"Loaded {len(self.songs_list)} songs.")
            else:
                self.current_song_label.configure(text="No songs found.")

    def play_song(self):
        # Play the selected song
        if self.songs_list:
            # Get the song at the current index
            song = self.songs_list[self.current_song_index]
            pygame.mixer.music.load(song)  # Load the song
            pygame.mixer.music.play()  # Play the song

            self.current_song_length = pygame.mixer.Sound(song).get_length()

            # Update the playing status
            self.is_playing = True  
            # Update the label
            self.current_song_label.configure(text=f"Playing: {song}")  

            # Update the Listbox selection to highlight the playing song
            self.song_listbox.selection_clear(0, 'end')  # Clear previous selection
            self.song_listbox.selection_set(self.current_song_index)  # Select current song
            self.song_listbox.activate(self.current_song_index)  # Make sure the song is visible

            # Start the timer update loop
            self.update_timer() 

    def pause_song(self):
        # Pause or unpause the song
        if self.is_playing:
            # If music is playing, pause it
            pygame.mixer.music.pause()
            self.is_playing = False
        else:
            # If music is paused, unpause it
            pygame.mixer.music.unpause()
            self.is_playing = True
    
    def stop_song(self):
        # Stop the currently playing song
        pygame.mixer.music.stop()  # Stop the song
        self.is_playing = False  # Update the playing status
        self.progress_bar.set(0)  # Reset progress bar

    def next_song(self):
        # Play the next song in the list
        if self.songs_list:
            # Increment the current song index with wrap-around
            self.current_song_index = (self.current_song_index + 1) % len(self.songs_list)
            # Play the next song
            self.play_song()  

    def previous_song(self):
        # Play the previous song in the list
        if self.songs_list:
            # Decrement the current song index with wrap-around
            self.current_song_index = (self.current_song_index - 1) % len(self.songs_list)
            # Play the previous song
            self.play_song()  

    def select_song(self, event):
        # Select a song from the list
        if self.song_listbox.curselection():
            # Update the current song index to the selected one
            self.current_song_index = self.song_listbox.curselection()[0]
            self.play_song()  # Play the selected song

    def on_double_click(self, event):
        # Play song on double-click in the listbox
        if self.song_listbox.curselection():
            # Update the current song index to the double-clicked song
            self.current_song_index = self.song_listbox.curselection()[0]
            # Play the selected song
            self.play_song()  

    def set_volume(self, volume):
        # Set the volume of the music
        pygame.mixer.music.set_volume(float(volume))  # Adjust the volume based on slider

    def update_progress_bar(self):
        # Update the progress bar based on the current position of the song
        if pygame.mixer.music.get_busy():
            # Current position in seconds
            current_pos = pygame.mixer.music.get_pos() / 1000  
            progress = current_pos / self.current_song_length if self.current_song_length > 0 else 0
            # Update the progress bar value
            self.progress_bar.set(progress)  

    def update_timer(self):
    # Update the timer label with the current playback time
        if self.is_playing or pygame.mixer.music.get_busy():  # Check if music is playing or paused
            # Get the current playback position in milliseconds
            current_pos_ms = pygame.mixer.music.get_pos()
            current_pos_sec = int(current_pos_ms / 1000)  # Convert to seconds
        
            # Format minutes and seconds (MM:SS)
            minutes = current_pos_sec // 60
            seconds = current_pos_sec % 60
            time_formatted = f"{minutes:02}:{seconds:02}"

            # Update the timer label with the formatted time
            self.current_time_label.configure(text=time_formatted)
    
        # Schedule the next update in 1 second (1000 milliseconds)
        self.root.after(1000, self.update_timer)

# Create the main application window
root = ctk.CTk()
app = MusicPlayer(root)
root.mainloop()