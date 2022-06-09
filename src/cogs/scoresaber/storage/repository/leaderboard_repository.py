from typing import Optional, Type

import pyscoresaber
from sqlalchemy import select

from ..model.leaderboard import Leaderboard
from src.kiyomi.database import BaseStorageRepository


class LeaderboardRepository(BaseStorageRepository[Leaderboard]):
    @property
    def _table(self) -> Type[Leaderboard]:
        return Leaderboard

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
        )
        return await self._first(stmt)
