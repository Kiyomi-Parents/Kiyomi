import re
from typing import Optional, TYPE_CHECKING

from kiyomi import Kiyomi
from kiyomi.service.base_basic_service import BaseBasicService
from .beatmap_service import BeatmapService
from ..storage import StorageUnitOfWork
from ..storage.model.beatmap import Beatmap

if TYPE_CHECKING:
    from ...scoresaber.storage.model.leaderboard import Leaderboard


class TextToBeatmapService(BaseBasicService[StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, storage_uow: StorageUnitOfWork, beatmaps: BeatmapService):
        super().__init__(bot, storage_uow)
        self.beatmaps = beatmaps

    async def get_beatmap_from_text(self, text: str) -> Optional[Beatmap]:
        for get_beatmap in (
            self._beatmap_from_scoresaber,
            self._beatmap_from_bsr
        ):
            beatmap = await get_beatmap(text)
            if beatmap is not None:
                return beatmap

    async def _beatmap_from_scoresaber(self, text: str) -> Optional[Beatmap]:
        scoresaber_leaderboard_pattern = r"(https://)?scoresaber\.com/leaderboard/(\d+)"
        scoresaber_match = re.match(scoresaber_leaderboard_pattern, text)

        if scoresaber_match:
            leaderboard_id = scoresaber_match.group(2)
            async with self.bot.get_cog_api("ScoreSaberAPI") as scoresaber:
                leaderboard: Optional["Leaderboard"] = await scoresaber.get_leaderboard_by_id(leaderboard_id)
            if leaderboard is not None:
                return await self.beatmaps.get_beatmap_by_hash(leaderboard.song_hash)

    async def _beatmap_from_bsr(self, text: str) -> Optional[Beatmap]:
        bsr_pattern = r"((https://)?beatsaver\.com/maps/|!bsr )([\dA-Fa-f]+)"
        bsr_match = re.match(bsr_pattern, text)

        if bsr_match:
            map_key = bsr_match.group(3)
            return await self.beatmaps.get_beatmap_by_key(map_key)
