import pybeatsaver
import sentry_sdk

from kiyomi import Kiyomi
from .arg_resolvers import *
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .beatsaver_ui import BeatSaverUI
from .services import ServiceUnitOfWork
from .storage import StorageUnitOfWork


async def setup(bot: Kiyomi):
    with sentry_sdk.start_transaction(name="Beatsaver"):
        beatsaver_api_client = pybeatsaver.BeatSaverAPI(bot.loop)
        await beatsaver_api_client.start()

        storage_uow = StorageUnitOfWork(bot.database.session)
        service_uow = ServiceUnitOfWork(bot, storage_uow, beatsaver_api_client)

        bot.error_resolver.add(BeatmapHashResolver(service_uow))
        bot.error_resolver.add(BeatmapKeyResolver(service_uow))

        await bot.add_cog(BeatSaver(bot, service_uow))
        await bot.add_cog(BeatSaverAPI(bot, service_uow))
        await bot.add_cog(BeatSaverUI(bot, service_uow))
