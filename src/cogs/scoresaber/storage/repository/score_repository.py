from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Query

from src.kiyomi.database import BaseRepository
from ..model.score import Score


class ScoreRepository(BaseRepository[Score]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Score) \
            .filter(Score.id == entry_id)

    def get_all(self) -> Optional[List[Score]]:
        return self.session.query(Score) \
            .all()

    def get_by_score_id(self, score_id: int) -> Optional[Score]:
        return self.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .first()

    def get_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> Optional[List[Score]]:
        return self.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .filter(Score.leaderboard_id == leaderboard_id) \
            .all()

    def get_all_by_score_id(self, score_id: int) -> Optional[List[Score]]:
        return self.session.query(Score) \
            .filter(Score.score_id == score_id) \
            .all()

    def get_scores(self, scores: List[Score]):
        return self.session.query(Score) \
            .filter(Score.id.in_([score.id for score in scores])) \
            .all()

    def get_previous_score(self, score: Score) -> Optional[Score]:
        db_scores = self.get_all_by_score_id(score.score_id)
        previous_score = None

        for old_db_score in db_scores:
            if old_db_score.modified_score >= score.modified_score:
                continue

            if previous_score is None:
                previous_score = old_db_score
                continue

            if old_db_score.modified_score > previous_score.modified_score:
                previous_score = old_db_score

        return previous_score

    def get_player_scores(self, player):
        return self.session.query(Score).filter(Score.player_id == player.id).all()

    def get_all_player_recent_scores(self, player_id: str) -> List[Score]:
        return self.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .all()

    def get_player_recent_scores(self, player_id: str, count: int) -> List[Score]:
        return self.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.time_set.desc()) \
            .limit(count) \
            .all()

    def exists_by_score_id_and_time_set(self, score_id: int, time_set: datetime) -> bool:
        return self.session.query(Score) \
                   .filter(Score.score_id == score_id) \
                   .filter(Score.time_set == time_set) \
                   .first() is not None

    def get_player_scores_sorted_by_pp(self, player_id: str) -> List[Score]:
        return self.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .order_by(Score.pp.desc()) \
            .all()
