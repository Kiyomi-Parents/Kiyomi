from typing import Optional, List

from sqlalchemy.orm import Query

from src.cogs.scoresaber.storage.model.score import Score
from src.database import BaseRepository
from ..model import SentScore


class SentScoreRepository(BaseRepository[SentScore]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(SentScore) \
            .filter(SentScore.id == entry_id)

    def get_all(self) -> Optional[List[SentScore]]:
        return self.session.query(SentScore) \
            .all()

    def get_by_score_id_and_guild_id(self, score_id: int, guild_id: int) -> Optional[SentScore]:
        return self.session.query(SentScore) \
            .filter(SentScore.score_id == score_id) \
            .filter(SentScore.guild_id == guild_id) \
            .first()

    def get_unsent_scores(self, guild_id: int, player_id: int) -> Optional[List[Score]]:
        player_score_ids = self.session.query(Score.id) \
            .filter(Score.player_id == player_id) \
            .subquery()

        sent_score_ids = self.session.query(SentScore.score_id) \
            .filter(SentScore.guild_id == guild_id) \
            .filter(SentScore.score_id.in_(player_score_ids.select())) \
            .subquery()

        return self.session.query(Score) \
            .filter(Score.player_id == player_id) \
            .filter(Score.id.not_in(sent_score_ids.select())) \
            .all()
