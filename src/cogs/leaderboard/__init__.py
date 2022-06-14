from src.kiyomi import Kiyomi
from .leaderboard import Leaderboard
from .leaderboard_api import LeaderboardAPI
from .leaderboard_ui import LeaderboardUI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    await bot.add_cog(Leaderboard(bot, service_uow))
    await bot.add_cog(LeaderboardAPI(bot, service_uow))
    await bot.add_cog(LeaderboardUI(bot, service_uow))
