from src.kiyomi import Kiyomi
from .achievement import Achievements
from .achievement_api import AchievementsAPI
from .services.registry_service import RegistryService
from .services.user_achievement_service import UserAchievementService
from .storage.unit_of_work import UnitOfWork


async def setup(bot: Kiyomi):
    uow = UnitOfWork(await bot.database.get_session())

    registry_service = RegistryService(bot, uow)
    user_achievement_service = UserAchievementService(bot, uow, registry_service)

    await bot.add_cog(Achievements(bot, user_achievement_service))
    await bot.add_cog(AchievementsAPI(bot, user_achievement_service))
