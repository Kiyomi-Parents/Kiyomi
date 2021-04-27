import requests

from src.beatsaver import Beatsaver
from src.player import Player
from src.score import Score


class Scoresaber:
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self._beatsaver = Beatsaver()

    def get_player(self, playerID):
        response = requests.get(f'{self._url}/player/{playerID}/basic', timeout=5)
        player_info = response.json()["playerInfo"]

        return Player(player_info, self)

    def get_recent_scores(self, playerID):
        response = requests.get(f"{self._url}/player/{playerID}/scores/recent", timeout=5)
        recent_scores = response.json()["scores"]

        recent_score_list = []

        for recent_score in recent_scores:
            recent_score_list.append(Score(recent_score, self._beatsaver))

        return recent_score_list
