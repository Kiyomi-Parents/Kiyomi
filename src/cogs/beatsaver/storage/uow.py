from pybeatsaver import BeatSaverAPI

from Kiyomi import Kiyomi
from .repository.beatmap_repository import BeatmapRepository
from .repository.beatmap_version_repository import BeatmapVersionRepository


class UnitOfWork:
    def __init__(self, bot: Kiyomi, beatsaver: BeatSaverAPI = None):
        self.beatmap_repo = BeatmapRepository(bot.database)
        self.beatmap_version_repo = BeatmapVersionRepository(bot.database)

        if beatsaver is None:
            self.beatsaver = BeatSaverAPI()
        else:
            self.beatsaver = beatsaver

        self.bot = bot
