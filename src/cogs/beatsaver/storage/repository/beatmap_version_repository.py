from typing import Optional, List

from sqlalchemy.orm import Query

from src.database import BaseRepository
from ..model import BeatmapVersion


class BeatmapVersionRepository(BaseRepository[BeatmapVersion]):
    def query_by_id(self, entry_id: int) -> Query:
        return self.session.query(BeatmapVersion) \
            .filter(BeatmapVersion.id == entry_id)

    def get_all(self) -> Optional[List[BeatmapVersion]]:
        return self.session.query(BeatmapVersion)\
            .all()
