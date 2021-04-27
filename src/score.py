import json
import os

from dateutil import parser


class Score:
    _save_file = "scores.json"

    def __init__(self, scoreJson, beatsaver):
        self.rank = scoreJson["rank"]
        self.scoreId = scoreJson["scoreId"]
        self.score = scoreJson["score"]
        self.unmodififiedScore = scoreJson["unmodififiedScore"]
        self.mods = scoreJson["mods"]
        self.pp = scoreJson["pp"]
        self.weight = scoreJson["weight"]
        self.timeSet = scoreJson["timeSet"]
        self.leaderboardId = scoreJson["leaderboardId"]
        self.songHash = scoreJson["songHash"]
        self.songName = scoreJson["songName"]
        self.songSubName = scoreJson["songSubName"]
        self.songAuthorName = scoreJson["songAuthorName"]
        self.levelAuthorName = scoreJson["levelAuthorName"]
        self.difficulty = scoreJson["difficulty"]
        self.difficultyRaw = scoreJson["difficultyRaw"]
        self.maxScore = scoreJson["maxScore"]

        self._beatsaver = beatsaver

    def get_scores(self):
        if os.path.isfile(self._save_file):
            with open(self._save_file, "r") as file:
                return json.load(file)

    def save(self):
        scores = self.get_scores()

        if scores:
            scores["scoreIds"].append(self.scoreId)
        else:
            scores = {"scoreIds": [self.scoreId]}

        with open(self._save_file, "w") as file:
            json.dump(scores, file)

    @property
    def is_saved(self):
        scores = self.get_scores()

        if not scores:
            return False

        return self.scoreId in scores["scoreIds"]

    @property
    def leaderboard_url(self):
        page = (self.rank - 1) // 12 + 1
        return f"http://scoresaber.com/leaderboard/{self.leaderboardId}?page={page}"

    @property
    def song_name_full(self):
        if self.songSubName:
            return f"{self.songName}: {self.songSubName}"
        else:
            return self.songName

    @property
    def difficulty_name(self):
        difficulties = {
            1: "Easy",
            2: "2?",
            3: "Normal",
            4: "4?",
            5: "Hard",
            6: "6?",
            7: "Expert",
            8: "8?",
            9: "Expert Plus"
        }

        return difficulties[self.difficulty]

    @property
    def song_image_url(self):
        return f"https://scoresaber.com/imports/images/songs/{self.songHash}.png"

    @property
    def accuracy(self):
        if self.maxScore:
            return round(self.score / self.maxScore * 100, 3)
        else:
            return "N/A"

    @property
    def weighted_pp(self):
        return round(self.pp * self.weight, 2)

    def get_date(self):
        return parser.isoparse(self.timeSet).replace(tzinfo=None)

    def get_song(self):
        return self._beatsaver.get_song_by_hash(self.songHash)

    def __str__(self):
        return self.scoreId

    def __repr__(self):
        return str(self.scoreId)
