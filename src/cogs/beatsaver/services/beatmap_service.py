from typing import List, Optional

import pybeatsaver

from .beatsaver_service import BeatSaverService
from ..errors import BeatmapHashNotFound, BeatmapKeyNotFound
from ..storage.model.beatmap import Beatmap
from ..storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty


class BeatmapService(BeatSaverService):

    async def get_missing_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps = []

        try:
            async for map_detail in self.beatsaver.beatmaps_by_keys(beatmap_keys):
                beatmaps.append(Beatmap(map_detail))
        except pybeatsaver.NotFoundException as error:
            raise BeatmapKeyNotFound(error.url.split("/")[-1]) from error

        self.uow.beatmaps.add_all(beatmaps)
        self.uow.save_changes()

        return beatmaps

    async def get_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps = self.uow.beatmaps.get_all_by_ids(beatmap_keys)
        missing_beatmaps_keys = beatmap_keys.copy()

        for beatmap in beatmaps:
            for beatmap_version in beatmap.versions:
                if beatmap_version.key in missing_beatmaps_keys:
                    missing_beatmaps_keys.remove(beatmap_version.key)

        beatmaps += await self.get_missing_beatmaps_by_keys(missing_beatmaps_keys)

        return beatmaps

    async def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap = self.uow.beatmaps.get_by_id(beatmap_key)

        if beatmap is None:
            return (await self.get_missing_beatmaps_by_keys([beatmap_key]))[0]

        return beatmap

    async def get_missing_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps = []

        try:
            async for map_details in self.beatsaver.beatmaps_by_hashes_all(beatmap_hashes):
                new_beatmaps = [Beatmap(map_detail) for map_detail in map_details]
                self.uow.beatmaps.add_all(new_beatmaps)
                beatmaps += new_beatmaps
        except pybeatsaver.NotFoundException as error:
            raise BeatmapHashNotFound(error.url.split("/")[-1]) from error

        self.uow.save_changes()

        return beatmaps

    async def get_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps = []

        beatmap_versions = self.uow.beatmap_versions.get_all_by_hashes(beatmap_hashes)
        missing_beatmaps_hashes = beatmap_hashes.copy()

        for beatmap_version in beatmap_versions:
            if beatmap_version.hash in missing_beatmaps_hashes:
                missing_beatmaps_hashes.remove(beatmap_version.hash)
                beatmaps.append(beatmap_version.beatmap)

        beatmaps += await self.get_missing_beatmaps_by_hashes(missing_beatmaps_hashes)

        return beatmaps

    async def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap_version = self.uow.beatmap_versions.get_by_hash(beatmap_hash)

        if beatmap_version is None:
            return (await self.get_missing_beatmaps_by_hashes([beatmap_hash]))[0]

        return beatmap_version.beatmap

    async def get_beatmap_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        beatmap_hash = self.uow.beatmap_versions.get_hash_by_key(beatmap_key)

        if beatmap_hash is None:
            beatmap = await self.get_beatmap_by_key(beatmap_key)
            beatmap_hash = beatmap.latest_version.hash

        return beatmap_hash

    async def get_beatmap_difficulty(
            self,
            beatmap_hash: str,
            characteristic: pybeatsaver.ECharacteristic,
            difficulty: pybeatsaver.EDifficulty
    ) -> BeatmapVersionDifficulty:
        beatmap_difficulty = self.uow.beatmap_version_difficulties.get_by_hash_and_characteristic_and_difficulty(
                beatmap_hash,
                characteristic,
                difficulty
        )

        if beatmap_difficulty is None:
            await self.get_beatmap_by_hash(beatmap_hash)

            beatmap_difficulty = self.uow.beatmap_version_difficulties.get_by_hash_and_characteristic_and_difficulty(
                    beatmap_hash,
                    characteristic,
                    difficulty
            )

        return beatmap_difficulty
