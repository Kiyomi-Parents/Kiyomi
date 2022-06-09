from .presence_service import PresenceService
from ..storage import StorageUnitOfWork
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.presences = PresenceService(bot, storage_uow.presences, storage_uow)
