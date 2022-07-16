from kiyomi import Kiyomi
from .achievement import Achievements
from .achievement_api import AchievementsAPI
from .services import ServiceUnitOfWork
from .services.registry_service import RegistryService
from .services.user_achievement_service import UserAchievementService
from .storage.storage_unit_of_work import StorageUnitOfWork


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    await bot.add_cog(Achievements(bot, service_uow))
    await bot.add_cog(AchievementsAPI(bot, service_uow))
