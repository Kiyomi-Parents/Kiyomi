from datetime import datetime, timedelta
from typing import Optional, Type

import pyscoresaber
from sqlalchemy import select, exists
from sqlalchemy.orm import raiseload

from kiyomi.database.base_cacheable_repository import BaseCacheableRepository
from ..model.leaderboard import Leaderboard


class LeaderboardRepository(BaseCacheableRepository[Leaderboard]):
    @property
    def _table(self) -> Type[Leaderboard]:
        return Leaderboard

    @property
    def _expire_threshold(self) -> datetime:
        return datetime.today() - timedelta(days=7)

    async def get_by_song_hash(
        self,
        song_hash: str,
        song_game_mode: pyscoresaber.GameMode,
        song_difficulty: pyscoresaber.BeatmapDifficulty,
    ) -> Optional[Leaderboard]:
        stmt = (
            select(self._table)
            .where(self._table.song_hash == song_hash)
            .where(self._table.game_mode == song_game_mode.name)
            .where(self._table.difficulty == song_difficulty.name)
            .where(self._table.cached_at >= self._expire_threshold)
            .options(
                    raiseload(self._table.beatmap_version)
            )
        )
        return await self._first(stmt)

    async def exists_by_song_hash(
        self,
        song_hash: str,
        song_game_mode: pyscoresaber.GameMode,
        song_difficulty: pyscoresaber.BeatmapDifficulty,
    ) -> bool:
        stmt = (
            select(self._table)
            .where(self._table.song_hash == song_hash)
            .where(self._table.game_mode == song_game_mode.name)
            .where(self._table.difficulty == song_difficulty.name)
            .where(self._table.cached_at >= self._expire_threshold)
            .options(
                    raiseload(self._table.beatmap_version)
            )
        )
        stmt = exists(stmt).select()
        result = await self._execute_scalars(stmt)
        return result.one()
