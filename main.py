from library.library import Library
from spotify_library.library import SpotifyLibrary
from ui.app import Musync
import sys
import os

from dotenv import load_dotenv
load_dotenv()

music_path = sys.argv[1]
if not music_path:
    print("Please provide a path to your music library")
    sys.exit(1)

local_library = Library(sys.argv[1])

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

spotify_library = SpotifyLibrary(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)

if __name__ == "__main__":
    app = Musync(local_library, spotify_library)
    app.run()
