from textual.app import ComposeResult
from textual.binding import Binding
from textual.widgets import Label, ListItem, ListView
from textual.containers import Horizontal, Container


def build_song_item(song):
    return SongItem(
        title=song.title,
        artist=song.artist,
        album=song.album,
        duration=song.duration,
    )


class LibraryTab(Container):
    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
    ]

    def __init__(self, library) -> None:
        super().__init__()
        self.library = library

    def compose(self) -> ComposeResult:
        yield TableHeader(id="library-table-header")
        yield ListView()

    def on_mount(self) -> None:
        songs = self.library.get_songs()
        list_view = self.query_one(ListView)

        for song in songs:
            list_view.append(build_song_item(song))

    def action_cursor_down(self) -> None:
        self.query_one(ListView).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one(ListView).action_cursor_up()


class TableHeader(Container):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("Title", classes="title")
            yield Label("Artist", classes="artist")
            yield Label("Album", classes="album")
            yield Label("Duration", classes="duration")


class SongItem(ListItem):
    def __init__(self, title, artist, album, duration) -> None:
        super().__init__()
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = str(duration)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self.title, classes="title")
            yield Label(self.artist, classes="artist")
            yield Label(self.album, classes="album")
            yield Label(self.duration, classes="duration")
