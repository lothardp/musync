from textual.app import App, ComposeResult
from textual.widgets import Footer, Label, TabbedContent, TabPane, Tabs
from textual.binding import Binding
from textual.widgets import Static

from .library_tab import LibraryTab
from .spotify_tab import SpotifyTab


class DownloadTab(Static):
    def __init__(self, youtube_service):
        super().__init__()
        self.youtube_service = youtube_service

    def compose(self) -> ComposeResult:
        yield Label("Download")


class Musync(App):
    CSS_PATH = "styles.tcss"

    BINDINGS = [
        Binding("h", "previous_tab", "Previous tab", show=False),
        Binding("l", "next_tab", "Next tab", show=False),
        Binding("L", "show_tab('library')", "Library", show=False),
        Binding("S", "show_tab('spotify')", "Spotify", show=False),
        Binding("D", "show_tab('download')", "Download", show=False),
        ("q", "quit", "Quit"),
    ]

    def __init__(self, local_library, spotify_library, youtube_service):
        super().__init__()
        self.local_library = local_library
        self.spotify_library = spotify_library
        self.youtube_service = youtube_service

    def compose(self) -> ComposeResult:
        with TabbedContent(initial="spotify"):
            with TabPane("Library (L)", id="library"):
                yield LibraryTab(self.local_library)
            with TabPane("Spotify (S)", id="spotify"):
                yield SpotifyTab(self.spotify_library)
            with TabPane("Download (D)", id="download"):
                yield DownloadTab(self.youtube_service)

        yield Footer()

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

    def action_next_tab(self) -> None:
        self.query_one(Tabs).action_next_tab()

    def action_previous_tab(self) -> None:
        self.query_one(Tabs).action_previous_tab()
