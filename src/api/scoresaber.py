import requests

from src.api.beatsaver import BeatSaver
from src.api.common import Common
from src.log import Logger
from src.storage.model.player import Player
from src.storage.model.score import Score


class ScoreSaber:
    _timeout = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self._beatsaver = BeatSaver()

    def get_player(self, playerID):
        response = Common.request(requests.get, f"{self._url}/player/{playerID}/basic", timeout=self._timeout)

        player_info = response.json()["playerInfo"]
        return Player(player_info)

    def get_recent_scores(self, db_player):
        response = Common.request(requests.get, f"{self._url}/player/{db_player.playerId}/scores/recent", timeout=self._timeout)

        recent_scores = response.json()["scores"]

        recent_score_list = []

        for recent_score in recent_scores:
            recent_score_list.append(Score(recent_score))

        Logger.log_add(f"Got {len(recent_score_list)} recent scores for {db_player}")
        return recent_score_list
