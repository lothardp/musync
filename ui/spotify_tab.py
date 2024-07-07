from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Horizontal, Container
from textual.binding import Binding
from textual.widgets import Label, ListItem, ListView


def build_song_item(song):
    return SongItem(
        title=song.title,
        artist=song.artist,
        album=song.album,
        duration=song.duration,
    )


def build_playlist_item(playlist):
    return PlaylistItem(
        pid=playlist["id"],
        name=playlist["name"],
        total=playlist["tracks"]["total"],
    )


class SpotifyTab(Container):
    BINDINGS = [
        Binding("j", "cursor_down", "Cursor Down", show=False),
        Binding("k", "cursor_up", "Cursor Up", show=False),
    ]

    def __init__(self, library):
        super().__init__()
        self.library = library
        self.playlists = None

    def compose(self) -> ComposeResult:
        yield Container(
            Button("Connect", id="connect-button", variant="primary"),
            id="connect-button-container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "connect-button":
            self.connect_spotify()
            self.show_playlists_list()
        if event.button.id == "refresh-button":
            self.refresh_playlists()
        if event.button.id == "back-button":
            self.query_one(SongsList).remove()
            self.show_playlists_list()

    def connect_spotify(self):
        self.library.connect()
        self.query_one("#connect-button-container").remove()

    def show_playlists_list(self):
        self.refresh_playlists()
        self.mount(PlaylistsList(self.playlists))

    def refresh_playlists(self):
        self.playlists = self.library.get_playlists()
        print(len(self.playlists))

    def action_cursor_down(self) -> None:
        self.query_one(ListView).action_cursor_down()

    def action_cursor_up(self) -> None:
        self.query_one(ListView).action_cursor_up()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "playlists-list":
            self.query_one(PlaylistsList).remove()
            songs = self.library.get_songs(event.item.pid)
            self.mount(SongsList(event.item.playlist_name, songs))


class PlaylistsList(Container):
    def __init__(self, playlists):
        super().__init__()
        self.playlists = playlists

    def compose(self) -> ComposeResult:
        with Horizontal(id="playlists-header"):
            yield Container(
                Label("Playlists", id="playlists-title")
            )
            yield Container(
                Button("Refresh", id="refresh-button", variant="primary"),
                id="refresh-button-container",
            )
        yield PlaylistTableHeader(id="library-table-header")
        yield ListView(id="playlists-list")

    def on_mount(self) -> None:
        list_view = self.query_one(ListView)

        for playlist in self.playlists:
            list_view.append(build_playlist_item(playlist))


class PlaylistTableHeader(Container):
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label("ID", classes="id")
            yield Label("Name", classes="name")
            yield Label("Total Tracks", classes="total")


class PlaylistItem(ListItem):
    def __init__(self, pid, name,  total) -> None:
        super().__init__()
        self.pid = pid
        self.playlist_name = name
        self.total = str(total)

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(self.pid, classes="id")
            yield Label(self.playlist_name, classes="name")
            yield Label(self.total, classes="total")


class SongsList(Container):
    def __init__(self, playlist_name, songs):
        super().__init__()
        self.playlist_name = playlist_name
        self.songs = songs

    def compose(self) -> ComposeResult:
        with Horizontal(id="songs-header"):
            yield Container(
                Button("Back", id="back-button", variant="primary"),
                id="back-button-container",
            )
            yield Container(
                Label(f"Playlist {self.playlist_name}", id="songs-title")
            )
        yield SongTableHeader(id="library-table-header")
        yield ListView(id="songs-list")

    def on_mount(self) -> None:
        list_view = self.query_one(ListView)

        for song in self.songs:
            list_view.append(build_song_item(song))


class SongTableHeader(Container):
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
