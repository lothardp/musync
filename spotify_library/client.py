import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyClient:
    def __init__(self, client_id, client_secret):
        # This is for the server connection, no user specific stuff
        # self.auth_manager = SpotifyClientCredentials(
        #     client_id=client_id,
        #     client_secret=client_secret,
        # )
        self.connected = False
        self.auth_manager = SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:3000",
            scope="user-library-read playlist-read-private"
        )

    def connect(self):
        self.client = spotipy.Spotify(auth_manager=self.auth_manager)
        self.connected = True

    def get_playlists(self):
        if not self.connected:
            return None

        return self.client.current_user_playlists().get("items", [])

    def get_playlist(self, playlist_id):
        if not self.connected:
            return None

        return self.client.playlist(playlist_id)
