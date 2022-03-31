from typing import Optional

import pybeatsaver

from src.kiyomi import Kiyomi
from src.log import Logger
from .services import BeatmapAutocompleteService
from .beatsaver_cog import BeatSaverCog
from .errors import SongNotFound
from .services import BeatmapService
from .storage import UnitOfWork
from .storage.model.beatmap import Beatmap
from .storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty


class BeatSaverAPI(BeatSaverCog):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService, beatmap_autocomplete_service: BeatmapAutocompleteService, uow: UnitOfWork):
        super().__init__(bot, beatmap_service, beatmap_autocomplete_service)

        self.uow = uow

    async def get_beatmap_by_key(self, key: str) -> Optional[Beatmap]:
        try:
            return await self.beatmap_service.get_beatmap_by_key(key)
        except SongNotFound as error:
            Logger.log(self.__class__.__name__, error)
            return None

    async def get_beatmap_difficulty_by_beatmap_key(self, beatmap_key: str, characteristic: pybeatsaver.ECharacteristic, difficulty: pybeatsaver.EDifficulty) -> Optional[BeatmapVersionDifficulty]:
        beatmap = await self.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            return None

        return self.get_beatmap_difficulty_by_beatmap(beatmap, characteristic, difficulty)

    @staticmethod
    def get_beatmap_difficulty_by_beatmap(beatmap: Beatmap, characteristic: pybeatsaver.ECharacteristic, difficulty: pybeatsaver.EDifficulty) -> Optional[BeatmapVersionDifficulty]:
        for beatmap_difficulty in beatmap.latest_version.difficulties:
            if beatmap_difficulty.characteristic is not characteristic:
                continue

            if beatmap_difficulty.difficulty is not difficulty:
                continue

            return beatmap_difficulty

        return None
