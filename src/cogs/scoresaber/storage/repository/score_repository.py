from typing import Optional, List

from src.database import Repository
from src.log import Logger
from .player_repository import PlayerRepository
from ..model.score import Score
from ...scoresaber_utils import ScoreSaberUtils


class ScoreRepository(Repository[Score]):

    def get_by_id(self, entry_id: int) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .all()

    def get_by_score_id(self, score_id: int) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .first()

    def get_by_song_hash(self, song_hash: str) -> Optional[Score]:
        return self._db.session.query(Score) \
            .filter(Score.song_hash == song_hash) \
            .first()

    def get_by_player_id_and_leaderboard_id(self, player_id: int, leaderboard_id: int) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .filter(Score.leaderboard_id == leaderboard_id) \
            .all()

    def get_all_by_score_id(self, score_id: int) -> Optional[List[Score]]:
        return self._db.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .all()

    def get_scores(self, scores: List[Score]):
        return self._db.session.query(Score) \
            .filter(Score.id.in_([score.id for score in scores])) \
            .all()

    # def get_leaderboard_id_by_hash(self, song_hash: str) -> Optional[int]:
    #     db_score = self._db.session.query(Score).filter(Score.song_hash == song_hash).first()
    #
    #     if db_score is not None:
    #         return db_score.leaderboard_id
    #
    #     return None

    def get_previous_score(self, score: Score) -> Optional[Score]:
        db_scores = self.get_all_by_score_id(score.score_id)
        previous_score = None

        for old_db_score in db_scores:
            if old_db_score.score >= score.score:
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
        return self._db.session.query(Score) \
            .filter(Score.player_id == player.id) \
            .filter(~Score.song.has()) \
            .all()

    def get_all_player_recent_scores(self, player_id: int) -> List[Score]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .all()

    def get_player_recent_score(self, player_id: int, index: int) -> Score:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .offset(index) \
            .first()

    def get_player_recent_scores(self, player_id: int, count: int) -> List[Score]:
        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .limit(count) \
            .all()

    def is_score_new(self, db_score: Score) -> bool:
        """Checks if the score already exists in the database by comparing scoreId and timeSet"""
        scores = self._db.session.query(Score) \
            .filter(Score.score_id == db_score.score_id) \
            .filter(Score.time_set == db_score.time_set) \
            .all()

        return 1 > len(scores)

    def update_score_pp_weight(self, db_score: Score, player_repo: PlayerRepository):
        player = player_repo.get_by_id(db_score.player_id)

        scores_with_more_pp = self._db.session.query(Score) \
            .filter(Score.player_id == player.id) \
            .filter(Score.score_id != db_score.score_id) \
            .order_by(Score.pp.desc()) \
            .filter(Score.pp >= db_score.pp) \
            .all()

        score_position = len(scores_with_more_pp) + 1
        new_pp_weight = ScoreSaberUtils.get_pp_weight_from_pos(score_position)

        db_score.weight = new_pp_weight

        return db_score
