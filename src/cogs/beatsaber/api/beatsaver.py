import json

import cfscrape

from src.cogs.beatsaber.api.cache import Cache
from src.cogs.beatsaber.api.common import Common
from src.cogs.beatsaber.storage.model.song import Song


class BeatSaver:
    _url = "https://beatsaver.com/api"
    _timeout = 10

    def __init__(self):
        self._session = cfscrape.create_scraper()

    def get_song_by_score(self, score):
        return self.get_song_by_hash(score.songHash)

    @Cache(hours=24)
    def _get_song_by_hash(self, song_hash):
        response = Common.request(self._session.get, f"{self._url}/maps/by-hash/{song_hash}", cookies={}, timeout=self._timeout)

        return json.loads(response.content)

    def get_song_by_hash(self, song_hash):
        song_info = self._get_song_by_hash(song_hash)

        return Song(song_info)

    @Cache(hours=24)
    def _get_song_by_key(self, song_key):
        response = Common.request(self._session.get, f"{self._url}/maps/detail/{song_key}", cookies={}, timeout=self._timeout)

        return json.loads(response.content)

    def get_song_by_key(self, song_key):
        song_info = self._get_song_by_key(song_key)

        return Song(song_info)
