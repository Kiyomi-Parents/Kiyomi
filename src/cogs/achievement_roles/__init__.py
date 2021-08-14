from .achievement_roles import AchievementRoles
from .storage.uow import UnitOfWork
from .tasks import Tasks


def setup(bot):
    uow = UnitOfWork(bot)
    achievement_role_tasks = Tasks(uow)

    achievement_role_tasks.update_member_roles.start()

    bot.add_cog(AchievementRoles(uow, achievement_role_tasks))
