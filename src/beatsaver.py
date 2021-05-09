import json

import cfscrape

from src.log import Logger
from src.storage.model.song import Song


class BeatSaver:
    _url = "https://beatsaver.com/api"

    def __init__(self):
        self._session = cfscrape.create_scraper()

    def get_song_by_score(self, score):
        return self.get_song_by_hash(score.songHash)

    def get_song_by_hash(self, song_hash):
        response = self._session.get(f"{self._url}/maps/by-hash/{song_hash}", cookies={}, timeout=10)

        if response.status_code == 200:
            song_info = json.loads(response.content)
            return Song(song_info)

        Logger.log_add(f"Got HTTP status code {response.status_code} for {response.url}")
        return None
