from src.log import Logger
from src.storage.model.score import Score


class ScoreRepository:

    def __init__(self, database):
        self._db = database

    def get_score(self, scoreId):
        return self._db.session.query(Score).filter(Score.scoreId == scoreId).first()

    def get_player_scores(self, player):
        return self._db.session.query(Score).filter(Score.player_id == player.id).all()

    def get_unsent_scores(self, player, guild):
        scores = self.get_player_scores(player)

        unsent_scores = []

        for score in scores:
            print(f'{score.scoreId} {score.msg_guilds}')
            if guild not in score.msg_guilds:
                unsent_scores.append(score)

        return unsent_scores

    def mark_score_sent(self, score, guild):
        current_score = self.get_score(score.scoreId)

        current_score.msg_guilds.append(guild)

        self._db.commit_changes()
        Logger.log_add(f"Marked {score} as sent for {guild}")

    def add_song(self, score, song):
        current_score = self.get_score(score.scoreId)

        if current_score.song is None:
            current_score.song = song

            self._db.commit_changes()
            Logger.log_add(f"Added {song} to {score}")
