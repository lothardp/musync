class Song:
    def __init__(self, title, artist, album, duration):
        self.title = title
        self.album = album
        self.artist = artist
        self.duration = duration

    def __str__(self):
        return f"{self.title} by {self.artist} from {self.album}"
