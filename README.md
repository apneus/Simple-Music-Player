DISCLAIMER: The description below explains my process while working through and improving 
the code best I can as a beginner. Clearly, experienced programmers will know this from a 
quick glance at the code, but for beginners, I hope this, along with the many comments in 
the code helps in some way.

This document is an overview and explanation of each section of the code. I have tried my 
best to include how it works and key features but please bear in mind I'm a beginner.

Very simple GUI Python music player,mostly to prove to myself I could do it. If this helps 
anyone else learning Python, job done. 

# TKINTER MUSIC PLAYER 4.0 

## 1. Importing Libraries and Initialization

```
import customtkinter as ctk
from tkinter import filedialog, Tk, Listbox
import pygame
import os

# Initialize Pygame Mixer for audio playback
pygame.mixer.init()

# Set the appearance mode for CustomTkinter
ctk.set_appearance_mode("dark")  # Set to 'dark' mode
```

### How it works: 

This section imports necessary libraries and initializes settings for the music player. 
The customtkinter library is used to create a modern-looking GUI, while pygame is used for audio playback. 
The filedialog module from tkinter helps in opening a dialog for selecting files.

### Key features:

Pygame Mixer Initialization prepares the pygame library to handle audio playback.
CustomTkinter Appearance Mode sets the theme of the GUI to 'dark' mode, providing a modern look and feel.


## 2. Music Player Class Definition

```
class MusicPlayer:
    def __init__(self, root):
        # Initialize the music player application
        self.root = root
        self.root.title("CustomTkinter Music Player")  # Set the window title
        self.root.geometry("600x450")  # Set the window size

        # List to store the loaded songs
        self.songs_list = []
        # Index to keep track of the currently playing song
        self.current_song_index = 0
        # Boolean to check if a song is currently playing
        self.is_playing = False

        # Create the GUI components
        self.create_widgets()
```

### How it works: 

This is the constructor method of the MusicPlayer class, which initializes the main window and various 
attributes needed for the music player, such as the song list, current song index, and playing status.

### Key features:

Window Initialization sets up the title and size of the application window.
Attribute Initialization prepares necessary attributes like songs_list, current_song_index, and is_playing 
for tracking and managing song playback.

## 3. Creating GUI Widgets

```
def create_widgets(self):
    # Create and arrange the widgets for the music player
    ...
    # Song Listbox for displaying songs
    self.song_listbox = Listbox(
        self.root, 
        height=10, 
        width=60, 
        bg="#2B2B2B",  # Dark background for the listbox
        fg="white",  # White text color
        ...
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
    self.load_button.grid(row=1, column=1, columnspan=2, pady=(10, 20), sticky="ew")
    ...
```

### How it works: 

This method creates and arranges all the GUI components, including the song listbox, buttons (Load, Play, Pause, Stop, Next, Previous), 
volume slider, and labels.

### Key features:

- Listbox for Song Display allows users to see the list of songs and select them by double-clicking.
- Buttons for Control: Includes buttons for loading songs, playing, pausing, stopping, and navigating through songs.
- Volume Control Slider: A slider to adjust the playback volume.
- Layout Management: Uses grid-based layout to properly arrange components.

## 4. Loading Songs

```
def load_songs(self):
    # Load songs from a selected directory
    self.songs_list.clear()  # Clear the internal song list
    self.song_listbox.delete(0, 'end')  # Clear the listbox UI

    # Open a directory selection dialog
    directory = filedialog.askdirectory()
    if directory:
        # Change current directory to the selected one
        os.chdir(directory)
        ...
        for file in os.listdir(directory):
            # Only add .mp3 files
            if file.endswith(".mp3"):
                self.songs_list.append(file)  # Add file to the internal song list
                self.song_listbox.insert("end", file)  # Add file to the listbox UI
        ...
```

### How it works: 

This method opens a directory selection dialog, allowing the user to select a folder. It then loads all .mp3 files 
from the selected directory into the listbox and internal song list.

### Key features:

