import os
import argparse
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Define your client secrets file path
CLIENT_SECRETS_FILE = "client_secret.json"

# Define the correct scope for accessing YouTube data
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube

def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description
            },
            "status": {
                "privacyStatus": "public"
            }
        }
    )
    response = request.execute()
    return response["id"]

def search_video_id(youtube, query):
    request = youtube.search().list(
        part="id",
        maxResults=1,  # Assuming you want the first search result
        q=query
    )
    response = request.execute()
    if "items" in response:
        video_id = response["items"][0]["id"]["videoId"]
        return video_id
    else:
        return None

def add_songs_to_playlist(youtube, playlist_id, song_file):
    added_songs = []
    not_found_songs = []

    with open(song_file, "r", encoding="utf-8") as file:
        songs = [line.strip() for line in file if line.strip()]

    for song in songs:
        video_id = search_video_id(youtube, song)
        if video_id:
            request = youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            request.execute()
            added_songs.append(song)
        else:
            not_found_songs.append(song)

    return added_songs, not_found_songs

def main():
    # Create an ArgumentParser to handle command-line arguments
    parser = argparse.ArgumentParser(description="YouTube Playlist Creator")
    parser.add_argument("title", help="Playlist title")
    parser.add_argument("description", help="Playlist description")
    args = parser.parse_args()

    youtube = authenticate()

    # Get the playlist title and description from the command-line arguments
    playlist_title = args.title
    playlist_description = args.description

    # Replace with the path to your song file
    song_file_path = "playlist_tracks.txt"

    # Create a new playlist and get its ID
    playlist_id = create_playlist(youtube, playlist_title, playlist_description)

    # Add songs to the playlist and get lists of added and not found songs
    added_songs, not_found_songs = add_songs_to_playlist(youtube, playlist_id, song_file_path)

    print(f"Playlist '{playlist_title}' created with {len(added_songs)} songs.")
    if not_found_songs:
        print("Songs not found on YouTube:")
        for song in not_found_songs:
            print(song)

if __name__ == "__main__":
    main()
