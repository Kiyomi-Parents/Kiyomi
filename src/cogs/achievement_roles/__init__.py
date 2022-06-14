from src.kiyomi import Kiyomi
from .achievement_roles import AchievementRoles
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork
from .tasks import Tasks


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    achievement_role_tasks = Tasks(bot, service_uow)
    achievement_role_tasks.update_member_roles.start()

    await bot.add_cog(AchievementRoles(bot, service_uow))
