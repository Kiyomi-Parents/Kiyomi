import requests
from src.api.cache import Cache
from src.api.common import Common
from src.storage.model import Player, Score


class ScoreSaber:
    _timeout = 10
    _url = "https://new.scoresaber.com/api"

    @Cache(minutes=2)
    def _get_player(self, player_id):
        response = Common.request(requests.get, f"{self._url}/player/{player_id}/basic", timeout=self._timeout)

        return response.json()

    def get_player(self, player_id):
        response = self._get_player(player_id)

        return Player(response["playerInfo"])

    @Cache(minutes=2)
    def _get_recent_scores(self, player_id):
        response = Common.request(requests.get, f"{self._url}/player/{player_id}/scores/recent", timeout=self._timeout)

        return response.json()

    def get_recent_scores(self, player_id):
        response = self._get_recent_scores(player_id)

        recent_score_list = []

        for recent_score in response["scores"]:
            recent_score_list.append(Score(recent_score))

        return recent_score_list
