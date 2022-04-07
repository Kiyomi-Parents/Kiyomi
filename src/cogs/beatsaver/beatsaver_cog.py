from src.kiyomi import BaseCog, Kiyomi
from .services import BeatmapAutocompleteService
from .services import BeatmapService


class BeatSaverCog(BaseCog):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService, beatmap_autocomplete_service: BeatmapAutocompleteService):
        super().__init__(bot)

        self.beatmap_service = beatmap_service
        self.beatmap_autocomplete_service = beatmap_autocomplete_service
