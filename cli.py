from library.library import Library
from spotify_library.library import SpotifyLibrary
from downloader.youtube import YoutubeService
from thefuzz import process


def get_songs_to_download(downloaded_songs, playlist_songs):
    titles = [song.title for song in downloaded_songs]
    candidates = []
    for song in playlist_songs:
        to_match = f"{song.title} {song.artist}"
        match = process.extractOne(to_match, titles)
        if match[1] < 85:
            print(f"Best Match ({match[1]}) for {song.title}: {match[0]}")
            if input("Do you want to download this song? (y/n): ") == 'y':
                candidates.append([song] + list(match))

    return candidates


class CLI:
    def __init__(self,
                 local_library: Library,
                 spotify_library: SpotifyLibrary,
                 youtube_service: YoutubeService,
                 playlist_id: str
                 ):
        self.local_library = local_library
        self.spotify_library = spotify_library
        self.youtube_service = youtube_service
        self.playlist_id = playlist_id

        self.spotify_library.connect()

    def sync_playlist(self):
        self.downloaded_songs = self.local_library.get_songs()
        self.playlist_songs = self.spotify_library.get_songs(self.playlist_id)

        songs_to_download = get_songs_to_download(
            self.downloaded_songs, self.playlist_songs
        )

        print("Songs to download:")
        for song in songs_to_download:
            print(f"{song[0]}")

        if input("Do you want to download these songs? (y/n): ") == 'y':
            for song in songs_to_download:
                self.youtube_service.download_song(song[0])
