import asyncio
import pybeatsaver.errors

from .storage.uow import UnitOfWork
from .errors import SongNotFound
from .storage.model import Beatmap, BeatmapVersion


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap = self.uow.beatmap_repo.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            try:
                # Beat Saver api likes when you wait 0.2 seconds
                await asyncio.sleep(0.2)

                map_detail = await self.uow.beatsaver.get_map_by_key(beatmap_key)
                beatmap = Beatmap(map_detail)

                if self.uow.beatmap_repo.get_by_id(beatmap.id) is None:
                    beatmap = self.uow.beatmap_repo.add(Beatmap(map_detail))
            except pybeatsaver.NotFoundException as error:
                raise SongNotFound(f"Could not find song with key {beatmap_key}") from error

        return beatmap

    async def get_beatmap_version_by_hash(self, beatmap_hash: str) -> BeatmapVersion:
        beatmap = self.uow.beatmap_version_repo.get_by_id(beatmap_hash)

        if beatmap is None:
            try:
                # Beat Saver api likes when you wait 0.2 seconds
                await asyncio.sleep(0.2)

                map_detail = await self.uow.beatsaver.get_map_by_hash(beatmap_hash)
                beatmap = Beatmap(map_detail)

                if self.uow.beatmap_repo.get_by_id(beatmap.id) is None:
                    beatmap = self.uow.beatmap_repo.add(Beatmap(map_detail))
            except pybeatsaver.NotFoundException as error:
                raise SongNotFound(f"Could not find song with hash {beatmap_hash}") from error

        return beatmap
