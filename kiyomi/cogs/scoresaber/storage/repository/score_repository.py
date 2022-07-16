from datetime import datetime
from typing import Optional, List, Type

from sqlalchemy import select, desc, exists

from kiyomi.database import BaseStorageRepository
from ..model.score import Score


class ScoreRepository(BaseStorageRepository[Score]):
    @property
    def _table(self) -> Type[Score]:
        return Score

    async def get_by_score_id(self, score_id: int) -> Optional[Score]:
        stmt = select(self._table).where(self._table.score_id == score_id)
        return await self._first(stmt)

    async def get_all_by_player_id_and_leaderboard_id(self, player_id: str, leaderboard_id: int) -> List[Score]:
        stmt = (
            select(self._table).where(self._table.player_id == player_id).where(self._table.leaderboard_id == leaderboard_id)
        )
        return await self._all(stmt)

    async def get_previous(self, score: Score) -> Optional[Score]:
        stmt = (
            select(self._table)
            .where(self._table.score_id == score.score_id)
            .where(self._table.time_set < score.time_set)
            .order_by(desc(self._table.time_set))
            .limit(1)
        )
        return await self._first(stmt)

    async def get_recent(self, player_id: str, count: int) -> List[Score]:
        stmt = (
            select(self._table).where(self._table.player_id == player_id).order_by(desc(self._table.time_set)).limit(count)
        )
        return await self._all(stmt)

    async def exists_by_score_id_and_time_set(self, score_id: int, time_set: datetime) -> bool:
        stmt = select(self._table).where(self._table.score_id == score_id).where(self._table.time_set == time_set)
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()

    async def get_all_sorted_by_pp(self, player_id: str) -> List[Score]:
        stmt = select(self._table).where(self._table.player_id == player_id).order_by(desc(self._table.pp))
        return await self._all(stmt)