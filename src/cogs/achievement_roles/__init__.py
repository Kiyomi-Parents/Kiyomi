from .achievement_roles import AchievementRoles
from .storage.uow import UnitOfWork
from .tasks import Tasks
from src.kiyomi import Kiyomi


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot)
    achievement_role_tasks = Tasks(uow)

    if not bot.running_tests:
        achievement_role_tasks.update_member_roles.start()

    bot.add_cog(AchievementRoles(uow, achievement_role_tasks))
