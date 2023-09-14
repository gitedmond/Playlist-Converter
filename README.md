Playlist Converter
This Python program offers a solution to convert your Spotify playlists into YouTube Music playlists by leveraging both Spotify's and Google's APIs.

Purpose
The primary motivation behind developing this program was to address a common challenge faced by us and our peers: the hassle of exchanging playlists between Spotify and YouTube Music. With this tool, you can now effortlessly transfer playlists between these platforms within minutes.

How it Works
Spotify Playlist Conversion (spotifyplylst.py):

Run spotifyplylst.py, which will prompt you to:
- Select a playlist from your Spotify account for conversion.
- Specify the desired name and description for the new YouTube Music playlist.
Utilizing the subprocess module, spotifyplylst.py triggers the execution of youtubeplylst.py.
YouTube Music Playlist Creation (youtubeplylst.py):
- After logging in with your Google account, youtubeplylst.py creates the YouTube Music playlist, using the title and 
  description provided.
- If any songs from the Spotify playlist are unavailable on YouTube Music, the program generates a list of these songs, 
  ensuring transparency about which tracks could not be added due to unavailability.
Please note that while Spotify offers a vast collection of songs, podcasts, and audio content, not all of these may be available on YouTube. As a result, this program helps identify and report any content that could not be added to the YouTube Music playlist.

Prerequisites
Before using this program, you will need to set up your Spotify and Google API credentials. Detailed instructions for setting up these credentials can be found in the respective documentation provided with this repository.

Usage
1. Clone this repository to your local machine.
2. Configure your Spotify and Google API credentials as per the instructions.
3. Run spotifyplylst.py and follow the prompts to initiate the conversion process.
Contributions
We welcome contributions and improvements to this project! If you have suggestions or would like to contribute to its development, please create a pull request or raise an issue in this repository.
