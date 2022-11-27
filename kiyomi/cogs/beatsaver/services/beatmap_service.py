from typing import List

import pybeatsaver
from pybeatsaver import BeatSaverAPI

from kiyomi import BaseService, Kiyomi
from ..storage import StorageUnitOfWork
from ..errors import BeatmapHashNotFound, BeatmapKeyNotFound, BeatmapDifficultyNotFound
from ..storage.model.beatmap import Beatmap
from ..storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from ..storage.repository.beatmap_repository import BeatmapRepository


class BeatmapService(BaseService[Beatmap, BeatmapRepository, StorageUnitOfWork]):
    def __init__(self, bot: Kiyomi, repository: BeatmapRepository, storage_uow: StorageUnitOfWork, beatsaver: BeatSaverAPI):
        super().__init__(bot, repository, storage_uow)

        self.beatsaver = beatsaver

    async def get_missing_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        try:
            beatmaps = []

            async for map_detail in self.beatsaver.beatmaps_by_keys(beatmap_keys):
                beatmaps.append(Beatmap(map_detail))

            return await self.repository.add_all(beatmaps)
        except pybeatsaver.NotFoundException as error:
            raise BeatmapKeyNotFound(error.url.split("/")[-1]) from error

    async def get_missing_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        try:
            map_detail = await self.beatsaver.beatmap(beatmap_key)

            return await self.repository.add(Beatmap(map_detail))
        except pybeatsaver.NotFoundException as error:
            raise BeatmapKeyNotFound(error.url.split("/")[-1]) from error

    async def get_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps = await self.repository.get_all_by_ids(beatmap_keys)
        missing_beatmaps_keys = beatmap_keys.copy()

        for beatmap in beatmaps:
            for beatmap_version in beatmap.versions:
                if beatmap_version.key in missing_beatmaps_keys:
                    missing_beatmaps_keys.remove(beatmap_version.key)

        beatmaps += await self.get_missing_beatmaps_by_keys(missing_beatmaps_keys)

        return beatmaps

    async def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap = await self.repository.get_by_id(beatmap_key)

        if beatmap is None:
            return await self.get_missing_beatmap_by_key(beatmap_key)

        return beatmap

    async def get_missing_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        try:
            beatmaps = []

            async for map_details in self.beatsaver.beatmaps_by_hashes_all(beatmap_hashes):
                new_beatmaps = [Beatmap(map_detail) for map_detail in map_details]

                await self.repository.add_all(new_beatmaps)

                beatmaps += new_beatmaps

            return beatmaps
        except pybeatsaver.NotFoundException as error:
            raise BeatmapHashNotFound(error.url.split("/")[-1]) from error

    async def get_missing_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        try:
            map_detail = await self.beatsaver.beatmap_by_hash(beatmap_hash)
            new_beatmap = Beatmap(map_detail)

            await self.repository.add(new_beatmap.latest_version)

            return new_beatmap
        except pybeatsaver.NotFoundException as error:
            raise BeatmapHashNotFound(error.url.split("/")[-1]) from error

    async def get_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps = []

        beatmap_versions = await self.storage_uow.beatmap_versions.get_all_by_hashes(beatmap_hashes)
        missing_beatmaps_hashes = beatmap_hashes.copy()

        for beatmap_version in beatmap_versions:
            if beatmap_version.hash in missing_beatmaps_hashes:
                missing_beatmaps_hashes.remove(beatmap_version.hash)
                beatmaps.append(beatmap_version.beatmap)

        beatmaps += await self.get_missing_beatmaps_by_hashes(missing_beatmaps_hashes)

        return beatmaps

    async def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap_version = await self.storage_uow.beatmap_versions.get_by_hash(beatmap_hash)

        if beatmap_version is None:
            return await self.get_missing_beatmap_by_hash(beatmap_hash)

        return beatmap_version.beatmap

    async def get_beatmap_hash_by_key(self, beatmap_key: str) -> str:
        beatmap_hash = await self.storage_uow.beatmap_versions.get_hash_by_key(beatmap_key)

        if beatmap_hash is None:
            beatmap = await self.get_beatmap_by_key(beatmap_key)
            beatmap_hash = beatmap.latest_version.hash

        return beatmap_hash

    async def get_beatmap_difficulty(
        self,
        beatmap_hash: str,
        characteristic: pybeatsaver.ECharacteristic,
        difficulty: pybeatsaver.EDifficulty,
    ) -> BeatmapVersionDifficulty:
        beatmap_difficulty = (
            await self.storage_uow.beatmap_version_difficulties.get_by_hash_and_characteristic_and_difficulty(
                beatmap_hash, characteristic, difficulty
            )
        )

        if beatmap_difficulty is not None:
            return beatmap_difficulty

        new_beatmap = await self.get_beatmap_by_hash(beatmap_hash)

        for new_version in new_beatmap.versions:
            if new_version.hash is not beatmap_hash:
                continue

            for new_difficulty in new_version.difficulties:
                if new_difficulty.characteristic is not characteristic:
                    continue

                if new_difficulty.difficulty is not difficulty:
                    continue

                return new_difficulty

        raise BeatmapDifficultyNotFound(beatmap_hash, characteristic, difficulty)

    async def add(self, beatmap: Beatmap) -> Beatmap:
        self.repository.exists(beatmap.id)

        return await self.repository.add(beatmap)
