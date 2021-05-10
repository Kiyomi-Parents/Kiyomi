from sqlalchemy.orm import joinedload

from src.log import Logger
from src.storage.model.score import Score
from src.storage.model.song import Song


class ScoreRepository:

    def __init__(self, database):
        self._db = database

    def get_score(self, scoreId):
        return self._db.session.query(Score).filter(Score.scoreId == scoreId).first()

    def get_player_scores(self, player):
        return self._db.session.query(Score).filter(Score.player_id == player.id).all()

    def get_scores_without_song(self):
        return self._db.session.query(Score).filter(~Score.song.has()).all()

    def update_score(self, score):
        old_score = self.get_score(score.scoreId)

        old_score.rank = score.rank
        old_score.scoreId = score.scoreId
        old_score.score = score.score
        old_score.unmodififiedScore = score.unmodififiedScore
        old_score.mods = score.mods
        old_score.pp = score.pp
        old_score.weight = score.weight
        old_score.timeSet = score.timeSet
        old_score.leaderboardId = score.leaderboardId
        old_score.songHash = score.songHash
        old_score.songName = score.songName
        old_score.songSubName = score.songSubName
        old_score.songAuthorName = score.songAuthorName
        old_score.levelAuthorName = score.levelAuthorName
        old_score.difficulty = score.difficulty
        old_score.difficultyRaw = score.difficultyRaw
        old_score.maxScore = score.maxScore

        self._db.commit_changes()
        Logger.log_add(f"Updated {old_score}")

        self.mark_score_unsent(score)

    def update_scores(self, scores):
        for new_score in scores:
            old_score = self.get_score(new_score.scoreId)

            if new_score.score != old_score.score:
                self.update_score(new_score)

    def get_unsent_scores(self, player, guild):
        scores = self.get_player_scores(player)

        unsent_scores = []

        for score in scores:
            if guild not in score.msg_guilds:
                unsent_scores.append(score)

        return unsent_scores

    def mark_score_sent(self, score, guild):
        current_score = self.get_score(score.scoreId)

        current_score.msg_guilds.append(guild)

        self._db.commit_changes()
        Logger.log_add(f"Marked {score} as sent for {guild}")

    def mark_score_unsent(self, score):
        current_score = self.get_score(score.scoreId)

        current_score.msg_guilds = []

        self._db.commit_changes()
        Logger.log_add(f"Marked {score} as unsent")

    def add_song(self, score, song):
        current_score = self.get_score(score.scoreId)

        if current_score.song is None:
            current_score.song = song

            self._db.commit_changes()
            Logger.log_add(f"Added {song} to {score}")
