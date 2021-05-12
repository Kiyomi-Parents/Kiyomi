from bs4 import BeautifulSoup
import requests

from src.beatsaver import BeatSaver
from src.log import Logger
from src.storage.model.player import Player
from src.storage.model.score import Score


class ScoreSaber:
    _timeout = 10
    _url = "https://new.scoresaber.com/api"

    def __init__(self):
        self._beatsaver = BeatSaver()

    def get_player_scrape(self, playerID):
        response = requests.get(f'https://scoresaber.com/u/{playerID}', timeout=self._timeout)
        soup = BeautifulSoup(response.content, 'html.parser')

        player_json = {"playerId": "76561198029447509",
                       "playerName": soup.find("h5", class_="title is-5").a.text.strip(),
                       "avatar": soup.find("img", attrs={"title": "Profile Image"})["src"],
                       "rank": int(soup.find("a", attrs={"href": "/global"}).text.strip("#")),
                       "countryRank": int(soup.find("a", attrs={"href": "/global"}).parent.find("img").parent.text.strip().strip("#")),
                       "pp": float(soup.find("strong", string="Performance Points:").next_sibling.strip().strip("pp").replace(",", "")),
                       "country": soup.find("a", attrs={"href": "/global"}).parent.find("img").parent["href"].strip().strip("/global?country="),
                       "role": None, "badges": None, "history": None,
                       "permissions": None, "inactive": None, "banned": None}

        return Player(player_json)

    def get_player(self, playerID):
        response = requests.get(f'{self._url}/player/{playerID}/basic', timeout=self._timeout)

        if response.status_code == 200:
            player_info = response.json()["playerInfo"]
            return Player(player_info)
        elif response.status_code == 502:
            return self.get_player_scrape(playerID)

        Logger.log_add(f"Got HTTP status code {response.status_code} for {response.url}")
        return None

    def get_recent_scores(self, db_player):
        response = requests.get(f"{self._url}/player/{db_player.playerId}/scores/recent", timeout=self._timeout)

        if response.status_code == 200:
            recent_scores = response.json()["scores"]

            recent_score_list = []

            for recent_score in recent_scores:
                recent_score_list.append(Score(recent_score))

            Logger.log_add(f"Got {len(recent_score_list)} recent scores for {db_player}")
            return recent_score_list

        Logger.log_add(f"Got HTTP status code {response.status_code} for {response.url}")
        return None
