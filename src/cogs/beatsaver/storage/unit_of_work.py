from sqlalchemy.ext.asyncio import AsyncSession

from .repository.beatmap_repository import BeatmapRepository
from .repository.beatmap_version_difficulty_repository import (
    BeatmapVersionDifficultyRepository,
)
from .repository.beatmap_version_repository import BeatmapVersionRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

        self.beatmaps = BeatmapRepository(session)
        self.beatmap_versions = BeatmapVersionRepository(session)
        self.beatmap_version_difficulties = BeatmapVersionDifficultyRepository(session)
