from typing import Optional

from src.kiyomi import Kiyomi
from src.log import Logger
from .beatsaver_cog import BeatSaverCog
from .errors import SongNotFound
from .services import BeatmapService
from .storage import UnitOfWork
from .storage.model.beatmap import Beatmap


class BeatSaverAPI(BeatSaverCog):
    def __init__(self, bot: Kiyomi, beatmap_service: BeatmapService, uow: UnitOfWork):
        super().__init__(bot, beatmap_service)

        self.uow = uow

    async def get_beatmap_by_key(self, key: str) -> Optional[Beatmap]:
        try:
            return await self.beatmap_service.get_beatmap_by_key(key)
        except SongNotFound as error:
            Logger.log(self.__class__.__name__, error)
            return None
