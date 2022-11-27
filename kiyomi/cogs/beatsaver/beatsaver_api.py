import logging
from typing import Optional

import pybeatsaver

from kiyomi import BaseCog
from .services import ServiceUnitOfWork
from .storage.model.beatmap import Beatmap
from .storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty

_logger = logging.getLogger(__name__)


class BeatSaverAPI(BaseCog[ServiceUnitOfWork]):
    def register_events(self):
        pass

    async def get_beatmap_by_key(self, key: str) -> Optional[Beatmap]:
        beatmap = await self._service_uow.beatmaps.get_beatmap_by_key(key)
        await self._service_uow.save_changes()

        return await self._service_uow.refresh(beatmap)

    async def get_beatmap_by_hash(self, beatmap_hash: str) -> Optional[Beatmap]:
        beatmap = await self._service_uow.beatmaps.get_beatmap_by_hash(beatmap_hash)
        await self._service_uow.save_changes()

        return await self._service_uow.refresh(beatmap)

    async def get_beatmap_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        beatmap = await self._service_uow.beatmaps.get_beatmap_hash_by_key(beatmap_key)
        await self._service_uow.save_changes()

        return await self._service_uow.refresh(beatmap)

    async def get_beatmap_difficulty_by_key(
        self,
        beatmap_key: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> Optional[BeatmapVersionDifficulty]:
        beatmap_hash = await self._service_uow.beatmaps.get_beatmap_hash_by_key(beatmap_key)

        beatmap_version_difficulty = await self._service_uow.beatmaps.get_beatmap_difficulty(
            beatmap_hash, characteristic, difficulty
        )

        await self._service_uow.save_changes()

        return await self._service_uow.refresh(beatmap_version_difficulty)

    async def get_beatmap_difficulty_by_hash(
        self,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> Optional[BeatmapVersionDifficulty]:
        beatmap_version_difficulty = await self._service_uow.beatmaps.get_beatmap_difficulty(
            beatmap_hash, characteristic, difficulty
        )

        await self._service_uow.save_changes()

        return await self._service_uow.refresh(beatmap_version_difficulty)
