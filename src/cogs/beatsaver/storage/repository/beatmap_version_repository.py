from typing import Optional, List

from sqlalchemy.orm import Query

from ..model.beatmap_version import BeatmapVersion
from src.kiyomi.database import BaseRepository


class BeatmapVersionRepository(BaseRepository[BeatmapVersion]):
    def query_by_id(self, entry_id: str) -> Query:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.hash == entry_id)

    def get_all(self) -> Optional[List[BeatmapVersion]]:
        return self.session.query(BeatmapVersion) \
            .all()
