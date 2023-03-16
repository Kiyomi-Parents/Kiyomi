import logging
from typing import Optional, Type

import pybeatsaver
from sqlalchemy import select

from kiyomi.cogs.beatsaver.storage.model.beatmap_version_difficulty import (
    BeatmapVersionDifficulty,
)
from kiyomi.database.base_cacheable_repository import BaseCacheableRepository

_logger = logging.getLogger(__name__)

class BeatmapVersionDifficultyRepository(BaseCacheableRepository[BeatmapVersionDifficulty]):
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
            .where(self._table.cached_at >= self._expire_threshold)
        )
        return await self._first(stmt)
