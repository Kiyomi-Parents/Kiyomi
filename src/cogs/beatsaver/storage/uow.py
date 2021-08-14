from pybeatsaver import BeatSaver

from Kiyomi import Kiyomi
from .repository.beatmap_repository import BeatmapRepository


class UnitOfWork:
    def __init__(self, bot: Kiyomi, beatsaver: BeatSaver = None):
        self.beatmap_repo = BeatmapRepository(bot.database)

        if beatsaver is None:
            self.beatsaver = BeatSaver()
        else:
            self.beatsaver = beatsaver

        self.bot = bot
