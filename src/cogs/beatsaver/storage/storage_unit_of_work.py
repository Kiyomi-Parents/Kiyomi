from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from .repository.beatmap_repository import BeatmapRepository
from .repository.beatmap_version_difficulty_repository import (
    BeatmapVersionDifficultyRepository,
)
from .repository.beatmap_version_repository import BeatmapVersionRepository
from src.kiyomi import BaseStorageUnitOfWork


class StorageUnitOfWork(BaseStorageUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.beatmaps = BeatmapRepository(self._session)
        self.beatmap_versions = BeatmapVersionRepository(self._session)
        self.beatmap_version_difficulties = BeatmapVersionDifficultyRepository(self._session)
