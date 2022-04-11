from typing import List, Optional

from sqlalchemy.orm import Query, joinedload

from ..model.beatmap import Beatmap
from src.kiyomi.database import BaseRepository
from ..model.beatmap_version import BeatmapVersion


class BeatmapRepository(BaseRepository[Beatmap]):

    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(Beatmap) \
            .filter(Beatmap.id == entry_id) \
            .options(
                joinedload(Beatmap.versions).
                joinedload(BeatmapVersion.difficulties)
            )

    def get_all(self) -> Optional[List[Beatmap]]:
        return self.session.query(Beatmap) \
            .options(
                joinedload(Beatmap.versions).
                joinedload(BeatmapVersion.difficulties)
            ) \
            .all()

    def get_all_by_ids(self, beatmap_keys: List[str]) -> List[Beatmap]:
        return self.session.query(Beatmap) \
            .filter(Beatmap.id.in_(beatmap_keys)) \
            .options(
                joinedload(Beatmap.versions).
                joinedload(BeatmapVersion.difficulties)
            ) \
            .all()
