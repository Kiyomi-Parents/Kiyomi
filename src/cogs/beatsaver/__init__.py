import pybeatsaver

from src.kiyomi import Kiyomi
from .arg_resolvers import *
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .beatsaver_ui import BeatSaverUI
from .services import BeatmapService, BeatmapAutocompleteService
from .storage import UnitOfWork


async def setup(bot: Kiyomi):
    beatsaver_api_client = pybeatsaver.BeatSaverAPI(bot.loop)
    uow = UnitOfWork(bot.database.session)
    
    bot.error_resolver.add(BeatmapHashResolver(uow))
    bot.error_resolver.add(BeatmapKeyResolver(uow))

    beatmap_service = BeatmapService(bot, uow, beatsaver_api_client)
    beatmap_autocomplete_service = BeatmapAutocompleteService(bot, uow, beatsaver_api_client, beatmap_service)

    await bot.add_cog(BeatSaver(bot, beatmap_service, beatmap_autocomplete_service))
    await bot.add_cog(BeatSaverAPI(bot, beatmap_service, beatmap_autocomplete_service, uow))
    await bot.add_cog(BeatSaverUI(bot, beatmap_service, beatmap_autocomplete_service))
