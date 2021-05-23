import requests

from src.api.beatsaver import BeatSaver
from src.api.common import Common
from src.storage.model import *


class ScoreSaber:
    _timeout = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self._beatsaver = BeatSaver()

    def get_player(self, playerID):
        response = Common.request(requests.get, f"{self._url}/player/{playerID}/basic", timeout=self._timeout)

        player_info = response.json()["playerInfo"]
        return Player(player_info)

    def get_recent_scores(self, playerID):
        response = Common.request(requests.get, f"{self._url}/player/{playerID}/scores/recent", timeout=self._timeout)

        recent_scores = response.json()["scores"]

        recent_score_list = []

        for recent_score in recent_scores:
            recent_score_list.append(Score(recent_score))

        return recent_score_list
