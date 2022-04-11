from typing import Optional, List

import pybeatsaver
from sqlalchemy.orm import Query

from src.cogs.beatsaver.storage.model.beatmap_version_difficulty import BeatmapVersionDifficulty
from src.kiyomi import BaseRepository
from src.kiyomi.database.base_repository import T


class BeatmapVersionDifficultyRepository(BaseRepository):
    def query_by_id(self, entry_id: int) -> Query:
        pass

    def get_all(self) -> Optional[List[T]]:
        pass

    def get_by_hash_and_characteristic_and_difficulty(
            self,
            beatmap_hash: str,
            characteristic: pybeatsaver.ECharacteristic,
            difficulty: pybeatsaver.EDifficulty
    ) -> Optional[BeatmapVersionDifficulty]:
        return self.session.query(BeatmapVersionDifficulty) \
            .filter(BeatmapVersionDifficulty.version_hash == beatmap_hash) \
            .filter(BeatmapVersionDifficulty.characteristic == characteristic.name) \
            .filter(BeatmapVersionDifficulty.difficulty == difficulty.name) \
            .first()
