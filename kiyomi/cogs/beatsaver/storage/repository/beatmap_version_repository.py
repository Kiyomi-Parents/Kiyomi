import logging
from typing import Optional, List, Type

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from kiyomi.database.base_cacheable_repository import BaseCacheableRepository
from ..model.beatmap_version import BeatmapVersion

_logger = logging.getLogger(__name__)

class BeatmapVersionRepository(BaseCacheableRepository[BeatmapVersion]):
    @property
    def _table(self) -> Type[BeatmapVersion]:
        return BeatmapVersion

    async def get_by_hash(self, beatmap_hash: str) -> Optional[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.hash == beatmap_hash)
            .where(self._table.cached_at >= self._expire_threshold)
        )

        return await self._first(stmt)

    async def get_all_by_hashes(self, beatmap_hashes: List[str]) -> List[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.hash.in_(beatmap_hashes))
            .where(self._table.cached_at >= self._expire_threshold)
        )

        return await self._all(stmt)

    async def get_by_key(self, beatmap_key: str) -> Optional[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.key == beatmap_key)
            .where(self._table.cached_at >= self._expire_threshold)
        )

        return await self._first(stmt)

    async def get_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        stmt = (
            select(self._table.c.hash)
            .options(joinedload(BeatmapVersion.beatmap))
            .where(self._table.beatmap.id == beatmap_key)
            .where(self._table.cached_at >= self._expire_threshold)
        )
        return await self._first(stmt)
