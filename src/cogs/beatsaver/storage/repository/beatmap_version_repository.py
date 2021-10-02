from typing import Optional, List

from src.database import Repository
from ..model import BeatmapVersion


class BeatmapVersionRepository(Repository):
    def get_by_id(self, entry_id: str) -> Optional[BeatmapVersion]:
        return self._db.session.query(BeatmapVersion)\
            .filter(BeatmapVersion.hash == entry_id)\
            .first()

    def get_all(self) -> Optional[List[BeatmapVersion]]:
        return self._db.session.query(BeatmapVersion)\
            .all()
