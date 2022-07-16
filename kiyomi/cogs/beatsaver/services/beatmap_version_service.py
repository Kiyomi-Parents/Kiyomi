from typing import Optional

from ..storage import StorageUnitOfWork
from ..storage.model.beatmap_version import BeatmapVersion
from ..storage.repository.beatmap_version_repository import BeatmapVersionRepository
from kiyomi import BaseService


class BeatmapVersionService(BaseService[BeatmapVersion, BeatmapVersionRepository, StorageUnitOfWork]):
    async def get_by_hash(self, beatmap_hash: str) -> Optional[BeatmapVersion]:
        return await self.repository.get_by_hash(beatmap_hash)
