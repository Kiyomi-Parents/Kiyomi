from sqlalchemy.orm import Session

from src.database import BaseUnitOfWork
from .repository import BeatmapRepository, BeatmapVersionRepository


class UnitOfWork(BaseUnitOfWork):
    def __init__(self, session: Session):
        super().__init__(session)

        self.beatmap_repo = BeatmapRepository(session)
        self.beatmap_version_repo = BeatmapVersionRepository(session)
