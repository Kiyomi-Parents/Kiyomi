from typing import List

import pybeatsaver

from .beatsaver_service import BeatSaverService
from ..errors import SongNotFound
from ..storage import Beatmap


class BeatmapService(BeatSaverService):

    async def get_missing_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps = []

        try:
            async for map_detail in self.beatsaver.beatmaps_by_keys(beatmap_keys):
                beatmaps.append(Beatmap(map_detail))
        except pybeatsaver.NotFoundException as error:
            raise SongNotFound(f"Could not find song at {error.url}") from error

        self.uow.beatmap_repo.add_all(beatmaps)

        return beatmaps

    async def get_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps = self.uow.beatmap_repo.get_beatmaps_by_keys(beatmap_keys)
        missing_beatmaps_keys = beatmap_keys.copy()

        for beatmap in beatmaps:
            for beatmap_version in beatmap.versions:
                if beatmap_version.key in missing_beatmaps_keys:
                    missing_beatmaps_keys.remove(beatmap_version.key)

        beatmaps += await self.get_missing_beatmaps_by_keys(missing_beatmaps_keys)

        return beatmaps

    async def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap = self.uow.beatmap_repo.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            return (await self.get_missing_beatmaps_by_keys([beatmap_key]))[0]

        return beatmap

    async def get_missing_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps = []

        try:
            async for map_details in self.beatsaver.beatmaps_by_hashes_all(beatmap_hashes):
                new_beatmaps = [Beatmap(map_detail) for map_detail in map_details]
                self.uow.beatmap_repo.add_all(new_beatmaps)
                beatmaps += new_beatmaps
        except pybeatsaver.NotFoundException as error:
            raise SongNotFound(f"Could not find song with hash {beatmap_hashes}") from error

        return beatmaps

    async def get_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps = self.uow.beatmap_repo.get_beatmaps_by_hashes(beatmap_hashes)
        missing_beatmaps_hashes = beatmap_hashes.copy()

        for beatmap in beatmaps:
            for beatmap_version in beatmap.versions:
                if beatmap_version.hash in missing_beatmaps_hashes:
                    missing_beatmaps_hashes.remove(beatmap_version.hash)

        beatmaps += await self.get_missing_beatmaps_by_hashes(missing_beatmaps_hashes)

        return beatmaps

    async def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap = self.uow.beatmap_repo.get_beatmap_by_hash(beatmap_hash)

        if beatmap is None:
            return (await self.get_missing_beatmaps_by_hashes([beatmap_hash]))[0]

        return beatmap