Directory Selection Dialog uses filedialog.askdirectory() to prompt the user to select a directory.
MP3 Filtering: Only .mp3 files are added to the list to ensure compatibility with the player.

## 5. Playing a Song

```
def play_song(self):
    # Play the selected song
    if self.songs_list:
        # Get the song at the current index
        song = self.songs_list[self.current_song_index]
        pygame.mixer.music.load(song)  # Load the song
        pygame.mixer.music.play()  # Play the song
        self.is_playing = True  # Update the playing status
        self.current_song_label.configure(text=f"Playing: {song}")  # Update the label
        ...
```

### How it works: 

This method plays the currently selected song from the songs_list using the pygame mixer. 
It updates the label to show the current song playing.

### Key features:

Audio Playback: Uses pygame.mixer.music.load() and pygame.mixer.music.play() for loading and playing the song.
Playback Status Update: Updates the playback status and the GUI label to reflect the current song.

## 6. Pausing and Stopping Songs

```
def pause_song(self):
    # Pause or unpause the song
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        self.is_playing = False
    else:
        pygame.mixer.music.unpause()
        self.is_playing = True

def stop_song(self):
    # Stop the currently playing song
    pygame.mixer.music.stop()  # Stop the song
    self.is_playing = False  # Update the playing status
```

### How it works: 

These methods manage song playback by pausing/unpausing or stopping the current song using the pygame mixer.

### Key features:

Toggle Pause/Unpause: Uses pygame.mixer.music.pause() and pygame.mixer.music.unpause() for pausing and resuming songs.
Stop Playback: Uses pygame.mixer.music.stop() to stop the song.

## 7. Navigating Songs

```
def next_song(self):
    # Play the next song in the list
    if self.songs_list:
        self.current_song_index = (self.current_song_index + 1) % len(self.songs_list)
        self.play_song()

def previous_song(self):
    # Play the previous song in the list
    if self.songs_list:
        self.current_song_index = (self.current_song_index - 1) % len(self.songs_list)
        self.play_song()
```

### How it works: 

These methods handle navigating to the next or previous song in the songs_list. 
They update the current_song_index and then call play_song().

### Key features:

Circular Navigation: Uses modulo operations to loop back to the start or end of the list when navigating through songs.

## 8. Selecting and Setting Volume

```
def select_song(self, event):
    # Select a song from the list
    if self.song_listbox.curselection():
        self.current_song_index = self.song_listbox.curselection()[0]
        self.play_song()

def set_volume(self, volume):
    # Set the volume of the music
    pygame.mixer.music.set_volume(float(volume))  # Adjust the volume based on slider
```

### How it works: 

The select_song method updates the song to play based on the user's selection in the listbox. 
The set_volume method adjusts the playback volume based on the slider value.

### Key features:

Dynamic Volume Control: The volume slider allows the user to adjust the playback volume in real-time.
Interactive Song Selection: Users can click on a song in the listbox to select it for playback.

## 9. Main Application Loop

```
# Create the main application window
root = ctk.CTk()
app = MusicPlayer(root)
root.mainloop()
```

### How it works: 

This section creates the main application window and starts the GUI event loop, making the application responsive to user input.

### Key features:

GUI Event Loop: The root.mainloop() function keeps the application running, waiting for user interactions such as button clicks and song selections.

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.0 USABILITY AMENDMENTS AND ISSUES

## 1. Make the music player automatically play the next song

I Added functionality that detects when a song has finished playing and then starts the next song in the playlist.
The pygame library provides a way to detect when a song finishes using the pygame.mixer.music.set_endevent() function. 
I thought this function would allow me to set up an event that gets triggered when a song ends, which I then used to 
play the next song.

### Attempted Modifications 1:

- Set up an Event Handler for Song End: Used pygame.mixer.music.set_endevent() to create an event that triggers when 
the song finishes.
- Added an Event Loop to Handle the Next Song: Modified the main event loop to listen for this custom event and then 
call the next_song 
method to play the next song.
- Modified the __init__ method of the MusicPlayer class to set up the end event and add a new method to handle playing 
the next song:

