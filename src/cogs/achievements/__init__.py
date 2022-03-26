from src.kiyomi import Kiyomi
from .achievements import Achievements
from .achievements_api import AchievementsAPI
from .actions import Actions
from .storage.unit_of_work import UnitOfWork


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot)
    achievements_actions = Actions(uow)

    bot.add_cog(Achievements(uow, achievements_actions))
    bot.add_cog(AchievementsAPI(uow, achievements_actions))
