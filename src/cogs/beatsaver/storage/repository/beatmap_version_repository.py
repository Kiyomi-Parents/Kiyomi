from typing import Optional, List

from sqlalchemy.orm import Query, joinedload

from ..model.beatmap_version import BeatmapVersion
from src.kiyomi.database import BaseRepository


class BeatmapVersionRepository(BaseRepository[BeatmapVersion]):
    def query_by_id(self, entry_id: str) -> Query:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash == entry_id) \
            .options(
                    joinedload(BeatmapVersion.beatmap),
                    joinedload(BeatmapVersion.difficulties)
            )

    def get_all(self) -> Optional[List[BeatmapVersion]]:
        return self.session.query(BeatmapVersion) \
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties)
            ) \
            .all()

    def get_by_hash(self, beatmap_hash: str) -> Optional[BeatmapVersion]:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash == beatmap_hash) \
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties)
            ) \
            .first()

    def get_all_by_hashes(self, beatmap_hashes: List[str]) -> List[BeatmapVersion]:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash.in_(beatmap_hashes)) \
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties)
            ) \
            .all()

    def get_by_key(self, beatmap_key: str) -> Optional[BeatmapVersion]:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.key == beatmap_key) \
            .options(
                joinedload(BeatmapVersion.beatmap),
                joinedload(BeatmapVersion.difficulties)
            ) \
            .first()

    def get_hash_by_key(self, beatmap_key: str) -> Optional[str]:
        return self.session.query(BeatmapVersion.hash) \
            .options(joinedload(BeatmapVersion.beatmap)) \
            .filter(BeatmapVersion.beatmap.id == beatmap_key) \
            .first()
