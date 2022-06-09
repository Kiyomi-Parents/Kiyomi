from typing import Optional, List, Type

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..model.beatmap_version import BeatmapVersion
from src.kiyomi.database import BaseStorageRepository


class BeatmapVersionRepository(BaseStorageRepository[BeatmapVersion]):
    @property
    def _table(self) -> Type[BeatmapVersion]:
        return BeatmapVersion

    async def get_by_hash(self, beatmap_hash: str) -> Optional[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.hash == beatmap_hash)
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties),
            )
        )

        return await self._first(stmt)

    async def get_all_by_hashes(self, beatmap_hashes: List[str]) -> List[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.hash.in_(beatmap_hashes))
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties),
            )
        )

        return await self._all(stmt)

    async def get_by_key(self, beatmap_key: str) -> Optional[BeatmapVersion]:
        stmt = (
            select(self._table)
            .where(self._table.key == beatmap_key)
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties),
            )
        )

        return await self._first(stmt)

    async def get_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        stmt = (
            select(self._table.c.hash)
            .options(joinedload(BeatmapVersion.beatmap))
            .where(self._table.beatmap.id == beatmap_key)
        )
        return await self._first(stmt)
