from pybeatsaver import BeatSaverAPI

from .beatmap_version_service import BeatmapVersionService
from ..storage import StorageUnitOfWork
from .beatmap_service import BeatmapService
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork, beatsaver: BeatSaverAPI):
        super().__init__(storage_uow)

        self.beatmaps = BeatmapService(bot, storage_uow.beatmaps, storage_uow, beatsaver)
        self.beatmap_versions = BeatmapVersionService(bot, storage_uow.beatmap_versions, storage_uow)
