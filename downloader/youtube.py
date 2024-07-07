from googleapiclient.discovery import build
import subprocess

from music.song import Song


COMMAND = ["yt-dlp", "-f", "bestaudio", "-x", "--audio-format", "mp3", "--audio-quality",
           "0", "--add-metadata", "--embed-thumbnail", "-o", "%(title)s.%(ext)s"]


class YoutubeService:
    def __init__(self, download_directory, api_key):
        self.download_directory = download_directory
        self.client = build('youtube', 'v3', developerKey=api_key)
        self.queries = {}

    def search(self, query):
        if query in self.queries:
            return self.queries[query]

        request = self.client.search().list(
            part="snippet",
            maxResults=5,
            q=query
        )
        self.queries[query] = request.execute()

        return self.queries[query]

    def download_url(self, url):
        res = subprocess.run(COMMAND + [
            "-o",
            f"{self.download_directory}/%(title)s.%(ext)s",
            url
        ])

        return res.returncode == 0

    def download_song(self, song: Song):
        query = f"{song.title} - {song.artist} audio"
        search_results = self.search(query)

        item = search_results['items'][0]
        video_id = item['id']['videoId']
        url = f"https://www.youtube.com/watch?v={video_id}"
        if self.download_url(url):
            return True

        return False
