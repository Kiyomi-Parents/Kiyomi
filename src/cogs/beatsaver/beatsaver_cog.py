from .services import BeatmapService
from src.kiyomi import BaseCog, Kiyomi


class BeatSaverCog(BaseCog):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService):
        super().__init__(bot)

        self.beatmap_service = beatmap_service
