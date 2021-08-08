from typing import List

from pybeatsaver import MapDetail

from src.cogs.beatsaber.storage.model.beatmap import Beatmap
from src.cogs.beatsaber.storage.model.beatmap_version import BeatmapVersion


class BeatmapRepository:
    def __init__(self, database):
        self._db = database

    def get_all_beatmaps(self) -> List[Beatmap]:
        return self._db.session.query(Beatmap).all()

    def get_beatmap_by_id(self, beatmap_id: str) -> Beatmap:
        return self._db.session.query(Beatmap).filter(Beatmap.id == beatmap_id).first()

    def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap_version = self._db.session.query(BeatmapVersion).filter(BeatmapVersion.hash == beatmap_hash).first()

        if beatmap_version is not None:
            return beatmap_version.beatmap

    def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap_version = self._db.session.query(BeatmapVersion).filter(BeatmapVersion.key == beatmap_key).first()

        if beatmap_version is not None:
            return beatmap_version.beatmap

    def add_beatmap(self, beatmap: Beatmap):
        self._db.add_entry(beatmap)

        return self.get_beatmap_by_id(beatmap.id)
