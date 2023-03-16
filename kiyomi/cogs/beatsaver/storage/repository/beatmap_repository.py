import logging
from typing import List, Type

from sqlalchemy import select

from kiyomi.database.base_cacheable_repository import BaseCacheableRepository
from ..model.beatmap import Beatmap

_logger = logging.getLogger(__name__)

class BeatmapRepository(BaseCacheableRepository[Beatmap]):
    @property
    def _table(self) -> Type[Beatmap]:
        return Beatmap

    async def get_all_by_ids(self, beatmap_keys: List[str]) -> List[Beatmap]:
        stmt = (
            select(self._table)
            .where(self._table.id.in_(beatmap_keys))
            .where(self._table.cached_at >= self._expire_threshold)
        )
        return await self._all(stmt)