### Errors

The first error I encountered, _tkinter.TclError: bad event type or keysym "song_end", indicated that Tkinter does not 
recognize the custom event type <song_end> because Tkinter has strict requirements for event types.

To handle song endings in Pygame while using Tkinter, I needed a different approach because Tkinter doesn’t support 
custom events in the same way as other GUI frameworks. I needed to check for the SONG_END event using a timer 
(with after()) to poll for the end of a song and then proceed to play the next one.

### Attempted Modifications 2:

- Polling for Song End: I removed the use of a custom Tkinter event. Instead, the check_for_song_end() method now 
directly checks for the SONG_END event and calls self.next_song() when detected. self.root.after(100, self.check_for_song_end) 
keeps the polling loop active.
- Error Resolution: I also removed self.root.bind("<song_end>", self.on_song_end) since Tkinter does not support custom event 
strings in the way I tried to use them.
- How It Works Now: The check_for_song_end function checks every 100 milliseconds for the SONG_END event from Pygame.
When a song finishes (SONG_END event is detected), it automatically triggers self.next_song(), playing the next song 
in the list.

### Errors

The next error I encountered, pygame.error: video system not initialized, turned out was caused by the fact that Pygame’s event 
system needs the video system to be initialized. This typically happens when pygame.init() or pygame.display.init() is called. 
However, since the application is using Tkinter for the GUI, I was not initializing Pygame's video subsystem, which was causing 
this error.

### Attempted Modifications 3:

To resolve this, it turned out I needed to initialize only the mixer module of Pygame (since I was only using it for audio), 
and I also needed to avoid using pygame.event.get() which relies on the video subsystem being initialized.
Instead, I used pygame.mixer.music.get_busy() to check if a song is still playing and determine when to play the next song.

- Using pygame.mixer.music.get_busy(): This function checks if the mixer is currently playing audio. It returns False if 
the music has stopped playing, indicating that it should proceed to the next song.

- Polling Mechanism: The check_for_song_end() method now uses pygame.mixer.music.get_busy() to determine if the song has 
ended, instead of using the Pygame event system, which avoids initializing the video system.

### How It Works:

The check_for_song_end function runs every 100 milliseconds. It checks if music is still playing (pygame.mixer.music.get_busy() returns True) 
and whether self.is_playing is True to determine if it should play the next song. If the music is not busy and self.is_playing is True, 
it means the song has ended, so it calls self.next_song().

This avoids initializing Pygame’s video system and still allows automatic song transitions.

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.1 USABILITY ISSUES AND AMENDMENTS

## 1. Make the music player non-resizable 
I achieved this by setting the minimum and maximum size of the window using the minsize and maxsize method. This 
method allowed me to specify the minimum and maximum width and height that the window can be resized to. 

### Set minimum and maximum size for a Tkinter window

Important to  remember that the minsize and maxsize methods are written slightly differently to the original geometry 
method that sets the opening dimensions.

```
class MusicPlayer:
    def __init__(self, root):
        # Initialize the music player application
        self.root = root
        self.root.title("CustomTkinter Music Player")  # Set the window title

        self.root.geometry("600x700")  # Set the window size
        # Set the window to fixed
        self.root.minsize(600, 700)  
        self.root.maxsize(600, 700)
```

## 2. Add a progress bar 

I tried to add a progress bar to the player using customtkinter. A progress bar is a must have on any 
media player. Tried to add a Progress Bar Widget to create a progress bar using CTkProgressBar.

### Attempted Modifications 1:

- Add a Progress Bar Widget:
- Create a CTkProgressBar widget.
- Position the Progress Bar under the volume control slider or wherever you prefer.

- Update the Progress Bar
- Use pygame.mixer.music.get_pos() to get the current position of the song in milliseconds.
- Use pygame.mixer.Sound.get_length() to get the total length of the song.
- Update the progress bar periodically based on the current position of the song.


### Errors

