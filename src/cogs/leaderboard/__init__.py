from .actions import Actions
from .leaderboard_api import LeaderboardAPI
from .storage.uow import UnitOfWork
from .leaderboard import Leaderboard


def setup(bot):
    uow = UnitOfWork(bot)
    leaderboard_actions = Actions(uow)

    bot.add_cog(Leaderboard(uow, leaderboard_actions))
    bot.add_cog(LeaderboardAPI(uow, leaderboard_actions))
