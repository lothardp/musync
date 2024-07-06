from .client import SpotifyClient
from dotenv import load_dotenv
import os

load_dotenv()


class SpotifyLibrary:
    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    def __init__(self):
        self.client = SpotifyClient(
            client_id=self.SPOTIFY_CLIENT_ID,
            client_secret=self.SPOTIFY_CLIENT_SECRET
        )
        self.playlists_dict = {}

    def get_playlists(self):
        if self.playlists is None:
            self.load_playlists()

        return self.playlists

    def get_playlist(self, playlist_id):
        if playlist_id not in self.playlists_dict:
            self.load_playlist(playlist_id)

        return self.playlists_dict[playlist_id]

    def load_playlists(self):
        self.playlists = self.client.get_playlists()

    def load_playlist(self, playlist_id):
        self.playlists_dict[playlist_id] = self.client.get_playlist(
            playlist_id
        )

    def get_songs(self, playlist_id):
        playlist = self.get_playlist(playlist_id)
        return playlist["tracks"]["items"]

