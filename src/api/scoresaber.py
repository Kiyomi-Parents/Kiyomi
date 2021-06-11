import requests

from src.api.beatsaver import BeatSaver
from src.api.cache import Cache
from src.api.common import Common
from src.storage.model import *


class ScoreSaber:
    _timeout = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self._beatsaver = BeatSaver()

    @Cache(minutes=2)
    def _get_player(self, playerID):
        response = Common.request(requests.get, f"{self._url}/player/{playerID}/basic", timeout=self._timeout)

        return response.json()

    def get_player(self, playerID):
        response = self._get_player(playerID)

        return Player(response["playerInfo"])

    @Cache(minutes=2)
    def _get_recent_scores(self, playerID):
        response = Common.request(requests.get, f"{self._url}/player/{playerID}/scores/recent", timeout=self._timeout)

        return response.json()

    def get_recent_scores(self, playerID):
        response = self._get_recent_scores(playerID)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score(recent_score))

        return recent_score_list
