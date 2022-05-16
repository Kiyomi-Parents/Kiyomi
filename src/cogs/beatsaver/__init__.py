import pybeatsaver

from src.kiyomi import Kiyomi
from .arg_resolvers import *
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .beatsaver_ui import BeatSaverUI
from .services import BeatmapService
from .storage import UnitOfWork


async def setup(bot: Kiyomi):
    beatsaver_api_client = pybeatsaver.BeatSaverAPI(bot.loop)
    await beatsaver_api_client.start()

    uow = UnitOfWork(await bot.database.get_session())
    
    bot.error_resolver.add(BeatmapHashResolver(uow))
    bot.error_resolver.add(BeatmapKeyResolver(uow))

    beatmap_service = BeatmapService(bot, uow, beatsaver_api_client)

    await bot.add_cog(BeatSaver(bot, beatmap_service))
    await bot.add_cog(BeatSaverAPI(bot, beatmap_service, uow))
    await bot.add_cog(BeatSaverUI(bot, beatmap_service))
