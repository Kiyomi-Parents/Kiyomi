from src.kiyomi import Kiyomi
from .leaderboard import Leaderboard
from .leaderboard_api import LeaderboardAPI
from .services.player_leaderboard_service import PlayerLeaderboardService
from .storage.unit_of_work import UnitOfWork


def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    player_leaderboard_service = PlayerLeaderboardService(bot, uow)

    bot.add_cog(Leaderboard(bot, player_leaderboard_service))
    bot.add_cog(LeaderboardAPI(bot, player_leaderboard_service, uow))
