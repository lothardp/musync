from library.library import Library
from spotify_library.library import SpotifyLibrary
from ui.app import Musync
import sys

music_path = sys.argv[1]
if not music_path:
    print("Please provide a path to your music library")
    sys.exit(1)

lib = Library(sys.argv[1])
# sp_lib = SpotifyLibrary()

if __name__ == "__main__":
    app = Musync(lib)
    app.run()
