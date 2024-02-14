import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import requests
import subprocess

# Replace with your Spotify access token
access_token = 'YOUR_OWN_TOKEN'

# Define the file path for the playlist tracks
playlist_file = 'C:/Users/sarge/OneDrive/Desktop/converter/playlist_tracks.txt'

# Function to fetch a user's playlists
def get_user_playlists():
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    
    if response.status_code == 200:
        playlists = response.json()['items']
        return playlists
    else:
        print('Error fetching playlists:', response.status_code)
        return None

# Function to fetch tracks from a playlist
def get_tracks_from_playlist(playlist_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers)
    
    if response.status_code == 200:
        tracks = response.json()['items']
        return tracks
    else:
        print('Error fetching playlist tracks:', response.status_code)
        return None

# Function to export playlist tracks to a .txt file
def export_tracks_to_txt(tracks):
    with open(playlist_file, 'w', encoding='utf-8') as file:
        for track in tracks:
            track_name = track['track']['name']
            artist_names = ', '.join([artist['name'] for artist in track['track']['artists']])
            file.write(f'{track_name} by {artist_names}\n')
    print(f'Playlist tracks exported to {playlist_file}')

# Function to handle the export button click
def export_button_click():
    selected_playlist_name = playlist_combobox.get()
    if selected_playlist_name:
        selected_playlist_id = playlist_ids[selected_playlist_name]
        playlist_tracks = get_tracks_from_playlist(selected_playlist_id)
        if playlist_tracks:
            export_tracks_to_txt(playlist_tracks)
            
            # Prompt the user for YouTube playlist title and description
            youtube_playlist_title = simpledialog.askstring("YouTube Playlist", "Enter YouTube playlist title:")
            youtube_playlist_description = simpledialog.askstring("YouTube Playlist", "Enter YouTube playlist description:")
            
            # After exporting Spotify tracks, run the YouTube program with these values
            run_youtube_program(youtube_playlist_title, youtube_playlist_description)            
            
# Function to run the YouTube program
def run_youtube_program(youtube_playlist_title, youtube_playlist_description):
    try:
        subprocess.run(["python", "youtube.py", youtube_playlist_title, youtube_playlist_description], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running YouTube program: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.title("Spotify Playlist Exporter")

# Fetch user playlists
playlists = get_user_playlists()

if playlists:
    # Create a dictionary to store playlist IDs by name
    playlist_ids = {playlist["name"]: playlist["id"] for playlist in playlists}

    # Create a label
    label = ttk.Label(root, text="Select a playlist to export:")
    label.pack(pady=10)

    # Create a combobox to select a playlist
    playlist_combobox = ttk.Combobox(root, values=list(playlist_ids.keys()))
    playlist_combobox.pack()

    # Create an export button
    export_button = ttk.Button(root, text="Export", command=export_button_click)
    export_button.pack(pady=10)

    root.mainloop()
else:
    print("No playlists found. Please check your Spotify access token.")



