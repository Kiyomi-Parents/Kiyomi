from .registry_service import RegistryService
from .user_achievement_service import UserAchievementService
from ..storage import StorageUnitOfWork
from kiyomi import BaseServiceUnitOfWork, Kiyomi


class ServiceUnitOfWork(BaseServiceUnitOfWork[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork):
        super().__init__(storage_uow)

        self.registry = RegistryService(bot, storage_uow)
        self.user_achievements = UserAchievementService(bot, storage_uow, self.registry)
