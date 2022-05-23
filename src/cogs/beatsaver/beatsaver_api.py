from typing import Optional

import pybeatsaver

from src.kiyomi import Kiyomi
from src.log import Logger
from .services import BeatmapService
from .beatsaver_cog import BeatSaverCog
from .errors import BeatmapNotFound
from .storage import UnitOfWork
from .storage.model.beatmap import Beatmap
from .storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty


class BeatSaverAPI(BeatSaverCog):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService, uow: UnitOfWork):
        super().__init__(bot, beatmap_service)

        self.uow = uow

    async def get_beatmap_by_key(self, key: str) -> Optional[Beatmap]:
        try:
            return await self.beatmap_service.get_beatmap_by_key(key)
        except BeatmapNotFound as error:
            Logger.log(self.__class__.__name__, error)
            return None

    async def get_beatmap_by_hash(self, beatmap_hash: str) -> Optional[Beatmap]:
        try:
            return await self.beatmap_service.get_beatmap_by_hash(beatmap_hash)
        except BeatmapNotFound as error:
            Logger.log(self.__class__.__name__, error)
            return None

    async def get_beatmap_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        return await self.beatmap_service.get_beatmap_hash_by_key(beatmap_key)

    async def get_beatmap_difficulty_by_key(
        self,
        beatmap_key: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> Optional[BeatmapVersionDifficulty]:
        beatmap_hash = await self.beatmap_service.get_beatmap_hash_by_key(beatmap_key)

        return await self.beatmap_service.get_beatmap_difficulty(beatmap_hash, characteristic, difficulty)

    async def get_beatmap_difficulty_by_hash(
        self,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> Optional[BeatmapVersionDifficulty]:
        return await self.beatmap_service.get_beatmap_difficulty(beatmap_hash, characteristic, difficulty)
