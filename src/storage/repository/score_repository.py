from src.log import Logger
from src.storage.model.score import Score


class ScoreRepository:

    def __init__(self, database):
        self._db = database

    def get_score(self, score_id):
        return self._db.session.query(Score).filter(Score.scoreId == score_id).first()

    def get_scores(self, scores=None):
        if scores is None:
            return self._db.session.query(Score).all()

        db_scores = []

        for score in scores:
            db_scores.append(self.get_score(score.scoreId))

        return db_scores

    def get_all_scores_by_id(self, score_id):
        return self._db.session.query(Score).filter(Score.scoreId == score_id).all()

    def get_all_scores_by_leaderboardId_and_guildId(self, leaderboardId, guildId):
        pass

    def get_previous_score(self, db_score):
        db_scores = self.get_all_scores_by_id(db_score.scoreId)

        previous_score = None

        for old_db_score in db_scores:
            if old_db_score.score == db_score.score:
                continue

            if previous_score is None:
                previous_score = old_db_score
                continue

            if old_db_score.score > previous_score.score:
                previous_score = old_db_score

        return previous_score

    def get_player_scores(self, player):
        return self._db.session.query(Score).filter(Score.player_id == player.id).all()

    def get_player_scores_without_song(self, player):
        return self._db.session.query(Score)\
            .filter(Score.player_id == player.id)\
            .filter(~Score.song.has()).all()

    def get_scores_without_song(self):
        return self._db.session.query(Score).filter(~Score.song.has()).all()

    def update_score(self, new_db_score):
        old_db_score = self.get_score(new_db_score.scoreId)

        old_db_score.rank = new_db_score.rank
        old_db_score.scoreId = new_db_score.scoreId
        old_db_score.score = new_db_score.score
        old_db_score.unmodififiedScore = new_db_score.unmodififiedScore
        old_db_score.mods = new_db_score.mods
        old_db_score.pp = new_db_score.pp
        old_db_score.weight = new_db_score.weight
        old_db_score.timeSet = new_db_score.timeSet
        old_db_score.leaderboardId = new_db_score.leaderboardId
        old_db_score.songHash = new_db_score.songHash
        old_db_score.songName = new_db_score.songName
        old_db_score.songSubName = new_db_score.songSubName
        old_db_score.songAuthorName = new_db_score.songAuthorName
        old_db_score.levelAuthorName = new_db_score.levelAuthorName
        old_db_score.difficulty = new_db_score.difficulty
        old_db_score.difficultyRaw = new_db_score.difficultyRaw
        old_db_score.maxScore = new_db_score.maxScore

        self._db.commit_changes()
        Logger.log(old_db_score, "Updated")

        self.mark_score_unsent(old_db_score)

    def update_scores(self, new_scores):
        for new_score in new_scores:
            old_db_score = self.get_score(new_score.scoreId)

            if new_score.score != old_db_score.score:
                self.update_score(new_score)

    @staticmethod
    def get_unsent_scores(db_player, db_guild):
        unsent_scores = []

        for db_score in db_player.scores:
            if db_guild not in db_score.msg_guilds:
                unsent_scores.append(db_score)

        return unsent_scores

    def is_score_new(self, db_score):
        db_scores = self.get_all_scores_by_id(db_score.scoreId)

        return 1 >= len(db_scores)

    def mark_score_sent(self, db_score, db_guild):
        db_score.msg_guilds.append(db_guild)

        self._db.commit_changes()
        Logger.log(db_score, f"Marked as sent in {db_guild}")

    def mark_score_unsent(self, db_score):
        db_score.msg_guilds = []

        self._db.commit_changes()
        Logger.log(db_score, "Marked as unsent")

    def add_song(self, db_score, db_song):
        if db_score.song is None:
            db_score.song = db_song

            self._db.commit_changes()
            Logger.log(db_score, f"Added {db_song}")
