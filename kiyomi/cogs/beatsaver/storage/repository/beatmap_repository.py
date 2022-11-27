from typing import List, Type

from sqlalchemy import select

from ..model.beatmap import Beatmap
from kiyomi.database import BaseStorageRepository


class BeatmapRepository(BaseStorageRepository[Beatmap]):
    @property
    def _table(self) -> Type[Beatmap]:
        return Beatmap

    async def get_all_by_ids(self, beatmap_keys: List[str]) -> List[Beatmap]:
        stmt = (
            select(self._table)
            .where(self._table.id.in_(beatmap_keys))
        )
        return await self._all(stmt)
