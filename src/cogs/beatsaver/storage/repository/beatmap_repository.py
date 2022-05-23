from typing import List, Type

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..model.beatmap import Beatmap
from src.kiyomi.database import BaseRepository
from ..model.beatmap_version import BeatmapVersion


class BeatmapRepository(BaseRepository[Beatmap]):
    @property
    def _table(self) -> Type[Beatmap]:
        return Beatmap

    async def get_all_by_ids(self, beatmap_keys: List[str]) -> List[Beatmap]:
        stmt = (
            select(self._table)
            .where(self._table.id.in_(beatmap_keys))
            .options(joinedload(Beatmap.versions).joinedload(BeatmapVersion.difficulties))
        )
        return await self._all(stmt)
