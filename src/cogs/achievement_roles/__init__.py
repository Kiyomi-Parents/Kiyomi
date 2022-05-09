from src.kiyomi import Kiyomi
from .achievement_roles import AchievementRoles
from .services import MemberAchievementRoleService
from .storage import UnitOfWork
from .tasks import Tasks


async def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    member_service = MemberAchievementRoleService(bot, uow)

    achievement_role_tasks = Tasks(bot, member_service)

    if not bot.running_tests:
        achievement_role_tasks.update_member_roles.start()

    await bot.add_cog(AchievementRoles(bot, member_service))
