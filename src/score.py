import json
import os

from dateutil import parser, tz


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
                try:
                    return json.load(file)
                except:
                    return {}
        else:
            return {}

    def save(self, guildID):
        scores = self.get_scores()

        try:
            scores[str(guildID)]["scoreIds"].append(self.scoreId)
        except KeyError:
            scores = {str(guildID): {"scoreIds": [self.scoreId]}}
        
        if len(scores[str(guildID)]["scoreIds"]) > 150:
            scores[str(guildID)]["scoreIds"].pop(0)

        with open(self._save_file, "w") as file:
            json.dump(scores, file)
            #print(f'saved {self.scoreId} to {guildID}')

    #@property
    def is_saved(self, guildID):
        scores = self.get_scores()

        if not scores:
            return False

        try:
            return self.scoreId in scores[str(guildID)]["scoreIds"]
        except KeyError:
            return False

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
        timestamp = parser.isoparse(self.timeSet).replace(tzinfo=tz.gettz('UTC'))
        return timestamp.astimezone(tz.tzlocal())

    def get_song(self):
        return self._beatsaver.get_song_by_hash(self.songHash)

    def __str__(self):
        return self.scoreId

    def __repr__(self):
        return str(self.scoreId)