- The tracking, start and stop worked perfectly with the progress bar but, it made the music skip every 
1- 2 seconds. It turns out this happens because the pygame.mixer.music.get_pos() function only provides 
the current position of the song in milliseconds while playing, and it's reset to -1 when paused or stopped, 
which was causing unintended behavior in the loop.

### Attempted Modifications 2:

- To prevent the music from stopping or resetting due to incorrect handling of song state and progress updates, 
I tried adjusting the way the progress bar updates were handled.

- New approach tried was to use a timer to update the Progress Bar. I made sure that the progress bar is only 
updated when the music is playing, and prevent any unnecessary updates when the music is stopped or paused.
- To handle song state correctly, I used boolean flags to correctly manage the state of the music 
(whether it is playing or paused).

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.2 COMPLETING THE PROGRESS BAR

Finally got the progress bar working so decided to make it version 5.2 for the changes.

### 1. Add a Variable to Store Song Length

- In the __init__ method, initialize a variable to store the current song length.

```
self.current_song_length = 0
```

### 2. Calculate Song Length Once When a Song is Loaded

- Next was to update the 'play_song' method to calculate and store the song length only once when a song is loaded.

```
def play_song(self):
    # Play the selected song
    if self.songs_list:
        # Get the song at the current index
        song = self.songs_list[self.current_song_index]
        pygame.mixer.music.load(song)  # Load the song
        pygame.mixer.music.play()  # Play the song
        
        # Calculate and store the song length once
        self.current_song_length = pygame.mixer.Sound(song).get_length()
        
        self.is_playing = True  # Update the playing status
        self.current_song_label.configure(text=f"Playing: {song}")  # Update the label

        # Update the Listbox selection to highlight the playing song
        self.song_listbox.selection_clear(0, 'end')  # Clear previous selection
        self.song_listbox.selection_set(self.current_song_index)  # Select current song
        self.song_listbox.activate(self.current_song_index)  # Make sure the song is visible
```

### 3. Use the Pre-calculated song length

- The progress bar update now only involves getting the current position (get_pos()) and using the pre-calculated 
song length, making it more efficient.

```
def update_progress_bar(self):
    # Update the progress bar based on the current position of the song
    if pygame.mixer.music.get_busy():
        current_pos = pygame.mixer.music.get_pos() / 1000  # Current position in seconds
        progress = current_pos / self.current_song_length if self.current_song_length > 0 else 0
        self.progress_bar.set(progress)  # Update the progress bar value
```

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.3 ADDING SONG TIME COUNTER

To add a timer to show how long each track has been playing in your music player, I decided to implement 
a label that updates in real-time with the current playback position. This involved two primary tasks.

### 1. Create a Label to Display the Timer: 

- For this I added a label widget in the GUI to show the current playback time by adding a label in 
the create_widgets method of the MusicPlayer class.
- This displayed the elapsed time of the current song, and needed to be after defining the current song 
label (self.current_song_label).

```
# Label to display the current time of the song
self.current_time_label = ctk.CTkLabel(
    self.root,
    text="00:00",  # Initialize with 0:00
    text_color="white"
)

# Position the timer label below the progress bar
self.current_time_label.grid(row=6, column=0, columnspan=4, pady=(10, 0))
```

### 2. Update the Timer in Real-Time: 

- Next I created  the update_timer method to update this label every second.

```
def update_timer(self):
    """Update the timer label with the current playback time."""
    if pygame.mixer.music.get_busy():  # If music is playing
        # Current playback position in milliseconds
        current_pos_ms = pygame.mixer.music.get_pos()
        current_pos_sec = int(current_pos_ms / 1000)  # Convert to seconds
        
        # Format minutes and seconds (MM:SS)
        minutes = current_pos_sec // 60
        seconds = current_pos_sec % 60
        time_formatted = f"{minutes:02}:{seconds:02}"

        # Update the timer label with the formatted time
        self.current_time_label.configure(text=time_formatted)
    else:
        # If the music is not playing, reset the timer to 0:00
        self.current_time_label.configure(text="00:00")

    # Schedule the next update in 1 second (1000 milliseconds)
    self.root.after(1000, self.update_timer)
```

