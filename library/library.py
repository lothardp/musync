import os
from mutagen import File

def is_song_file(file: str) -> bool:
    return file.endswith('.mp3')


class Library:
    def __init__(self, songs_directory: str):
        self.songs_directory = songs_directory
        self.load_songs()

    def load_songs(self):
        all_contents = os.listdir(self.songs_directory)

        self.songs = [File(os.path.join(self.songs_directory, f))
                      for f in all_contents if is_song_file(f)]

    def print_songs(self):
        for song in self.songs:
            print(song.tags.get('TIT2'), song.tags.get('TPE1'))

