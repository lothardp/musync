import os
from mutagen import File

from music.song import Song


def is_song_file(file: str) -> bool:
    return file.endswith('.mp3')


def build_song(file: File):
    return Song(
        title=str(file.tags.get('TIT2')),
        artist=str(file.tags.get('TPE1')),
        album=str(file.tags.get('TALB')),
        duration=int(file.info.length)
    )


class Library:
    def __init__(self, songs_directory: str):
        self.songs_directory = songs_directory
        self.load_songs()

    def load_songs(self):
        all_contents = os.listdir(self.songs_directory)

        self.raw_songs = [File(os.path.join(self.songs_directory, f))
                          for f in all_contents if is_song_file(f)]

        self.songs = [build_song(raw_song) for raw_song in self.raw_songs]

    def get_songs(self):
        return self.songs
