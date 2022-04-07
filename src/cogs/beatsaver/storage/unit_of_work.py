from sqlalchemy.orm import Session

from .repository.beatmap_repository import BeatmapRepository
from .repository.beatmap_version_repository import BeatmapVersionRepository
from src.kiyomi.database import BaseUnitOfWork


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)

        self.beatmap_repo = BeatmapRepository(session)
        self.beatmap_version_repo = BeatmapVersionRepository(session)
