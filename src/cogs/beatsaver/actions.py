import pybeatsaver.errors

from .storage.uow import UnitOfWork
from .errors import SongNotFound
from .storage.model import Beatmap


class Actions:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap = self.uow.beatmap_repo.get_beatmap_by_key(beatmap_key)

        if beatmap is None:
            try:
                map_detail = self.uow.beatsaver.get_map_by_key(beatmap_key)
                beatmap = self.uow.beatmap_repo.add(Beatmap(map_detail))
            except pybeatsaver.NotFoundException as error:
                raise SongNotFound(f"Could not find song with key {beatmap_key}") from error

        return beatmap

    def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap = self.uow.beatmap_repo.get_beatmap_by_hash(beatmap_hash)

        if beatmap is None:
            try:
                map_detail = self.uow.beatsaver.get_map_by_hash(beatmap_hash)
                beatmap = self.uow.beatmap_repo.add(Beatmap(map_detail))
            except pybeatsaver.NotFoundException as error:
                raise SongNotFound(f"Could not find song with hash {beatmap_hash}") from error

        return beatmap
