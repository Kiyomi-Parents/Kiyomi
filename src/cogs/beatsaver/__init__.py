import pybeatsaver

from src.kiyomi import Kiyomi
from .arg_resolvers import *
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .beatsaver_ui import BeatSaverUI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork


async def setup(bot: Kiyomi):
    beatsaver_api_client = pybeatsaver.BeatSaverAPI(bot.loop)
    await beatsaver_api_client.start()

    storage_uow = StorageUnitOfWork(await bot.database.get_session())
    service_uow = ServiceUnitOfWork(bot, storage_uow, beatsaver_api_client)

    bot.error_resolver.add(BeatmapHashResolver(storage_uow))
    bot.error_resolver.add(BeatmapKeyResolver(storage_uow))

    await bot.add_cog(BeatSaver(bot, service_uow))
    await bot.add_cog(BeatSaverAPI(bot, service_uow))
    await bot.add_cog(BeatSaverUI(bot, service_uow))
