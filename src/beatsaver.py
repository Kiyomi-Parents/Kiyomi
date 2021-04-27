import json

import cfscrape

from src.song import Song


class Beatsaver:
    _url = "https://beatsaver.com/api"

    def __init__(self):
        self._session = cfscrape.create_scraper()

    def get_song_by_hash(self, song_hash):
        response = self._session.get(f"{self._url}/maps/by-hash/{song_hash}", cookies={}, timeout=10)
        song_info = json.loads(response.content)

        return Song(song_info)
