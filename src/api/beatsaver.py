import json

import cfscrape

from src.api.cache import Cache
from src.api.common import Common
from src.storage.model.song import Song


class BeatSaver:
    _url = "https://beatsaver.com/api"

    def __init__(self):
        self._session = cfscrape.create_scraper()

    def get_song_by_score(self, score):
        return self.get_song_by_hash(score.songHash)

    @Cache(hours=24)
    def _get_song_by_hash(self, song_hash):
        response = Common.request(self._session.get, f"{self._url}/maps/by-hash/{song_hash}", cookies={}, timeout=10)

        return json.loads(response.content)

    def get_song_by_hash(self, song_hash):
        song_info = self._get_song_by_hash(song_hash)

        return Song(song_info)
