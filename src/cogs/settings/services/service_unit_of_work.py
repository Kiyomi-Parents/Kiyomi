from .setting_service import SettingService
from ..storage import StorageUnitOfWork
from src.kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.settings = SettingService(bot, storage_uow.settings_repo, storage_uow)
