from .fancy_presence import FancyPresence
from .fancy_presence_api import FancyPresenceAPI
from .services.presence_service import PresenceService
from .storage.unit_of_work import UnitOfWork
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    uow = UnitOfWork(bot.database.session)

    presence_service = PresenceService(bot, uow)

    await bot.add_cog(FancyPresence(bot, presence_service))
    await bot.add_cog(FancyPresenceAPI(bot, presence_service))
