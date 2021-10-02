from typing import Optional, List

from src.cogs.scoresaber.storage.model.score import Score
from src.database import Repository
from ..model import SentScore


class SentScoreRepository(Repository):
    def get_by_id(self, entry_id: int) -> Optional[SentScore]:
        return self._db.session.query(SentScore) \
            .filter(SentScore.id == entry_id) \
            .first()

    def get_all(self) -> Optional[List[SentScore]]:
        return self._db.session.query(SentScore) \
            .all()

    def get_by_score_id_and_guild_id(self, score_id: int, guild_id: int) -> Optional[SentScore]:
        return self._db.session.query(SentScore) \
            .filter(SentScore.score_id == score_id) \
            .filter(SentScore.guild_id == guild_id) \
            .first()

    def get_unsent_scores(self, guild_id: int, player_id: int) -> Optional[List[Score]]:
        player_score_ids = self._db.session.query(Score.id) \
            .filter(Score.player_id == player_id) \
            .subquery()

        sent_score_ids = self._db.session.query(SentScore.score_id) \
            .filter(SentScore.guild_id == guild_id) \
            .filter(SentScore.score_id.in_(player_score_ids.select())) \
            .subquery()

        return self._db.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .filter(Score.id.not_in(sent_score_ids.select())) \
            .all()
