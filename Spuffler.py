import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
from collections import defaultdict

def process_playlist(client_id, client_secret, playlist_id):
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri="http://localhost:8888/callback",
                                                       scope="playlist-modify-public playlist-modify-private playlist-read-private"))

        sp.current_user()

        playlist_tracks = sp.playlist_tracks(playlist_id)
        
        if not playlist_tracks or 'items' not in playlist_tracks:
            print("❌ Failed to retrieve tracks from the playlist. Please check the Playlist ID.")
            return

        tracks = []
        for item in playlist_tracks['items']:
            track = item.get('track', None)
            if track is not None:
                artist_name = track['artists'][0]['name']
                tracks.append((artist_name, track['id']))
            else:
                print(f"❌ Error in one of the playlist items: {item}")
        
        if not tracks:
            print("❌ No tracks found in this playlist.")
            return

        artist_songs = defaultdict(list)
        for artist, track_id in tracks:
            artist_songs[artist].append(track_id)

        print("Artists before Spuffling:", list(artist_songs.keys()))

        artists = list(artist_songs.keys())
        random.shuffle(artists)

        shuffled_tracks = []
        while artists:
            random.shuffle(artists)
            for artist in artists[:]:
                if artist_songs[artist]:
                    shuffled_tracks.append(artist_songs[artist].pop(0))
                if not artist_songs[artist]:
                    artists.remove(artist)

        sp.playlist_replace_items(playlist_id, shuffled_tracks)
        print("✅ Playlist has been spuffled!")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

client_id = input("Enter your Client ID: ")
client_secret = input("Enter your Client Secret: ")
playlist_id = input("Enter Playlist ID: ")

process_playlist(client_id, client_secret, playlist_id)
