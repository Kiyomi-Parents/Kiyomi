from typing import Optional, List, Type

from sqlalchemy import select, desc

from ..model.sent_score import SentScore
from src.cogs.scoresaber.storage.model.score import Score
from src.kiyomi.database import BaseRepository


class SentScoreRepository(BaseRepository[SentScore]):
    @property
    def _table(self) -> Type[SentScore]:
        return SentScore

    async def get_by_score_id_and_guild_id(self, score_id: int, guild_id: int) -> Optional[SentScore]:
        stmt = select(self._table).where(self._table.score_id == score_id).where(self._table.guild_id == guild_id)
        return await self._first(stmt)

    async def get_sent_scores_count(self, guild_id: int, player_id: int) -> int:
        player_score_ids = select(Score.c.id).where(Score.player_id == player_id).subquery()

        stmt = (
            select(self._table.c.score_id)
            .where(self._table.guild_id == guild_id)
            .where(self._table.score_id.in_(player_score_ids.select()))
            .count()
        )

        return await self._first(stmt)

    async def get_unsent_scores_count(self, guild_id: int, player_id: int) -> int:
        player_score_ids = select(Score.c.id).where(Score.player_id == player_id).subquery()

        sent_score_ids = (
            select(self._table.c.score_id)
            .where(self._table.guild_id == guild_id)
            .where(self._table.score_id.in_(player_score_ids.select()))
            .subquery()
        )

        stmt = (
            select(Score)
            .where(Score.player_id == player_id)
            .where(Score.id.not_in(sent_score_ids.select()))
            .order_by(desc(Score.time_set))
            .count()
        )

        return await self._first(stmt)

    async def get_unsent_scores(self, guild_id: int, player_id: int) -> List[Score]:
        player_score_ids = select(Score.c.id).where(Score.player_id == player_id).subquery()

        sent_score_ids = (
            select(self._table.c.score_id)
            .where(self._table.guild_id == guild_id)
            .where(self._table.score_id.in_(player_score_ids.select()))
            .subquery()
        )

        stmt = (
            select(Score)
            .where(Score.player_id == player_id)
            .where(Score.id.not_in(sent_score_ids.select()))
            .order_by(desc(Score.time_set))
        )

        return await self._all(stmt)
