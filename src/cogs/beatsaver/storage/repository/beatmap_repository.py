from typing import List, Optional

from src.database import Repository
from ..model import Beatmap, BeatmapVersion


class BeatmapRepository(Repository[Beatmap]):

    def get_all(self) -> Optional[List[Beatmap]]:
        return self._db.session.query(Beatmap).all()

    def get_by_id(self, beatmap_id: str) -> Optional[Beatmap]:
        return self._db.session.query(Beatmap).filter(Beatmap.id == beatmap_id).first()

    def get_beatmap_by_hash(self, beatmap_hash: str) -> Beatmap:
        beatmap_version = self._db.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash == beatmap_hash) \
            .first()

        if beatmap_version is not None:
            return beatmap_version.beatmap

    def get_beatmaps_by_hashes(self, beatmap_hashes: List[str]) -> List[Beatmap]:
        beatmaps_version = self._db.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash.in_(beatmap_hashes)) \
            .all()

        return [beatmap_version.beatmap for beatmap_version in beatmaps_version]

    def get_beatmap_by_key(self, beatmap_key: str) -> Beatmap:
        beatmap_version = self._db.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.key == beatmap_key) \
            .first()

        if beatmap_version is not None:
            return beatmap_version.beatmap

    def get_beatmaps_by_keys(self, beatmap_keys: List[str]) -> List[Beatmap]:
        beatmaps_version = self._db.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.key.in_(beatmap_keys)) \
            .all()

        return [beatmap_version.beatmap for beatmap_version in beatmaps_version]
