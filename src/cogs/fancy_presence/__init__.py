from .fancy_presence import FancyPresence
from .fancy_presence_api import FancyPresenceAPI
from .services import ServiceUnitOfWork
from .storage.storage_unit_of_work import StorageUnitOfWork
from src.kiyomi import Kiyomi


async def setup(bot: Kiyomi):
    storage_uow = StorageUnitOfWork(bot.database.session)
    service_uow = ServiceUnitOfWork(bot, storage_uow)

    await bot.add_cog(FancyPresence(bot, service_uow))
    await bot.add_cog(FancyPresenceAPI(bot, service_uow))
