from typing import Optional, Type

import pybeatsaver
from sqlalchemy import select

from src.cogs.beatsaver.storage.model.beatmap_version_difficulty import (
    BeatmapVersionDifficulty,
)
from src.kiyomi import BaseRepository


class BeatmapVersionDifficultyRepository(BaseRepository[BeatmapVersionDifficulty]):
    @property
    def _table(self) -> Type[BeatmapVersionDifficulty]:
        return BeatmapVersionDifficulty

    async def get_by_hash_and_characteristic_and_difficulty(
        self,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> Optional[BeatmapVersionDifficulty]:
        stmt = (
            select(self._table)
            .where(self._table.version_hash == beatmap_hash)
            .where(self._table.characteristic == characteristic.name)
            .where(self._table.difficulty == difficulty.name)
        )
        return await self._first(stmt)
