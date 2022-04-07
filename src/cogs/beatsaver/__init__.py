import pybeatsaver

from src.kiyomi import Kiyomi
from .beatsaver import BeatSaver
from .beatsaver_api import BeatSaverAPI
from .services import BeatmapService, BeatmapAutocompleteService
from .storage import UnitOfWork


def setup(bot: Kiyomi):
    beatsaver_api_client = pybeatsaver.BeatSaverAPI(bot.loop)
    uow = UnitOfWork(bot.database.session)

    beatmap_service = BeatmapService(bot, uow, beatsaver_api_client)
    beatmap_autocomplete_service = BeatmapAutocompleteService(bot, uow, beatsaver_api_client, beatmap_service)

    bot.add_cog(BeatSaver(bot, beatmap_service, beatmap_autocomplete_service))
    bot.add_cog(BeatSaverAPI(bot, beatmap_service, beatmap_autocomplete_service, uow))
