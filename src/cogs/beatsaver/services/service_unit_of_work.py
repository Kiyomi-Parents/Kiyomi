from pybeatsaver import BeatSaverAPI

from ..storage import StorageUnitOfWork
from .beatmap_service import BeatmapService
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork, beatsaver: BeatSaverAPI):
        super().__init__(storage_uow)

        self.beatmaps = BeatmapService(bot, storage_uow.beatmaps, storage_uow, beatsaver)