### 3. Initialize Timer Update

- Here I needed to start the timer update loop when a song starts playing. 
- I did this by adding a call to self.update_timer() in the play_song method.

```
def play_song(self):
    # Play the selected song
    if self.songs_list:
        # Get the song at the current index
        song = self.songs_list[self.current_song_index]
        pygame.mixer.music.load(song)  # Load the song
        pygame.mixer.music.play()  # Play the song

        self.current_song_length = pygame.mixer.Sound(song).get_length()
        self.is_playing = True  # Update the playing status
        self.current_song_label.configure(text=f"Playing: {song}")  # Update the label

        # Update the Listbox selection to highlight the playing song
        self.song_listbox.selection_clear(0, 'end')  # Clear previous selection
        self.song_listbox.selection_set(self.current_song_index)  # Select current song
        self.song_listbox.activate(self.current_song_index)  # Make sure the song is visible

        # Start the timer update loop
        self.update_timer()
```

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.4 USABILITY ISSUES AND AMENDMENTS

### Error 1

- Even though the timer would stop when paused and continue from the corect time.
- Discovered on testing that the song timer would revert to 0.00 while paused.

### Modification 1

- So, turns out that currently, when the pause button is pressed, the timer resets to 00:00 because the update_timer 
method detects that the music is not playing. Steps to fix this included:
- Modified the update_timer method to check if the song is paused and handle the timer accordingly.
- I also made sure that the pause_song method properly toggled the self.is_playing state to maintain the timer when paused.

### Error 2

- This fixed the timer resetting to 0.00 issue but caused an additional issue. Once paused the pause button no longer worked.
- The issue here was due to how the update_timer function was managed when the pause button is pressed again to resume playback. 
- When the timer was paused, the method pygame.mixer.music.get_busy() returned False, so the timer update loop wasn't being 
scheduled correctly, causing the playback to not continue when pressing the pause button again.

### Modification 2

### 1. Ensure the timer and playback correctly toggle between pause and resume.

- Modify the update_timer method to better handle the paused state:

```
def update_timer(self):
    """Update the timer label with the current playback time."""
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
```


### 2. Adjust the timer logic to only stop updating when music is stopped, not when paused.

- Adjust the pause_song method to ensure that playback resumes correctly:

```
def pause_song(self):
    """Pause or unpause the song."""
    if self.is_playing:
        # If music is playing, pause it
        pygame.mixer.music.pause()
        self.is_playing = False
    else:
        # If music is paused, unpause it
        pygame.mixer.music.unpause()
        self.is_playing = True
```

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.5 AESTHETIC AMENDMENTS

### Modification - Drop down box to change interface theme 

- For this I used customtkinter.CTkOptionMenu. This option menu allows the user to change the appearance mode.
- I updated the create_widgets method and added the logic to handle appearance mode changes.

```
    # Add a theme selection dropdown menu at the bottom of the interface
    self.appearance_mode_menu = ctk.CTkOptionMenu(
        self.root,
        values=["System", "Light", "Dark"],
        command=self.change_appearance_mode_event
    )
    # Set the initial appearance mode to "Dark"
    self.appearance_mode_menu.set("Dark")
    # Place the dropdown menu at the bottom
    self.appearance_mode_menu.grid(row=7, column=0, columnspan=4, pady=20, padx=10, sticky="ew")

def change_appearance_mode_event(self, new_appearance_mode: str):
    # Change the appearance mode (theme)
    ctk.set_appearance_mode(new_appearance_mode)
    
```

----------------------------------------------------------------------------------

# TKINTER MUSIC PLAYER 5.6 USABILITY AMENDMENTS

### Moved the elements aroung to make interface flow better

- Moved volume slider below progress bar
- Moved 'Previous' and 'Next' buttons to either side of progress bar
- Moved the timer and song loaded labels to better position
- Generally centered and cleaned up buttons 



